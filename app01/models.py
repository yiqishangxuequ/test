from django.db import models
from django.contrib.auth.models import AbstractUser

# 类对应表单，由类创造的对象对应表中的一行，类中的每个属性对应表中的一列

class UserInfo(AbstractUser):
    # 也可以不设置AutoField字段，默认会使用名为id的主键
    # Field英语意思为 字段
    nid = models.AutoField(primary_key=True)
    # 头像: FileField文件(此处不用varchar类型)
    # default:默认值. upload_to上传的路径，如果没有会自动生成。
    '''
    VARCHAR(M)是一种比CHAR更加灵活的数据类型，同样用于表示字符数据，但是VARCHAR可以保存可变长度的字符串。
    其中M代表该数据类型所允许保存的字符串的最大长度，只要长度小于该最大值的字符串都可以被保存在该数据类型中
    对应于django中的CharField(max_length= )
    
    数据库中一列称为字段，可见avatar = models.FileField()实际上是定义了数据中的一列
    而FileField()规定了这一列的数据类型
    比如CharField()规定了这一列都是字符串类型
    '''
    avatar = models.FileField(upload_to='avatar/',default='avatar/default.png',)
    # 跟blog表一对一
    # OneToOneField本质就是ForeignKey，只不过有个唯一性约束
    # 等价于blog = modes.ForeignKey(to='Blog', to_field='nid', null=True,unique=True)
    blog = models.OneToOneField(to='Blog',null=True,to_field='nid',on_delete=models.CASCADE)

    class Meta:
        # db_table = 'xxx'

        # 在admin中显示的表名，否则将显示UserInfo
        verbose_name = '用户表'
        # 去掉用户表中的s，即令单词的复数等于单数形式
        verbose_name_plural = verbose_name

class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    # 站点名称
    title = models.CharField(max_length=64)
    # 站点副标题
    site_name = models.CharField(max_length=32)
    # 不同人不同主题
    theme = models.CharField(max_length=64)

    # 打印对象时显示site_name的值
    def __str__(self):
        return self.site_name

class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    # 分类名称
    title = models.CharField(max_length=64)

    # 跟博客是一对多的关系，关联字段写在多的一方
    # to 是跟哪个表关联 to_field跟表中的哪个字段做关联
    # 如果被关联的类中没有定义nid = models.AutoField(primary_key=True)，
    # 则ForeignKey中的to_field='nid'不写也行

    # null = True表示该字段可以为空
    # 如果null=False，当Blog类没有没被创建时，blog是创建不出来的，
    # 现在null=True，即使Blog类没有被创建，blog也是可以创建出来的，后期再做关联
    blog = models.ForeignKey(to='Blog',to_field='nid',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    #标签名字
    title = models.CharField(max_length=64)
    # 跟博客是一对多的关系，关联字段写在多的一方
    blog = models.ForeignKey(to='Blog',to_field='nid',null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    # verbose_name 在admin中显示该字段的中文
    title = models.CharField(max_length=64,verbose_name='文章标题')
    # 文章摘要
    desc = models.CharField(max_length=255)
    # 文章内容 大文本
    content = models.TextField()
    # 文章所属院系
    college = models.CharField(max_length=64,verbose_name='所属学院')

    # DateTimeField 年月日时分秒 （注意跟datafield的区别）
    # auto_now_add =True: 插入数据会存入当前时间
    # auto_now =True ： 修改数据会存入当前时间
    create_time = models.DateTimeField(auto_now_add=True)

    commit_num=models.IntegerField(default=0)
    up_num=models.IntegerField(default=0)
    down_num=models.IntegerField(default=0)
    

    # 一对多的关系
    blog = models.ForeignKey(to='Blog',to_field='nid',null=True,on_delete=models.CASCADE)


    # 一对多的关系
    category = models.ForeignKey(to='Category',to_field='nid',null=True,on_delete=models.CASCADE)
    # 多对多的关系 through_fields 不能写反了；
    # 注意through_fields('article','tag')中的'article'和’tag‘是中介表中的字段，即中介表中定义的article和tag属性
    # 当前是从article表中寻找tag，所以写成through_fields('article','tag')
    # 如果这个关联定义在tag中，写成('tag','article')
    # 如果不写through,则会自动生成第三张表
    tag =models.ManyToManyField(to='Tag',through='ArticleTOTag',through_fields=('article','tag'))
    def __str__(self):
        return self.title+'----'+self.blog.userinfo.username

# 如果在Article中的ManyToManyField中使用through,则无需建立ArticleTOTag
# 这个中介表。手动建立中介表是为了在中介表增加一些东西
class ArticleTOTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag', to_field='nid',on_delete=models.CASCADE)

class Commit(models.Model):
    # 谁对哪篇文章评论了什么内容
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article',to_field='nid',on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    # 评论时间
    create_time = models.DateTimeField(auto_now_add=True)

    # create_time = models.DateTimeField(default=now)
    # 不能写成now()，否则程序一执行，now()就执行了，成为一个固定的数据
    # 程序执行是什么时间，就是什么时间了

    # 自关联（）
    parent = models.ForeignKey(to='self',to_field='nid',null=True,blank=True,on_delete=models.CASCADE)
    # parent = models.ForeignKey(to='Commit',to_field='nid',null=True,blank=True,on_delete=models.CASCADE)
    # parent = models.IntegerField()
    '''
    1. 用户id--1 文章id--1 评论--写的真好  关联信息:null
    2. 用户id--2 文章id--1 评论--写的不好  关联信息:1
    3. 用户id--1 文章id--1 评论--我觉好    关联信息:2
    '''
class UpAndDown(models.Model):
    # 谁对哪篇文章点赞或点踩
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    article = models.ForeignKey(to='Article',to_field='nid',on_delete=models.CASCADE)
    is_up = models.BooleanField()

    class Meta:
        # 联合唯一，一个用户只能给一篇文章点赞或点踩
        unique_together = (('user','article'),)

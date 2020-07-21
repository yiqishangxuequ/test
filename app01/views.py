from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
# ImageDraw在图片上写字
# ImageFont写字的格式，比如宋体
from PIL import Image,ImageDraw,ImageFont
import random
from django.contrib import  auth
from app01.bbsforms import RegForm
from app01 import models

# 相当于把文件以byte格式存到内存中
from io import BytesIO

from django.db.models import Count

from django.db.models.functions import TruncMonth

import json
from django.db.models import F
from django.db import transaction
# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.is_ajax(): # 判断是否是ajax请求
        response={'code':100,'msg':None,'url':'/index/'}
        # request.body 可以获得请求体
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        code = request.POST.get('code')
        print(name)
        #忽略大小写
        #print(type(request.session['valid_code']))
        #print('haha')
        if request.session['valid_code'].upper()==code.upper():
            user = auth.authenticate(request,username=name,password=pwd)
            if user:
                response['msg']='登录成功'
                # 一定不要忘记这个，为什么要用这个？
                # 在后续的视图函数中直接requests.uer 取到当前登录用户
                # 登录的时候首先请求了视图函数get_code，用户名密码之类的也是
                # 传到了get_code中，而现在我们在login中得到了用户名
                # 所以auth.login这个函数显然用到了中间件
                user = auth.login(request,user)

            else:
                response['code']=101
                response['msg']="用户名或密码错误"
        else:
            response['code'] = 102
            response['msg'] = "验证码错误"
        return JsonResponse(response,)
        # 由JsonRespinse的源码可知
        # 如果返回值中文乱码，则用下面的格式
        # return JsonResponse(response,json_dumps_params={'ensure_ascii':False})
        # 如果要序列化列表，需要设置safe=False

def get_random_color():
    return(random.randint(0,255),random.randint(0,255),random.randint(0,255))

def get_code(request):
    '''
    # #方式一，返回固定图片
    # with open('static/img/Figure_1.png','rb') as f:
    #     data = f.read()
    # return  HttpResponse(data)

    # # 方式二，自动生成图片（需要借助第三方模块pillow）图像处理模块
    # # 新生成一张图片
    # # img接收的是对象，而目前需要返回二进制，所以不能直接使用
    # # 需要先把图片保存起来
    # # img = Image.new('RGB',(350,40),'green')中的'green'可以写成三原色(1,255,3)
    # img = Image.new('RGB',(350,40),get_random_color())
    # with open('static/img/code.png','wb') as f:
    #     # 注意用img对象的save方法，把f传入
    #     img.save(f)
    # # 打开返回
    # with open('static/img/code.png','rb') as f:
    #     data = f.read()
    # return  HttpResponse(data)
    '''
    '''
    # 方式三（不把文件保存在硬盘上，保存在内存中）
    # 新生成一张图片
    img = Image.new('RGB',(350,40),get_random_color())
    # 生成一个ByteIO对象
    f = BytesIO()
    # 把文件保存到对象中
    # 注意这里保存要写图片格式，否则会报错
    img.save(f,'png')
    # f.getvalue() 把文件从对象中取出来
    return  HttpResponse(f.getvalue())
    '''
    '''
    # 方式四：在图片上写文字，并且保存到内存中
    img = Image.new('RGB',(350,40),get_random_color())
    # 写文字
    # 生成一个字体对象
    font = ImageFont.truetype('static/font/yujian.ttf',34)
    # 调用方法，返回一个画板对象，可以在画板上写东西
    draw = ImageDraw.Draw(img)
    draw.text((0,0),'python',font=font)
    f = BytesIO()
    img.save(f,'png')
    return  HttpResponse(f.getvalue())
    '''
    valid_code=''
    #最终版本
    img = Image.new('RGB', (350, 40), get_random_color())
    font = ImageFont.truetype('static/font/yujian.ttf', 34)
    draw = ImageDraw.Draw(img)
    # 动态生成大写，小写，数字 5个
    # draw.text((0, 0), 'python', font=font)
    for i in range(5):
        # 注意randint(0,9)可以产生0和9之间的值，包括0和9
        num = str(random.randint(0,9))
        up_char = str(chr(random.randint(65,90)))
        lower_chr = str(chr(random.randint(97,122)))
        # 从三个字符中选一个字符
        randchar = random.choice([num,up_char,lower_chr])
        # 把验证码放到session中

        valid_code += randchar
        # fill=get_random_color()可以让字体的颜色随机
        draw.text((30 + i * 30, 0), randchar, font=font,fill=get_random_color())
    request.session['valid_code']=valid_code
    # print(request.session['valid_code'])
    # # 画点和线
    # width = 320
    # height = 35
    # for i in range(10):
    #     x1 = random.randint(0,width)
    #     x2 = random.randint(0,width)
    #     y1 = random.randint(0,height)
    #     y2 = random.randint(0,height)
    #     # 在图片上画线
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(100):
    #     # 画点
    #     draw.point([random.randint(0,width),random.randint(0,height)],fill=get_random_color())
    #     x = random.randint(0,width)
    #     y = random.randint(0,height)
    #     # 画弧形
    #     draw.arc((x,y,x+4,y+4),0,90,fill=get_random_color())

    f = BytesIO()
    img.save(f, 'png')
    return HttpResponse(f.getvalue())

def register(request):
    if request.method == 'GET':
        # 这个FegForm是我们写在bbsforms中的类
        form = RegForm()
        return render(request,'register.html',{'form':form})
    elif request.is_ajax():
        response = {'code':100,'msg':None}
        # 前段是formdata编码过来的，数据部分放在了POST里面
        # 文件部分放在了FILE里面
        # urlencoding编号只有数据部分，全都放在POST里面
        # json格式哪里都没有放
        # 这是django框架帮忙干的事情
        form = RegForm(request.POST)
        if form.is_valid():
            # 校验通过的数据
            # 先对bbsforms.py中RegForm定义的各种属性做校验
            # 然后对类中的方法，即全局钩子和局部钩子做校验
            # 全部通过了才算通过
            clean_data=form.cleaned_data
            #把 re_pwd剔除
            clean_data.pop('re_pwd')
            #取出头像，在register.html中头像的key值是'avatar'
            avatar = request.FILES.get('avatar')
            if avatar:
                # clean_data['avatar']中的avatar将要存入在app01.models中
                # 的UserInfo类中定义的avatar属性
                # 因为用的是FileField，只需要把文件对象赋值给avatar字段，自动做保存

                clean_data['avatar'] = avatar
            user = models.UserInfo.objects.create_user(**clean_data)
            if user:
                response['msg']='创建成功'
            else:
                response['code']=103
                # 把校验不通过的数据返回
                response['msg']='创建失败'
        else:
            response['code']=101
            # 把校验不通过的数据返回
            response['msg']=form.errors
            print(type(form.errors))
        return JsonResponse(response,safe=False)

# 引入分页类
from django.core.paginator import Paginator

def index(request,college='',pIndex=''):
# 设置college和pIndex的默认值为''，确保直接输入http://127.0.0.1:8000就可以直接访问到主页
    if college == '':
        # 查询所有文章信息
        article_list0=models.Article.objects.all()
    else:
        article_list0 = models.Article.objects.filter(college=college)
    # 将文章信息按一页10条进行分页
    print(college)
    p = Paginator(article_list0,1)
    # 如果当前没有传递页码信息，则认为是第一页，这样写是为了请求第一页时可以不写页码
    if pIndex == '':
        pIndex = '1'
    # 通过url匹配的参数都是字符串类型，转成int类型
    pIndex = int(pIndex)
    # 获取第pIndex页的数据
    article_list = p.page(pIndex)
    # 获取所有的页码信息
    plist = p.page_range
    # 将当前页码、当前页的数据、页码信息传递到模板中
    return render(request,'index.html',{'article_list':article_list
                                        ,'plist':plist,'pIndex':pIndex,'college':college})

def logout(request):
    auth.logout(request)
    return redirect('/index/')

def site_page(request,username,*args,**kwargs):
    print(args)
    print(kwargs)

    # filter查询返回的是一个包含所有对象的查询集，需用first()返回查询集中第一个对象
    # 例如>>> Article.objects.all()

    # <QuerySet [<Article: 111----smart>, <Article: C语言课件分享！！！----smart>,
    # <Article: 2233----smart>, <Article: django课件----smart>, <Article: 生命科学院----xiake>]>

    # >>> Article.objects.all().first()
    # <Article: 111----smart>
    user=models.UserInfo.objects.filter(username=username).first()

    if not user:
        return render(request,'error.html')
    #用户存在
    #查出文章的所有文章
    #根据用户得到个人站点
    blog = user.blog
    #取到当前站点下所有文章
    article_list = blog.article_set.all()
    # 过滤
    condition = kwargs.get('condition')
    param = kwargs.get('param')
    if condition == 'tag':
        article_list = article_list.filter(tag=param)
    elif condition == 'category':
        article_list = article_list.filter(category_id=param)
    elif condition == 'archive':
        # 2019-07
        year_t = param.split('-')
        article_list = article_list.filter(create_time__year=year_t[0],create_time__month=year_t[1])


    # 查询当前站点下所有标签对应的文章数（用到分组查询）

    # 查询当前站点下所有分类对应的文章数
    # 查询所有分类对应的文章数
    # 分组查询固定规则
    # filter 在annotate前表示where条件
    # values 在annotate前表示group
    # filter 在annotate后表示having条件
    # values 在annotate后表示取值
    # pk在这里表示主键

    #category = models.Category.objects.all().values('pk').annotate(cou=Count('article__nid')).values('title','cou')
    # 如果不写values时，默认为Category的主键作为values的值，所以可以不写

    # 加上filter(blog=blog)表示先把当前站点下过滤出来再去数数
    #category = models.Category.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values('title', 'cou')

    # 如果末尾的values用values_list，则返回列表形式
    #category = models.Category.objects.all().annotate(cou=Count('article__nid')).values_list('title', 'cou')

    # ret应该是return的缩写
    category_ret = models.Category.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values_list('title', 'cou','nid')
    print(category_ret)

    # 查询当前站点下所有标签对应的文章数
    tag_ret = models.Tag.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values_list('title','cou','nid')
    print(tag_ret)


    # 查询某年某月下对应的文章数

    '''
            官方文档，截取到月
            
            from django.db.models.functions import TruncMonth
            Sales.objects
            .annotate(month=TruncMonth('timestamp')) # Truncate to month and add to select list
            .value('month') # Group By month
            .annotate(c=Count('id')) #Select the count of the grouping
            .values('month','c') #(might be redundant,haven't tested) select month an count
    '''
    year_ret = models.Article.objects.all().annotate(month=TruncMonth('create_time')).values('month').annotate(c=Count('nid')).values_list('month','c')
    print(year_ret)

    # locals()表示把当前作用域(视图函数)下的变量都传入模板
    return render(request,'site_page.html',locals())

def article_detail(request,username,pk):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error.html')
    # 用户存在
    # 查出文章的所有文章
    # 根据用户得到个人站点
    blog = user.blog
    category_ret = models.Category.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values_list('title', 'cou', 'nid')
    tag_ret = models.Tag.objects.all().filter(blog=blog).annotate(cou=Count('article__nid')).values_list('title', 'cou','nid')
    year_ret = models.Article.objects.all().annotate(month=TruncMonth('create_time')).values('month').annotate(c=Count('nid')).values_list('month', 'c')

    article = models.Article.objects.filter(nid=pk).first()
    # commit_list =article.commit_set.all()
    return render(request,'article_detail.html',locals())

def diggit(request):
    response = {'code':100,'msg':None}
    # 当前登录用户id
    if request.user.is_authenticated: #判断用户是否登录
        # 视频中用的request.user.is_authenticated()，不过那样会报505的错误，所以在此把()去掉
        user_id = request.user.nid
        is_up = request.POST.get('is_up')
        print(type(is_up))
        print(is_up)
        # json模块可以把字符串类型转成python中的类型
        # 可以把python中的类型转成json字符串
        is_up = json.loads(is_up)
        article_id=request.POST.get('article_id')
        # 如果有值，则表示点过赞了
        up_ret = models.UpAndDown.objects.filter(user_id=user_id,article_id=article_id).first()
        if up_ret:
            response['code'] = 102
            response['msg'] = '您已经点过了'
        else:
            # 这一段要么都成功，要么都失败，所以是事务性的操作
            # 可以用装饰器，只让这一段在事务里

            # 只要缩进在with中，就相当于在事务中了。
            # 如果不用事务，当models.UpAndDown.objects.create()执行成功，数据库中会添加数据
            # 而接下来的语句执行失败时，会造成数据错乱，所以干脆让它们一起成功和失败

            # 开启事务
            with transaction.atomic():

                models.UpAndDown.objects.create(article_id=article_id,user_id=user_id,is_up=is_up)
                if is_up:
                    # 文章表点赞字段加一
                    models.Article.objects.filter(pk =article_id).update(up_num=F('up_num')+1)
                    response['msg'] = '点赞成功'
                else:
                    models.Article.objects.filter(pk =article_id).update(down_num=F('down_num')+1)
                    response['msg'] = '点踩成功'
    else:
        response['code']=101
        response['msg']='请先登录'
    # 因为response里面可能有列表，列表是序列化不了的，所以要令safe=False
    return JsonResponse(response,safe=False)

def commit(request):
    response = {'code':100,'msg':None}
    # 当前登录用户id
    if request.user.is_authenticated: #判断用户是否登录
        # 视频中用的request.user.is_authenticated()，不过那样会报505的错误，所以在此把()去掉
        user_id = request.user.nid
        article_id=request.POST.get('article_id')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        # 开始事务性的操作
        with transaction.atomic():
            ret = models.Commit.objects.create(article_id=article_id,content=content,user_id=user_id,parent_id=parent_id)
            models.Article.objects.filter(pk=article_id).update(commit_num=F('commit_num') + 1)
            response['username'] = ret.user.username
            response['reply_content'] = ret.content
            if parent_id:
                response['parent_name']=ret.parent.user.username
            response['msg'] = '评论成功'
    else:
        response['code']=101
        response['msg']='请先登录'
    # 因为response里面可能有列表，列表是序列化不了的，所以要令safe=False
    return JsonResponse(response,safe=False)

from django.contrib.auth.decorators import  login_required
#导入登录认证装饰器，本质上是一个函数
@login_required(login_url='/login/')
# 如果写成@login_required()，则相当于在此执行函数，并返回结果在此处
# 加了@符号就相当于一个语法糖，会把它下面的函数当做参数给到@后面跟东西
# 如果写login_required()，则相当于把下面的函数传给login_required()函数执行完得到的结果里面
# 如果写成login_required，则相当于把下面的函数传给login_required函数执行，然后得到结果
def home_backend(request):
    # 查询该人的所有文章
    article_list = models.Article.objects.filter(blog=request.user.blog)

    return render(request,'backend/home_backend.html',locals())


# # 写一个装饰器来装饰一个函数
# # 用这个装饰器的时候显然不能@autu()，因为这样会返回inner这个函数
# # 即@autu()相当于inner，当传入装饰器下的函数时，显然会出错
# # 所以用装饰器时应当看装饰器是怎么写的
# def autu(func):
#         def inner(*args,**kwargs):
#             return func(*args,**kwargs)
#         return inner

@login_required(login_url='/login/')
def add_article(request):

    if request.method == 'GET':
        # 返回分类下拉框的数据
        user = request.user
        list = user.blog.category_set.all()
        # print(list)
        list2 = []
        for item in list:
            list2.append(item.title)
        return render(request,'backend/add_article.html',{'data': list2})
    else:
        title = request.POST.get('title')
        text_content = request.POST.get('text_content')
        college = request.POST.get('college')
        category = request.POST.get('category')
        category1 = request.user.blog.category_set.all().get(title=category)
        # print(college)
        #通过bs4 处理xss攻击,html文档解析库
        # pip3 install beautifulsoup4
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(text_content,'html.parser')
        # 查找所有的标签
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                # 从文档中删除该标签
                tag.decompose()
        # soup.text 文档的内容，不包含标签
        desc = soup.text[0:150]
        models.Article.objects.create(title=title,desc=desc ,content=str(soup),blog=request.user.blog,college=college,category=category1)
        return redirect('/backend/')

@login_required(login_url='/login/')
# 添加分类
def add_category(request):
    if request.method == 'GET':
        return render(request,'backend/add_category.html')
    else:
        category = request.POST.get('category')
        print(category)
        models.Category.objects.create(title=category,blog=request.user.blog)
    return redirect('/backend/')

# 返回学院下拉列表框
def college(request,bigclass_id):
    arts = ['商学院','旅游管理学院','政治与公共管理学院','法学院','文学院','新闻与传播学院','外国语与国际关系学院','马克思主义学院',
'教育学院','哲学学院','历史学院','信息管理学院','体育学院','音乐学院','美术学院','书法学院']
    science = ['数学与统计学院','化学学院','物理学院','信息工程学院','电气工程学院','材料科学与工程学院','机械与动力工程学院',
'水利科学与工程学院','化工学院','建筑学院','管理工程学院','力学与安全工程学院','生命科学学院','农学院','生态与环境学院',
               '地球科学与技术学院']
    medical =['医学院','公共卫生学院','药物研究院','药学院']
    if bigclass_id == '1':
        return JsonResponse({'data': science})
    if bigclass_id == '2':
        return JsonResponse({'data': medical})
    if bigclass_id == '3':
        return JsonResponse({'data': arts})



def uploadimg(request):
    response={
        #根据kindeditor编辑器文档要求的格式写失败和成功返回的值
        "error":0,
        "url":None
    }

    # print(request.FILES)
    fil =request.FILES.get('imgFile')
    # 查看源码，可知fil有name属性
    with open('media/img_file/'+fil.name,'wb') as f:
        for line in fil:
            f.write(line)
        response['url']='/media/img_file/'+fil.name
    return JsonResponse(response)

def uploadfile(request):
    response={
        "error":0,
        "url":None
    }

    fil =request.FILES.get('sourceFile')
    with open('media/source_file/'+fil.name,'wb') as f:
        for line in fil:
            f.write(line)
        response['url']='/media/source_file/'+fil.name
    return JsonResponse(response)


# # 响应院系的文章列表
# # article_category_(?P<college>\w+)_(?P<pIndex>[0-9]*))
# def article_category(request,college,pIndex):
#     # 查询对应文章信息
#     article_list0=models.Article.objects.filter(category=college)
#     # 将文章信息按一页10条进行分页
#     p = Paginator(article_list0,1)
#     # 如果当前没有传递页码信息，则认为是第一页，这样写是为了请求第一页时可以不写页码
#     if pIndex == '':
#         pIndex = '1'
#     # 通过url匹配的参数都是字符串类型，转成int类型
#     pIndex = int(pIndex)
#     # 获取第pIndex页的数据
#     article_list = p.page(pIndex)
#     # 获取所有的页码信息
#     plist = p.page_range
#     # 将当前页码、当前页的数据、页码信息传递到模板中
#     return render(request,'index.html',{'article_list':article_list
#                                         ,'plist':plist,'pIndex':pIndex})

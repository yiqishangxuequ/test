
from django import forms
from django.forms import  widgets

from django.core.exceptions import ValidationError
#导入ValidationError校验不通过这个异常

from app01 import models
# 导入app01应用的models，来从数据库中检索东西

# 写一个类，继承Form 没有头像校验的字段
class RegForm(forms.Form):
    username = forms.CharField(max_length=18,min_length=3,label="用户名",
                           error_messages={'max_length':'太长了',
                                           'min_length':'太短了',
                                            'required':'不能为空'},
                           widget = widgets.TextInput(attrs={'class':'form-control'}),)
    password = forms.CharField(max_length=18, min_length=3, label="密码",
                           error_messages={'max_length': '太长了',
                                           'min_length': '太短了',
                                           'required': '不能为空'},
                           widget=widgets.PasswordInput(attrs={'class': 'form-control'}),)
    re_pwd = forms.CharField(max_length=18, min_length=3, label="确认密码",
                           error_messages={'max_length': '太长了',
                                           'min_length': '太短了',
                                           'required': '不能为空'},
                           widget=widgets.PasswordInput(attrs={'class': 'form-control'}),)
    email = forms.EmailField(max_length=18, min_length=3, label="邮箱",
                           error_messages={'max_length': '太长了',
                                           'min_length': '太短了',
                                           'required': '不能为空'},
                           widget=widgets.EmailInput(attrs={'class': 'form-control'}),)

    # AOP 面向切面编程
    # 局部钩子，局部校验
    def clean_username(self):
        # 取出name对应的值
        # cleaned_data表示清洗后的数据
        name = self.cleaned_data.get('username')
        # if name.startswith('sb'):
        #     #校验不通过，抛出 导入的异常
        #     raise ValidationError('不能以sb开头')
        # else:
        #     return name
        user = models.UserInfo.objects.filter(username=name).first()
        if user:
            # 用户存在，抛异常
            raise ValidationError('用户已存在')
        else:
            return name
    #全局钩子，全局校验
    def clean(self):
        pwd = self.cleaned_data.get('password')
        r_pwd=self.cleaned_data.get('re_pwd')


        if pwd == r_pwd:
            #校验通过，返回清洗后的数据
            return self.cleaned_data
        else:
            # 校验不通过，抛出 导入的异常
            raise ValidationError('两次密码不一致')



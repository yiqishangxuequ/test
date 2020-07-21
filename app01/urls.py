from django.contrib import admin
from django.urls import path,re_path
from app01 import views
from django.views.static import serve
from BBS import settings

urlpatterns = [
    re_path(r'^$',views.index),
    # 以空开头，以空结尾；匹配根路径，访问index页面
    re_path(r'^login/',views.login),
    re_path(r'^get_code/',views.get_code),
    re_path(r'index(?P<college>[\u4E00-\u9FA5]*)(?P<pIndex>[0-9]*)$',views.index),
    re_path(r'^register/',views.register),
    re_path(r'^logout/',views.logout),
    # 点赞路由
    re_path(r'^diggit/',views.diggit),
    # 评论路由
    re_path(r'^commit/',views.commit),
    # 后台管理首页
    re_path(r'^backend/',views.home_backend),
    # 添加文章
    re_path(r'add_article',views.add_article),
    # 添加分类
    re_path(r'add_category', views.add_category),
    # 上传图片
    re_path(r'^uploadimg/',views.uploadimg),
    # 上传文件
    re_path(r'^uploadfile/', views.uploadfile),
    #开启media的口子
    re_path(r'^media/(?P<path>.*)',serve,kwargs={'document_root':settings.MEDIA_ROOT}),

    # re_path(r'^(?P<username>\w+)/tag/(?P<id>\d+)$', views.site_page),
    # re_path(r'^(?P<username>\w+)/category/(?P<id>\d+)$', views.site_page),
    # re_path(r'^(?P<username>\w+)/archive/(?P<id>\d+)$', views.site_page),
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)$', views.site_page),
    # 文章详情
    re_path(r'^(?P<username>\w+)/article/(?P<pk>\d)$', views.article_detail),

    re_path(r'^college(\d+)$', views.college),  # 院系下拉列表框


    # re_path(r'^article_category_(?P<college>\w+)(?P<pIndex>[0-9]*)$',views.article_category), # 响应不同院系的文章列表

    # 写到最后面，上面所有都匹配不上了再匹配这里
    re_path(r'^(?P<username>\w+)$',views.site_page),



]

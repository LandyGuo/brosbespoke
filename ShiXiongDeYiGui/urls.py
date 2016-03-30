#coding:utf8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import weixin
import wap
import order
from ShiXiongDeYiGui.views import handleRequest, wx_create_menu


# Uncomment the next two lines to enable the admin:
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ShiXiongDeYiGui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # 后台管理模块
    #url(r'^admin/wap/order/', include('order.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #对微信api的封装，没有前端内容
    url(r'^weixin/', include('weixin.urls')),
    #手机页面
    url(r'^wap/', include('wap.urls')),
    #订单页面
    url(r'^order/', include('order.urls')),
    url(r'^promote/', include('wap.urls')),
    #处理微信服务器过来的Get或post请求
    url(r'^$', handleRequest),
    #创建菜单。暂时没有使用这个地方。在微信的api调试工具页面直接设置的微信公众号菜单。
    #url(r'^wx_create_menu/(?P<app_secret>\w+)/$', wx_create_menu),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)


# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()


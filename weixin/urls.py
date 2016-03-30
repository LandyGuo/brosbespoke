#coding:utf8
from django.conf.urls import patterns, include, url 

import weixin

urlpatterns = patterns('weixin.views',
    url(r'^weixin_token$', 'weixin_token', name='weixin_token'),
    url(r'^(?P<slug>\d+)/$', 'weixin_api', name='weixin_api'),
    #使用微信 AppSecretet(应用密钥) 调用一次，创建菜单
    url(r'^wx_create_menu/(?P<app_secret>\w+)/$', 'wx_create_menu', name='wx_create_menu'),
    #微信支付告警通知URL
    url(r'^wxpay_notify_url$', 'wxpay_notify_url', name='wxpay_notify_url'),
    #微信支付URL
    url(r'^wxpay_pay/pay$', 'wxpay_pay', name='wxpay_pay'),
    url(r'^wxpay_pay/test/pay$', 'wxpay_pay', name='wxpay_pay'),
)

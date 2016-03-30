
# coding:utf-8
from django.conf.urls import *
from models import *
from views import *
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',

    url(r'^accounts/login/$', login_view),
    url(r'^accounts/logout/$', logout_view),
    url(r'order_login/$', order_login),
    url(r'order_manage/(?P<tab>.+)/$', order_manage),  
    url(r'login/?', order_login),
    url(r'order_denie/$',order_denie),
    url(r'kmail/$',kmail),
    url(r'exl/(?P<orderid>.+)/$',  exl_download, name="exl_download"),
    url(r'order_update_post/(?P<orderid>.+)/$', order_update_post),
    url(r'plant_statu/(?P<tab>.+)/$', plant_statu),
    url(r'order_post/$', order_post),
    url(r'get_user_name/$', get_user_name),
    url(r'get_address_name/$', get_address_name),
    url(r'manage_post/$', manage_post),
    url(r'^fx/$',  TemplateView.as_view(template_name='order/122.html')),
    url(r'get_product_name/$', get_product_name),
)

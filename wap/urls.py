#coding:utf8
from django.conf.urls import patterns, include, url 
from django.views.generic.base import TemplateView
import wap

urlpatterns = patterns('wap.views',
    #量身定制
    url(r'^culture/$',  TemplateView.as_view(template_name='wap/13.html'), name="culture"),
    #隐私声明
    url(r'^privacy/$',  TemplateView.as_view(template_name='wap/privacy.html'), name="privacy"),
    #登陆
    #url(r'^login/$',  TemplateView.as_view(template_name='wap/1.html'), name="login"),
    url(r'^login/$',  'login', name="login"),
    #post 结尾的这几个方法，是ajax调用的接口
    url(r'^login_post/$',  'login_post', name="login_post"),
    url(r'^logout_post/$',  'logout_post', name="logout_post"),
    url(r'^register_post/$',  'register_post', name="register_post"),
    url(r'^forget_password_post/$',  'forget_password_post', name="forget_password_post"),
    url(r'^send_sms_post/$',  'send_sms_post', name="send_sms_post"),
    url(r'^change_phone_post/$',  'change_phone_post', name="change_phone_post"),
    url(r'^change_name_post/$',  'change_name_post', name="change_name_post"),
    url(r'^change_sex_post/$',  'change_sex_post', name="change_sex_post"),  
    #优惠券
    url(r'^coupons/$',  'coupon_list', name="coupons"),
    #个人尺寸
    url(r'^show_my_size/$',  'show_my_size', name="show_my_size"),
    #分享尺寸页面
    url(r'^share_my_size/(?P<userid>\d+)/(?P<type>\w+)/$',  'share_my_size', name="share_my_size"),
    #个人信息页面
    url(r'^my_info/$',  'my_info', name="my_info"),
    #修改姓名
    url(r'^my_name_change/$',  'my_name_change', name="my_name_change"),
    #修改电话
    url(r'^my_phone_change/$',  'my_phone_change', name="my_phone_change"),
    
    #url(r'^login',  'login', name="login"),
    #url(r'^logout',  'logout', name="logout"),
    #定制需求第一个界面
    url(r'^buy/$',  'buy', name="buy"),
    #预约页面
    url(r'^buy_info/$', TemplateView.as_view(template_name='wap/12.html'), name="buy_info"),
    #衬衫或西装的列表
    #url(r'^buy_list/(?P<type>\w+)/$',  'buy_list', name="buy_list"),
    #西装或衬衫详情
    url(r'^buy_detail/(?P<product_id>\d+)/$', 'buy_detail', name="buy_detail"),
     #西装类别
    url(r'^product_type/$', 'product_type', name="product_type"),
    url(r'^type_post/$', 'type_post', name="type_post"),
    #为谁定制
    #url(r'^order4who/$', 'order4who', name="order4who"),
    #test
    url(r'^order4who/$',  TemplateView.as_view(template_name='wap/1.1.html'), name="order4who"),
    url(r'^order4who_test/$',  TemplateView.as_view(template_name='wap/1.1.html'), name="order4who"),
    url(r'^order4who_post/$', 'order4who_post', name="order4who_post"),
    #选择面料
    url(r'^fabric_select/$', 'fabric_select', name="fabric_select"),
    url(r'^fabric_select_post/$', 'fabric_select_post', name="fabric_select_post"),
    #款式选择  type:shangyi（上衣） xiku（西裤） chenshan（衬衫）
    url(r'^style_select_redirect/$', 'style_select_redirect', name="style_select"),
    url(r'^style_select/(?P<type>\w+)/$', 'style_select', name="style_select"),
    url(r'^style_select_post/$', 'style_select_post', name="style_select_post"),
    #个性化选择 type: suit or shirt
    url(r'^personalization_select/$', 'personalization_select', name="personalization_select"),
    url(r'^personalization_select_post/$', 'personalization_select_post', name="personalization_select_post"),
    #预约量体
    url(r'^reserve_measure/$', 'reserve_measure', name="reserve_measure"),
    url(r'^reserve_measure_post/$', 'reserve_measure_post', name="reserve_measure_post"),
    #推广预约
    url(r'^reserve/$', 'reserve', name="reserve"),
    url(r'^reserve_post/$', 'reserve_post', name="reserve_post"),
    #购物车
    url(r'^cart_add/$', 'cart_add', name="cart_add"),
    url(r'^cart_view/$', 'cart_view', name="cart_view"),
    url(r'^cart_post/$', 'cart_post', name="cart_post"),
    url(r'^cart_update_post/$', 'cart_update_post', name="cart_update_post"),
    url(r'^cart_clean/$', 'cart_clean', name="cart_clean"),
    url(r'^cart_delete_post/$', 'cart_delete_post', name="cart_delete_post"),
    #优惠券
    url(r'^redpacket_view/$', 'redpacket_view', name="redpacket_view"),
    url(r'^redpacket_post/$', 'redpacket_post', name="redpacket_post"),
    #订单列表 我的订单
    url(r'^order_list/$', 'order_list', name="order_list"),
    #订单详情
    url(r'^order_detail/(?P<order_id>\w+)/$', 'order_detail', name="order_detail"),
    ##提交订单
    #url(r'^order_summit_post/$', 'order_summit_post', name="order_summit_post"),
    #地址列表 地址选择页面
    url(r'^address_list/$', 'address_list', name="address_list"),
    #选择某个地址
    url(r'^address_select_post/$', 'address_select_post', name="address_select_post"),
    #添加地址
    url(r'^address_add_post/$', 'address_add_post', name="address_add_post"),
    #删除地址
    url(r'^address_delete_post/$', 'address_delete_post', name="address_delete_post"),
    #修改地址
    url(r'^address_update_post/$', 'address_update_post', name="address_update_post"),
    url(r'^buyorder_post/$', 'buyorder_post', name="buyorder_post"),
    url(r'^buyorder_cancel_post/$', 'buyorder_cancel_post', name="buyorder_cancel_post"),
    #定制文化
    url(r'^culture/$',  TemplateView.as_view(template_name='wap/13.html'), name="culture"),
    #关于我们
    url(r'^about/$',  TemplateView.as_view(template_name='wap/14.html'), name="about"),
    #服务条款
    url(r'^service/$',  TemplateView.as_view(template_name='wap/15.html'), name="about"),
    
    # 每次调用 会重新计算每个人胸围等尺寸的百分比,并写入数据库。用cron每天凌晨定时调用
    url(r'^cron/$',  'cron', name="cron"),
    #list of links , for debug only
    url(r'^index/$',  TemplateView.as_view(template_name='wap/index.html'), name="index"),
    
    
)

urlpatterns += patterns('wap.redpacket',
    url(r'^redpacket/$', 'redpacket_home', name="redpacket_home"),
    url(r'^redpacket_info/$', 'redpacket_info', name="redpacket_info"),
    url(r'^hbphone_post/$', 'hbphone_post', name="hbphone_post"),
    url(r'^redpackettop/$', 'redpackettop', name="redpackettop"),
    url(r'^forward_post/$', 'forward_post', name="forward_post"),
    url(r'^all_coupons/$', 'all_redpacket', name="all_redpacket"),
)

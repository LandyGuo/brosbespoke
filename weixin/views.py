#!/usr/bin/env python2.7
# coding:utf8
import re
import hashlib
import datetime


from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
import logging
from models import *
from wap.models import *
from ShiXiongDeYiGui.settings import TOKEN,APPID, APP_SECRET

from utils import *
from wxpayutil import *

import sys
from django.core.context_processors import request
reload(sys)
sys.setdefaultencoding('utf-8')

REPLY_DATA = '''
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    %s
    </xml>
'''

TYPE_CONTENT_DICT = {
    'text': '<Content><![CDATA[%s]]></Content>',
    'news': '<ArticleCount>%s</ArticleCount><Articles>%s</Articles>'
}

ARTICLES = '''
    <item>
    <Title><![CDATA[%s]]></Title> 
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
    </item>
'''
def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger

logging.basicConfig(level=logging.DEBUG)


def gen_xml(instance, app_item):
    retype = instance.message.retype
    type_content = TYPE_CONTENT_DICT.get(retype, '')
    resource = instance.message.get_resource()
   # user_info_url = 'https:#open.weixin.qq.com/connect/oauth2/authorize?appid='+app_item.appid+'&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
    # 文本回复
    if retype == 'text':
        content = type_content % resource.content
        
        
    #    content = type_content % c

    # 图文回复
    elif retype == 'news':
        if not resource:
            return ''
        articles_str = ''
        for article in resource.articles.all():
            art_param = (
                article.title,
                article.description,
                article.get_image_url(),
                article.get_url(),
            )
            articles_str += ARTICLES % art_param
        content = type_content % (resource.articles.count(), articles_str)
    
    params = (
        instance.from_user,
        instance.to_user,
        instance.message.get_create_time(),
        retype,
        content,
    )
    return REPLY_DATA % params


def home(request):
    return render_to_response('home.html')

# def index(request):
#    '''网页授权获取用户基本信息'''
#    api = 'https:#api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID, APP_SECRET, request.GET.get('code'))
#    data = method_get_api(api)
#    token = data.get('access_token')
#    openid = data.get('openid')
#    
#    api2 = 'https:#api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN'%(token, openid)
#    print method_get_api(api2)
# 
#    return HttpResponse(json_data, content_type="application/json")


class ParseMessage():
    touser_re = r'<ToUserName><!\[CDATA\[(.+)\]\]></ToUserName>'
    fromuser_re = r'<FromUserName><!\[CDATA\[(.+)\]\]></FromUserName>'
    content_re = r'<Content><!\[CDATA\[(.+)\]\]></Content>'
    msgtype_re = r'<MsgType><!\[CDATA\[(.+)\]\]></MsgType>' 
    picurl_re = r'<PicUrl><!\[CDATA\[(.+)\]\]></PicUrl>'
    mediaid_re = r'<MediaId><!\[CDATA\[(.+)\]\]></MediaId>'
    msgid_re = r'<MsgId>(\d+)</MsgId>'        
    event_re = r'<Event><!\[CDATA\[(.+)\]\]></Event>'    
    eventkey_re = r'<EventKey><!\[CDATA\[(.+)\]\]></EventKey>'    
    latitude_re = r'<Latitude>(.+)</Latitude>'
    longitude_re = r'<Longitude>(.+)</Longitude>'
    precision = r'<Precision>(.+)</Precision>'

    appid_re = r'<appid><!\[CDATA\[(.+)\]\]></appid>'
    bank_type_re = r'<bank_type><!\[CDATA\[(.+)\]\]></bank_type>'
    cash_fee_re = r'<cash_fee><!\[CDATA\[(.+)\]\]></cash_fee>'
    fee_type_re = r'<fee_type><!\[CDATA\[(.+)\]\]></fee_type>'
    is_subscribe_re = r'<is_subscribe><!\[CDATA\[(.+)\]\]></is_subscribe>'
    mch_id_re = r'<mch_id><!\[CDATA\[(.+)\]\]></mch_id>'
    nonce_str_re = r'<nonce_str><!\[CDATA\[(.+)\]\]></nonce_str>'
    openid_re = r'<openid><!\[CDATA\[(.+)\]\]></openid>'
    out_trade_no_re = r'<out_trade_no><!\[CDATA\[(.+)\]\]></out_trade_no>'
    result_code_re = r'<result_code><!\[CDATA\[(.+)\]\]></result_code>'
    return_code_re = r'<return_code><!\[CDATA\[(.+)\]\]></return_code>'
    sign_re = r'<sign><!\[CDATA\[(.+)\]\]></sign>'
    time_end_re = r'<time_end><!\[CDATA\[(.+)\]\]></time_end>'
    total_fee_re = r'<total_fee>(\d+)</total_fee>'
    trade_type_re = r'<trade_type><!\[CDATA\[(.+)\]\]></trade_type>'
    transaction_id_re = r'<transaction_id><!\[CDATA\[(.+)\]\]></transaction_id>'

    def __init__(self, body, WXConfig):
        self.body = body
        self.WXConfig = WXConfig

    def notify_parse_xml(self):     
        self.return_code = self.re_find(self.return_code_re)
        self.result_code = self.re_find(self.result_code_re)
        self.openid = self.re_find(self.openid_re)
        self.appid = self.re_find(self.appid_re)
        self.mch_id = self.re_find(self.mch_id_re)
        self.sign = self.re_find(self.sign_re)
        self.out_trade_no = self.re_find(self.out_trade_no_re)
        self.total_fee = self.re_find(self.total_fee_re)
        self.transaction_id = self.re_find(self.transaction_id_re)
        self.bank_type = self.re_find(self.bank_type_re)
        self.trade_type = self.re_find(self.trade_type_re)
    def parse_xml(self):     
        self.to_user = self.re_find(self.touser_re)
        self.from_user = self.re_find(self.fromuser_re)

        self.msgtype = self.re_find(self.msgtype_re)

        if self.msgtype != 'event':
            # 关键字回复
            self.content = self.re_find(self.content_re)
            self.message = self.WXConfig.messages.filter(keyword=self.content, tag='keyword_recontent').first()  
            if not self.message:
                # 无匹配回复
                self.message = self.WXConfig.messages.filter(tag='keyword_default_recontent').first()  
        else:
            self.event = self.re_find(self.event_re)
    
            if self.event == 'CLICK':
                # menu click事件
                self.eventkey = self.re_find(self.eventkey_re)
                self.message = self.WXConfig.messages.filter(tag='keyword_recontent', keyword=self.eventkey).first()
            elif self.event == 'subscribe':
                # 关注,是否有EventKey，有的话，就是扫描带参数二维码事件
                self.message = self.WXConfig.messages.filter(tag=self.event).first() 
            elif self.event == 'unsubscribe':
                # 取消关注
                pass
            elif self.event == 'LOCATION':
                # 地理位置
                pass
            elif self.event == 'SCAN':
                # 扫描带参数二维码事件，用户已关注时的事件推送
                pass
            

    def re_find(self, re_str):
        data_result = re.findall(re_str, self.body)
        return data_result and data_result[0] or ''

    
def check(params):
    #signature = params.get('signature', '')
    signature = params['signature']
    #timestamp = params.get('timestamp', '')
    timestamp = params['timestamp']
    #nonce = params.get('nonce', '')
    nonce = params['nonce']
    token = TOKEN

    #tmp_str = ''.join(sorted([token, timestamp, nonce]))
    #tmp_str = hashlib.sha1(tmp_str).hexdigest()
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    tmp_str=sha1.hexdigest()
    
    if tmp_str == signature:
        return True
    else:
        return False        

def checkSignature(request):  
    signature = request.GET.get("signature", None)  
    timestamp = request.GET.get("timestamp", None)  
    nonce = request.GET.get("nonce", None)  
    echoStr = request.GET.get("echostr",None)  
  
    token = TOKEN  
    tmpList = [token,timestamp,nonce]
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList)  
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:  
        return True  
    else:  
        return None  
    
@csrf_exempt
def weixin_token(request):
    if not checkSignature(request):
        raise Http404
    
    echostr = request.get("nonce", '') 
    
    #test
    #echostr = 'test'
    return HttpResponse(echostr,content_type="text/plain")


@csrf_exempt
def weixin_api(request, slug):
    app_item = WXConfig.objects.filter(id=slug)[0]
    
    if not app_item or not check(request.GET):
        raise Http404
    
    
    # 第一次验证开发者,如果失败，手动改is_valid为False,重新验证
    if not app_item.is_valid:
        echostr = request.GET.get('echostr', '')
        app_item.is_valid = True
        app_item.save()
        return HttpResponse(echostr)
    try:
        msg = ParseMessage(request.body, app_item)
        # file('/var/www/body.xml', 'w').write(request.body) #测试
        msg.parse_xml()
        return_data = ''
        if hasattr(msg, 'message'):
            if msg.message:
                return_data = gen_xml(msg, app_item)    
    except Exception, data:
        print '22222222222'
        print Exception, ":", data
    try:
        print 'aaaaaaaaaaa'
        if hasattr(msg, 'event'): 
            print 'bbbbbbbbbb'
            print msg.event
            # 关注后增加用户信息
            if msg.event == 'subscribe':
                openid = msg.from_user
                user_info = app_item.get_user_info(openid)
                user = WXUser.objects.filter(openid=msg.from_user).first()
                if not user:
                    user = WXUser()
                user.nickname = user_info.get('nickname')
                user.openid = user_info.get('openid')
                user.sex = user_info.get('sex')
                user.language = user_info.get('language')
                user.city = user_info.get('city')
                user.province = user_info.get('province')
                user.country = user_info.get('country')
                user.headimgurl = user_info.get('headimgurl')
                user.save()
                if not app_item.app_users.filter(openid=openid).exists():
                    app_item.app_users.add(user)
            elif msg.event == 'unsubscribe':
                openid = msg.from_user
                user = WXUser.objects.filter(openid=openid).first()
                app_item.app_users.remove(user)
    except Exception, data:
        print Exception, ":", data

    return HttpResponse(return_data, content_type="application/xhtml+xml")

@csrf_exempt
def wx_create_menu(request, app_secret):
    app_item = WXConfig.objects.filter(app_secret=app_secret)[0]
    menu = '''''{ 
    "button": [
        {
            "type": "view", 
            "name": "量身定制", 
            "url": "http://brosbespoke.com/wap/buy", 
            "sub_button": [ ]
        }, 
        {
            "name": "BB服务", 
            "sub_button": [
                {
                    "type": "view", 
                    "name": "售后服务", 
                    "url": "http://brosbespoke.com/wap/service", 
                    "sub_button": [ ]
                }, 
                {
                    "type": "view", 
                    "name": "定制文化", 
                    "url": "http://brosbespoke.com/wap/culture", 
                    "sub_button": [ ]
                }, 
                {
                    "type": "view", 
                    "name": "关于我们", 
                    "url": "http://brosbespoke.com/wap/about", 
                    "sub_button": [ ]
                }
            ]
        }, 
        {
            "name": "个人中心", 
            "sub_button": [
                {
                    "type": "view", 
                    "name": "优惠券", 
                    "url": "http://brosbespoke.com/wap/coupons", 
                    "sub_button": [ ]
                }, 
                {
                    "type": "view", 
                    "name": "我的尺寸", 
                    "url": "http://brosbespoke.com/wap/show_my_size", 
                    "sub_button": [ ]
                }, 
                {
                    "type": "view", 
                    "name": "我的订单", 
                    "url": "http://brosbespoke.com/wap/order_list", 
                    "sub_button": [ ]
                }, 
                {
                    "type": "view", 
                    "name": "个人信息", 
                    "url": "http://brosbespoke.com/wap/my_info", 
                    "sub_button": [ ]
                }
            ]
        }
    ]
     }''' 
    return app_item.create_menu( menu.encode('utf-8'))

    
def message(request):
    return HttpResponse('ok')

@csrf_exempt
def wxpay_notify_url(request):
    app_item = WXConfig.objects.get(appid=APPID)
    msg = ParseMessage(request.body, app_item)
    msg.notify_parse_xml()
    appid = msg.appid
    mch_id = msg.mch_id
    #nonce_str = msg.nonce_str
    openid = msg.openid
    out_trade_no = msg.out_trade_no
    result_code = msg.result_code
    return_code = msg.return_code
    sign = msg.sign
    total_fee = msg.total_fee
    transaction_id = msg.transaction_id
    bank_type = msg.bank_type
    trade_type = msg.trade_type
    try:
        item = Wxpay.objects.get(wxpay_id=transaction_id)
    except:
        wxpay = Wxpay.objects.get(out_trade_no=out_trade_no)
        wxpay.appid = appid
        wxpay.wxpay_id = transaction_id
        wxpay.mch_id = mch_id
        wxpay.openid = openid
        #wxpay.out_trade_no = out_trade_no
        wxpay.result_code = result_code
        wxpay.return_code = return_code
        wxpay.total_fee = total_fee
        wxpay.transaction_id = transaction_id
        wxpay.bank_type = bank_type
        wxpay.trade_type = trade_type
        wxpay.save()
        if wxpay.result_code == 'SUCCESS':
            redpackets= Redpacket.objects.filter(openid=openid, isUsed = '2')
            for redpacket in redpackets:
                redpacket.isUsed = '1'
                redpacket.save()
            cart_list = Cart.objects.filter(wxpay_id=wxpay.id)
            for carts in cart_list:
                order = Order()
                order.user_id = carts.user_id
                order.price = carts.price
                order.wxpay_id = carts.wxpay_id
                order.order_status ='已付款'
                order.product_id = carts.product_id
                order.is4friend = carts.is4friend
                order.friend_phone =carts.friend_phone
                order.fabric_id = carts.fabric_id
                order.address_id = carts.address_id
                #上衣参数carts
                order.kouxing_sy = carts.kouxing_sy
                order.lingxing_sy = carts.lingxing_sy
                order.yaodou_sy = carts.yaodou_sy
                order.kaiqi_sy = carts.kaiqi_sy
                order.xiukou_sy = carts.xiukou_sy
                order.neibuzaoxing_sy = carts.neibuzaoxing_sy
                order.neibudou_sy = carts.neibudou_sy
                # 西裤参数carts.
                order.kuzhe_xk = carts.kuzhe_xk
                order.houdou_xk = carts.houdou_xk
                order.kujiao_xk = carts.kujiao_xk
                #衬衫参数carts.
                order.lingxing_cs = carts.lingxing_cs
                order.xiukou_cs = carts.xiukou_cs
                order.xiabai_cs = carts.xiabai_cs
                order.menjin_cs = carts.menjin_cs
                order.houbei_cs = carts.houbei_cs
                order.koudai_cs = carts.koudai_cs
                # 个性化carts.
                order.add_kuzi = carts.add_kuzi
                order.add_majia = carts.add_majia
                order.majia_lingxing =carts.majia_lingxing
                order.majia_kouxing =carts.majia_kouxing
                order.add_bespoke = carts.add_bespoke
                order.add_xiuzi = carts.add_xiuzi
                order.xiuzi = carts.xiuzi
                order.save()
                order.order_number = '%0*d' % (12, order.id)
                order.save()
            cart_list = Cart.objects.filter(wxpay_id=wxpay.id).delete()


    return HttpResponse('ok')

def wxpay_pay(request):
    #/**
    # * JS_API支付demo
    # * ====================================================
    #* 在微信浏览器里面打开H5网页中执行JS调起支付。接口输入输出数据格式为JSON。
    #* 成功调起支付需要三个步骤：
    #* 步骤1：网页授权获取用户openid
    #* 步骤2：使用统一支付接口，获取prepay_id
    #* 步骤3：使用jsapi调起支付
    #*/
    
    #使用jsapi接口
    jsApi = JsApi_pub()
    #=========步骤1：网页授权获取用户openid============
    #通过code获得openid
    if not request.GET.get('code'):
        #触发微信返回code码
        url = jsApi.createOauthUrlForCode(WxPayConf_pub.JS_API_CALL_URL)
        #Header("Location: url");
        return HttpResponseRedirect(url) 
    else:
        #获取code码，以获取openid
        code = request.GET.get('code')
        jsApi.setCode(code)
        openid = jsApi.getOpenId()
    
    #=========步骤2：使用统一支付接口，获取prepay_id============
    #使用统一支付接口
    unifiedOrder = UnifiedOrder_pub()
    
    
        #title = title.append(str(order.product.title))
    #order = get_object_or_404(Order, id=2)
    #设置统一支付接口参数
    #设置必填参数
    #appid已填,商户无需重复填写
    #mch_id已填,商户无需重复填写
    #noncestr已填,商户无需重复填写
    #spbill_create_ip已填,商户无需重复填写
    #sign已填,商户无需重复填写
    unifiedOrder.setParameter("openid",openid)#商品描述
    unifiedOrder.setParameter("body",'brosbespoke')#商品描述
    #自定义订单号，此处仅作举例
    timeStamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    out_trade_no = WxPayConf_pub.APPID+''+timeStamp
    wxpay = Wxpay()
    wxpay.out_trade_no = out_trade_no
    wxpay.save()
    user_id = request.session['userid']
    cart_list = Cart.objects.filter(user_id=user_id)
    cartid = request.session['cartlist']
    price = 0
    for i in cartid:
        carts = cart_list[int(i)]
        price = price + carts.price
        carts.wxpay_id = wxpay.id
        carts.save()
    redpackets= Redpacket.objects.filter(user_id=user_id, isUsed = '2')
    for redpacket in redpackets:
        price = price - redpacket.money
        
        #order_price = order_price - redpackets.money
    unifiedOrder.setParameter("out_trade_no",out_trade_no)#商户订单号 
    unifiedOrder.setParameter("total_fee",str(int(float(price) * 100)) )#总金额
    unifiedOrder.setParameter("notify_url",WxPayConf_pub.NOTIFY_URL)#通知地址 
    unifiedOrder.setParameter("trade_type","JSAPI")#交易类型
    request.session['out_trade_no'] = out_trade_no
    #get_logger().debug('----------out_trade_no----'+ str(out_trade_no))
    #非必填参数，商户可根据实际情况选填
    #unifiedOrder.setParameter("sub_mch_id","XXXX");#子商户号  
    #unifiedOrder.setParameter("device_info","XXXX");#设备号 
    #unifiedOrder.setParameter("attach","XXXX");#附加数据 
    #unifiedOrder.setParameter("time_start","XXXX");#交易起始时间
    #unifiedOrder.setParameter("time_expire","XXXX");#交易结束时间 
    #unifiedOrder.setParameter("goods_tag","XXXX");#商品标记 
    #unifiedOrder.setParameter("openid","XXXX");#用户标识
    #unifiedOrder.setParameter("product_id","XXXX");#商品ID
    prepay_id = unifiedOrder.getPrepayId()
    #=========步骤3：使用jsapi调起支付============
    jsApi.setPrepayId(prepay_id)
    jsApiParameters = jsApi.getParameters()
    #echo jsApiParameters;
    return render_to_response('weixin/wxpay.html', {'jsApiParameters': jsApiParameters})
    
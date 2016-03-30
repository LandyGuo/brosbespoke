# coding:utf8
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.six.moves.urllib.parse import urlparse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import random
import json
import string
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from weixin.utils import method_get_api
from ShiXiongDeYiGui.settings import APPID , APP_SECRET
from urllib import quote_plus
import time
import logging
from urllib import urlencode
from weixin.models import WXUser

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger

logging.basicConfig(level=logging.DEBUG)


import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

import weixin.utils
from wap.models import *

#保存session
def flush_session(request):
    request.session.save()
    request.session.modified = True
    
# 发送短信验证码
def send_sms_code(phone, code):
    url = u'http://106.ihuyi.cn/webservice/sms.php?method=Submit&account=cf_bb8888&password=fubang309&mobile=' + phone + '&content=您的验证码是：【' + code + '】。请不要把验证码泄露给其他人。'
    ret = weixin.utils.method_get_api_xml(url)
    get_logger().debug('------------------------url= %s', url)
    return ret['SubmitResult']['code']

def check_user(func):
    ''' check user session '''
    def wrapper(request,*args, **kv):
        userinfo=request.session.get('userid',None)    
        path = request.get_full_path()
        if not userinfo:
            return HttpResponseRedirect('/wap/login?returnUrl='+ path) #没有登录，则跳转到登录页面       
        return func(request,*args, **kv)        
    return wrapper




#首页  
  
def buy(request):
    product_list1 = Product.objects.filter(type='suit')
    product_list2 = Product.objects.filter(type='shirt')
    banner_list = Banner.objects.all()
    try:
        user_id = request.session['userid']
        cart_list = Cart.objects.filter(user_id=user_id)
        request.session["carts_number"] = str(len(cart_list))
    except:
        request.session["carts_number"] = 0
    return render_to_response('wap/home.html', {'product_list1': product_list1,'product_list2': product_list2,'banner_list':banner_list,'request':request})


#产品详情

def buy_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.session['order__product_id'] = product_id
    request.session['order__product_type'] = product.type
    flush_session(request)
    fabric_list = Fabric.objects.filter(product_id = product_id)
    craft_desc = product.craft.split('|');
    fabric_desc = []
    fabric_items = product.fabricname.split('|');
    for str in fabric_items:
        fabric_desc.append(str.split('\n'));
    return render_to_response('wap/content.html', {'productinfo': product, 'craft_desc':craft_desc, 'fabric_desc':fabric_desc,'fabric_list':fabric_list,'request':request})


#西装类别页面
@csrf_exempt
def product_type(request):
    product_id = request.session['order__product_id']
    product_info = Product.objects.get(id = product_id)
    majia_config = OrderPersonalization.objects.get(name='单加马甲', product_name=product_info.title)
    order_price = int(product_info.price)
    mtm_prce2 = order_price
    mtm_prce3 = order_price + int(majia_config.price)
    product_prce2 = order_price + 800
    product_prce3 = product_prce2 + int(majia_config.price)
    return render_to_response('wap/custom/custom_type.html', {'order_price':order_price,
                                                'product_prce2':product_prce2,
                                                'product_prce3':product_prce3,
                                                'mtm_prce2':mtm_prce2,
                                                'mtm_prce3':mtm_prce3,
                                                })

#西装类别选择提交
@csrf_exempt
def type_post(request):
    response_data = {}
    response_data['code'] = '-1'
    if request.method == 'POST':
        product_id = request.session['order__product_id']
        product_info = Product.objects.get(id = product_id)
        majia_config = OrderPersonalization.objects.get(name='单加马甲', 
                                                        product_name=product_info.title
                                                        )
        order_price = int(product_info.price)
        add_majia = request.POST['add_majia']
        add_bespoke = request.POST['add_bespoke']
        request.session['order__personalization__add_majia'] = add_majia
        request.session['order__personalization__add_bespoke'] = add_bespoke
        if int(add_majia) == 1:
            order_price = order_price + int(majia_config.price)
        if int(add_bespoke) == 1:
            order_price = order_price + 800
        request.session['order__price'] = order_price
        #request.session['suit_type'] = suit_type
        response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def order4who_post(request):
    response_data = {}
    response_data['code'] = -1 
    if request.method == 'POST':
        is4friend = request.POST.get('is4friend','0')
        request.session['order__is4friend'] = is4friend
        if int(is4friend):
            request.session['order__friend_phone'] = request.POST.get('phone','')
        response_data['code'] = 0
        flush_session(request)
        if request.session['order__product_type'] == 'suit':
            response_data['url'] = '/wap/product_type' 
        elif request.session['order__product_type'] == 'shirt':
            response_data['url'] = '/wap/fabric_select'
        if int(is4friend):
            phone = request.session['order__friend_phone'] 
            fri_userinfo =User.objects.filter(phonenumber=str(phone))
            if not fri_userinfo:
                response_data['code'] = 1 #数据库没有朋友的信息
            elif fri_userinfo[0].measure_status==0:  #添加索引[0] 
                response_data['code'] = 1 #数据库有朋友的电话，但没有量体
        else: 
            userinfo=request.session.get('userid',None)
            if not userinfo:
                product_id = request.session.get('order__product_id',None)
                if product_id:
                    response_data['url'] = '/wap/reserve'
                else:
                    response_data['url'] = '/wap/reserve'
            else:
                userid = request.session['userid']
                userinfo = User.objects.get(id=userid)
                if userinfo.measure_status == 0:
                    response_data['code'] = 1 #没有量体
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 选择面料
def fabric_select(request):
    product_id = request.session['order__product_id']
    fabric_list = Fabric.objects.filter(product_id = product_id)
    product = get_object_or_404(Product, id=product_id)
    if request.session['order__product_type'] == 'suit':
        order_price = request.session['order__price']
        kuzi_config = OrderPersonalization.objects.get(name='单加裤子',product_name=product.title)
        info = 2
    elif request.session['order__product_type'] == 'shirt':
        request.session['order__price'] = product.price
        order_price = request.session['order__price']
        kuzi_config = None
        info = 1
    return render_to_response('wap/2.1.html', {'fabric_list':fabric_list,'product':product,
                                               'request':request,'kuzi_config':kuzi_config,
                                               'info':info,'order_price':order_price
                                               })

# 选择面料 post,参数
#    fabric_id, 面料id
# 返回值 code, -1：失败； 0：成功  
#    msg， 错误原因
@csrf_exempt
def fabric_select_post(request):
    get_logger().debug('------------------------fabric_select_post request')
    get_logger().debug('------------------------fabric_select_post request.POST["fabric_id"]'+request.POST['fabric_id'])
    response_data = {}
    if request.method == 'POST':
        order_price = request.session['order__price']
        add_kuzi = request.POST['add_kuzi']
        request.session['order__personalization__add_kuzi'] = add_kuzi
        if int(add_kuzi) ==1:
            product_id = request.session['order__product_id']
            product = get_object_or_404(Product, id=product_id)
            kuzi_config = OrderPersonalization.objects.get(name='单加裤子',product_name=product.title)
            request.session['order__price'] = order_price + kuzi_config.price
        fabric_id = request.POST['fabric_id']
        try:
            request.session['order__fabric'] = fabric_id
            flush_session(request)
            response_data['code'] = '0'
        except ObjectDoesNotExist:
            response_data['code'] = '-1'
            response_data['msg'] = '数据为空'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

# 选择款式 根据西服还是衬衫，重定向到相应的选择款式页面

def style_select_redirect(request):
    redirect_url = '/'
    if request.session['order__product_type'] == 'suit':
        redirect_url = '/wap/style_select/shangyi' 
    elif request.session['order__product_type'] == 'shirt':
         redirect_url = '/wap/style_select/chenshan'
    return HttpResponseRedirect(redirect_url)

# 选择款式.
@check_user
def style_select(request, type):
    is4friend = request.session['order__is4friend']
    if is4friend=='1':#肯定要加''号
        phone = request.session['order__friend_phone'] 
        fri_userinfo =User.objects.filter(phonenumber=phone)#得到的不只一个object
        if  not fri_userinfo:
            return HttpResponseRedirect('/wap/reserve_measure') #数据库没有朋友的信息则跳转到预约量体页面 
        if  fri_userinfo[0].measure_status==0:  #添加索引[0] 
            return HttpResponseRedirect('/wap/reserve_measure') #数据库有朋友的电话，但没有量体，则跳转到预约量体页面  
    else: 
        userid = request.session['userid']
        userinfo = User.objects.get(id=userid)
        if userinfo.measure_status == 0:
            return HttpResponseRedirect('/wap/reserve_measure') #没有量体，则跳转到预约量体页面 
    product_id = request.session['order__product_id']
    product = get_object_or_404(Product, id=product_id)
    if type == 'shangyi':
        if int(request.session['order__personalization__add_majia']):
            majia_kouxing_list = MaJiaKouXing.objects.all()
            majia_lingxing_list = MaJiaLingXing.objects.all()
        else:
            majia_kouxing_list = None
            majia_lingxing_list = None
        order_price = request.session['order__price']
        return render_to_response('wap/1.2.1西服款式选择.html', {'kouxing_list':KouXingShangYi.objects.all(),
                                                   'lingxing_list':LingXingShangYi.objects.all(),
                                                   'yaodou_list':YaoDouShangYi.objects.all(),
                                                   'kaiqi_list':KaiQiShangYi.objects.all(),
                                                   'xiukou_list':XiuKouShangYi.objects.all(),
                                                   'neibuzaoxing_list':NeiBuZaoXingShangYi.objects.all(),
                                                   'neibudou_list':NeiBuDouShangYi.objects.all(),
                                                   'kuzhe_list':KuZheXiKu.objects.all(),
                                                   'houdou_list':HouDouXiKu.objects.all(),
                                                   'kujiao_list':KuJiaoXiKu.objects.all(),
                                                   'product':product,
                                                   'order_price':order_price,
                                                   'request':request,'majia_kouxing_list':majia_kouxing_list,
                                                   'majia_lingxing_list':majia_lingxing_list
                                                   })
    #elif type == 'xiku':
        #return render_to_response('wap/3.2.html', {'kuzhe_list':KuZheXiKu.objects.all(),
                                                   #'houdou_list':HouDouXiKu.objects.all(),
                                                   #'kujiao_list':KuJiaoXiKu.objects.all(),
                                                   #'product':product,})
    elif type == 'chenshan':
        return render_to_response('wap/1.2.2衬衫款式选择.html', {'lingxing_list':LingXingChenShan.objects.all(),
                                                   'xiukou_list':XiuKouChenShan.objects.all(),
                                                   'xiabai_list':XiaBaiChenShan.objects.all(),
                                                   'menjin_list':MenJinChenShan.objects.all(),
                                                   'houbei_list':HouBeiChenShan.objects.all(),
                                                   'koudai_list':KouDaiChenShan.objects.all(),
                                                   'product':product,
                                                   'request':request})
    else:
        # 404
        pass
    return render_to_response('wap/3.1.html', {'request':request})

# 选择款式 post,参数
#    type:shangyi（上衣） xiku（西裤） chenshan（衬衫）
#    参数名：设计中参数名称全拼（首字母大写）+type中文名的全拼（首字符大写）； 值：已选的中文，如果是多选，用‘|’分隔. 
#        比如 ：上衣款型选择的领型 为平驳头， 则 post参数包含LingXingShangYi，对应值为‘平驳头'
# 返回值 code, -1：失败； 0：成功  
#    msg， 错误原因
@csrf_exempt
def style_select_post(request):
    response_data = {}
    response_data['code'] = '-1'
    
    if request.method == 'POST':
        keys = request.POST.keys()
        get_logger().debug('------------------------style_select_post start---------------')
        for key in keys:
            get_logger().debug('------------------------param: ('+str(key)+','+str(request.POST[key])+')')
            if key.endswith('ShangYi') or key.endswith('XiKu') or key.endswith('ChenShan') :
                request.session['order__style__'+key] = request.POST[key]
        get_logger().debug('------------------------style_select_post end---------------')
        try:
            request.session['order__personalization__majia_lingxing'] = request.POST['majia_lingxing']
            request.session['order__personalization__majia_kouxing'] = request.POST['majia_kouxing']
        except:
            request.session['order__personalization__majia_lingxing'] = []
            request.session['order__personalization__majia_kouxing'] = []
        flush_session(request)

        response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

# 个性化
def personalization_select(request):
    order_price = request.session['order__price']
    product_id = request.session['order__product_id']
    product = get_object_or_404(Product, id=product_id)
    if product.type == 'suit':
        info = 4
    #     xiuzi_config = OrderPersonalization.objects.get(product_type = 'suit',name='绣字')
    # # if product.type == 'suit':
    # #     xiuzi_config = OrderPersonalization.objects.get(product_type = 'suit',name='绣字')
    # #     bespoke_config = OrderPersonalization.objects.get(name='Bespoke')
    # #     product_id = request.session['order__product_id']
    # #     product_info = Product.objects.get(id=product_id) 
    # #     majia_config = OrderPersonalization.objects.get(name='单加马甲',product_name=product_info.title)
    # #     kuzi_config = OrderPersonalization.objects.get(name='单加裤子',product_name=product_info.title)
    # #     return render_to_response('wap/1.3.2个性化选择.html', {'kouxing_list':MaJiaKouXing.objects.all(),
    # #                                                'lingxing_list':MaJiaLingXing.objects.all(),
    # #                                                'xiuzi_price':"{0:.0f}".format(xiuzi_config.price),
    # #                                                'bespoke_price':"{0:.0f}".format(bespoke_config.price),
    # #                                                'majia_price':"{0:.0f}".format(majia_config.price),
    # #                                                'kuzi_price':"{0:.0f}".format(kuzi_config.price),
    # #                                                'product':product,'request':request})
    elif product.type == 'shirt':
        info = 3
    #     xiuzi_config = OrderPersonalization.objects.get(product_type = 'shirt',name='绣字')
    return render_to_response('wap/4.3.html', {'info':info,'product':product,'order_price':order_price,'request':request})
    # else:
    #     # 404
    #     pass
    # return render_to_response('wap/4.1.html', {'request':request})

# 选择个性化 post,参数
#    type:suit（西装） shirt（衬衫）
#    add_kuzi 单加裤子 1：选择 ； 0：没有选择
#    add_majia 单加马甲 1：选择 ； 0：没有选择
#    add_bespoke Bespoke 1：选择 ； 0：没有选择
#    add_xiuzi 绣字 1：选择 ； 0：没有选择
#    majia_lingxing 马甲领型  ：选择的中文
#    majia_kouxing 马甲扣型  ：选择的中文
#    xiuzi 绣字
# 返回值 code, -1：失败； 0：成功  
#    msg， 错误原因

@csrf_exempt
def personalization_select_post(request):
    response_data = {}
    response_data['code'] = '-1'
    if request.method == 'POST':
        # type = request.POST['type']

        product_id = request.session['order__product_id']
        #product = get_object_or_404(Product, id=product_id)
        #order_price = product.price
        #request.session['order__price'] = order_price
        #TODO: set correct price
        request.session['order__price'] = request.POST['price']
    
        #根据选择的设置，设置用户价格.安全起见，不能用前端post来的价格
        request.session['order__personalization__add_xiuzi'] = request.POST['add_xiuzi']
        if request.POST['add_xiuzi']:
            request.session['order__personalization__xiuzi'] = request.POST['xiuzi']
        # if type == 'suit':
        #     request.session['order__personalization__add_kuzi'] = request.POST['add_kuzi']
        #     request.session['order__personalization__add_majia'] = request.POST['add_majia']
        #     request.session['order__personalization__add_bespoke'] = request.POST['add_bespoke']
        #     if request.POST['add_majia']:
        #         request.session['order__personalization__majia_lingxing'] = request.POST['majia_lingxing']
        #         request.session['order__personalization__majia_kouxing'] = request.POST['majia_kouxing']
        # elif type == 'shirt':
        #     pass
        # else :
        #     #404
        #     pass
        flush_session(request)
        response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 量体预约.
def reserve_measure(request):
    return render_to_response('wap/addressee_1.6.html', {'request':request})

# 量体预约post,参数
#    sex(性别)‘男’‘女’
#    height(身高cm)
#    weight(体重kg)
#    reservation_time(预约时间) 格式 2015-04-01 16:00
#    address_region 省市两级：北京市 海淀区 
#    address_street 街道地址
# 返回值 code, -1：失败； 0：成功  
#    msg， 错误原因
@csrf_exempt
def reserve_measure_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '提交失败'
    userid = request.session['userid']
    userinfo = User.objects.get(id=userid)
    worktime = Worktime.objects.all()
    if request.method == 'POST':
        get_logger().debug('----------reservation_time---%s',request.POST['reservation_time'])
        timeArray = time.strptime(request.POST['reservation_time'], "%Y-%m-%d %H:%M")
        for work in worktime:
            if work.type =='A':
                workstart = [int(i) for i in work.start_time.split(':')]
                workend = [int(i) for i in work.end_time.split(':')]
                if timeArray.tm_hour < workstart[0] or timeArray.tm_hour > workend[0]:
                    response_data['code'] = '0'
                    response_data['msg'] = '请选择正常工作时间，重新提交'
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                if timeArray.tm_hour == workstart[0] and timeArray.tm_min < workstart[1]:
                    response_data['code'] = '0'
                    response_data['msg'] = '请选择正常工作时间，重新提交'
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                if timeArray.tm_hour == workend[0] and timeArray.tm_min > workend[1]:
                    response_data['code'] = '0'
                    response_data['msg'] = '请选择正常工作时间，重新提交'
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
            if work.type =='B':
                startday = time.strptime(work.start_day, '%Y-%m-%d %H:%M:%S+%z')

        reservation = MeasureReservation()
        reservation.user_id = request.session['userid']
        reservation.sex = request.POST['sex']
        #reservation.height = request.POST['height']
        #reservation.weight = request.POST['weight']
        if int(request.session['order__is4friend']) ==1:
            reservation.phone = request.session['order__friend_phone']
        else:
            reservation.phone = userinfo.phonenumber
        reservation.reservation_time = request.POST['reservation_time']
        reservation.address_region = request.POST['address_region']
        reservation.address_street = request.POST['address_street']
        reservation.save()
        reservation.reservation_number = 'R-' + '%0*d' % (8, reservation.id)
        reservation.save()
        response_data['code'] = '0'
        response_data['msg'] = '预约成功，我们的客服会尽快跟您联系'
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 推广预约.
def reserve(request):
    return render_to_response('wap/reserve_guest.html', {'request':request})


@csrf_exempt
def reserve_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '提交失败'
    worktime = Worktime.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        reservation = MeasureReservation()
        reservation.name = request.POST['name']
        reservation.phone = request.POST['phone']
        reservation.reservation_time = request.POST['reservation_time']
        get_logger().debug('----------reservation_time---%s',request.POST['reservation_time'])
        get_logger().debug('----------address_region---%s',request.POST['address_region'])
        get_logger().debug('----------address_street---%s',request.POST['address_street'])
        reservation.address_region = request.POST['address_region']
        reservation.address_street = request.POST['address_street']
        reservation.sex = request.POST['sex']
        reservation.save()
        reservation.reservation_number = 'R-' + '%0*d' % (8, reservation.id)
        reservation.save()
        response_data['code'] = '0'
        response_data['msg'] = '预约成功，我们的客服会尽快跟您联系'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
        


#购物车功能
def cart_add(request):
    cart = Cart()
    cart.user_id = request.session['userid']
    cart.price = request.session['order__price']
    cart.product_id = int(request.session['order__product_id'])
    cart.is4friend = int(request.session['order__is4friend'])
    cart.friend_phone = request.session['order__friend_phone']
    cart.fabric_id = int(request.session['order__fabric'])
    get_logger().debug('----------order__fabric---%s',cart.product_id)
    #上衣参数
    cart.kouxing_sy = request.session.get('order__style__KouXingShangYi', '')
    cart.lingxing_sy = request.session.get('order__style__LingXingShangYi', '')
    cart.yaodou_sy = request.session.get('order__style__YaoDouShangYi', '')
    cart.kaiqi_sy = request.session.get('order__style__KaiQiShangYi', '')
    cart.xiukou_sy = request.session.get('order__style__XiuKouShangYi', '')
    cart.neibuzaoxing_sy = request.session.get('order__style__NeiBuZaoXingShangYi', '')
    cart.neibudou_sy = request.session.get('order__style__NeiBuDouShangYi', '')
    # 西裤参数
    cart.kuzhe_xk = request.session.get('order__style__KuZheXiKu', '')
    cart.houdou_xk = request.session.get('order__style__HouDouXiKu', '')
    cart.kujiao_xk = request.session.get('order__style__KuJiaoXiKu', '')
    #衬衫参数
    cart.lingxing_cs = request.session.get('order__style__LingXingChenShan', '')
    cart.xiukou_cs = request.session.get('order__style__XiuKouChenShan', '')
    cart.xiabai_cs = request.session.get('order__style__XiaBaiChenShan', '')
    cart.menjin_cs = request.session.get('order__style__MenJinChenShan', '')
    cart.houbei_cs = request.session.get('order__style__HouBeiChenShan', '')
    cart.koudai_cs = request.session.get('order__style__HouDaiChenShan', '')
    # 个性化
    cart.add_kuzi = int(request.session.get('order__personalization__add_kuzi', '0'))
    cart.add_majia = int(request.session.get('order__personalization__add_majia', '0'))
    cart.majia_lingxing = request.session.get('order__personalization__majia_lingxing', '')
    cart.majia_kouxing = request.session.get('order__personalization__majia_kouxing', '')
    cart.add_bespoke = int(request.session.get('order__personalization__add_bespoke', '0'))
    cart.add_xiuzi = int(request.session.get('order__personalization__add_xiuzi', '0'))
    cart.xiuzi = request.session.get('order__personalization__xiuzi', '')
    cart.save()
    return HttpResponseRedirect('/wap/cart_view')
    

def summit_cart(request):
    user_id = request.session['userid']
    cart_list = Cart.objects.filter(user_id=user_id)
    cartid = request.session['cartlist']
    addresid = request.session['order__address']
    get_logger().debug('----------cartid----------cart:%s'%user_id)
    for i in cartid:
        carts = cart_list[int(i)]
        carts.address_id = int(addresid)
        carts.save()

       

@check_user
def cart_view(request):
    user_id = request.session['userid']
    cart_list = Cart.objects.filter(user_id=user_id)
    redpacket_list = Redpacket.objects.filter(user_id=user_id,isUsed__in = ['0','2']) #isUsed ='0')
    show_redpacket = True if redpacket_list else False
    request.session["carts_number"] = str(len(cart_list))
    cart_price = 0
    carts = []
    for i in cart_list:
        try:
            carts.append({'id':i.id,'img':i.product.img,'title':i.product.title,'price':int(i.price)})
            cart_price = cart_price + int(i.price)
        except:
            cart_price = 0
    return render_to_response('wap/car.html', {
        'carts': carts,
        'cart_price': cart_price,
        'request': request,
        'show_redpacket': show_redpacket,
    })


def cart_clean(request):
    user_id = request.session['userid']
    cart_list = Cart.objects.filter(user_id=user_id).delete()
    return HttpResponseRedirect('/wap/cart_view')


@csrf_exempt
def cart_delete_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '提交失败'
    if request.method == 'POST':
        cart_id = request.POST['cart_id']
        cart_list = Cart.objects.filter(id=int(cart_id)).delete()
        response_data['code'] = '0'
        response_data['msg'] = '删除成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def cart_post(request):
    response_data = {}
    cartlist = request.POST['id']
    cartid = [str(i) for i in cartlist.split(',')]
    request.session['cartlist'] = cartid
    return HttpResponse(json.dumps(response_data), content_type="application/json")
@csrf_exempt
def cart_update_post(request):
    response_data = {}
    cartlist = request.POST['id']
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@check_user
def redpacket_view(request):
    user_id = request.session['userid']
    redpacket_list = Redpacket.objects.filter(user_id=user_id,isUsed__in = ['0','2'])#)
    cart_list = Cart.objects.filter(user_id=user_id)
    cartid = request.session['cartlist']
    order_price = 0
    redpacket_limit = 0
    for i in cartid:
        carts = cart_list[int(i)]
        order_price = order_price + carts.price
        if carts.product.type == u'suit':
            redpacket_limit += 400
        else:
            redpacket_limit += 200
    return render_to_response('wap/coupon/use_redpacket.html', {
        'redpacket_list': redpacket_list,
        'order_price': int(order_price),
        'redpacket_limit': redpacket_limit,
        'request': request
    })
@csrf_exempt
@check_user
def redpacket_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '提交失败'
    if request.method == 'POST':
        request.session['redpacket_id'] =  [int(i) for i in request.POST['redpacket_id'].split(',')]
        get_logger().debug('------------id%s:', request.POST['redpacket_id'][0])
        response_data['code'] = '0'
        response_data['msg'] = '提交成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    

# 地址列表 地址选择页面
@check_user
def address_list(request):
    address_list = []
    userid = request.session['userid']
    address_list = Address4Order.objects.filter(user_id=userid).order_by('-id')
    cart_list = Cart.objects.filter(user_id=userid)
    cartid = request.session['cartlist']
    order_price = 0
    for i in cartid:
        carts = cart_list[int(i)]
        order_price = order_price + carts.price
    redpacket_id = request.session['redpacket_id']
    for redpacketid in redpacket_id:
        redpackets= Redpacket.objects.get(id = int(redpacketid))
        order_price = order_price - redpackets.money
    #order_price= request.session['order__price']
    return render_to_response('wap/addressee.html', {'address_list': address_list,'order_price':int(order_price),'request':request})

# 选择某个地址 param: 选择地址后自动下单
# address_id
@csrf_exempt
def address_select_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '提交失败'
    if request.method == 'POST':
        try:
            request.session['order__address'] = request.POST['address_id']
            redpacket_id = request.session['redpacket_id']
            for redpacketid in redpacket_id:
                get_logger().debug('------------id1:%s',redpacketid)
                redpackets= Redpacket.objects.get(id = int(redpacketid))
                redpackets.isUsed = '2'
                redpackets.save()
                get_logger().debug('-------ssss-----id:%s',redpackets.isUsed)
            flush_session(request)
            summit_cart(request)
            response_data['code'] = '0'
            request.session['redpacket_id'] = []
            response_data['msg'] = '提交成功'
        except ObjectDoesNotExist:
            response_data['code'] = '-1'
            response_data['msg'] = '地址不存在'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

#添加地址 post： 参数
#    recipient 收件人
#    phone
#    address_region 省市两级：北京市 海淀区 
#    address_street 街道地址
@csrf_exempt
def address_add_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '添加失败'
    if request.method == 'POST':
        address = Address4Order()
        address.user_id = request.session['userid']
        address.recipient = request.POST['recipient']
        address.phone = request.POST['phone']
        address.address_region = request.POST['address_region']
        address.address_street = request.POST['address_street']
        address.save()
        response_data['code'] = '0'
        response_data['msg'] = '添加成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#删除地址 post： 参数
#    address_id
@csrf_exempt
def address_delete_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '删除失败'
    if request.method == 'POST':
        Address4Order.objects.filter(id=request.POST['address_id']).delete()
        response_data['code'] = '0'
        response_data['msg'] = '删除成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#修改地址 post： 参数
#    address_id
@csrf_exempt
def address_update_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '修改失败'
    if request.method == 'POST':
        address = get_object_or_404(Address4Order, id=request.POST['address_id'])
        address.user_id = request.session['userid']
        address.recipient = request.POST['recipient']
        address.phone = request.POST['phone']
        address.address_region = request.POST['address_region']
        address.address_street = request.POST['address_street']
        address.save()
        response_data['code'] = '0'
        response_data['msg'] = '修改成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 我的订单 订单列表
def order_list(request):
    order_list = []
    if 'userid' not in request.session.keys() :
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/order_list/')
    userid = request.session['userid']
    order_list = Order.objects.filter(user_id=userid).order_by('-id')
    return render_to_response('wap/18.html', {'order_list': order_list,'request':request})

# 订单详情
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    xiuzi_config = OrderPersonalization.objects.get(product_type = order.product.type,name='绣字')
    bespoke_config = OrderPersonalization.objects.get(name='Bespoke')
    params = {'order': order,
              'xiuzi_price':"{0:.0f}".format(xiuzi_config.price),
               'bespoke_price':"{0:.0f}".format(bespoke_config.price),}
    if order.product.type == 'suit':
        majia_config = OrderPersonalization.objects.get(name='单加马甲',product_name=order.product.title)
        kuzi_config = OrderPersonalization.objects.get(name='单加裤子',product_name=order.product.title)
        params['majia_price']="{0:.0f}".format(majia_config.price)
        params[ 'kuzi_price']="{0:.0f}".format(kuzi_config.price)                     
    return render_to_response('wap/19.html', params)


def buyorder_post(request):
    return HttpResponseRedirect('/wap/buy')


def buyorder_cancel_post(request):
    return HttpResponseRedirect('/wap/buy')


# 4我的尺寸.psd
def show_my_size(request):
    if 'userid' not in request.session.keys() :
        # return render_to_response('wap/1.html', {})
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/show_my_size/')
    
    try:
        userid = request.session['userid']
        userinfo = User.objects.get(id=userid)
        return render_to_response('wap/4.html', {'userinfo': userinfo,'request':request}) 
    except ObjectDoesNotExist:
        del request.session['userid']
        request.session.modified = True
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/show_my_size/')


# 5分享界面.psd
def share_my_size(request, userid, type):
    
    userinfo = get_object_or_404(User, id=userid)
    size_name = ''
    size_value = 0
    size_value_persent = 0
    if type == 'waist':
        size_name = '小蛮腰'
        size_value = userinfo.waist
        size_value_persent = userinfo.waist_percent
    elif type == 'leg':
        size_name = '大长腿'
        #size_value = userinfo.leg
        size_value_persent = userinfo.leg_percent
    elif type == 'chest':
        size_name = '胸大肌'
        size_value = userinfo.chest
        size_value_persent = userinfo.chest_percent
    
    # 获取微信名
    wxname = ''
    try:
        wxuser = WXUser.objects.get(openid=userinfo.openid)
        wxname = wxuser.nickname
    except:
        pass
    return render_to_response('wap/5.html', {'size_name': size_name, 'size_value':size_value, 'size_value_percent':size_value_persent, 'wxname':wxname,'request':request})

# 6个人信息.psd
def my_info(request):
    if 'userid' not in request.session.keys() :
        # return render_to_response('wap/1.html', {})
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/my_info/')
    
    try:
        userid = request.session['userid']
        userinfo = User.objects.get(id=userid)
        return render_to_response('wap/6.html', {'userinfo': userinfo,'request':request}) 
    except ObjectDoesNotExist:
        del request.session['userid']
        request.session.modified = True
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/my_info/')

# 7名字.psd
#@csrf_exempt
def my_name_change(request):
    if 'userid' not in request.session.keys() :
        # return render_to_response('wap/1.html', {})
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/my_name_change/')
    userid = request.session['userid']
    
    userinfo = get_object_or_404(User, id=userid)
    return render_to_response('wap/7.html', {'userinfo': userinfo,'request':request})

# 8.6更换手机号——更换成功.psd
# 8.5更换手机号——未收到验证码.psd
# 8.4更换手机号——输入验证码.psd
# 8.3更换手机号——确认验证码.psd
# 8.2更换手机号——输入新号码.psd
# 8.1更换手机号.psd
def my_phone_change(request):
    if 'userid' not in request.session.keys() :
        # return render_to_response('wap/1.html', {})
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/my_phone_change/')
    userid = request.session['userid']
    
    userinfo = get_object_or_404(User, id=userid)
    return render_to_response('wap/8.1.html', {'userinfo': userinfo,'request':request})


def login(request):
    openid = ''
    # wechat authorization
    if 'code' not in request.GET.keys() :
        if 'state' in request.GET.keys() :
            # not authorized by user
            pass
        else:
            # show user the authorization page
            login_url = 'http://' + request.get_host() + request.get_full_path()
            get_logger().debug('------------------------login_url= %s', login_url)
            login_url = quote_plus(login_url)
            redirect_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID + '&redirect_uri=' + login_url + '&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
            return HttpResponseRedirect(redirect_url)
    else :
        #    网页授权获取用户基本信息
        api = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (APPID, APP_SECRET, request.GET.get('code'))
        data = method_get_api(api)
        token = data.get('access_token')
        openid = data.get('openid')
        if openid and len(openid) > 0:
            request.session['openid'] = openid
            try:
                user = User.objects.get(openid=openid)
                request.session['userid'] = user.id
                if 'returnUrl' in request.GET.keys():
                    return HttpResponseRedirect(request.GET['returnUrl'])
            except ObjectDoesNotExist:
                pass
    return render_to_response('wap/1.html', {})


# 1.1登录.psd
@csrf_exempt
def login_post(request):
    response_data = {} 
    if request.method == 'POST':
        phone = request.POST['phone'];
        pwd = request.POST['password'];
        try:
            user = User.objects.get(phonenumber=phone)
            try:
                user = User.objects.get(phonenumber=phone, password=pwd)
                request.session['userid'] = user.id

                if 'openid' in request.session.keys():
                    user.openid = request.session['openid']
                    user.save()
            
                response_data['code'] = '0'
                response_data['msg'] = '登陆成功'
                user_id = request.session['userid']
                cart_list = Cart.objects.filter(user_id=user_id)
                request.session["carts_number"] = str(len(cart_list))
            except ObjectDoesNotExist:
                response_data['code'] = '-1'
                response_data['msg'] = '密码错误'
        except ObjectDoesNotExist:
                response_data['code'] = '-2'
                response_data['msg'] = '用户名不存在'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def logout_post(request):
    if 'userid' in request.session.keys():
        try:
            userid = request.session['userid'] 
            user = User.objects.get(id=userid)
            user.openid = ''
            user.save()
        except ObjectDoesNotExist:
            pass
        del request.session['userid']
        del request.session['openid']
        #del request.session['cart']
        request.session.modified = True
    
    response_data = {} 
    response_data['code'] = '0'
    response_data['msg'] = '退出成功'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# 优惠券页面，注册就送200西服、100衬衫
def send_coupon_on_register(new_user):
    shirt_coupon = Coupon(money=100, type='shirt', user=new_user)
    shirt_coupon.save()
    shirt_coupon.title = 'BB-' + '%0*d' % (8, shirt_coupon.id)
    shirt_coupon.save()
    suit_coupon = Coupon(money=200, type='suit', user=new_user)
    suit_coupon.save()
    suit_coupon.title = 'BB-' + '%0*d' % (8, suit_coupon.id)
    suit_coupon.save()


def summit_redpacket(user):
    redpacket_list = Redpacket.objects.filter(phonenumber = user.phonenumber,isUsed = '0')
    for redpackets in redpacket_list:
        redpackets.user_id = user.id
        redpackets.save()


@csrf_exempt
def register_post(request):
    response_data = {} 
    if request.method == 'POST':
        smscode = request.POST['verification'];
        # TODO remove False, this is for debug only
        if 'smscode' not in request.session.keys() or smscode != request.session['smscode'] :
            response_data['code'] = '-2'
            response_data['msg'] = '验证码错误'
        else:
            phone = request.POST['phone'];
            pwd = request.POST['password'];
            sex = request.POST['sex'];
            nickname = request.POST['name']
            
            try:
                user = User.objects.get(phonenumber=phone)
                if not user.password:
                    if 'openid' in request.session.keys():
                        user.openid = request.session['openid']
                    user.password = pwd
                    user.sex = sex
                    user.nickname = nickname
                    user.save()
                    response_data['code'] = '0'
                    response_data['msg'] = '注册成功'
                    summit_redpacket(user)
                else:
                    response_data['code'] = '-1'
                    response_data['msg'] = '该手机号已经被注册'
            except ObjectDoesNotExist:
                new_user = User(phonenumber=phone, password=pwd, sex=sex,nickname=nickname)
                if 'openid' in request.session.keys():
                    new_user.openid = request.session['openid']
                new_user.save()
                response_data['code'] = '0'
                response_data['msg'] = '注册成功'
                summit_redpacket(new_user)
                # 优惠券页面，注册就送200西服、100衬衫
                # send_coupon_on_register(new_user)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def forget_password_post(request):
    response_data = {} 
    smscode = request.POST['verification'];
    # TODO remove False, this is for debug only
    if 'smscode' not in request.session.keys() or smscode != request.session['smscode'] :
        response_data['code'] = '-2'
        response_data['msg'] = '验证码错误'
    else:
        # phone = request.POST['phone'];
        pwd = request.POST['password'];
        
        try:
            user = User.objects.get(phonenumber=request.POST['phone'])
            user.password = pwd
            user.save()
            
            response_data['code'] = '0'
            response_data['msg'] = '密码重置成功，请重新登陆'
        except ObjectDoesNotExist:
            response_data['code'] = '-1'
            response_data['msg'] = '用户id不存在'
                
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def change_phone_post(request):
    response_data = {} 
    
    if 'userid' not in request.session.keys() :
        response_data['code'] = '-1'
        response_data['msg'] = '未登录'
    else:
        userid = request.session['userid']
        
        smscode = request.POST['verification'];
        # TODO remove False, this is for debug only
        if 'smscode' not in request.session.keys() or smscode != request.session['smscode'] :
            response_data['code'] = '-2'
            response_data['msg'] = '验证码错误'
        else:
            # old_phone = request.POST['old_phone'];
            new_phone = request.POST['new_phone'];
            
            try:
                user = User.objects.get(phonenumber=new_phone)
                
                response_data['code'] = '-3'
                response_data['msg'] = '此手机号码已经注册'
            except:
                try:
                    user = User.objects.get(id=userid)
                    user.phonenumber = new_phone
                    user.save()
                    
                    response_data['code'] = '0'
                    response_data['msg'] = '修改成功'
                except ObjectDoesNotExist:
                    response_data['code'] = '-1'
                    response_data['msg'] = '用户id不存在'
                
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def change_name_post(request):
    response_data = {} 
    
    if 'userid' not in request.session.keys() :
        response_data['code'] = '-1'
        response_data['msg'] = '未登录'
    else:
        userid = request.session['userid']
        
        try:
            user = User.objects.get(id=userid)
            user.nickname = request.POST['name']
            user.save()
        
            response_data['code'] = '0'
            response_data['msg'] = '修改成功'
        except ObjectDoesNotExist:
            response_data['code'] = '-2'
            response_data['msg'] = '用户id不存在'
            
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def change_sex_post(request):
    response_data = {} 
    
    if 'userid' not in request.session.keys() :
        response_data['code'] = '-1'
        response_data['msg'] = '未登录'
    else:
        userid = request.session['userid']
        try:
            user = User.objects.get(id=userid)
            user.sex = request.POST['sex']
            user.save()
        
            response_data['code'] = '0'
            response_data['msg'] = '修改成功'
        except ObjectDoesNotExist:
            response_data['code'] = '-2'
            response_data['msg'] = '用户id不存在'

    return HttpResponse(json.dumps(response_data), content_type="application/json")
    

@csrf_exempt
def send_sms_post(request):
    response_data = {} 
    if request.method == 'POST':
        phone = request.POST['phone'];
        smscode = string.join(random.sample('0123456789', 4)).replace(" ", "")
        request.session['smscode'] = smscode;
        sms_status = send_sms_code(phone, smscode)
        get_logger().debug('------------------------sms_status= %s', sms_status)
        if sms_status == '2':
            response_data['code'] = '0'
            response_data['msg'] = '验证码发送成功'
        else:  
            response_data['code'] = '-1'
            response_data['msg'] = '验证码发送失败'
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    
# 2.1新用户注册.psd
# 3忘记密码.psd
# 15售后服务.psd
# 16优惠券
def coupon_list(request):
    if 'userid' not in request.session.keys() :
        # return render_to_response('wap/1.html', {})
        return HttpResponseRedirect('/wap/login?returnUrl=/wap/coupons/')
    userid = request.session['userid']
    coupons = []
    try:
        user = User.objects.get(id=userid)
        coupons = Coupon.objects.filter(user=user).order_by('isUsed')
        redpacket = Redpacket.objects.filter(user=user).order_by('isUsed')
    except:
        pass
    return render_to_response('wap/16.html', {'coupons': coupons,'redpacket': redpacket})

# 14关于我们.psd
# 13定制文化.psd
# 12立即预约.psd

# 11产品详情西服.psd
# 10.2产品浏览衬衫.psd
# 10.1产品浏览西服.psd
    
# TODO: 每次调用 会重新计算每个人胸围等尺寸的百分比,并写入数据库。
def calculate_size_percentage(request):
    count_man = User.objects.filter(sex='男').count()
    count_women = User.objects.filter(sex='女').count()
    # chest
    # 男
    users_with_rank = User.objects.raw('SELECT id,  @curRank := @curRank + 1 AS rank FROM (select * from wap_user where sex="男") u, (SELECT @curRank := 0) r ORDER BY chest')
    for item in users_with_rank:
        try:
            user = User.objects.get(id=item.id)
            user.chest_percent = 100 * item.rank / count_man
            user.save()
        except:
            continue
    # 女
    users_with_rank = User.objects.raw('SELECT id,  @curRank := @curRank + 1 AS rank FROM (select * from wap_user where sex="女") u, (SELECT @curRank := 0) r ORDER BY chest')
    for item in users_with_rank:
        try:
            user = User.objects.get(id=item.id)
            user.chest_percent = 100 * item.rank / count_women
            user.save()
        except:
            continue
    # leg
    # 男
    users_with_rank = User.objects.raw('SELECT id,  @curRank := @curRank + 1 AS rank FROM (select * from wap_user where sex="男") u, (SELECT @curRank := 0) r ORDER BY kuchang')
    for item in users_with_rank:
        try:
            user = User.objects.get(id=item.id)
            user.leg_percent = 100 * item.rank / count_man
            user.save();
        except:
            continue
    # 女
    users_with_rank = User.objects.raw('SELECT id,  @curRank := @curRank + 1 AS rank FROM (select * from wap_user where sex="女") u, (SELECT @curRank := 0) r ORDER BY kuchang')
    for item in users_with_rank:
        try:
            user = User.objects.get(id=item.id)
            user.leg_percent = 100 * item.rank / count_women
            user.save();
        except:
            continue
    # waist
    # 男
    users_with_rank = User.objects.raw('SELECT id,  @curRank := @curRank + 1 AS rank FROM (select * from wap_user where sex="男") u, (SELECT @curRank := 0) r ORDER BY waist DESC')
    for item in users_with_rank:
        try:
            user = User.objects.get(id=item.id)
            user.waist_percent = 100 * item.rank / count_man
            user.save()
        except:
            continue
    # 女
    users_with_rank = User.objects.raw('SELECT id,  @curRank := @curRank + 1 AS rank FROM (select * from wap_user where sex="女") u, (SELECT @curRank := 0) r ORDER BY waist DESC')
    for item in users_with_rank:
        try:
            user = User.objects.get(id=item.id)
            user.waist_percent = 100 * item.rank / count_women
            user.save()
        except:
            continue
    
# 用cron每天凌晨定时调用
def cron(request):
    calculate_size_percentage(request)
    return HttpResponse("cron called")

# coding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json
import string
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from web.models import *
from wap.models import *
import logging
import weixin.utils
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger

logging.basicConfig(level=logging.DEBUG)


def flush_session(request):
    request.session.save()
    request.session.modified = True


# 检查登录
def check_user(func):
    def wrapper(request, *args, **kv):
        userinfo = request.session.get('userid', None)
        path = request.get_full_path()
        if not userinfo:
            return HttpResponseRedirect('/web/test3?returnUrl=' + path)
        return func(request, *args, **kv)
    return wrapper


#检测是否量体
@check_user
@csrf_exempt
def check_size(request):
    response_data = {}
    user_id = request.session['userid']
    users = User.objects.get(id = user_id)
    response_data['code'] = '0'
    if users.measure_status:
        response_data['code'] = '1'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#检测手机号是否注册
def check_phone(request):
    response_data = {}
    phone = request.GET['phonenumber']
    try:
        user = User.objects.get(phonenumber=phone)
        response_data['code'] = '-1'
        response_data['msg'] = '该手机号已经被注册'
    except ObjectDoesNotExist:
        response_data['code'] = '0'
        response_data['msg'] = '正常'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 发送短信验证码
@csrf_exempt
def send_sms_code(phone, code):
    url = u'http://106.ihuyi.cn/webservice/sms.php?method=Submit&account=cf_bb8888&password=\
fubang309&mobile=' + phone + '&content=您的验证码是：【' + code + '】。请不要把验证码泄露给其他人。'
    get_logger().debug('------s------url:%s:',url)
    ret = weixin.utils.method_get_api_xml(url)
    return ret['SubmitResult']['code']


@csrf_exempt
def send_sms_post(request):
    response_data = {}
    if request.method == 'POST':
        phone = request.POST['phone']
        smscode = string.join(random.sample('0123456789', 4)).replace(" ", "")
        request.session['smscode'] = smscode

        sms_status = send_sms_code(phone, smscode)
        get_logger().debug('------s------sms%s:',sms_status)
        if sms_status == '2':
            response_data['code'] = '0'
            response_data['msg'] = '验证码发送成功'
        else:
            response_data['code'] = '-1'
            response_data['msg'] = '验证码发送失败'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 登录.psd
@csrf_exempt
def login_post(request):
    response_data = {}
    if request.method == 'POST':
        phone = request.POST['phone']
        pwd = request.POST['password']
        try:
            user = User.objects.get(phonenumber=phone, password=pwd)
            request.session['userid'] = user.id
            response_data['code'] = '0'
            response_data['msg'] = '登陆成功'
        except ObjectDoesNotExist:
            response_data['code'] = '-1'
            response_data['msg'] = '登陆失败'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#退出
@csrf_exempt
def logout_post(request):
    if 'userid' in request.session.keys():
        del request.session['userid']
        request.session.modified = True
    response_data = {}
    response_data['code'] = '0'
    response_data['msg'] = '退出成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 注册.psd
@csrf_exempt
def register_post(request):
    response_data = {}
    if request.method == 'POST':
        smscode = request.POST['verification']
        # TODO remove False, this is for debug only
        if 'smscode' not in request.session.keys() or smscode != request.session['smscode']:
            response_data['code'] = '-2'
            response_data['msg'] = '验证码错误'
        else:
            phone = request.POST['phonenumber']
            pwd = request.POST['password']
            sex = request.POST['sex']
            nickname = request.POST['name']
            try:
                user = User.objects.get(phonenumber=phone)
                response_data['code'] = '-1'
                response_data['msg'] = '该手机号已经被注册'
            except ObjectDoesNotExist:
                new_user = User(phonenumber=phone, password=pwd, sex=sex, nickname=nickname)
                new_user.save()
                request.session['userid'] = new_user.id
                response_data['code'] = '0'
                response_data['msg'] = '注册成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def forget_password_post(request):
    response_data = {}
    smscode = request.POST['verification']
    # TODO remove False, this is for debug only
    if 'smscode' not in request.session.keys() or smscode != request.session['smscode']:
        response_data['code'] = '-2'
        response_data['msg'] = '验证码错误'
    else:
        pwd = request.POST['password']
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
    if 'userid' not in request.session.keys():
        response_data['code'] = '-1'
        response_data['msg'] = '未登录'
    else:
        userid = request.session['userid']
        smscode = request.POST['verification']
        # TODO remove False, this is for debug only
        if 'smscode' not in request.session.keys() or smscode != request.session['smscode']:
            response_data['code'] = '-2'
            response_data['msg'] = '验证码错误'
        else:
            new_phone = request.POST['new_phone']
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
    if 'userid' not in request.session.keys():
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
    if 'userid' not in request.session.keys():
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


def menus(request):
    menu_list = Menu.objects.all()
    submenu_list = {}
    user_id = request.session.get('userid',None)
    if user_id:
        users = User.objects.get(id = user_id)
        submenu_list['users'] = users
    submenu_list['menu_list'] = menu_list
    i = 1
    for menu in menu_list:
        submenu1 = menu.submenu.all()
        submenu_list['submenu' + str(i)] = submenu1
        submenu_list['submenu' + str(i)] = [{'name':submenu.name,'id':submenu.id,
                                               'secondaryname':[info for info in submenu.secondarymenu.all()]} for submenu in submenu1 ]
        l = 1
        for submenu in submenu1:
            secondarymenus = submenu.secondarymenu.all()
            submenu_list['secondarymenu' + str(l)] = secondarymenus
            l = l + 1
        i = i +1
    try:
        user_id = request.session['userid']
        cart_list = Cart_web.objects.filter(user_id=user_id)
        if len(cart_list):
            submenu_list['carts_number'] = str(len(cart_list))
        get_logger().debug('------s------title:%s',str(len(cart_list)))
    except:
        pass
    get_logger().debug('------submenu_list------title:%s',submenu_list)
    return submenu_list

def test(request,product_id):
    products = Product_web.objects.get(id=product_id)
    request.session['order__product_title'] = products.title
    request.session['order__product_id'] = products.id
    request.session['order__product_type'] = products.type
    if products.type == 'accessorie':
        return HttpResponseRedirect('/web/test4')

    return render_to_response('web/goods.html', menus(request))


def test2(request):

    return render_to_response('web/index.html', menus(request))


def test3(request):
    return render_to_response('web/login.html', menus(request))


def test4(request):
    return render_to_response('web/styleSelection.html', menus(request))


@check_user
def test5(request):
    return render_to_response('web/shopcar.html', menus(request))


def test6(request):
    return render_to_response('web/forecast.html', menus(request))


def test7(request):
    return render_to_response('web/changephone.html', menus(request))


def test8(request):
    return render_to_response('web/Forgetpass.html', menus(request))


@check_user
def test9(request):
    return render_to_response('web/personal.html', menus(request))


def test0(request):
    return render_to_response('web/tailor.html', menus(request))
    
def test10(request):
    return render_to_response('web/Forgetpass-2.html', menus(request))


def test1(request):
    m = request.GET.get('m', None)
    if m == '5':
        return HttpResponseRedirect('/web/test7')
    if m == '6':
        return HttpResponseRedirect('/web/journal_list')
    if m == '1':
        return HttpResponseRedirect('/web/test6')
    if m:
       mlist = m.split(',')
       if len(mlist) == 3:
           menu = mlist[0]
           submenu = mlist[1]
           subtitle = mlist[2]
       elif len(mlist) == 2:
           menu = mlist[0]
           submenu = mlist[1]
           subtitle = None
       elif len(mlist):
           menu = mlist[0]
           submenu = None
           subtitle = None
       request.session['menu'] = menu
       request.session['submenu'] = submenu
       request.session['subtitle'] = subtitle
    else:
        #return HttpResponseRedirect('http://www.brosbespoke.com')
        pass
    return render_to_response('web/productList.html', menus(request))


#首页
@csrf_exempt
def home_post(request):
    response_data = {}
    poster = [{'title': info.id, 'href': info.img_href, 'img': info.img.url}
              for info in Poster.objects.all()]
    focus = [{'title': info.id, 'img': info.img.url, 'href': info.img_href}
             for info in Focus.objects.all()]
    response_data['poster'] = poster
    response_data['focus'] = focus
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def poster(request,poster_id):
    posters = Poster.objects.get(id = poster_id)
    if posters.sort == '网址':
        url = 'http://' + posters.img_href
    elif posters.sort == '产品':
        titles = posters.img_href
        products = Product_web.objects.get(title=titles)
        request.session['order__product_title'] = titles
        request.session['order__product_id'] = products.id
        request.session['order__product_type'] = products.type
        url = '/web/test/' + str(products.id)
    elif posters.sort == '产品列表':
        productlist = posters.img_href.split('|')
        if len(productlist) == 1:
            menu = productlist[0]
            menu_li = Menu.objects.get(name=menu)
            menu = menu_li.id
            submenu = None
            subtitle = None
        elif len(productlist) == 2:
            menu = productlist[0]
            submenu = productlist[1]
            submenu_li = Submenu.objects.get(name=submenu)
            submenu = submenu_li.id
            subtitle = None
        else:
            menu = productlist[0]
            submenu = productlist[1]
            subtitle = productlist[2]
            menu_li = Menu.objects.get(name=menu)
            menu = menu_li.id
            submenu_li = Submenu.objects.get(name=submenu)
            submenu = submenu_li.id
            subtitle_li = Secondarymenu.objects.get(name=subtitle)
            subtitle = subtitle_li.id
        request.session['menu'] = menu
        request.session['submenu'] = submenu
        request.session['subtitle'] = subtitle
        url = '/web/test1/'
    else:
        url = '/web/test2/'
    get_logger().debug('------sort------sort:%s',posters.sort)

    return HttpResponseRedirect(url)

def focus(request,focus_id):
    id = focus_id
    response_data = {'focus_id':id}
    focuss = Focus.objects.get(id = focus_id)
    if focuss.sort == '网址':
        url = 'http://' + focuss.img_href
    elif focuss.sort == '产品':
        titles = focuss.img_href
        products = Product_web.objects.get(title=titles)
        get_logger().debug('------titles------titles:%s',titles)
        request.session['order__product_title'] = titles
        request.session['order__product_id'] = products.id
        request.session['order__product_type'] = products.type
        url = '/web/test/' + str(products.id)
    elif focuss.sort == '产品列表':
        productlist = focuss.img_href.split('|')
        if len(productlist) == 1:
            menu = productlist[0]
            submenu = None
            subtitle = None
        elif len(productlist) == 2:
            menu = productlist[0]
            submenu = productlist[1]
            subtitle = None
        else:
            menu = productlist[0]
            submenu = productlist[1]
            subtitle = productlist[2]

        request.session['menu'] = menu
        request.session['submenu'] = submenu
        request.session['subtitle'] = subtitle
        url = '/web/test1/'
    else:
        url = '/web/test2/'
    get_logger().debug('------sort------sort:%s',focuss.sort)
    return HttpResponseRedirect(url)


#菜单点击
@csrf_exempt
def menu_post(request):
    response_data = {}
    if request.method == 'POST':
        get_logger().debug('------requestbody------body:%s',request.body)
        menu = request.POST.get('menu')
        submenu = request.POST.get('submenu', None)
        subtitle = request.POST.get('subtitle', None)
        get_logger().debug('------subtitle------subtitle:%s',subtitle)
        request.session['menu'] = menu
        request.session['submenu'] = submenu
        request.session['subtitle'] = subtitle
        response_data['code'] = 0
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#产品列表
@csrf_exempt
def productlist_post(request):
    response_data = {}
    if request.method == 'POST':
        get_logger().debug('------requestbody------body:%s',request.body)
        menu = request.session['menu']
        submenu = request.session['submenu']
        subtitle = request.session['subtitle']
        try:
            menu = int(menu)
        except:
            menu_li = Menu.objects.get(name=menu)
            menu = menu_li.id
            if submenu:
                submenu_li = Submenu.objects.get(name=submenu)
                submenu = submenu_li.id
            if subtitle:
                subtitle_li = Secondarymenu.objects.get(name=subtitle)
                subtitle = subtitle_li.id

        menus = Menu.objects.get(id=int(menu))
        response_data['menu'] = {'name': menus.name, 'mingzi': menus.mingzi}
        if submenu:
            if subtitle:
                submenus = Submenu.objects.get(id=int(submenu))
                response_data['submenu'] = submenus.name
                get_logger().debug('------submenu------submenu:%s',response_data['menu'] )
                product_web_list = submenus.product_web_set.filter(menu__id=menu, secondarymenu__id=subtitle)

            else:
                submenu = Submenu.objects.get(id=submenu)
                response_data['submenu'] = submenu.name
                product_web_list = submenu.product_web_set.filter(menu__id=menu)

        else:
            if int(menu) == 1:
                product_web_list = Product_web.objects.filter(latest_product = 1)
            else:
                get_logger().debug('------menu------title:%s',menu)
                product_web_list = Product_web.objects.filter(menu__id=menu)
        get_logger().debug('------menu------title:%s',menu)
        if int(menu) == 3:
            get_logger().debug('------menu4------title:%s',menu)
            product_list = [{'id':info.id, 'title': info.title, 'subtitle': info.subtitle, 'img': info.img.url, 'price': info.price
                            } for info in product_web_list]
        else:
            get_logger().debug('------1111111111111111------title:%s',menu)
            product_list = [{'id':info.id, 'title': info.title, 'subtitle': info.subtitle, 'img': info.img.url, 'price': info.fabric_web_default.price
                            } for info in product_web_list]
        response_data['product_list'] = product_list

        menu_list = Menu.objects.filter(id=menu)
        for menu in menu_list:
            submenu1 = menu.submenu.all()
            response_data['submenu_list'] = [[submenu.name]+[info.name for info in submenu.secondarymenu.all()] for submenu in submenu1 ]
        get_logger().debug('------response_data------title:%s',response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#选择产品
@csrf_exempt
def buy_post(request):
    response_data = {}
    product_id = request.POST['product_id']
    get_logger().debug('------------title:%s',product_id)
    products = Product_web.objects.get(id=product_id)
    get_logger().debug('------------title:%s',product_id)
    # request.session['order__product_'] = product_id
    request.session['order__product_id'] = product_id
    request.session['order__product_type'] = products.type
    response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#产品详情
@csrf_exempt
def detail_post(request):
    response_data = {}
    #request.session['order__product_title'] = '150'
    get_logger().debug('------------order__product_title:%s',request.session['order__product_id'])
    product_li = Product_web.objects.get(id=request.session['order__product_id'])
    products_img = [{'img': product_li.img.url, 'img_thumbnail': str(product_li.img_thumbnail.url)},
                        {'img': product_li.img2.url, 'img_thumbnail': str(product_li.img2_thumbnail.url)},
                        {'img': product_li.img3.url, 'img_thumbnail': str(product_li.img3_thumbnail.url)},
                        {'img': product_li.img4.url, 'img_thumbnail': str(product_li.img4_thumbnail.url)},
                        {'img': product_li.img5.url, 'img_thumbnail': str(product_li.img5_thumbnail.url)},
                        {'img': product_li.img6.url, 'img_thumbnail': str(product_li.img6_thumbnail.url)
                        }]
    if product_li.type == 'accessorie':
        products = {'title': product_li.title,'product_id': product_li.id,
                    'subtitle': product_li.subtitle,'introduction': product_li.introduction,
                    'size_description': product_li.size_description, 'price': product_li.price,
                    'craft_description': product_li.craft_description,'custom_description': product_li.custom_description
                   }
    else:
        fabrics = [{'fabric_id': info.id,'color':info.color, 'design':info.desigh, 'weight':info.weight,
                    'composition':info.composition, 'name': info.name, 'thumbnail_url': info.thumbnail_url.url,
                    'price':info.price,'bespoke_price':info.price + 800, 'image_url': info.image_url.url} for info in product_li.fabric_web.all()]
        get_logger().debug('------------fabrics:%s',fabrics)
        products = {'title': product_li.title,'product_id': product_li.id,
                     'default_fabrics': product_li.fabric_web_default.id,'subtitle': product_li.subtitle,
                    'introduction': product_li.introduction, 'size_description': product_li.size_description,
                    'craft_description': product_li.craft_description,'custom_description': product_li.custom_description
                    }
        request.session['order__default__fabrics'] = product_li.fabric_web_default.id
        response_data['fabrics'] = fabrics
    get_logger().debug('------------products:%s',products)
    response_data['products'] = products
    response_data['products_img'] = products_img
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#选择面料和为谁定制
@csrf_exempt
def fabric_post(request):
    response_data = {}
    response_data['code'] = -1
    if request.method == 'POST':
        # is4friend = request.POST.get('is4friend', '0')
        default_fabrics = request.session['order__default__fabrics']
        fabric_id = request.POST.get('fabric_id', default_fabrics)
        if fabric_id in '':
            fabric_id = default_fabrics
        add_bespoke = request.POST['add_bespoke']
        request.session['order__fabric'] = fabric_id
        fabric_webs = Fabric_web.objects.get(id = fabric_id )
        products = Product_web.objects.get(id=request.session['order__product_id'])
        request.session['order__price'] = fabric_webs.price
        order_price = request.session['order__price']
        get_logger().debug('------------fabric_id:%s',fabric_id)
        get_logger().debug('------------add_bespoke:%s',add_bespoke)
        if int(add_bespoke) == 1:
            order_price = order_price + 800
        request.session['order__price'] = order_price
        response_data['code'] = 0
        flush_session(request)
        cart = Cart_web()
        cart.user_id = request.session.get('userid', '')
        cart.price = order_price
        cart.product_id = products.id
        cart.is4friend = int(request.session.get('order__is4friend', '0'))
        cart.friend_phone = request.session.get('order__friend_phone', '')
        cart.fabric_id = fabric_id
        # 个性化
        cart.add_bespoke = int(add_bespoke)
        cart.save()
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#购物车数据
@csrf_exempt
@check_user
def cart_view_post(request):
    user_id = request.session['userid']
    cart_list = Cart_web.objects.filter(user_id=int(user_id))
    cart_price = 0
    carts = []
    for i in cart_list:
        try:
            carts.append({'id': i.id, 'img': i.product.img.url,'fabric_id':i.fabric.id,
                          'add_bespoke':i.add_bespoke, 'title': i.product.title, 'product_id': i.product.id, 'price': i.price
                          })
            cart_price = cart_price + int(i.price)
        except:
            cart_price = 0
    response_data = {'carts': carts, 'cart_price': cart_price}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#购物车更新
@csrf_exempt
@check_user
def cart_update_post(request):
    response_data = {}
    response_data['code'] = '-1'
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        fabric_id = request.POST.get('fabric_id', '')
        get_logger().debug('------------ti%s',request.body)
        add_bespoke = request.POST['add_bespoke']
        fabric_webs = Fabric_web.objects.get(id = int(fabric_id))
        request.session['order__price'] = fabric_webs.price
        order_price = request.session['order__price']
        if int(add_bespoke) == 1:
            order_price = order_price + 800
        carts = Cart_web.objects.get(id=int(cart_id))
        carts.price = order_price
        carts.fabric_id = fabric_id
        carts.add_bespoke = int(add_bespoke)
        carts.save()
        response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#购物车删除
@csrf_exempt
@check_user
def cart_delete_post(request):
    response_data = {}
    cart_id = request.POST.get('id')
    user_id = request.session['userid']
    cart_list = Cart_web.objects.get(id=int(cart_id)).delete()
    response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#预约量体提交
@csrf_exempt
def reserve_measure_post(request):
    response_data = {}
    response_data['code'] = -1
    if request.method == 'POST':
        get_logger().debug('------------title:%s',request.body)
        get_logger().debug('------------height:%s',request.POST['height'])
        userid = request.session['userid']
        userinfo = User.objects.get(id=userid)
        reservation = MeasureReservation()
        reservation.user_id = userid
        if request.POST['sex'] == '先生':
            reservation.sex = '男'
        elif  request.POST['sex'] == '女士':
            reservation.sex = '女'
        reservation.height = request.POST['height']
        reservation.weight = request.POST['weight']
        reservation.phone = userinfo.phonenumber
        reservation.reservation_time_period = request.POST['reservation_time']
        reservation.address_region = request.POST['address_region']
        reservation.address_street = request.POST['address_street']
        reservation.name = userinfo.name
        reservation.save()
        reservation.reservation_number = 'R-' + '%0*d' % (8, reservation.id)
        reservation.save()
        response_data['code'] = '0'
        response_data['msg'] = '预约成功，我们的客服会尽快跟您联系'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#订单列表
@csrf_exempt
def orderList_post(request):
    response_data = {}
    order_list = []
    if 'userid' not in request.session.keys():
        return HttpResponseRedirect('/web/login?returnUrl=/web/orderList_post/')
    userid = request.session['userid']
    order_list = Order.objects.filter(user_id=userid).order_by('-id')
    orderDict = []
    for info in order_list:
        product = info.product
        product = {'title': product.title, 'img': str(product.img), 'price': product.price}
        order_dict = {'product': product, 'order_number': info.order_number,
                      'order_status': info.order_status, 'create_time': str(info.create_time)
                      }
        orderDict.append(order_dict)
    response_data['orderDict'] = orderDict
    orderNum = len(order_list)
    response_data['orderNum'] = orderNum
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 订单详情
@csrf_exempt
def orderDetail_post(request, order_id):
    response_data = {}
    if 'userid' not in request.session.keys():
        return HttpResponseRedirect('/web/login?returnUrl=/web/orderDetail_post/')
    userid = request.session['userid']
    order_list = Order.objects.filter(user_id=userid).order_by('-id')
    id = int(order_id)
    orderinfo = order_list[id]
    if orderinfo.product.type == 'suit':
        product_design = {'kouxing_sy': orderinfo.kouxing_sy, 'lingxing_sy': orderinfo.lingxing_sy,
                          'yaodou_sy': orderinfo.yaodou_sy, 'kaiqi_sy': orderinfo.kaiqi_sy,
                          'xiukou_sy': orderinfo.xiukou_sy, 'neibuzaoxing_sy': orderinfo.neibuzaoxing_sy,
                          'neibudou_sy': orderinfo.neibudou_sy, 'kuzhe_xk': orderinfo.kuzhe_xk,
                          'houdou_xk': orderinfo.houdou_xk, 'kujiao_xk': orderinfo.kujiao_xk,
                          'add_kuzi': orderinfo.add_kuzi, 'add_majia': orderinfo.add_majia,
                          'add_xiuzi': orderinfo.add_xiuzi, 'add_bespoke': orderinfo.add_bespoke
                          }
    else:
        product_design = {'lingxing_cs': orderinfo.lingxing_cs, 'xiukou_cs': orderinfo.xiukou_cs,
                          'xiabai_cs': orderinfo.xiabai_cs, 'menjin_cs': orderinfo.menjin_cs,
                          'houbei_cs': orderinfo.houbei_cs, 'koudai_cs': orderinfo.koudai_cs,
                          'add_xiuzi': orderinfo.add_xiuzi
                          }
    response_data['product_design'] = product_design
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 我的尺寸
@csrf_exempt
@check_user
def show_my_size_post(request):
    userid = request.session['userid']
    userinfo = User.objects.get(id=userid)
    userinfo = {'chest': userinfo.chest, 'waist': userinfo.waist, 'shoulder': userinfo.shoulder,
                'hip': userinfo.hip, 'kuchang': userinfo.kuchang
                }
    return HttpResponse(json.dumps(userinfo), content_type="application/json")


# 个人信息-地址簿
@csrf_exempt
@check_user
def address_list_post(request):
    response_data = {}
    userid = request.session['userid']
    addressDict = []
    address_list = Address4Order.objects.filter(user_id=userid).order_by('-id')
    for info in address_list:
        address_dict = {'address_id':info.id,'default':info.default_address, 'recipient': info.recipient,'sex': info.sex, 'phone': info.phone,
                        'address_region': info.address_region, 'address_street': info.address_street
                        }
        addressDict.append(address_dict)
    response_data['addressDict'] = addressDict
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 个人信息修改查询
@csrf_exempt
@check_user
def my_info_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '修改失败'
    if request.method == 'POST':
        try:
            userid = request.session['userid']
            users = User.objects.get(id=userid)
            nickname = request.POST['nickname']
            if len(nickname)>1:
                users.nickname = request.POST['nickname']
                if request.POST['sex'] == '先生':
                    users.sex = '男'
                elif  request.POST['sex'] == '女士':
                    users.sex = '女'
                users.age = request.POST['age']
                users.job = request.POST['occupation']
                get_logger().debug('------------occupation:%s',request.POST['occupation'])
                #users.phonenumber = request.POST['phonenumber']
                users.save()
                response_data['code'] = '0'
                response_data['msg'] = '修改成功'
        except:
            response_data['code'] = '-1'
            response_data['msg'] = '修改失败'

    else:
        userid = request.session['userid']
        users = User.objects.get(id=userid)
        if users.sex == '男':
            sexs = '先生'
        elif  users.sex == '女':
            sexs = '女士'
        userinfo = {'nickname': users.nickname, 'sex': sexs, 'age':users.age,
                    'occupation': users.job, 'phonenumber': users.phonenumber
                    }
        get_logger().debug('------------userinfo:%s',userinfo)
        return HttpResponse(json.dumps(userinfo), content_type="application/json")
    get_logger().debug('------------response_data:%s',response_data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# 个人信息-新增地址
@csrf_exempt
@check_user
def address_add_post(request):
    response_data = {}
    user_id = request.session['userid']
    if Address4Order.objects.filter(user__id =user_id):
        response_data['code'] = '-3'
    else:
        response_data['code'] = '-2'
    response_data['msg'] = '添加失败'
    if request.method == 'POST':
        user_id = request.session['userid']
        address = Address4Order()
        address.user_id = request.session['userid']
        address.recipient = request.POST['recipient']
        address.phone = request.POST['phone']
        address.address_region = request.POST['address_region']
        address.address_street = request.POST['address_street']
        if request.POST['sex'] == '先生':
            address.sex = '男'
        elif  request.POST['sex'] == '女士':
            address.sex = '女'
        if len(Address4Order.objects.filter(user__id =user_id))>=1:
            address.default_address = 0
        else:
            address.default_address = 1
        address.save()
        response_data['code'] = '0'
        response_data['msg'] = '添加成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#删除地址
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


#默认地址
@csrf_exempt
def address_default_post(request):
    response_data = {}
    response_data['code'] = '-1'
    response_data['msg'] = '失败'
    if request.method == 'POST':
        try:
            defaultaddress =  Address4Order.objects.get(user__id=request.session['userid'],default_address= True)

            defaultaddress.default_address = 0
            get_logger().debug('------------defaultaddress:%s',defaultaddress)
            defaultaddress.save()
        except:
            get_logger().debug('------------defaultaddress:')
            pass
        address =  Address4Order.objects.get(id=request.POST['address_id'])
        address.default_address = 1
        address.save()
        response_data['code'] = '0'
        response_data['msg'] = '成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def kmail(content):
    response_data ={}
    subject, from_email, to = '意见反馈', 'aegeggwd@163.com', 'kanghy@brosbespoke.com'
    text_content = 'wsrhwrjwrehwrj'

    html_content = '用户手机号'+content
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    response_data['code'] = 0
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#意见反馈
@csrf_exempt
def feedback_post(request):
    response_data = {}
    response_data['msg'] = '失败'
    response_data['code'] = '-1'
    if request.method == 'POST':
        content = request.POST['feedback']
        kmail(content)
        response_data['code'] = '0'
        response_data['msg'] = '成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#弹出窗
@csrf_exempt
def footer_post(request):
    response_data = {}
    footer_list = [{'name': info.name+'|'+info.mz+'|'+info.content} for info in Footer.objects.all()]
    return HttpResponse(json.dumps(footer_list), content_type="application/json")


#修改地址
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
        if request.POST['sex'] == '先生':
            address.sex = '男'
        elif  request.POST['sex'] == '女士':
            address.sex = '女'
        address.save()
        response_data['code'] = '0'
        response_data['msg'] = '修改成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

#个人信息-修改密码
@csrf_exempt
def modify_password_post(request):
    if 'userid' not in request.session.keys():
        return HttpResponseRedirect('/wep/login?returnUrl=/wep/modify_password_post/')
    userid = request.session['userid']
    user = User.objects.get(id=userid)
    response_data = {}
    if request.method == 'POST':
        orignal_password = request.POST['orignal_password']
        if orignal_password != user.password:
            response_data['code'] = '-1'
            response_data['msg'] = '当前密码错误'
        else:
            new_password = request.POST['new_password']
            user.password = new_password
            user.save()
            response_data['code'] = '0'
            response_data['msg'] = '密码重置成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#款式选择
def style_post(request):
    response_data = {}
    if request.session['order__product_type'] == 'suit':
        KouXing = [{'name': info.name, 'image_url': info.image.url} for info in KouXingShangYi.objects.all()]
        LingXing = [{'name': info.name, 'image_url': info.image.url} for info in LingXingShangYi.objects.all()]
        YaoDou = [{'name': info.name, 'image_url': info.image.url} for info in YaoDouShangYi.objects.all()]
        KaiQi = [{'name': info.name, 'image_url': info.image.url} for info in KaiQiShangYi.objects.all()]
        XiuKou = [{'name': info.name, 'image_url': info.image.url} for info in XiuKouShangYi.objects.all()]
        NeiBuZaoXing = [{'name': info.name, 'image_url': info.image.url} for info in NeiBuZaoXingShangYi.objects.all()]
        NeiBuDou = [{'name': info.name, 'image_url': info.image.url} for info in NeiBuDouShangYi.objects.all()]
        KuZhe = [{'name': info.name, 'image_url': info.image.url} for info in KuZheXiKu.objects.all()]
        HouDou = [{'name': info.name, 'image_url': info.image.url} for info in HouDouXiKu.objects.all()]
        KuJiao = [{'name': info.name, 'image_url': info.image.url} for info in KuJiaoXiKu.objects.all()]
        response_data = {'KouXing': KouXing, 'LingXing': LingXing, 'YaoDou': YaoDou, 'KaiQi': KaiQi,
                         'XiuKou': XiuKou,'NeiBuZaoXing': NeiBuZaoXing, 'NeiBuDou': NeiBuDou, 'KuZhe': KuZhe,
                         'HouDou': HouDou, 'KuJiao': KuJiao
                         }
    if request.session['order__product_type'] == 'shirt':
        LingXing = [{'name': info.name, 'image_url': info.image.url} for info in LingXingChenShan.objects.all()]
        Xiukou = [{'name': info.name, 'image_url': info.image.url} for info in XiuKouChenShan.objects.all()]
        Xiabai = [{'name': info.name, 'image_url': info.image.url} for info in XiaBaiChenShan.objects.all()]
        Menjin = [{'name': info.name, 'image_url': info.image.url} for info in MenJinChenShan.objects.all()]
        Houbei = [{'name': info.name, 'image_url': info.image.url} for info in HouBeiChenShan.objects.all()]
        Koudai = [{'name': info.name, 'image_url': info.image.url} for info in KouDaiChenShan.objects.all()]
        response_data = {'LingXing': LingXing, 'XiuKou': Xiukou, 'Xiabai': Xiabai, 'Menjin': Menjin,
                         'Houbei': Houbei, 'Koudai': Koudai
                         }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#款式选择提交
@csrf_exempt
def style_select_post(request):
    response_data = {}
    response_data['code'] = '-1'
    if request.method == 'POST':
        keys = request.POST.keys()
        for key in keys:
            if key.endswith('ShangYi') or key.endswith('XiKu') or key.endswith('ChenShan'):
                request.session['order__style__' + key] = request.POST[key]
        response_data['code'] = '0'
    product_title = request.session.get('order__product_title', '')
    product_list = Product.objects.get(title=product_title)
    cart = Cart()
    cart.user_id = request.session.get('userid', '')
    cart.price = product_list.price
    cart.product_id = product_list.id
    cart.is4friend = int(request.session.get('order__is4friend', '0'))
    cart.friend_phone = request.session.get('order__friend_phone', '')
    cart.fabric_id = int(request.session.get('order__fabric', ''))
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
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def journal_list(request):
    journal_list = Journal.objects.all()
    return_data = menus(request)
    return_data['journal_list'] =  journal_list
    return render_to_response('web/tailor.html', return_data)

def journal(request, journal_id):
    journal_list = Journal.objects.get(id = journal_id)
    return_data = menus(request)
    return_data['journal_s'] =  journal_list
    return render_to_response('web/journ.html', return_data)
# coding:utf-8
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse 
from wap.models import *
from django.core.mail import EmailMultiAlternatives  
from django.core.mail import send_mail as core_send_mail
from django.utils import timezone
from django.core import serializers
from django.template import Context, loader
from SizeConverter.SizeConverter import *
from cyexl import xizhuang,chenshan
import json
import logging
import time
import datetime
import threading

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger


logging.basicConfig(level=logging.DEBUG)


def login_view(request):    
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None :
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        login(request, user)    
        print request.user    
        return HttpResponseRedirect('/order/order_manage')
    else:
        #验证失败，暂时不做处理
        return HttpResponseRedirect('/order/order_login')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/order/order_login')

def order_login(request):
    t = get_template('order/order_login.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))
    
def order_denie(request):
    t = get_template('order/order_denie.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

def not_in_orders_group(user):
    if user:
        return user.groups.filter(name='orders').count() == 1
    return False

def not_in_Factory_group(user):
    if user:
        return user.groups.filter(name='Factory').count() == 1
    return False
def not_in_addorder_group(user):
    if user:
        return user.groups.filter(name='addorder').count() == 1
    return False

@login_required
#@user_passes_test(not_in_addorder_group, login_url='/admin/')
def order_manage(request,tab):
    mailtext = '已发送'
    c = RequestContext(request,locals())
    mailurl = '#'
    if tab == 'order':
        if request.user.groups.filter(name='addorder').count() ==1:
            nav = '订单审核'
            plant_update_issue = Plant_update.objects.filter(plant_status='退回订单',order__gh=request.user)
            plant_update_list = Plant_update.objects.filter(plant_status='订单审查',order__gh=request.user)
            mailtext = '提交复审'
            mailurl = '/order/order_update_post'
            return render_to_response('order/order_add.html', {'a': plant_update_issue,'b':plant_update_list,
                                                                    'user':c,'nav':nav,'mailtext':mailtext,
                                                                    'mailurl':mailurl})
    if tab == 'wxd':
        nav = '复审订单'
        if request.user.groups.filter(name='orders').count() ==1:
            plant_update_list = Plant_update.objects.filter(plant_status='复审中')
            order_list = Order.objects.filter(order_status='复审中')
            mailtext = '发送邮件'
            mailurl = '/order/kmail'
            return render_to_response('order/order_manage.html', {'a': plant_update_list,'user':c,'nav':nav,'mailtext':mailtext,'mailurl':mailurl})
        return HttpResponseRedirect('/admin/')
    elif tab == 'dzing':
        nav = '定制中订单'
        order_list = Order.objects.filter(order_status='定制中')
    elif tab == 'dzwc':
        nav = '制作完成订单'
        order_list = Order.objects.filter(order_status='定制完成')
    elif tab == 'psing':
        nav = '配送中订单'
        order_list = Order.objects.filter(order_status='配送中')
    elif tab == 'ywc':
        nav = '已完成订单'
        order_list = Order.objects.filter(order_status='已收货')
    return render_to_response('order/orderok.html', {'a': order_list,'user':c,'nav':nav,'mailtext':mailtext,'mailurl':mailurl})


@csrf_exempt
def manage_post(request):
    response_data = {}
    response_data['code'] = -1 
    if request.method == 'POST':
        orderlist = request.POST.get('id')
        orderlist_number = [str(i) for i in orderlist.split(',')]
        for ordernumber in orderlist_number: 
            plant_update = get_object_or_404(Plant_update, order__order_number=ordernumber)
            if plant_update.plant_status == '订单审查' or plant_update.plant_status == '退回订单' :
                plant_update.plant_status = '复审中'
                plant_update.save()
                
            else:
            #if plant_update.plant_status == '复审中':
                issue = request.POST.get('issue')
                plant_update.plant_status = '退回订单'
                plant_update.issue = issue
                plant_update.save()
                return HttpResponseRedirect('/order/order_manage/wxd/')
    return HttpResponseRedirect('/order/order_manage/order/')

    

@csrf_exempt
@user_passes_test(not_in_orders_group, login_url='/order/order_denie')
def kmail(request):
    #send_mail(u'123', u'456789','aegeggwd@163.com',['kanghy@brosbespoke.com'], fail_silently=False)
    #order = Order.objects.get(order_number= orderid)
    orderlist = request.POST.get('id')
    orderlist_number = [str(i) for i in orderlist.split(',')]
    get_logger().debug('---------------------%s'% orderlist_number)
    response_data ={}
    subject, from_email, to = '订单号'+orderlist +'下单表', 'aegeggwd@163.com', 'muskliu@brosbespoke.com' 
    #subject, from_email, to = '订单号'+orderlist +'下单表', 'aegeggwd@163.com', 'kanghy@brosbespoke.com' 
    text_content = '下单表'  
    html_content = '<p>This is an <strong>important</strong> message.</p>'  
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])  
    msg.attach_alternative(html_content, "text/html") 
    for ordernumber in orderlist_number: 
        oederlist = get_object_or_404(Order, order_number=ordernumber)
        fir_name = unicode(oederlist.id) + unicode(oederlist.user.nickname) + '-' + unicode(oederlist.user.phonenumber) + '.xls'
        try:        
            msg.attach_file('/home/Download/'+ fir_name)
        except:
            exl_download(request,ordernumber)
            msg.attach_file('/home/Download/'+ fir_name)
            
        order = Order.objects.get(order_number= ordernumber)
        order.order_status = '定制中'
        order.save()
        plant_update = Plant_update.objects.get(order__order_number= ordernumber)
        plant_update.plant_status = '等待制作'
        plant_update.save()
        pack = Pack.objects.all()
        for packs in pack:
            packs.volume = packs.volume -1
            packs.save()
        try:
            fabric = Fabric.objects.get(id= order.fabric_id)
            if order.product.type == 'suit':
                fabric.volume = fabric.volume - 3.5
            if order.product.type == 'shirt':
                fabric.volume = fabric.volume - 1.7
            fabric.save()
            
        except:
            pass

    msg.send() 
    response_data['code'] = 0
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    #return render_to_response('order/mailok.html', {'mailok': mailok,'orderid':orderid})


@login_required
#@user_passes_test(not_in_orders_group, login_url='/order/order_denie')
def exl_download(request,orderid):
    oederlist = get_object_or_404(Order, order_number=orderid)
    user_id = oederlist.user_id
    userid = oederlist.user_id
    if oederlist.is4friend:
        userlist = get_object_or_404(User, phonenumber=oederlist.friend_phone)
        user_id = userlist.id
    userinfo = get_object_or_404(User, id=user_id)
    users = get_object_or_404(User, id=userid)
    sleeve_lefet = userinfo.sleeve_lefet
    stomach = userinfo.stomach
    favor = userinfo.favor
    istie = userinfo.istie
    iswatch = userinfo.iswatch
    suit_shangyi = userinfo.suit_shangyi
    majia_qianchang = userinfo.majia_qianchang
    majia_houchang = userinfo.majia_houchang

    if not sleeve_lefet or sleeve_lefet == '0':
        sleeve_lefet = userinfo.sleeve_right
    if not majia_qianchang or majia_qianchang == '0':
        majia_qianchang = 0
    if not majia_houchang or majia_houchang == '0':
        majia_houchang = 0
    if not stomach:
        stomach = 0
    if not favor:
        favor = 1
    if not istie:
        istie = 0
    if not iswatch:
        iswatch = 2
    if not suit_shangyi:
        suit_shangyi = 1
    #get_logger().debug('-------stomach-------%s'%stomach)
    sizeList=[
                    float(userinfo.lingwei),#领围
                    float(userinfo.chest),#胸围
                    float(userinfo.waist),#腰围
                    float(userinfo.shoulder),#肩宽
                    float(userinfo.sleeve_right),#袖长(右)
                    float(sleeve_lefet),#袖长(左)
                    float(userinfo.back_cloth),#后衣长
                    float(userinfo.hip),#臀围
                    float(userinfo.kuyao),#裤腰围
                    float(userinfo.kuchang),#裤长
                    float(userinfo.hengdang),#横档
                    float(userinfo.xiwei),#膝围
                    float(userinfo.kukou),#裤口
                    float(majia_houchang),#后长
                    float(userinfo.xiulong),#袖笼
                    float(userinfo.chougenfen),#袖根肥
                    float(userinfo.xiukou_right),#袖口,暂时用的右袖口
                    float(stomach),#肚围
                    float(majia_qianchang),#马甲前长
                    float(userinfo.height),#身高
                    float(userinfo.weight),#体重
                   ]
    userChoice={
                    'm':int(favor),#m取值  0-修身 1-合身 2-宽松
                    'i':int(istie),#i取值 0-打领带 1-不打领带
                    'j':int(iswatch),#j取值 0-手表左 1-手表右 2-无手表
                    'q':int(suit_shangyi),#q取值0-长款 1-短款
                }  
    get_logger().debug('-------sizeList-%s',sizeList)
    get_logger().debug('-------userChoice-%s',userChoice)
    d1 = datetime.date.today()
    timdata = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    d2 = d1 + datetime.timedelta(10)
    if oederlist.add_xiuzi and oederlist.product.type == 'shirt':
        d2 = d1 + datetime.timedelta(12)
    get_logger().debug('-------sizes-'+ str(d2))
    order_xx ={'user':users.name,'phone':users.phonenumber,'tmime':timdata,'d2':str(d2)} 
    bzcc ={}
    #get_logger().debug('-------sizes-------%s'%order_xx)
    
    xzks ={}
    cycc = SizeConverter(sizeList,userChoice).convert()
    get_logger().debug('-------sizes-:%s', cycc)
    if oederlist.product.type == 'suit':
        bcc = xizhuang(userinfo,users,cycc,oederlist,order_xx)
    else:
        bcc = chenshan(userinfo,users,cycc,oederlist,order_xx)

    def file_iterator(file_name, chunk_size=512):
        with open('/home/Download/'+file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = str(oederlist.id) + str(users.nickname) +'-'+ str(users.phonenumber) +".xls"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response



@login_required
@user_passes_test(not_in_Factory_group, login_url='/admin/')
def plant_statu(request,tab):

    naotext = '已发送'
    naourl = '#'
    if tab == 'ddzz':
        nao = '等待制作订单'
        naotext = '提交制作'
        naourl = '/order/order_update_post'
        plant_update = Plant_update.objects.filter(plant_status ='等待制作')
        
    elif tab == 'zzing':
        nao = '制作中订单'
        naotext = '提交完成'
        naourl = '/order/order_update_post'
        plant_update = Plant_update.objects.filter(plant_status ='制作中')
        
    elif tab == 'zzwc':
        nao = '定制中订单'
        naotext = '提交发货'
        naourl = '/order/order_update_post'
        plant_update = Plant_update.objects.filter(plant_status ='制作完成')
       
    elif tab == 'psing':
        nao = '送货中订单'
        naotext = '提交完成'
        naourl = '/order/order_update_post'
        plant_update = Plant_update.objects.filter(plant_status ='配送中')
       
    elif tab == 'yjf':
        nao = '已收货订单'
        naotext = '已收货订单'
        try:
            numberid = request.GET['state']
            orderid = request.GET['id']
            order = Order.objects.get(id= orderid)
            plant = Plant_update.objects.get(order_id= order.id)
            order.huifang = numberid
            order.save()
            plant.plant_status = '订单完成'
            #plant.jiaofu_time = time
            plant.save()

        except:
            pass

        plant_update = Plant_update.objects.filter(plant_status ='已收货')
        c = RequestContext(request,locals())
        return render_to_response('order/plant_statu_is.html', {'user':c,'naotext':naotext,'nao':nao,'naourl':naourl,'a':plant_update})
    elif tab == 'ddwc':
        nao = '订单已完成'
        naotext = '订单已完成'
        plant_update = Plant_update.objects.filter(plant_status ='订单完成')
    c = RequestContext(request,locals())
    return render_to_response('order/plant_statu.html', {'user':c,'naotext':naotext,'nao':nao,'naourl':naourl,'a':plant_update})


@csrf_exempt
def order_update_post(request,orderid):
    order = Order.objects.get(order_number= orderid)
    plant = Plant_update.objects.get(order_id= order.id)
    time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    plant_statu = plant.plant_status
    order_statu = order.order_status
    if plant_statu == '等待制作':
        order.order_status = '定制中'
        order.save()
        plant.plant_status = '制作中'
        plant.zhizuo_time = time
        plant.save()
        return HttpResponseRedirect('/order/plant_statu/ddzz/')

    elif plant_statu == '制作中':
        order.order_status = '定制完成'
        order.save()
        plant.plant_status = '制作完成'
        plant.wancheng_time = time
        plant.save()
        return HttpResponseRedirect('/order/plant_statu/zzing/')

    elif plant_statu == '制作完成':
        order.order_status = '配送中'
        order.save()
        plant.plant_status = '配送中'
        plant.peishong_time = time
        plant.save()
        return HttpResponseRedirect('/order/plant_statu/zzwc/')

    elif plant_statu == '配送中':
        order.order_status = '已收货'
        order.save()
        plant.plant_status = '已收货'
        plant.jiaofu_time = time
        plant.save()
        return HttpResponseRedirect('/order/plant_statu/psing/')
    return HttpResponseRedirect('/order/plant_statu/zzwc')


def order_post(request):
    response_data ={}
    nam =[]
    fabricid = []
    addressnam = []
    addressid = []
    product = request.POST.get('product')
    if not product:
        product = 1
    user = request.POST.get('user')
    response_list = Fabric.objects.filter(product=product)
    address_list = Address4Order.objects.filter(user=user)
    username = User.objects.get(id=user)
    for i in response_list:
        nam.append(i.name)
        fabricid.append(str(i.id))
    for i in address_list:
        addressnam.append(str(i))
        addressid.append(str(i.id))
    response_data = {'fabricid':fabricid,'nam':nam,'addressnam':addressnam,'addressid':addressid,'username':str(username)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_user_name(request):
    response_data ={}
    user_id = request.GET['user_id']
    username = User.objects.get(id=user_id)
    response_data={'user_name':str(username)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_address_name(request):
    response_data ={}
    address_id = request.POST['user']
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_product_name(request):
    response_data ={}
    product_name = request.POST['product']
    try:
        products = Product.objects.get(id = product_name)
        response_data['type'] = products.type
    except:
        response_data['type'] = 'suit'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

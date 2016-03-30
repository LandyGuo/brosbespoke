# coding:utf8
import string
import json
import sys
from wap.models import *
from urllib import quote_plus
from django.views.decorators.csrf import csrf_exempt
from weixin.utils import method_get_api, get_token, get_ticket
from weixin.models import WXUser
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from ShiXiongDeYiGui.settings import APPID, APP_SECRET
from django.core.exceptions import ObjectDoesNotExist
import logging
import random
from sign import Sign
import datetime

def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger

logging.basicConfig(level=logging.DEBUG)


#保存session
def flush_session(request):
    request.session.save()
    request.session.modified = True


#首页获取微信信息
def redpacket_home(request):
    openid = ''
    hide = True
    if not request.session.get('openid', None) or not request.session.get('nickname', None):
        #用户确认授权
        if 'code' not in request.GET.keys():
            if 'state' in request.GET.keys():
                pass
            else:
                login_url = 'http://' + request.get_host() + request.get_full_path()
                login_url = quote_plus(login_url)
                redirect_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID \
                    + '&redirect_uri=' + login_url + '&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
                return HttpResponseRedirect(redirect_url)
        else:
            # 获取用户基本信息
            api = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' \
                % (APPID, APP_SECRET, request.GET.get('code'))
            data = method_get_api(api)
            token = data.get('access_token')
            openid = data.get('openid')
            api2 = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (token, openid)
            data2 = method_get_api(api2)
            nickname = data2.get('nickname') 
            headimgurl = data2.get('headimgurl')
            if openid and len(openid) > 0:
                request.session['openid'] = openid
                request.session['nickname'] = nickname
                request.session['headimgurl'] = headimgurl
    openid = request.session.get('openid', None)
    nickname = request.session.get('nickname', None)
    headimgurl = request.session.get('headimgurl', None)
    ticket = get_ticket()
    sign = Sign(ticket, str(request.build_absolute_uri()))
    config = sign.sign()
    if request.session.get('hbphone', None):
        all_coupons = Redpacket.objects.filter(openid=request.session['openid'], type='A')
        if len(all_coupons) >= 2:
            redpacket_money ='红包领取已满'
            info = '快去使用'
            hbphone = request.session.get('hbphone', None)
            url = "weixin://profile/gh_8a9626f68eca"
            return render_to_response('wap/coupon/coupon_index.html', {'url':url,'config':config,'hbphone':hbphone,'info':info,'text':hide,'hide_full':hide,'send':hide,'redpacket_money':redpacket_money})
    return render_to_response('wap/coupon/index_input.html', {'config':config,'hide_money':hide,'hide_cloud':hide,'send':hide,'hide_full':hide})


def redpacket_info(request):
    openid = ''
    hide = True
    if not request.session.get('openid', None) or not request.session.get('nickname', None):
        return HttpResponseRedirect('/promote/redpacket/')
    ticket = get_ticket()
    sign = Sign(ticket, str(request.build_absolute_uri()))
    config = sign.sign()
    redpacket_money = request.session['redpacket_money']
    hbphone = request.session['hbphone']
    info = '抢到了！手气不错！'
    url = "#"
    return render_to_response('wap/coupon/coupon_index.html', {'url':url,'config':config,'hbphone':hbphone,'info':info,'redpacket_money':str(redpacket_money) + '元','hide_money':hide,'hide_cloud':hide,'send':hide,'hide_full':hide})


#提交手机号，生成红包
@csrf_exempt
def hbphone_post(request):
    response_data = {}
    if request.method == 'POST':
        all_coupons = Redpacket.objects.filter(openid=request.session['openid'], type='A')
        if len(all_coupons) >= 2:
            response_data['code'] = '2'
        else:
            hbphone = request.POST['hbphone']
            money = random.randint(50, 100)
            redpacket = Redpacket()
            redpacket.openid = request.session.get('openid', None)
            nickname = request.session.get('nickname', None)
            redpacket.nickname = nickname
            redpacket.headimgurl = request.session.get('headimgurl', '')
            redpacket.money = money
            redpacket.phonenumber = hbphone
            d1 = datetime.datetime.now() +datetime.timedelta(days=60)
            redpacket.end_day = d1.strftime("%Y-%m-%d")
            request.session['hbphone'] = hbphone
            try:
                users = User.objects.get(phonenumber = hbphone)
                redpacket.user_id = users.id
            except:
                pass
            redpacket.type = 'A'
            try:
                redpacket.save()
            except:
                redpacket.nickname = ''
                redpacket.save()
            response_data['code'] = '0'
        request.session['redpacket_money'] = redpacket.money
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#抢红包排行
@csrf_exempt
def redpackettop(request):
    response_data = {}
    response_data['code'] = '-1'
    if request.method == 'GET':
        redpacket_top = [{'nickname':info.nickname,'headimgurl':info.headimgurl,'money':info.money, 
                          'create_timemonth':info.create_time.month,'create_timeday':info.create_time.day} 
                          for info in Redpacket.objects.order_by('-money').filter(type='A')[0:20]]
        redpacket = Redpacket.objects.filter(type='A').latest('id')
        response_data = {'redpacket_top':redpacket_top,'redpacket':[{'nickname':redpacket.nickname,
                         'headimgurl':redpacket.headimgurl,'money':redpacket.money,
                         'create_timemonth':redpacket.create_time.month,'create_timeday':redpacket.create_time.day}]
                         }
        response_data['code'] = '0'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#转发成功页面
@csrf_exempt
def forward_post(request):
    response_data = {}
    response_data['code'] = '-1'
    if request.method == 'GET':
        all_coupons = Redpacket.objects.filter(openid=request.session['openid'], type='B')
        if len(all_coupons) < 5:
            money = random.randint(50, 100)
            redpacket = Redpacket()
            hbphone = request.session.get('hbphone', None)
            redpacket.openid = request.session.get('openid', '')
            redpacket.nickname = request.session.get('nickname', '')
            d1 = datetime.datetime.now() +datetime.timedelta(days=60)
            redpacket.end_day = d1.strftime("%Y-%m-%d")
            redpacket.headimgurl = request.session.get('headimgurl', '')
            if hbphone:
                try:
                    users = User.objects.get(phonenumber = hbphone)
                    redpacket.user_id = users.id
                except:
                    pass
            redpacket.money = money
            #hbphone = request.POST['hbphone']
            redpacket.phonenumber = hbphone
            redpacket.type = 'B'
            try:
                redpacket.save()
            except:
                redpacket.nickname = ''
                redpacket.save()
            response_data['code'] = '0'
            response_data['money'] = redpacket.money
            response_data['phone'] = hbphone
        else:
            response_data['code'] = '1'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#红包列表
def all_redpacket(request):
    all_coupons = Redpacket.objects.filter(openid = request.session.get('openid',''))
    #all_coupons = Redpacket.objects.all()
    return render_to_response('wap/person_coupon.html', {'all_coupons': all_coupons})

#coding:utf8

from django.db import models

import time
import datetime
import urllib2
import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.core.cache import cache
from utils import upload_file_handler, method_get_api, method_post_api
from ShiXiongDeYiGui.settings import TIME_ZONE, TOKEN_CACHE_PRE, TOKEN


class WXUser(models.Model):
   # subscribe = models.IntegerField(max_length=2, verbose_name="是否关注", blank=True, null=True, choices=SUBSCRIBE_STATUS_CHOICES)
    openid = models.CharField(max_length=128, blank=True, null=True, verbose_name='用户标识')
    nickname = models.CharField(max_length=128, blank=True, null=True, verbose_name='昵称')
    sex = models.IntegerField(max_length=2, verbose_name="性别", blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True, verbose_name='城市')
    province = models.CharField(max_length=128, blank=True, null=True, verbose_name='省份')
    country = models.CharField(max_length=128, blank=True, null=True, verbose_name='国家')
    language = models.CharField(max_length=128, blank=True, null=True, verbose_name='用户语言')
    headimgurl = models.CharField(max_length=500, blank=True, null=True, verbose_name='头像')
   # subscribe_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户关注的时间')

    def __unicode__(self):
        return self.nickname
    class Meta:
        verbose_name = '关注微信用户'
        verbose_name_plural = '关注微信用户'

class WXConfig(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    slug = models.CharField(max_length=128, blank=True, null=True, verbose_name='app名称,唯一' )
    domain = models.CharField(max_length=128, blank=True, null=True, verbose_name='全域名(不包含http://)')
    appid = models.CharField(max_length=128, blank=True, null=True, verbose_name='APPID')
    app_secret = models.CharField(max_length=128, blank=True, null=True, verbose_name='APP_SECRET')
    token_cache_key = models.CharField(max_length=128, default='shixiongdeyigui_access_token', blank=True, null=True, verbose_name='缓存token的key')
#    app_groups = models.ManyToManyField('AppGroup', blank=True, null=True, verbose_name='app内的组') 
#    app_users = models.ManyToManyField('WXUser', blank=True, null=True, verbose_name='app内用户') 
#    menu_buttons = models.ManyToManyField('MenuButton', blank=True, null=True, verbose_name='app内的button') 
#    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name='app内的处理事件') 
#    qrcodes = models.ManyToManyField('QRCode', blank=True, null=True, verbose_name='app内的二维码') 
#    categories = models.ManyToManyField('Category', blank=True, null=True, verbose_name='分类') 
#    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='元素材') 
#    news = models.ManyToManyField('News', blank=True, null=True, verbose_name='图文素材') 
    is_valid = models.BooleanField(default=False, verbose_name="是否验证")
    def __unicode__(self):
        return self.name or self.appid
    class Meta:
        verbose_name = '微信设置'
        verbose_name_plural = '微信设置'

    def get_weixin_api(self):
        return 'http://%s/%s/%s/' % (self.domain, TOKEN, self.id)
        
    def successed(self, data):
        if data.get('errcode') == 0 and data.get('errmsg') == 'ok':
            return True
        else:
            return False

    def get_token(self):
        token_cache_key = TOKEN_CACHE_PRE+'__'+self.appid #对不同的app指定不同的缓存
        token = cache.get(token_cache_key)
        if token:
            return token
        else:
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid, self.app_secret)
            dict_data = method_get_api(url)
            token = dict_data.get('access_token')
            expires_in = dict_data.get('expires_in')
            if token and expires_in:
                cache.set(token_cache_key, token, expires_in-60)
            return token or ''
    
    def get_all_user(self, next_id=None):
        '''得到所有用户列表''' 
        suffix = ''
        if next_id:
            suffix = '&next_openid=' + next_id
        return method_get_api('https://api.weixin.qq.com/cgi-bin/user/get?access_token='+self.get_token()+suffix)
    
    def get_user_info(self, openid):
        '''得到用户的详细信息''' 
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (self.get_token(), openid)
        return method_get_api(url)
    
    
    def create_menu(self, post_data):
        '''创建菜单，成功返回True'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+self.get_token()
        return_data = method_post_api(url, post_data)
        print return_data
        return return_data
        #return self.successed(return_data)
    
    def select_menu(self):
        '''查询menu'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + self.get_token()
        return method_get_api(url)

    def delete_menu(self):
        '''删除menu'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='+self.get_token()
        return self.successed(method_get_api(url))

    def create_qrcode(self, scene_id, permanent=False, expire_seconds=1800):
        '''创建带参数二维码,永久的要permanent=True'''
        scene_id = str(scene_id)
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % self.get_token()
        if permanent:
            post_data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            dirpath = '/var/data/yimi-img/upload/qrcode/'+self.appid+'/permanent/'
            expire_seconds = 0
        else:
            post_data = {"expire_seconds": expire_seconds, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            dirpath = '/var/data/yimi-img/upload/qrcode/'+self.appid+'/tmp/'

        return_data = method_post_api(url, post_data)
        if return_data.get('ticket'):
            qrcode = self.qrcodes.filter(scene_id=scene_id).first()
            url = dirpath+scene_id+'.jpg'
            url = url.replace('/var/data/yimi-img/upload/', 'http://%s/media/' % self.domain)
            if not qrcode:
                qrcode = self.qrcodes.create(scene_id=scene_id, url=url, expire_seconds=expire_seconds)
            else:
                qrcode.url=url
                qrcode.expire_seconds=expire_seconds
                qrcode.save()
            filedata = urllib2.urlopen('https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='+return_data.get('ticket')).read()
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            file(dirpath+scene_id+'.jpg', 'wb').write(filedata)
            
    def send_create_menu(self):
        '''发送创建menu''' 
        menu_buttons = self.menu_buttons.exclude(name=None).exclude(name="")
        button_data = []
        for button in menu_buttons:
            button_name = button.name
            if button.type == 'click':
                data = {
                    'type': 'click',
                    'name': button_name,
                    'key': button.key
                }
            elif button.type == 'view':
                data = {
                    'type': 'view',
                    'name': button_name,
                    'url': button.url,
                }
    
            elif button.type == 'sub_button':
                sub_data = []
                
                for sub_button in button.sub_button.exclude(name=None).exclude(name="") :
                    sub_button_name = sub_button.name
                    if sub_button.type == 'click':
                        son_data = {
                            'type': 'click',
                            'name': sub_button_name,
                            'key': sub_button.key
                        }
                    elif sub_button.type == 'view':
                        son_data = {
                            'type': 'view',
                            'name': sub_button_name,
                            'url': sub_button.url,
                        }
                    sub_data.append(son_data)
                data = {
                    'name': button.name,
                    'sub_button': sub_data
                }
            button_data.append(data)
        post_data = {'button':button_data}
        return self.create_menu(post_data)


    def get_user_openid(self, request):
        '''微网站获取用户openid'''
        code = request.GET.get("code", '')
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (self.appid, self.app_secret, code)
        data = method_get_api(url)
        openid = data.get("openid")
        return openid 

     
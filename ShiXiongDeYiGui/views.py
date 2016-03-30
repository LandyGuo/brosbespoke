#coding:utf8
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode
from django.conf.urls import patterns, include, url 
from weixin import utils
from weixin.models import WXUser
from django.core.exceptions import ObjectDoesNotExist
from ShiXiongDeYiGui.settings import APPID, APP_SECRET

from django.shortcuts import get_object_or_404
from weixin.models import WXConfig
from ShiXiongDeYiGui.settings import TOKEN
import json
import xml.etree.ElementTree as ET
import urllib,urllib2,time,hashlib
import re
import logging

def get_logger():
	logger = logging.getLogger()
	logger.setLevel(__debug__)
	return logger

logging.basicConfig(level=logging.DEBUG)

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')



YOUDAO_KEY = "2103657563"
YOUDAO_KEY_FROM = "weixin4youdao"
YOUDAO_DOC_TYPE = "xml"

REPLY_DATA = '''
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[%s]]></MsgType>
	<Content><![CDATA[%s]]></Content>
	</xml>
'''
REPLY_NEWS_DATA = '''
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>1</ArticleCount>
    <Articles>
    <item>
    <Title><![CDATA[title1]]></Title> 
    <Description><![CDATA[description1]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[url]]></Url>
    </item>
    </Articles>
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

	def __init__(self, body, WXConfig):
		self.body = body
		self.WXConfig = WXConfig

	def parse_xml(self):	 
		self.to_user = self.re_find(self.touser_re)
		self.from_user = self.re_find(self.fromuser_re)

		self.msgtype = self.re_find(self.msgtype_re)
		self.content = self.re_find(self.content_re)
		zjText = u'''欢迎关注师兄的衣柜Bros.Bespoke！
点击“在线定制”，查看更多定制产品。
点击“预约量体”，预约专业的形象设计师上门量体。
点击“注册登录”，量体后可在次日查看“我的尺寸”。

师兄的衣柜，北京大学2010级创业团队，专注于商务装的量身定制。我们苛求细节，精益求精，愿陪伴憧憬未来的你，见证生命中的不平凡时刻。

定制生活，从这里开始！'''
		wycjText = u'''亲爱的北大师弟，感谢你参与本次抽奖活动！我们会在48小时内告知获奖情况。

定制生活，从这里开始！'''	
		wyltText = u'''亲爱的北大师弟，感谢你参与本次量体活动！我们会在6.23（周二）上午10:30-17:00在光华1号楼地下一层咖啡厅免费为您量体，带给您一次专属的定制体验。

定制生活，从这里开始！'''
		self.zj_data = REPLY_DATA % (self.from_user, self.to_user, str(int(time.time())),u'text',zjText)
		self.wycj_data =  REPLY_DATA % (self.from_user, self.to_user, str(int(time.time())),u'text',wycjText)
		self.wylt_data =  REPLY_DATA % (self.from_user, self.to_user, str(int(time.time())),u'text',wyltText)
		twurl = 'http://mmbiz.qpic.cn/mmbiz/LShzZFIvBMkibB8nrianIjeKs8mAc88fVnf5O4PQBPptbdTjOSgOXgfDncSVt5wBVVo7xLnjjYV9icWwRDy3hyq0Q/640?wx_fmt=jpeg&tp=webp&wxfrom=5'
		self.tuwen_data =  REPLY_NEWS_DATA % (self.from_user, self.to_user, str(int(time.time())),twurl)
		if self.msgtype == 'event':
			self.event = self.re_find(self.event_re)
			if self.event == 'VIEW':
				get_logger().debug( 'url menu clicked')
			if self.event == 'subscribe':
				get_logger().debug( '-----------------------enter subscribe:%s'%self.event)
				replayText = u'欢迎关注师兄的衣柜BrosBespoke！点击下方“量身定制”可以查看更多产品。'
				self.return_data = REPLY_DATA % (self.from_user, self.to_user, str(int(time.time())),u'text',zjText)
	def re_find(self, re_str):
		data_result = re.findall(re_str, self.body)
		return data_result and data_result[0] or ''

@csrf_exempt
def handleRequest(request):
	#get_logger().debug( 'request logging---------------------')
	if request.method == 'GET':
		#response = HttpResponse(request.GET['echostr'],content_type="text/plain")
		response = HttpResponse(checkSignature(request),content_type="text/plain")
		return response
	elif request.method == 'POST':
		#c = RequestContext(request,{'result':responseMsg(request)})
		#t = Template('{{result}}')
		#response = HttpResponse(t.render(c),content_type="application/xml")
		#response = HttpResponse(responseMsg(request),content_type="application/xml")
		#return response
		return_data = ''
		try:
			app_item = WXConfig.objects.get(appid=APPID)
			try:
				#get_logger().debug('request: %s',request.body)
				msg = ParseMessage(request.body, app_item)
				# file('/var/www/body.xml', 'w').write(request.body) #测试
				msg.parse_xml()
				# if  '我要抽奖' in msg.content:
				# 	return_data =msg.wycj_data
				# elif  '我要量体'in msg.content:
				# 	return_data =msg.wylt_data
				if hasattr(msg, 'event'): 
					get_logger().debug( '------------------------msg.event:%s', msg.event)
					#get_logger().debug( '------------------------subscribe----------'+msg.content)
					get_logger().debug( '------------------------from_user: %s',  msg.to_user)
					# 关注后增加用户信息
					if msg.event == 'VIEW':
						request.session['openid']=msg.from_user
					elif msg.event == 'subscribe':
						get_logger().debug( '------------------------subscribe----------')
						openid = msg.from_user
						user_info = app_item.get_user_info(openid)
						
						wxuser = WXUser()
						try:
							wxuser = WXUser.objects.get(openid=msg.from_user)
						except:
							pass
						return_data =msg.return_data
						get_logger().debug( '------------------------subscribe----------%s',return_data)
						wxuser.nickname = user_info.get('nickname')
						wxuser.openid = user_info.get('openid')
						wxuser.sex = user_info.get('sex')
						wxuser.language = user_info.get('language')
						wxuser.city = user_info.get('city')
						wxuser.province = user_info.get('province')
						wxuser.country = user_info.get('country')
						wxuser.headimgurl = user_info.get('headimgurl')
						get_logger().debug( '------------------------wx nicknaem=%s',user_info.get('nickname'))
						wxuser.save()
			except Exception, data:
				print 'pass message exception'
				print Exception, ":", data
		except ObjectDoesNotExist:
			#get_logger().debug( '------------------------app id not exists')
			pass
		
		get_logger().debug( '------------------------return_data %s', return_data)
		return HttpResponse(return_data, content_type="application/xhtml+xml")
	else:
		return None

def checkSignature(request):
	global TOKEN
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
		return echoStr
	else:
		return None

@csrf_exempt
def wx_create_menu(request, app_secret):
	app_item = get_object_or_404(WXConfig,app_secret=app_secret)
	menu = '''{ 
	 "button":[ 
		   { 
			   "type":"view",
			   "name":"量身定制",
			   "url":"http://shixiongdeyigui.vipsinaapp.com/wap/buy"
		   }, 
	 
		  { 
			   "name":"BB服务", 
			   "sub_button": 
			   [{ 
				   "type":"view", 
				   "name":"售后服务", 
					"url":"http://shixiongdeyigui.vipsinaapp.com/wap/service" 
				}, 
				{ 
				   "type":"view", 
				   "name":"定制文化", 
				   "url":"http://shixiongdeyigui.vipsinaapp.com/wap/culture" 
				}, 
				{ 
				   "type":"view", 
				   "name":"关于我们", 
				   "url":"http://shixiongdeyigui.vipsinaapp.com/wap/about" 
				} 
				] 
		  }, 
		  { 
				"name":"个人中心", 
			   "sub_button": 
			   [{ 
				   "type":"view", 
				   "name":"优惠券", 
					"url":"http://shixiongdeyigui.vipsinaapp.com/wap/coupons" 
				}, 
				{ 
				   "type":"view", 
				   "name":"我的尺寸", 
				   "url":"http://shixiongdeyigui.vipsinaapp.com/wap/show_my_size" 
				}, 
				{ 
				   "type":"view", 
				   "name":"个人信息", 
				   "url":"http://shixiongdeyigui.vipsinaapp.com/wap/my_info" 
				} 
				] 
		   }] 
	 }'''
	#menu ='{{"button":[{"type":"click","name":"今日歌曲","key":"V1001_TODAY_MUSIC","sub_button":[]},{"type":"click","name":"歌手简介","key":"V1001_TODAY_SINGER","sub_button":[]},{"name":"菜单","sub_button":[{"type":"click","name":"hello word","key":"V1001_HELLO_WORLD","sub_button":[]},{"type":"click","name":"赞一下我们","key":"V1001_GOOD","sub_button":[]}]}]}}' 
	return_data = app_item.create_menu( menu.encode('utf-8'))
	return HttpResponse(json.dumps(return_data),content_type="application/json");

def responseMsg(request):
	rawStr = smart_str(request.raw_post_data)
	#rawStr = smart_str(request.POST['XML'])
	msg = paraseMsgXml(ET.fromstring(rawStr))
	
	queryStr = msg.get('Content','You have input nothing~')

	raw_youdaoURL = "http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=%s&version=1.1&q=" % (YOUDAO_KEY_FROM,YOUDAO_KEY,YOUDAO_DOC_TYPE)	
	youdaoURL = "%s%s" % (raw_youdaoURL,urllib2.quote(queryStr))

	req = urllib2.Request(url=youdaoURL)
	result = urllib2.urlopen(req).read()

	replyContent = paraseYouDaoXml(ET.fromstring(result))

	return getReplyXml(msg,replyContent)

def paraseMsgXml(rootElem):
	msg = {}
	if rootElem.tag == 'xml':
		for child in rootElem:
			msg[child.tag] = smart_str(child.text)
	return msg

def paraseYouDaoXml(rootElem):
	replyContent = ''
	if rootElem.tag == 'youdao-fanyi':
		for child in rootElem:
			# 错误码
			if child.tag == 'errorCode':
				if child.text == '20':
					return 'too long to translate\n'
				elif child.text == '30':
					return 'can not be able to translate with effect\n'
				elif child.text == '40':
					return 'can not be able to support this language\n'
				elif child.text == '50':
					return 'invalid key\n'

			# 查询字符串
			elif child.tag == 'query':
				replyContent = "%s%s\n" % (replyContent, child.text)

			# 有道翻译
			elif child.tag == 'translation': 
				replyContent = '%s%s\n%s\n' % (replyContent, '-' * 3 + u'有道翻译' + '-' * 3, child[0].text)

			# 有道词典-基本词典
			elif child.tag == 'basic': 
				replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'基本词典' + '-' * 3)
				for c in child:
					if c.tag == 'phonetic':
						replyContent = '%s%s\n' % (replyContent, c.text)
					elif c.tag == 'explains':
						for ex in c.findall('ex'):
							replyContent = '%s%s\n' % (replyContent, ex.text)

			# 有道词典-网络释义
			elif child.tag == 'web': 
				replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'网络释义' + '-' * 3)
				for explain in child.findall('explain'):
					for key in explain.findall('key'):
						replyContent = '%s%s\n' % (replyContent, key.text)
					for value in explain.findall('value'):
						for ex in value.findall('ex'):
							replyContent = '%s%s\n' % (replyContent, ex.text)
					replyContent = '%s%s\n' % (replyContent,'--')
	return replyContent

def getReplyXml(msg,replyContent):
	extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
	extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',replyContent)
	return extTpl
1
	
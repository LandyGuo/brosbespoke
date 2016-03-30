#coding:utf8
from django.contrib import admin
from import_export.admin import ImportExportMixin, ExportActionModelAdmin
from wap.models import *
from django import forms
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
import logging
from django.utils.translation import ugettext as _
from django.conf import settings
from django.forms.models import model_to_dict
import copy
import tablib
from django.db.models.query import QuerySet
from import_export.forms import (
    ImportForm,
    ConfirmImportForm,
    ExportForm,
    export_action_form_factory,
)
from django.template.response import TemplateResponse



def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger

logging.basicConfig(level=logging.DEBUG)


class UserResource(resources.ModelResource):
    name = fields.Field(column_name=u'姓名', attribute=u'name')
    sex = fields.Field(column_name=u'性别', attribute=u'sex')
    measure_status = fields.Field(column_name=u'是否量体完成', attribute=u'measure_status')
    measure_time = fields.Field(column_name=u'量体时间', attribute=u'measure_time')
    phonenumber = fields.Field(column_name=u'电话', attribute=u'phonenumber')
    height = fields.Field(column_name=u'身高', attribute=u'height')
    weight = fields.Field(column_name=u'体重', attribute=u'weight')
    favor = fields.Field(column_name=u'个人偏好', attribute=u'favor')
    lingwei = fields.Field(column_name=u'领围', attribute=u'lingwei')
    chest = fields.Field(column_name=u'胸围', attribute=u'chest')
    waist = fields.Field(column_name=u'腰围', attribute=u'waist')
    shoulder = fields.Field(column_name=u'肩宽', attribute=u'shoulder')
    sleeve_lefet = fields.Field(column_name=u'袖长（左）', attribute=u'sleeve_lefet')
    sleeve_right = fields.Field(column_name=u'袖长（右）', attribute=u'sleeve_right')
    back_cloth = fields.Field(column_name=u'后衣长', attribute=u'back_cloth')
    dianjian_left = fields.Field(column_name=u'垫肩（左）', attribute=u'dianjian_left')
    dianjian_right = fields.Field(column_name=u'垫肩（右）', attribute=u'dianjian_right')
    chest_distance = fields.Field(column_name=u'胸间距', attribute=u'chest_distance')
    chest_height = fields.Field(column_name=u'胸高点', attribute=u'chest_height')
    stomach = fields.Field(column_name=u'肚围', attribute=u'stomach')
    hip = fields.Field(column_name=u'臀围', attribute=u'hip')
    kuyao = fields.Field(column_name=u'裤腰围', attribute=u'kuyao')
    kuchang = fields.Field(column_name=u'裤长', attribute=u'kuchang')
    hengdang = fields.Field(column_name=u'横裆', attribute=u'hengdang')
    xiwei = fields.Field(column_name=u'膝围', attribute=u'xiwei')
    kukou = fields.Field(column_name=u'裤口', attribute=u'kukou')
    qunchang = fields.Field(column_name=u'裙长', attribute=u'qunchang')
    lidang = fields.Field(column_name=u'立裆', attribute=u'lidang')
    majia_qianchang = fields.Field(column_name=u'马甲前长', attribute=u'majia_qianchang')
    majia_houchang = fields.Field(column_name=u'马甲后长', attribute=u'majia_houchang')
    xiulong = fields.Field(column_name=u'袖笼', attribute=u'xiulong')
    chougenfen = fields.Field(column_name=u'袖根肥', attribute=u'chougenfen')
    xiukou_right = fields.Field(column_name=u'右袖口', attribute=u'xiukou_right')
    xiukou_left = fields.Field(column_name=u'左袖口', attribute=u'xiukou_left')
    tingxiong = fields.Field(column_name=u'挺胸', attribute=u'tingxiong')
    tuobei = fields.Field(column_name=u'驼背', attribute=u'tuobei')
    liangtishi = fields.Field(column_name=u'量体师', attribute=u'liangtishi')
    favor = fields.Field(column_name=u'个人偏好', attribute=u'favor')
    istie = fields.Field(column_name=u'是否打领带', attribute=u'istie')
    iswatch = fields.Field(column_name=u'是否戴手表', attribute=u'iswatch')
    suit_shangyi = fields.Field(column_name=u'西装上衣', attribute=u'suit_shangyi')

    class Meta:
        model = User
        try:
            widgets = {
                    'measure_time': {'format': '%Y-%m-%d'},
                    }
        except:
            try:
                widgets = {
                        'measure_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        }
            except:
                widgets = {
                        'measure_time': {'format': 'None'},
                        }
        exclude = ( 'openid'  , 'password' , 'measure_phonenumber', 'shoulder_percent' , 
            'chest_percent' , 'waist_percent' , 'hip_percent' , 'leg_percent' , 'create_time',
            )
      
        export_order = ( 'name','sex','measure_status','measure_time','phonenumber',
            'height','weight','favor','lingwei','chest','waist','shoulder','sleeve_lefet',
            'sleeve_right','back_cloth','dianjian_left','dianjian_right','chest_distance',
            'chest_height','stomach','hip','kuyao','kuchang','hengdang','xiwei','kukou',
            'qunchang','lidang','majia_qianchang','majia_houchang','xiulong','chougenfen',
            'xiukou_right','xiukou_left','tingxiong','tuobei','liangtishi','favor','istie',
            'iswatch','suit_shangyi','id',
            )
        
    def get_instance(self, instance_loader, row):
        return False

    def save_instance(self, instance, real_dry_run):
        if not real_dry_run:
            try:
                try:
                    instance.favor = int(instance.favor)
                except:
                    instance.favor = 1
                try:
                    instance.istie = int(instance.istie)
                except:
                    instance.istie = 0

                try:
                    instance.iswatch = int(instance.iswatch)
                except:
                    instance.iswatch = 2

                try:
                    instance.suit_shangyi = int(instance.suit_shangyi)
                except:
                    instance.suit_shangyi = 1
                instance.phonenumber = int(instance.phonenumber)
                obj = User.objects.get(phonenumber=instance.phonenumber)
                instance.id= obj.id
                instance.create_time = obj.create_time
                instance.password = obj.password
                instance.openid = obj.openid
                instance.nickname = obj.nickname
                instance.job = obj.job
                instance.age = obj.age
                instance.measure_time = obj.measure_time
                if not instance.favor:
                    instance.favor = '1'
                if not instance.iswatch:
                    instance.iswatch = '2'
                if not instance.suit_shangyi:
                    instance.suit_shangyi = '1'
                obj = instance
                obj.save()
            except:
                try:
                    instance.phonenumber = int(instance.phonenumber)
                    obj = User.objects.get(id=instance.id)
                    instance.create_time = obj.create_time
                    instance.password = obj.password
                    instance.openid = obj.openid
                    instance.nickname = obj.nickname
                    instance.job = obj.job
                    instance.age = obj.age
                    instance.measure_time = obj.measure_time
                    if not instance.favor:
                        instance.favor = '1'
                    if not instance.istie:
                        instance.istie = '0'
                    if not instance.iswatch:
                        instance.iswatch = '2'
                    if not instance.suit_shangyi:
                        instance.suit_shangyi = '1'
                    instance.favor = int(instance.favor)
                    instance.istie = int(instance.istie)
                    instance.iswatch = int(instance.iswatch)
                    instance.suit_shangyi = int(instance.suit_shangyi)
                    obj = instance
                    obj.save()
                except:
                    instance.phonenumber = int(instance.phonenumber)
                    if not instance.favor:
                        instance.favor = '1'
                    if not instance.istie:
                        instance.istie = '0'
                    if not instance.iswatch:
                        instance.iswatch = '2'
                    if not instance.suit_shangyi:
                        instance.suit_shangyi = '1'
                    instance.favor = int(instance.favor)
                    instance.istie = int(instance.istie)
                    instance.iswatch = int(instance.iswatch)
                    instance.suit_shangyi = int(instance.suit_shangyi)
                    obj = instance
                    obj.save()

    def before_import(self, dataset, dry_run):
        #get_logger().debug('----------ataset.get_col----:%s',dataset.get_col(3)[0])
        if 'id' not in dataset.headers:
            dataset.headers.append('id')
        

class UserForm(forms.ModelForm):
    phonenumber = forms.CharField(required=True, label='电话')
    height = forms.CharField(required=True, label='身高')
    weight = forms.CharField(required=True, label='体重')
    kuchang = forms.CharField(required=True, label='裤长')
    hengdang = forms.CharField(required=True, label='横裆')
    xiwei = forms.CharField(required=True, label='膝围')
    kukou = forms.CharField(required=True, label='裤口')
    xiulong = forms.CharField(required=True, label='袖笼')
    chougenfen = forms.CharField(required=True, label='袖根肥')
    xiukou_right = forms.CharField(required=True, label='右袖口')
    #majia_qianchang = forms.CharField(required=True, label='马甲前长')
    #majia_houchang = forms.CharField(required=True, label='马甲后长')
    kukou = forms.CharField(required=True, label='裤口')
    lingwei = forms.CharField(required=True, label='领围')
    chest = forms.CharField(required=True, label='胸围')
    waist = forms.CharField(required=True, label='腰围')
    shoulder = forms.CharField(required=True, label='肩宽')
    sleeve_right = forms.CharField(required=True, label='袖长（默认右）')
    back_cloth = forms.CharField(required=True, label='后衣长')
    hip = forms.CharField(required=True, label='臀围')
    kuyao = forms.CharField(required=True, label='裤腰围')


class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    form = UserForm
    resource_class = UserResource
    search_fields = ['phonenumber', 'name', 'nickname']
    list_display = ['name','nickname', 'order_link','address_link', 'phonenumber', 'id','liangtishi', 'measure_status']
    list_filter = ('measure_status',)
    exclude = ('openid','nickname', 'measure_phonenumber','shoulder_percent', 
               'chest_percent', 'waist_percent', 'hip_percent', 'leg_percent','password','liangtishi',
               'age','job'
               )
    list_display_links = ('phonenumber', 'name')
    # def sdgg(self,obj,):
    #     staus = Order.objects.filter(user_id=obj.id)
    #     return staus
    #def get_changeform_initial_data(self, request):
        #nub = request.user.first_name + request.user.last_name
        #return {'liangtishi': nub}
    def export_action(self, request, *args, **kwargs):
        if str(request.user) != 'admin':
            return HttpResponse('无权限')
        get_logger().debug('----------phonenumber----:')
        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()

            queryset = self.get_export_queryset(request)
            export_data = self.get_export_data(file_format, queryset)
            content_type = 'application/octet-stream'
            # Django 1.7 uses the content_type kwarg instead of mimetype
            try:
                response = HttpResponse(export_data, content_type=content_type)
            except TypeError:
                response = HttpResponse(export_data, mimetype=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                self.get_export_filename(file_format),
            )
            return response

        context = {}
        context['form'] = form
        context['opts'] = self.model._meta
        return TemplateResponse(request, [self.export_template_name],
                                context, current_app=self.admin_site.name)

    def save_model(self, request, obj, form, change):
        a = obj.phonenumber
        if getattr(obj, 'id', None) is None:
            try:
                lis = obj
                di = model_to_dict(lis)
                nua = User.objects.get(phonenumber = a)
                obj = nua
                if getattr(lis, 'nickname', None):
                    obj.nickname = di['nickname']
                if getattr(lis, 'password', None):
                    obj.password = di['password']
                if getattr(lis, 'measure_time', None):
                    obj.measure_time = di['measure_time']
                if getattr(lis, 'measure_status', None):
                    obj.measure_status = di['measure_status']
                obj.height = di['height']
                obj.weight = di['weight']
                obj.favor = di['favor']
                obj.istie = di['istie']
                obj.iswatch = di['iswatch']
                obj.suit_shangyi = di['suit_shangyi']
                obj.lingwei = di['lingwei']
                obj.chest = di['chest']
                obj.waist = di['waist']
                obj.shoulder = di['shoulder']
                obj.sleeve_right = di['sleeve_right']
                obj.sleeve_lefet = di['sleeve_lefet']
                obj.back_cloth = di['back_cloth']
                obj.dianjian_right = di['dianjian_right']
                obj.dianjian_left = di['dianjian_left']
                obj.chest_distance = di['chest_distance']
                obj.chest_height = di['chest_height']
                obj.stomach = di['stomach']
                obj.hip = di['hip']
                obj.kuyao = di['kuyao']
                obj.kuchang = di['kuchang']
                obj.hengdang = di['hengdang']
                obj.xiwei = di['xiwei']
                obj.kukou = di['kukou']
                obj.qunchang = di['qunchang']
                obj.lidang = di['lidang']
                obj.majia_qianchang = di['majia_qianchang']
                obj.majia_houchang = di['majia_houchang']
                obj.xiulong = di['xiulong']
                obj.chougenfen = di['chougenfen']
                obj.xiukou_right = di['xiukou_right']
                obj.xiukou_left = di['xiukou_left']
                obj.tingxiong = di['tingxiong']
                obj.tuobei = di['tuobei']
                if obj.gh =='':
                    obj.gh = request.user.username
                if obj.liangtishi == '':
                    obj.liangtishi = request.user.last_name + request.user.first_name
            except:    
                obj.gh = request.user.username
                obj.liangtishi = request.user.last_name + request.user.first_name
        else:
            get_logger().debug('----------phonenumber----:%s',obj.liangtishi)
            if obj.gh =='':
                obj.gh = request.user.username
            if obj.liangtishi == '':
                obj.liangtishi = request.user.last_name + request.user.first_name

        obj.save()


class CouponAdmin(admin.ModelAdmin):
    search_fields = ['user__phonenumber']
    list_display = ['title', 'user', 'money']


class FabricAdmin(admin.ModelAdmin):
    list_display = ['name', 'volume']


class PackAdmin(ExportActionModelAdmin):
    resource_class = PackResource
    list_display = ['name', 'volume']


class MeasureReservationAdmin(ExportActionModelAdmin):
    resource_class = MeasureReservationResource


class OrderAdminForm(forms.ModelForm):
    product = forms.CharField(required=True, label='产品')
    address = forms.CharField(required=True, label='地址')
    kouxing_sy = forms.CharField(required=True, label='扣型（上衣）:')


class OrderAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    
    def queryset(self, request):
        qs = super(OrderAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(gh=request.user)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'id', None) is None:
            try:
                nua = Order.objects.latest('id')
                obj.order_number = '%0*d' % (12, int(nua.id)+1)
            except:
                obj.order_number = '000000000001'
            
            obj.gh = request.user.username
            obj.xdy = request.user.last_name + request.user.first_name
            get_logger().debug('---------------------%s'% obj.xdy)
            obj.order_status = '已付款'
        obj.price = obj.product.price
        if obj.add_kuzi:
            kuzi_config = OrderPersonalization.objects.get(name='单加裤子', product_name=obj.product.title)
            obj.price = obj.price + kuzi_config.price
        if obj.add_majia:
            majia_config = OrderPersonalization.objects.get(name='单加马甲',product_name=obj.product.title)
            obj.price = obj.price + majia_config.price
        if obj.add_bespoke:
            obj.price = obj.price + 998
        obj.save()
        plant_update = Plant_update()
        try:
            Plant_update.objects.get(order_id = obj.id)
        except:
            plant_update.order_id = obj.id
            plant_update.plant_status = '订单审查'
            plant_update.save()

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = [
            url(r'^my_view/$', self.admin_site.admin_view(self.my_view))
        ]
        return my_urls + urls
    #def get_changeform_initial_data(self, request):
        #nua=Order.objects.latest('id') 
        #nub=nua.order_number[0:-1] +str(int(nua.order_number) + 1)
        #return {'order_status': '已付款'}

    def my_view(self, request, from_url=''):
        a = request.user
        get_logger().debug('---------------------%s'% a)
        if str(a) == 'admin':
            return HttpResponseRedirect('/order/order_manage')
        return HttpResponseRedirect(from_url or reverse('admin:wap_order_changelist'))
    resource_class = OrderResource
    fields = ['user','info','product','fabric','address','kouxing_sy','lingxing_sy', 'yaodou_sy','kaiqi_sy','xiukou_sy','neibudou_sy','libu_sy','beizhu_sy','kuzhe_xk','houdou_xk','kujiao_xk','beizhu_xk','lingxing_cs','xiukou_cs','xiabai_cs','menjin_cs','houbei_cs','koudai_cs','beizhu_cs','add_kuzi','add_majia','majia_lingxing','majia_kouxing','beizhu','add_bespoke','add_xiuzi','xiuzi']
    #form = OrderAdminForm
    list_display = ['order_number','create_time','order_statu','user', 'product', 'price','wxpay']
    list_display_links = ('order_number', 'user')
    raw_id_fields=('user',)
    readonly_fields = ['info','addressinfo']
    #readonly_fields =('address','user')
    #exclude = ('huifang','Plant_status','order_number','price','order_status')
    search_fields = ['user__phonenumber','user__name','user__nickname','order_number']
    list_filter = ('create_time',)
    
    def order_statu(self,obj,):
        staus = obj.order_status
        return staus

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(measure_status=1)
        return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    

    

class address4orderAdmin(ExportActionModelAdmin):
    search_fields = ['user__phonenumber','user__nickname']
    resource_class = Address4OrderResource
    list_display = ['id','recipient','address_street','user']
    raw_id_fields=('user',)

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #if db_field.name == "user":
            #kwargs["queryset"] = User.objects.filter(measure_status=1)
        #return super(address4orderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class Plant_updateAdmin(ExportActionModelAdmin):
    list_display = ['order','create_time','plant_status','gh']


class RedpacketAdmin(admin.ModelAdmin):
    list_display = ['user', 'phonenumber','isUsed','money','type']
    search_fields = ['user__phonenumber','user__nickname']

admin.site.site_header = 'Bros.Bespoke 管理中心'
admin.site.register(User,UserAdmin)
admin.site.register(Product)
admin.site.register(Coupon,CouponAdmin)
#admin.site.register(VerificationCode)
admin.site.register(KouXingShangYi)
admin.site.register(LingXingShangYi)
admin.site.register(YaoDouShangYi)
admin.site.register(KaiQiShangYi)
admin.site.register(XiuKouShangYi)
admin.site.register(NeiBuZaoXingShangYi)
admin.site.register(NeiBuDouShangYi)
admin.site.register(KuZheXiKu)
admin.site.register(HouDouXiKu)
admin.site.register(KuJiaoXiKu)
admin.site.register(MaJiaLingXing)
admin.site.register(MaJiaKouXing)
admin.site.register(LingXingChenShan)
admin.site.register(XiuKouChenShan)
admin.site.register(XiaBaiChenShan)
admin.site.register(MenJinChenShan)
admin.site.register(HouBeiChenShan)
admin.site.register(KouDaiChenShan)
admin.site.register(Plant_update, Plant_updateAdmin)
admin.site.register(Pack, PackAdmin)
admin.site.register(OrderPersonalization)
admin.site.register(Order, OrderAdmin)
admin.site.register(Fabric, FabricAdmin)
admin.site.register(MeasureReservation, MeasureReservationAdmin)
admin.site.register(Address4Order, address4orderAdmin)
admin.site.register(Wxpay)
admin.site.register(Banner)
admin.site.register(Cart)
admin.site.register(Redpacket, RedpacketAdmin)
admin.site.register(Worktime)

#import and export :https://django-import-export.readthedocs.org/en/latest/getting_started.html#importing-data
# coding:utf8
from django.db import models
from django.template.defaultfilters import default
from django.template.defaultfilters import escape
from wap.models import User
from DjangoUeditor.models import UEditorField


# Create your models here.
def get_uploadto_path(model, filename):
    return 'web/%s' % (filename)


MENU_LIST = (
    ('最新产品', '最新产品'),
    ('定制西装', '定制西装'),
    ('定制衬衫', '定制衬衫'),
    ('配件配饰', '配件配饰'),
    ('实体店铺', '实体店铺'),
    ('品味搭配', '品味搭配'),
)

PRODUCT_TYPE_LIST = (
    ('suit', '西服'),
    ('shirt', '衬衫'),
    ('item', '单品'),
    ('accessorie', '配饰'),
)

FABRIC_WEB_LIST= (
    ('BB NATSUN', 'BB NATSUN'),
    ('BB VBC', 'BB VBC'),
    ('BB Scaball', 'BB Scaball'),
    ('BB Smart', 'BB Smart'),
    ('BB Star', 'BB Star'),
)


KOUXING_TYPE_LIST = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('2*1', '2*1'),
    ('4*2', '4*2'),
    ('6*2', '6*2'),
)


LINGXING_TYPE_LIST = (
    ('平驳头', '平驳头'),
    ('枪驳头', '枪驳头'),
    ('礼服领', '礼服领'),
)


YAODOU_TYPE_LIST = (
    ('普通', '普通'),
    ('斜兜', '斜兜'),
    ('双牙兜', '双牙兜'),
)


KAIQI_TYPE_LIST = (
    ('后开气', '后开气'),
    ('侧开气', '侧开气'),
    ('无', '无'),
)


XIUKOU_TYPE_LIST = (
    ('3', '3'),
    ('4', '4'),
)


NEIBUZAOXING_TYPE_LIST = (
    ('时尚款', '时尚款'),
    ('传统款', '传统款'),
)



NEIBUDOU_TYPE_LIST = (
    ('里兜', '里兜'),
    ('笔兜', '笔兜'),
    ('烟兜', '烟兜'),
    ('里兜|笔兜', '里兜|笔兜'),
    ('里兜|烟兜', '里兜|烟兜'),
    ('笔兜|烟兜', '笔兜|烟兜'),
    ('里兜|笔兜|烟兜', '里兜|笔兜|烟兜'),
)


KUZHE_TYPE_LIST = (
    ('无褶', '无褶'),
    ('单褶', '单褶'),
    ('双褶', '双褶'),
)


HOUDOU_TYPE_LIST = (
    ('右边', '右边'),
    ('两边', '两边'),
)


KUJIAO_TYPE_LIST = (
    ('内折边', '内折边'),
    ('外翻边', '外翻边'),
)


MAJIA_LINGXING_TYPE_LIST = (
    ('V领', 'V领'),
    ('U领', 'U领'),
)


MAJIA_KOUXING_TYPE_LIST = (
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('4*2', '4*2'),
    ('6*3', '6*3'),
    ('8*4', '8*4'),
)



ORDER_STATUS_TYPE_LIST = (
    ('未付款', '未付款'),
    ('已付款', '已付款'),
    ('定制中', '定制中'),
    ('定制完成', '定制完成'),
    ('配送中', '配送中'),
    ('已交付', '已交付'),
)

PLANT_STATUS_TYPE_LIST = (
    ('等待制作', '等待制作'),
    ('制作中', '制作中'),
    ('制作完成', '制作完成'),
    ('配送中', '配送中'),
    ('已交付', '已交付'),
)



CHENSHAN_LINGXING_TYPE_LIST = (
    ('标准', '标准'),
    ('八字', '八字'),
    ('一字', '一字'),
    ('领尖扣领', '领尖扣领'),
    ('小方领', '小方领'),
    ('礼服领', '礼服领'),

)



CHENSHAN_XIUKOU_TYPE_LIST = (
    ('2粒直角', '2粒直角'),
    ('2粒斜角', '2粒斜角'),
    ('2粒圆角', '2粒圆角'),
    ('法式直角', '法式直角'),
    ('法式斜角', '法式斜角'),
    ('法式圆角', '法式圆角'),
)



CHENSHAN_XIABAI_TYPE_LIST = (
    ('直下摆', '直下摆'),
    ('小圆下摆', '小圆下摆'),
    ('大圆下摆', '大圆下摆'),
)



CHENSHAN_MENJIN_TYPE_LIST = (
    ('明门襟', '明门襟'),
    ('暗门襟', '暗门襟'),
    ('平门襟', '平门襟'),
)



CHENSHAN_HOUBEI_TYPE_LIST = (
    ('肩部双褶', '肩部双褶'),
    ('后背工字褶', '后背工字褶'),
    ('腰部双褶', '腰部双褶'),
    ('后背无', '后背无'),
)



CHENSHAN_KOUDAI_TYPE_LIST = (
    ('无口袋', '无口袋'),
    ('园口袋', '园口袋'),
    ('六角口袋', '六角口袋'),
    ('尖口袋', '尖口袋'),
)


LIBU_TYPE_LIST = (
    ('黑顺：K-2','黑顺：K-2'),
    ('黑撞：J-33','黑撞：J-33'),
    ('蓝顺：#45','蓝顺：#45'),
    ('蓝撞：k-10','蓝撞：k-10'),
    ('灰顺：#40','灰顺：#40'),
    ('灰撞：#57','灰撞：#57'),
)

GUOMIAN_TYPE_LIST = (
    ('直过面','直过面'),
    ('连耳皮','连耳皮'),
)

POSTER_TYPE_LIST= (
    ('产品','产品'),
    ('产品列表','产品列表'),
    ('网址','网址')
)


#次级菜单
class Secondarymenu(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='参数名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '次级菜单'
        verbose_name_plural = '次级菜单'


#次级菜单分组
class Submenu(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='参数名称')
    secondarymenu = models.ManyToManyField(Secondarymenu, blank=True, null=True, verbose_name='次级菜单')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '次级菜单分组'
        verbose_name_plural = '次级菜单分组'


#菜单
class Menu(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='名称')
    mingzi = models.CharField(max_length=32, blank=True, null=True, verbose_name='英文名称')
    submenu = models.ManyToManyField(Submenu, blank=True, null=True, verbose_name='次级菜单分组')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单'


#分类
class Categorie(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

#面料品牌
class Brand_fabric(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='名称')
    image_url = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='品牌log')
    content = models.TextField(blank=True, null=True, verbose_name='面料品牌描述')
    type = models.CharField(max_length=10, blank=False, null=False, default='suit', choices=PRODUCT_TYPE_LIST, verbose_name='面料品牌类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '面料品牌'
        verbose_name_plural = '面料品牌'

#网站面料
class Fabric_web(models.Model):
    name = models.CharField(max_length=64,  null=True, verbose_name='名称')
    #brand = models.CharField(max_length=64, blank=True, null=True, choices=FABRIC_WEB_LIST, verbose_name='面料品牌')
    brand_fabric = models.ForeignKey(Brand_fabric,blank=True,  null=True, verbose_name='面料品牌')
    color = models.CharField(max_length=64, blank=True, null=True, verbose_name='Color')
    desigh = models.CharField(max_length=64, blank=True, null=True, verbose_name='Design')
    weight = models.CharField(max_length=64, blank=True, null=True, verbose_name='Weight')
    composition = models.CharField(max_length=64, blank=True, null=True, verbose_name='Composition')
    volume =models.FloatField(max_length=64, blank=True, null=True, verbose_name='数量')
    thumbnail_url = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='面料缩略图')
    image_url = models.ImageField(upload_to=get_uploadto_path, null=True, verbose_name='面料大图')
    content = models.TextField(blank=True, null=True, verbose_name='面料描述')
    price = models.IntegerField(max_length=11, null=True, verbose_name='价格')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __unicode__(self):
        return self.name +':' + str(self.price)

    class Meta:
        verbose_name = '面料信息'
        verbose_name_plural = '面料信息'


#网站产品
class Product_web(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name='标题')
    subtitle = models.CharField(max_length=128, blank=True, null=True, verbose_name='副标题')
    price = models.IntegerField(max_length=11, blank=True, null=True, verbose_name='单品价格')
    introduction = models.TextField(blank=True, null=True, verbose_name='产品介绍，|分割')
    fabric_web = models.ManyToManyField(Fabric_web, blank=True, null=True, verbose_name='面料', related_name='fabric_web')
    fabric_web_default = models.ForeignKey(Fabric_web, blank=True, null=True, verbose_name='默认面料', related_name='fabric_web_default')
    size_description = models.TextField(blank=True, null=True, verbose_name='尺寸说明，|分割')
    craft_description = models.TextField(blank=True, null=True, verbose_name='工艺细节，|分割')
    custom_description = models.TextField(blank=True, null=True, verbose_name='定制说明与发货，|分割')
    latest_product = models.BooleanField(default=False,  verbose_name='是否为最新产品')
    menu = models.ForeignKey(Menu, verbose_name='菜单', blank=True, null=True)
    submenu = models.ManyToManyField(Submenu, blank=True, null=True, verbose_name='次级菜单分组')
    secondarymenu = models.ForeignKey(Secondarymenu, blank=True, null=True, verbose_name='所属次级菜单')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    categorie = models.ForeignKey(Categorie, verbose_name='分类', blank=True, null=True)
    type = models.CharField(max_length=10, blank=False, null=False, default='shirt', choices=PRODUCT_TYPE_LIST, verbose_name='产品类型')
    img = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片一')
    img_thumbnail = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片一缩略图')
    img2 = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片二')
    img2_thumbnail = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片二缩略图')
    img3 = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片三')
    img3_thumbnail = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片三缩略图')
    img4 = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片四')
    img4_thumbnail = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片四缩略图')
    img5 = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片五')
    img5_thumbnail = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片五缩略图')
    img6 = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片六')
    img6_thumbnail = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片六缩略图')
    # 上衣参数
    kouxing_sy = models.CharField(max_length=16, blank=True, null=True, default='', choices=KOUXING_TYPE_LIST, verbose_name='扣型（上衣）')
    lingxing_sy = models.CharField(max_length=16, blank=True, null=True, default='',choices=LINGXING_TYPE_LIST, verbose_name='领型（上衣）')
    yaodou_sy = models.CharField(max_length=16, blank=True, null=True, default='',choices=YAODOU_TYPE_LIST, verbose_name='腰兜（上衣）')
    kaiqi_sy = models.CharField(max_length=16, blank=True, null=True, default='',choices=KAIQI_TYPE_LIST, verbose_name='开气（上衣）')
    xiukou_sy = models.CharField(max_length=16, blank=True, null=True, default='',choices=XIUKOU_TYPE_LIST, verbose_name='袖扣（上衣）')
    neibuzaoxing_sy = models.CharField(max_length=16, blank=True, null=True, default='',choices=NEIBUZAOXING_TYPE_LIST, verbose_name='内部造型（上衣）')
    neibudou_sy = models.CharField(max_length=16, blank=True, null=True, default='',choices=NEIBUDOU_TYPE_LIST, verbose_name='内部兜( 多选用  ‘|’ 线分割)（上衣）')

    # 西裤参数
    kuzhe_xk = models.CharField(max_length=16, blank=True, null=True, default='',choices=KUZHE_TYPE_LIST, verbose_name='裤褶（西裤）')
    houdou_xk = models.CharField(max_length=16, blank=True, null=True, default='',choices=HOUDOU_TYPE_LIST, verbose_name='后兜（西裤）')
    kujiao_xk = models.CharField(max_length=16, blank=True, null=True, default='',choices=KUJIAO_TYPE_LIST, verbose_name='裤脚（西裤）')

    #衬衫参数
    lingxing_cs = models.CharField(max_length=16, blank=True, null=True, default='',choices=CHENSHAN_LINGXING_TYPE_LIST, verbose_name='领型（衬衫）')
    xiukou_cs = models.CharField(max_length=16, blank=True, null=True, default='',choices=CHENSHAN_XIUKOU_TYPE_LIST, verbose_name='袖口（衬衫）')
    xiabai_cs = models.CharField(max_length=16, blank=True, null=True, default='',choices=CHENSHAN_XIABAI_TYPE_LIST, verbose_name='下摆（衬衫）')
    menjin_cs = models.CharField(max_length=16, blank=True, null=True, default='',choices=CHENSHAN_MENJIN_TYPE_LIST, verbose_name='门襟（衬衫）')
    houbei_cs = models.CharField(max_length=16, blank=True, null=True, default='',choices=CHENSHAN_HOUBEI_TYPE_LIST,verbose_name='后背（衬衫）')
    koudai_cs = models.CharField(max_length=16, blank=True, null=True, default='',choices=CHENSHAN_KOUDAI_TYPE_LIST, verbose_name='口袋（衬衫）')

    def __unicode__(self):
        return format(self.title)

    class Meta:
        verbose_name = '产品(网站)'
        verbose_name_plural = '产品(网站)'


#首页展示图
class Focus(models.Model):
    name = models.CharField(max_length=256, default='', verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    #product_web = models.ForeignKey(Product_web, verbose_name='所属产品', blank=True, null=True)
    img = models.ImageField(upload_to=get_uploadto_path, blank=True, null=True,
                            verbose_name='展示图')
    sort = models.CharField(max_length=26, blank=False, null=True, choices=POSTER_TYPE_LIST, verbose_name='跳转类型')
    img_href = models.CharField(max_length=256, blank=True, null=True, default='',
                                verbose_name='跳转链接|网址不填:Http://,产品名填产品ID ,产品列表填写菜单名按级别用|分割')

    def __unicode__(self):
        return format(self.id)

    class Meta:
        verbose_name = '首页焦点图'
        verbose_name_plural = '首页焦点图'


#首页海报
class Poster(models.Model):
    name = models.CharField(max_length=256, default='', verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    #product_web = models.ForeignKey(Product_web, verbose_name='所属产品', blank=True, null=True)
    img = models.ImageField(upload_to=get_uploadto_path, blank=True, null=True,
                            verbose_name='展示图')
    sort = models.CharField(max_length=26, blank=False, null=True, choices=POSTER_TYPE_LIST, verbose_name='跳转类型')
    img_href = models.CharField(max_length=256, blank=True, null=True, default='',
                                verbose_name='跳转链接|网址不填:Http://,产品名填产品ID ,产品列表填写菜单名多级别用|分割')

    def __unicode__(self):
        return format(self.id)

    class Meta:
        verbose_name = '首页海报'
        verbose_name_plural = '首页海报'


class Cart_web(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True, related_name='user')
    #wxpay = models.ForeignKey(Wxpay, blank=True, null=True, verbose_name='微信支付记录')
    product = models.ForeignKey(Product_web, verbose_name='产品', blank=True)
    price = models.FloatField(blank=True, null=True, default=0, verbose_name='价格')
    is4friend = models.BooleanField(default=False, verbose_name='是否为重视的人定制')
    friend_phone = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='朋友电话')
    fabric = models.ForeignKey(Fabric_web, blank=True, null=True, verbose_name='面料')
    #address = models.ForeignKey(Address4Order, blank=True, null=True, verbose_name='地址')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    # 个性化
    add_bespoke = models.BooleanField(default=False, verbose_name='是否Bespoke')
    add_xiuzi = models.BooleanField(default=False, verbose_name='是否绣字')
    xiuzi = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='绣字')
    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车'


#弹窗
class Footer(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='名称')
    mz = models.CharField(max_length=32, blank=True, null=True, verbose_name='英文名称')
    content = models.TextField(blank=True, null=True, verbose_name='弹窗内容，|分段')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '弹窗'
        verbose_name_plural = '弹窗'


#期刊
class Journal(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name='标题')
    subtitle = models.CharField(max_length=128, blank=True, null=True, verbose_name='副标题')
    img = models.ImageField(upload_to=get_uploadto_path, blank=True, null=True,
                            verbose_name='展示图')
    content = UEditorField(blank=True, width=800, height=480, toolbars="full", null=True, verbose_name='主文')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = '期刊'
        verbose_name_plural = '期刊'
        ordering  = ['-create_time']

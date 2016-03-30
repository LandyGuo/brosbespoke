# coding:utf8
from django.db import models
from django.template.defaultfilters import default

from import_export import fields
from import_export import resources

# Create your models here.
def get_uploadto_path(model, filename):  
    return 'media/%s' % (filename)

SEX_TYPE_LIST = (
    ('女', '女'),
    ('男', '男'),
)

PRODUCT_TYPE_LIST = (
    ('suit', '西服'),
    ('shirt', '衬衫'),
)

USED_TYPE_LIST = (
    ('1', '已使用'),
    ('0', '未使用'),
)

COUPON_TYPE_LIST = (
    ('shirt', '衬衫优惠券'),
    ('suit', '西服优惠券'),
    ('redpacket', '微信红包优惠券'),
)

PIANHAO_TYPE_LIST = (
    ('0', '修身'),
    ('1', '合身'),
    ('2', '宽松'),

)

LINGDAI_TYPE_LIST = (
    ('0', '打领带'),
    ('1', '不打领带'),

)

SOUBIAO_TYPE_LIST = (
    ('2', '无手表'),
    ('1', '手表右'),
    ('0', '手表左'),

)
SUIT_SHANGYI_TYPE_LIST = (
    ('0', '长'),
    ('1', '短'),
)

class User(models.Model):
    openid = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name='微信用户标识')
    nickname = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name='昵称')
    name = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name='姓名')
    sex = models.CharField(max_length=10, blank=True, null=True, default='男', choices=SEX_TYPE_LIST, verbose_name='性别')
    phonenumber = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='电话')
    password = models.CharField(max_length=64, blank=True, null=True, default='', verbose_name='密码')
    shoulder_percent = models.IntegerField(max_length=11, blank=True, null=True, default='0', verbose_name='肩宽百分比')
    chest_percent = models.IntegerField(max_length=11, blank=True, null=True, default='0', verbose_name='胸围百分比')
    waist_percent = models.IntegerField(max_length=11, blank=True, null=True, default='0', verbose_name='腰围百分比')
    hip_percent = models.IntegerField(max_length=11, blank=True, null=True, default='0', verbose_name='臀围百分比')
    leg_percent = models.IntegerField(max_length=11, blank=True, null=True, default='0', verbose_name='腿长百分比')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    measure_time = models.DateTimeField(blank=True, null=True, verbose_name='量体时间')
    measure_phonenumber = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='量体时记录的电话')
    measure_status = models.BooleanField(default=False, verbose_name='是否量体完成')
    height = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='身高')
    weight = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='体重')
    #tixing = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='体型')
    favor = models.CharField(max_length=32, blank=True, null=True, default='',choices=PIANHAO_TYPE_LIST, verbose_name='个人偏好')
    istie = models.CharField(max_length=32, blank=True, null=True, default='',choices=LINGDAI_TYPE_LIST, verbose_name='是否打领带')
    iswatch = models.CharField(max_length=32, blank=True, null=True, default='',choices=SOUBIAO_TYPE_LIST, verbose_name='是否戴手表')
    suit_shangyi = models.CharField(max_length=32, blank=True, null=True, default='',choices=SUIT_SHANGYI_TYPE_LIST, verbose_name='西装上衣')
    lingwei = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='领围')
    chest = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='胸围')
    waist = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='腰围')
    shoulder = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='肩宽')
    sleeve_right = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='袖长（默认右）')
    sleeve_lefet = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='袖长（左）')
    back_cloth = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='后衣长')
    dianjian_right = models.CharField(max_length=32, blank=True,  default='0', verbose_name='垫肩（默认右）')
    dianjian_left = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='垫肩（左）')
    chest_distance = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='胸间距')
    chest_height = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='胸高点')
    stomach = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='肚围')
    hip = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='臀围')
    kuyao = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='裤腰围')
    kuchang = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='裤长')
    hengdang = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='横裆')
    xiwei = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='膝围')
    kukou = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='裤口')
    qunchang = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='裙长')
    lidang = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='立裆')
    majia_qianchang = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='马甲前长')
    majia_houchang = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='马甲后长')
    xiulong = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='袖笼')
    chougenfen = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='袖根肥')
    xiukou_right = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='右袖口')
    xiukou_left = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='左袖口')
    tingxiong = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='挺胸')
    tuobei = models.CharField(max_length=32, blank=True, null=True, default='0', verbose_name='驼背')
    liangtishi = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='量体师')
    
    def __unicode__(self):
        return self.name + ':' + str(self.phonenumber)
    class Meta:
        verbose_name = '注册用户'
        verbose_name_plural = '注册用户'



class Product(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    img_with_text = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='带文字的产品图片，用在产品列表')
    img = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='产品图片，用在产品详情顶部')
    price = models.IntegerField(max_length=11, blank=True, null=True, verbose_name='价格')
    fabricname = models.TextField(blank=True, null=True, verbose_name='面料，|分割')
    craft = models.TextField(blank=True, null=True, verbose_name='工艺，|分割')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    type = models.CharField(max_length=10, blank=False, null=False, default='shirt', choices=PRODUCT_TYPE_LIST, verbose_name='产品类型')

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = '产品(西装衬衫)'
        verbose_name_plural = '产品(西装衬衫)'


# 优惠券
class Coupon(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    money = models.IntegerField(max_length=8, blank=True, null=True, default=0, verbose_name='金额')
    user = models.ForeignKey(User, verbose_name='用户', blank=True, null=True)
    isUsed = models.CharField(max_length=2, blank=False, null=False, default='0', choices=USED_TYPE_LIST, verbose_name='是否使用')
    type = models.CharField(max_length=10, blank=False, null=False, default='shirt', choices=COUPON_TYPE_LIST, verbose_name='优惠券类型')
    expire_time = models.DateTimeField(blank=True, null=True, verbose_name='失效时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    use_time = models.DateTimeField(blank=True, null=True, verbose_name='使用时间')

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = '优惠券'
        verbose_name_plural = '优惠券'

# 短信验证码
class VerificationCode(models.Model):
    code = models.CharField(max_length=8, blank=True, null=True, verbose_name='验证码')
    phone = models.CharField(max_length=16, blank=True, null=True, verbose_name='手机号码')
    use_time = models.DateTimeField(auto_now_add=False, null=True, verbose_name='验证时间')
    expire_time = models.DateTimeField(auto_now_add=False, null=True, verbose_name='失效时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.code
    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = '验证码'

# 订单地址
class Address4Order(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True, null=True)
    #user_id = models.IntegerField(max_length=11, blank=True, null=True, default=0, verbose_name='用户id')
    recipient = models.CharField(max_length=128, blank=True, null=True, verbose_name='收件人')
    phone = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='收件人电话')
    address_region = models.CharField(max_length=64, blank=True, null=True, default='', verbose_name='所在市区')
    address_street = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name='街道详细地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.recipient+ ':' + self.address_region+ ':' +self.address_street
    class Meta:
        verbose_name = '用户常用订单地址'
        verbose_name_plural = '用户常用订单地址'

class Address4OrderResource(resources.ModelResource):
    class Meta:
        model = Address4Order

        
# 面料
class Fabric(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='名称')
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name='所属产品')
    volume =models.FloatField(max_length=64, blank=True, null=True, verbose_name='数量')
    thumbnail_url = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='面料缩略图')
    image_url = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='面料大图')
    content = models.TextField(blank=True, null=True, verbose_name='面料描述')
    price = models.IntegerField(max_length=11, blank=True, null=True, verbose_name='价格')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '面料信息'
        verbose_name_plural = '面料信息'


class Pack(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='名称')
    volume = models.FloatField(max_length=64, blank=True, null=True, verbose_name='数量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '包装材料'
        verbose_name_plural = '包装材料'

class PackResource(resources.ModelResource):
    class Meta:
        model = Pack

# 预约量体
class MeasureReservation(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True, null=True)
    #user_id = models.IntegerField(max_length=11, blank=True, null=True, default=0, verbose_name='用户id')
    reservation_number = models.CharField(max_length=128, blank=True, null=True, verbose_name='量体预约号')
    phone = models.CharField(max_length=128, blank=True, null=True, verbose_name='预约手机')
    sex = models.CharField(max_length=10, blank=True, null=True, default='女', choices=SEX_TYPE_LIST, verbose_name='性别')
    weight = models.FloatField(blank=True, null=True, default=0, verbose_name='体重')
    height = models.FloatField(blank=True, null=True, default=0, verbose_name='身高')
    reservation_time = models.DateTimeField(blank=True, null=True, verbose_name='预约时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    address_region = models.CharField(max_length=64, blank=True, null=True, default='', verbose_name='所在市区')
    address_street = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name='街道详细地址')
    def __unicode__(self):
        return self.reservation_number
    class Meta:
        verbose_name = '预约量体'
        verbose_name_plural = '预约量体'
        
class MeasureReservationResource(resources.ModelResource):
    class Meta:
        model = MeasureReservation
        
class ClothParam(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='参数名称')
    price = models.FloatField(blank=True, null=True, default=0, verbose_name='价格')
    image = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='图片')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    def __unicode__(self):
        return self.name
# 扣型（上衣）
class KouXingShangYi(ClothParam):
    class Meta:
        verbose_name = '扣型（上衣）'
        verbose_name_plural = '扣型（上衣）'

KOUXING_TYPE_LIST = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('2*1', '2*1'),
    ('4*2', '4*2'),
    ('6*2', '6*2'),
)
# 领型（上衣）
class LingXingShangYi(ClothParam):
    class Meta:
        verbose_name = '领型（上衣）'
        verbose_name_plural = '领型（上衣）'

LINGXING_TYPE_LIST = (
    ('平驳头', '平驳头'),
    ('枪驳头', '枪驳头'),
    ('礼服领', '礼服领'),
)
# 腰兜（上衣）
class YaoDouShangYi(ClothParam):
    class Meta:
        verbose_name = '腰兜（上衣）'
        verbose_name_plural = '腰兜（上衣）'

YAODOU_TYPE_LIST = (
    ('普通', '普通'),
    ('斜兜', '斜兜'),
    ('双牙兜', '双牙兜'),
)
# 开气（上衣）
class KaiQiShangYi(ClothParam):
    class Meta:
        verbose_name = '开气（上衣）'
        verbose_name_plural = '开气（上衣）'

KAIQI_TYPE_LIST = (
    ('后开气', '后开气'),
    ('侧开气', '侧开气'),
    ('无', '无'),
)
# 袖扣（上衣）
class XiuKouShangYi(ClothParam):
    class Meta:
        verbose_name = '袖扣（上衣）'
        verbose_name_plural = '袖扣（上衣）'

XIUKOU_TYPE_LIST = (
    ('3', '3'),
    ('4', '4'),
)
# 内部造型（上衣）
class NeiBuZaoXingShangYi(ClothParam):
    class Meta:
        verbose_name = '内部造型（上衣）'
        verbose_name_plural = '内部造型（上衣）'

NEIBUZAOXING_TYPE_LIST = (
    ('时尚款', '时尚款'),
    ('传统款', '传统款'),
)

# 内部兜（上衣）
class NeiBuDouShangYi(ClothParam):
    class Meta:
        verbose_name = '内部兜（上衣）'
        verbose_name_plural = '内部兜（上衣）'

NEIBUDOU_TYPE_LIST = (
    ('里兜', '里兜'),
    ('笔兜', '笔兜'),
    ('烟兜', '烟兜'),
    ('里兜|笔兜', '里兜|笔兜'),
    ('里兜|烟兜', '里兜|烟兜'),
    ('笔兜|烟兜', '笔兜|烟兜'),
    ('里兜|笔兜|烟兜', '里兜|笔兜|烟兜'),
)
# 裤褶（西裤）
class KuZheXiKu(ClothParam):
    class Meta:
        verbose_name = '裤褶（西裤）'
        verbose_name_plural = '裤褶（西裤）'

KUZHE_TYPE_LIST = (
    ('无褶', '无褶'),
    ('单褶', '单褶'),
    ('双褶', '双褶'),
)
# 后兜（西裤）
class HouDouXiKu(ClothParam):
    class Meta:
        verbose_name = '后兜（西裤）'
        verbose_name_plural = '后兜（西裤）'

HOUDOU_TYPE_LIST = (
    ('右边', '右边'),
    ('两边', '两边'),
)
# 裤脚（西裤）
class KuJiaoXiKu(ClothParam):
    class Meta:
        verbose_name = '裤脚（西裤）'
        verbose_name_plural = '裤脚（西裤）'

KUJIAO_TYPE_LIST = (
    ('内折边', '内折边'),
    ('外翻边', '外翻边'),
)
# 马甲领型
class MaJiaLingXing(ClothParam):
    class Meta:
        verbose_name = '马甲领型'
        verbose_name_plural = '马甲领型'

MAJIA_LINGXING_TYPE_LIST = (
    ('V领', 'V领'),
    ('U领', 'U领'),
)
# 马甲 扣型
class MaJiaKouXing(ClothParam):
    class Meta:
        verbose_name = '马甲扣型'
        verbose_name_plural = '马甲扣型'

MAJIA_KOUXING_TYPE_LIST = (
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('4*2', '4*2'),
    ('6*3', '6*3'),
    ('8*4', '8*4'),
)

# 定制个性化设置. 如果某个个性化参数根据产品有所不同，就在产品字段填写对应产品名称和类型
class OrderPersonalization(ClothParam):
    product_type = models.CharField(max_length=10, blank=True, null=True, default='shirt', choices=PRODUCT_TYPE_LIST, verbose_name='对应产品类型')
    product_name = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='对应产品名称')
    class Meta:
        verbose_name = '定制个性化'
        verbose_name_plural = '定制个性化'

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

# 领型（衬衫）
class LingXingChenShan(ClothParam):
    class Meta:
        verbose_name = '领型（衬衫）'
        verbose_name_plural = '领型（衬衫）'

CHENSHAN_LINGXING_TYPE_LIST = (
    ('标准', '标准'),
    ('八字', '八字'),
    ('一字', '一字'),
    ('领尖扣领', '领尖扣领'),
    ('小方领', '小方领'),
    ('礼服领', '礼服领'),
    
)

# 袖口（衬衫）
class XiuKouChenShan(ClothParam):
    class Meta:
        verbose_name = '袖口（衬衫）'
        verbose_name_plural = '袖口（衬衫）'

CHENSHAN_XIUKOU_TYPE_LIST = (
    ('2粒直角', '2粒直角'),
    ('2粒斜角', '2粒斜角'),
    ('2粒圆角', '2粒圆角'),
    ('法式直角', '法式直角'),
    ('法式斜角', '法式斜角'),
    ('法式圆角', '法式圆角'),
)

# 下摆（衬衫）
class XiaBaiChenShan(ClothParam):
    class Meta:
        verbose_name = '下摆（衬衫）'
        verbose_name_plural = '下摆（衬衫）'

CHENSHAN_XIABAI_TYPE_LIST = (
    ('直下摆', '直下摆'),
    ('小圆下摆', '小圆下摆'),
    ('大圆下摆', '大圆下摆'),
)

# 门襟（衬衫）
class MenJinChenShan(ClothParam):
    class Meta:
        verbose_name = '门襟（衬衫）'
        verbose_name_plural = '门襟（衬衫）'

CHENSHAN_MENJIN_TYPE_LIST = (
    ('明门襟', '明门襟'),
    ('暗门襟', '暗门襟'),
    ('平门襟', '平门襟'),
)

# 后背（衬衫）
class HouBeiChenShan(ClothParam):
    class Meta:
        verbose_name = '后背（衬衫）'
        verbose_name_plural = '后背（衬衫）'

CHENSHAN_HOUBEI_TYPE_LIST = (
    ('肩部双褶', '肩部双褶'),
    ('后背工字褶', '后背工字褶'),
    ('腰部双褶', '腰部双褶'),
    ('后背无', '后背无'),
)

# 口袋（衬衫）
class KouDaiChenShan(ClothParam):
    class Meta:
        verbose_name = '口袋（衬衫）'
        verbose_name_plural = '口袋（衬衫）'

CHENSHAN_KOUDAI_TYPE_LIST = (
    ('无口袋', '无口袋'),
    ('园口袋', '园口袋'),
    ('六角口袋', '六角口袋'),
    ('尖口袋', '尖口袋'),
)


#微信支付记录
class Wxpay(models.Model):
    wxpay_id = models.CharField(max_length=128, blank=True, null=True, verbose_name='微信支付订单号')
    out_trade_no = models.CharField(max_length=128, blank=True, null=True, verbose_name='商户订单号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    result_code = models.CharField(max_length=16, blank=True, null=True, verbose_name='业务结果')
    return_code = models.CharField(max_length=16, blank=True, null=True, verbose_name='返回状态码')
    openid = models.CharField(max_length=32, default='', verbose_name='微信用户标识')
    total_fee = models.FloatField(blank=True, null=True, default=0, verbose_name='总金额') 
    trade_type = models.CharField(max_length=16, blank=True, null=True, verbose_name='交易类型')
    bank_type = models.CharField(max_length=16, blank=True, null=True, verbose_name='付款银行')
    appid = models.CharField(max_length=32, blank=True, null=True, verbose_name='公众账号')
    mch_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='商户号')
    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '微信支付记录'
        verbose_name_plural = '微信支付记录'


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True)
    wxpay = models.ForeignKey(Wxpay, blank=True, null=True, verbose_name='微信支付记录')
    product = models.ForeignKey(Product, verbose_name='产品', blank=True)
    price = models.FloatField(blank=True, null=True, default=0, verbose_name='价格') 
    is4friend = models.BooleanField(default=False, verbose_name='是否为重视的人定制')
    friend_phone = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='朋友电话')
    fabric = models.ForeignKey(Fabric, blank=True, null=True, verbose_name='面料')
    address = models.ForeignKey(Address4Order, blank=True, null=True, verbose_name='地址')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

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
    
    # 个性化
    add_kuzi = models.BooleanField(default=False, verbose_name='是否单加裤子')
    add_majia = models.BooleanField(default=False, verbose_name='是否单加马甲')
    majia_lingxing = models.CharField(max_length=16, blank=True, null=True, default='', choices=MAJIA_LINGXING_TYPE_LIST, verbose_name='马甲领型')
    majia_kouxing = models.CharField(max_length=16, blank=True, null=True, default='', choices=MAJIA_KOUXING_TYPE_LIST, verbose_name='马甲扣型')
    add_bespoke = models.BooleanField(default=False, verbose_name='是否Bespoke')
    add_xiuzi = models.BooleanField(default=False, verbose_name='是否绣字')
    xiuzi = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='绣字')
    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车'


# 订单详情
# PS：为了兼容以后各种参数的修改，订单中直接保存参数的名称; 多选用  ‘|’ 线分割
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True)
    wxpay = models.ForeignKey(Wxpay, blank=True, null=True, verbose_name='微信支付记录')
    #user_id = models.IntegerField(max_length=11, blank=True, null=True, default=0, verbose_name='用户id')
    order_number = models.CharField(max_length=128, blank=True, null=True, verbose_name='订单号')
    product = models.ForeignKey(Product, verbose_name='产品', blank=True)
    order_status = models.CharField(max_length=10, verbose_name='订单状态', blank=True, null=True, choices=ORDER_STATUS_TYPE_LIST)
    #Plant_status = models.CharField(max_length=10, verbose_name='工厂状态', blank=True, null=True, choices=PLANT_STATUS_TYPE_LIST)
    price = models.FloatField(blank=True, null=True, default=0, verbose_name='价格') 
    #measure_reservation = models.ForeignKey(MeasureReservation, blank=True, null=True, verbose_name='预约量体')
    is4friend = models.BooleanField(default=False, verbose_name='是否为重视的人定制')
    friend_phone = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='朋友电话')
#    fabric = models.ForeignKey(Fabric, blank=True, null=True, verbose_name='面料')
    fabric = models.CharField(max_length=128, blank=True, null=True, verbose_name='面料')
    address = models.ForeignKey(Address4Order, blank=True, null=True, verbose_name='地址')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

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
    
    # 个性化
    add_kuzi = models.BooleanField(default=False, verbose_name='是否单加裤子')
    add_majia = models.BooleanField(default=False, verbose_name='是否单加马甲')
    majia_lingxing = models.CharField(max_length=16, blank=True, null=True, default='', choices=MAJIA_LINGXING_TYPE_LIST, verbose_name='马甲领型')
    majia_kouxing = models.CharField(max_length=16, blank=True, null=True, default='', choices=MAJIA_KOUXING_TYPE_LIST, verbose_name='马甲扣型')
    add_bespoke = models.BooleanField(default=False, verbose_name='是否Bespoke')
    add_xiuzi = models.BooleanField(default=False, verbose_name='是否绣字')
    xiuzi = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='绣字')
    beizhu = models.CharField(max_length=256, blank=True, null=True, default='', verbose_name='订单备注')
    huifang = models.CharField(max_length=256, blank=True, null=True, default='', verbose_name='回访结果')
    xdy = models.CharField(max_length=256, blank=True, null=True, default='', verbose_name='下单员')
    def __unicode__(self):
        return '{0:012d}'.format(self.id)
    def info(self):
        return '<p id="user_name"><font color="#FF0000">请点击上面搜索按钮，选择要创建订单的用户。完成后在此处显示名字和手机号码</font></p>'
    def addressinfo(self):
        return '<p id="address_name"><font color="#FF0000">请点击上面搜索按钮，选择要创建订单的地址。完成后在此处显示地址详情</font></p>'
    info.allow_tags = True
    addressinfo.allow_tags = True
       
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
    #def product(self):
        #return Product.objects.get(id=self.product_id)



class OrderResource(resources.ModelResource):
    
    class Meta:
        model = Order


#工单状态变更表
class Plant_update(models.Model):
    order = models.ForeignKey(Order, verbose_name='订单')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    zhizuo_time = models.DateTimeField(blank=True, null=True,  verbose_name='制作时间')
    wancheng_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    peishong_time = models.DateTimeField(blank=True, null=True, verbose_name='配送时间')
    jiaofu_time = models.DateTimeField(blank=True, null=True, verbose_name='交付时间')
    plant_status = models.CharField(max_length=32, default='', verbose_name='工单状态')
    issue = models.CharField(max_length=256,blank=True, null=True, default='', verbose_name='问题反馈')
    gh = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name='工号')

    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '工单状态'
        verbose_name_plural = '工单状态'

Worktime_TYPE_LIST = (
    ('A', '工作时间'),
    ('B', '特殊日期'),
)
   
Time_TYPE_LIST = (
    ('0:00', '0:00'),('0:30', '0:30'),('1:00', '1:00'),('1:30', '1:30'),('2:00', '2:00'),('2:30', '2:30'),
    ('3:00', '3:00'),('3:30', '3:30'),('4:00', '4:00'),('4:30', '4:30'),('5:00', '5:00'),('5:30', '5:30'),
    ('6:00', '6:00'),('6:30', '6:30'),('7:00', '7:00'),('7:30', '7:30'),('8:00', '8:00'),('8:30', '8:30'),
    ('9:00', '9:00'),('9:30', '9:30'),('10:00', '10:00'),('10:30', '10:30'),('11:00', '11:00'),('11:30', '11:30'),
    ('12:00', '12:00'),('12:30', '12:30'),('13:00', '13:00'),('13:30', '13:30'),('14:00', '14:00'),('14:30', '14:30'),
    ('15:00', '15:00'),('15:30', '15:30'),('16:00', '16:00'),('16:30', '16:30'),('17:00', '17:00'),('17:30', '17:30'),
    ('18:00', '18:00'),('18:30', '18:30'),('19:00', '19:00'),('19:30', '19:30'),('20:00', '20:00'),('20:30', '20:30'),
    ('21:00', '21:00'),('21:30', '21:30'),('22:00', '22:00'),('22:30', '22:30'),('23:00', '23:00'),('23:30', '23:30'),
)     
        
#展示图
class Banner(models.Model):
    name = models.CharField(max_length=256, default='', verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    product = models.ForeignKey(Product, verbose_name='所属产品', blank=True, null=True)
    img = models.ImageField(upload_to=get_uploadto_path,blank=True, null=True, verbose_name='展示图')
    type = models.CharField(max_length=10, blank=True, null=True, default='', verbose_name='展示图类型')
    img_href = models.CharField(max_length=256,blank=True, null=True, default='', verbose_name='外部超链接')
    
    
    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '展示图'
        verbose_name_plural = '展示图'


#预约时间限制
class Worktime(models.Model):
    name = models.CharField(max_length=256, default='', verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    type = models.CharField(max_length=10, blank=True, null=True, default='A',choices=Worktime_TYPE_LIST, verbose_name='类型')
    start_time = models.CharField(max_length=10,blank=True, null=True, default='0:00', choices=Time_TYPE_LIST,verbose_name='开始时间')
    end_time = models.CharField(max_length=10,blank=True, null=True, default='0:00', choices=Time_TYPE_LIST,verbose_name='结束时间')
    start_day = models.DateTimeField(blank=True, null=True, verbose_name='开始日期')
    end_day = models.DateTimeField(blank=True, null=True, verbose_name='结束日期')
    
    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '预约时间限制'
        verbose_name_plural = '预约时间限制'
        

Redpacket_TYPE_LIST = (
    ('A', '抽取红包'),
    ('B', '转发红包'),
)


#微信红包
class Redpacket(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True, null=True)
    openid = models.CharField(max_length=256, default='', verbose_name='微信标识号')
    phonenumber = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='电话')
    nickname = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name='微信昵称')
    headimgurl = models.CharField(max_length=500, blank=True, null=True, verbose_name='微信头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    money = models.IntegerField(max_length=8, blank=True, null=True, default=0, verbose_name='金额')
    #iscoupon = models.CharField(max_length=2, blank=False, null=False, default='0', choices=USED_TYPE_LIST, verbose_name='是否转优惠券')
    #couponid = models.IntegerField(max_length=11, blank=True, null=True, default=0, verbose_name='已转优惠券id')
    type = models.CharField(max_length=10, blank=True, null=True, default='',choices=Redpacket_TYPE_LIST, verbose_name='红包类型')
    end_day = models.DateTimeField(blank=True, null=True, verbose_name='失效日期')
    
    def __unicode__(self):
        return format(self.id)
    class Meta:
        verbose_name = '微信红包'
        verbose_name_plural = '微信红包'




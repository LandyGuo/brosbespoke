#coding:utf8
from django.contrib import admin
from models import *
from PIL import Image
import glob, os
from wap.models import Product
import logging


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(__debug__)
    return logger

logging.basicConfig(level=logging.DEBUG)


def thumbnail(size,img_url):
    get_logger().debug('----------ataset.1----:%s',size)
    for infile in glob.glob('.'+ img_url):
        get_logger().debug('----------ataset.infile----:%s',infile)
        file, ext = os.path.splitext(infile)
        file_thumbnail, ext_thumbnail = os.path.splitext(img_url)
        im = Image.open(infile)
        width, height = im.size
        if width == height:
            region = im
        else:
            if width > height:
                delta = (width - height)/2
                box = (delta, 0, delta+height, height)
            else:
                delta = (height - width)/2
                box = (0, delta, width, delta+width)
            region = im.crop(box)
        region.thumbnail(size)
        thumbnail_url = file_thumbnail + '_thumbnail' +  ".jpg"
        region.save( file + '_thumbnail' +  ".jpg", "JPEG")
        get_logger().debug('----------ataset.thumbnail----:%s',thumbnail_url)
        return thumbnail_url


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'categorie']
    filter_horizontal = ('fabric_web',)
    exclude = ('img_thumbnail','img2_thumbnail','img3_thumbnail','img4_thumbnail','img5_thumbnail','img6_thumbnail')
    def save_model(self, request, obj, form, change):
        obj.save()
        url = obj.img.url
        url2 = obj.img2.url
        url3 = obj.img3.url
        url4 = obj.img4.url
        url5 = obj.img5.url
        url6 = obj.img6.url
        sizes = 72, 72
        obj.img_thumbnail = thumbnail(sizes, str(url))
        obj.img2_thumbnail = thumbnail(sizes, str(url2))
        obj.img3_thumbnail = thumbnail(sizes, str(url3))
        obj.img4_thumbnail = thumbnail(sizes, str(url4))
        obj.img5_thumbnail = thumbnail(sizes, str(url5))
        obj.img6_thumbnail = thumbnail(sizes, str(url6))
        get_logger().debug('----------ataset.img4_thumbnail----:%s',obj.img4_thumbnail)
        obj.save()


class MenuAdmin(admin.ModelAdmin):
    filter_horizontal = ('submenu',)

class Fabric_webAdmin(admin.ModelAdmin):
    exclude = ('thumbnail_url',)
    def save_model(self, request, obj, form, change):
        obj.save()
        url = obj.image_url.url
        sizes = 72, 72
        obj.thumbnail_url = thumbnail(sizes, str(url))
        get_logger().debug('----------ataset.obj.thumbnail_url----:%s',obj.thumbnail_url)
        obj.save()

class SubmenuAdmin(admin.ModelAdmin):
    filter_horizontal = ('secondarymenu',)

admin.site.register(Menu, MenuAdmin)
admin.site.register(Submenu, SubmenuAdmin)
admin.site.register(Focus)
admin.site.register(Categorie)
admin.site.register(Product_web, ProductAdmin)
#admin.site.register(Product_web)
admin.site.register(Poster)
admin.site.register(Fabric_web, Fabric_webAdmin)
admin.site.register(Cart_web)
admin.site.register(Brand_fabric)
admin.site.register(Secondarymenu)
admin.site.register(Footer)
admin.site.register(Journal)
from django.contrib import admin
from models import *

class DataAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'content']
    search_fields = ['keyword']

class AppItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_weixin_api']
class AppUserAdmin(admin.ModelAdmin):
    search_fields = ['nickname']
    list_display = ['nickname', 'openid']

admin.site.register(WXUser, AppUserAdmin)
admin.site.register(WXConfig, AppItemAdmin)
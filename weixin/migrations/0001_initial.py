# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WXConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('slug', models.CharField(max_length=128, null=True, verbose_name=b'app\xe5\x90\x8d\xe7\xa7\xb0,\xe5\x94\xaf\xe4\xb8\x80', blank=True)),
                ('domain', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x85\xa8\xe5\x9f\x9f\xe5\x90\x8d(\xe4\xb8\x8d\xe5\x8c\x85\xe5\x90\xabhttp://)', blank=True)),
                ('appid', models.CharField(max_length=128, null=True, verbose_name=b'APPID', blank=True)),
                ('app_secret', models.CharField(max_length=128, null=True, verbose_name=b'APP_SECRET', blank=True)),
                ('token_cache_key', models.CharField(default=b'shixiongdeyigui_access_token', max_length=128, null=True, verbose_name=b'\xe7\xbc\x93\xe5\xad\x98token\xe7\x9a\x84key', blank=True)),
                ('is_valid', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\xaa\x8c\xe8\xaf\x81')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u5fae\u4fe1\u8bbe\u7f6e',
                'verbose_name_plural': '\u5fae\u4fe1\u8bbe\u7f6e',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WXUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=128, null=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe6\xa0\x87\xe8\xaf\x86', blank=True)),
                ('nickname', models.CharField(max_length=128, null=True, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0', blank=True)),
                ('sex', models.IntegerField(max_length=2, null=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', blank=True)),
                ('city', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x9f\x8e\xe5\xb8\x82', blank=True)),
                ('province', models.CharField(max_length=128, null=True, verbose_name=b'\xe7\x9c\x81\xe4\xbb\xbd', blank=True)),
                ('country', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x9b\xbd\xe5\xae\xb6', blank=True)),
                ('language', models.CharField(max_length=128, null=True, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe8\xaf\xad\xe8\xa8\x80', blank=True)),
                ('headimgurl', models.CharField(max_length=500, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f', blank=True)),
            ],
            options={
                'verbose_name': '\u5173\u6ce8\u5fae\u4fe1\u7528\u6237',
                'verbose_name_plural': '\u5173\u6ce8\u5fae\u4fe1\u7528\u6237',
            },
            bases=(models.Model,),
        ),
    ]

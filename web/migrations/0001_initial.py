# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('wap', '0002_auto_20150619_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart_web',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(default=0, null=True, verbose_name=b'\xe4\xbb\xb7\xe6\xa0\xbc', blank=True)),
                ('is4friend', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe9\x87\x8d\xe8\xa7\x86\xe7\x9a\x84\xe4\xba\xba\xe5\xae\x9a\xe5\x88\xb6')),
                ('friend_phone', models.CharField(default=b'', max_length=16, null=True, verbose_name=b'\xe6\x9c\x8b\xe5\x8f\x8b\xe7\x94\xb5\xe8\xaf\x9d', blank=True)),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('add_bespoke', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6Bespoke')),
                ('add_xiuzi', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe7\xbb\xa3\xe5\xad\x97')),
                ('xiuzi', models.CharField(default=b'', max_length=16, null=True, verbose_name=b'\xe7\xbb\xa3\xe5\xad\x97', blank=True)),
            ],
            options={
                'verbose_name': '\u8d2d\u7269\u8f66',
                'verbose_name_plural': '\u8d2d\u7269\u8f66',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fabric_web',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('brand', models.CharField(blank=True, max_length=64, null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\x93\x81\xe7\x89\x8c', choices=[(b'BB NATSUN', b'BB NATSUN'), (b'BB VBC', b'BB VBC'), (b'BB Scaball', b'BB Scaball'), (b'BB Smart', b'BB Smart'), (b'BB Star', b'BB Star')])),
                ('volume', models.FloatField(max_length=64, null=True, verbose_name=b'\xe6\x95\xb0\xe9\x87\x8f', blank=True)),
                ('thumbnail_url', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('image_url', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\xa4\xa7\xe5\x9b\xbe', blank=True)),
                ('content', models.TextField(null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('price', models.IntegerField(max_length=11, null=True, verbose_name=b'\xe4\xbb\xb7\xe6\xa0\xbc', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u9762\u6599\u4fe1\u606f',
                'verbose_name_plural': '\u9762\u6599\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Focus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('img', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe5\xb1\x95\xe7\xa4\xba\xe5\x9b\xbe', blank=True)),
                ('img_href', models.CharField(default=b'', max_length=256, null=True, verbose_name=b'\xe5\xa4\x96\xe9\x83\xa8\xe8\xb6\x85\xe9\x93\xbe\xe6\x8e\xa5', blank=True)),
            ],
            options={
                'verbose_name': '\u9996\u9875\u7126\u70b9\u56fe',
                'verbose_name_plural': '\u9996\u9875\u7126\u70b9\u56fe',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('mingzi', models.CharField(max_length=32, null=True, verbose_name=b'\xe8\x8b\xb1\xe6\x96\x87\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u83dc\u5355',
                'verbose_name_plural': '\u83dc\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('img', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe5\xb1\x95\xe7\xa4\xba\xe5\x9b\xbe', blank=True)),
                ('img_href', models.CharField(default=b'', max_length=256, null=True, verbose_name=b'\xe5\xa4\x96\xe9\x83\xa8\xe8\xb6\x85\xe9\x93\xbe\xe6\x8e\xa5', blank=True)),
            ],
            options={
                'verbose_name': '\u9996\u9875\u6d77\u62a5',
                'verbose_name_plural': '\u9996\u9875\u6d77\u62a5',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product_web',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, null=True, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', blank=True)),
                ('subtitle', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x89\xaf\xe6\xa0\x87\xe9\xa2\x98', blank=True)),
                ('introduction', models.TextField(null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe4\xbb\x8b\xe7\xbb\x8d\xef\xbc\x8c|\xe5\x88\x86\xe5\x89\xb2', blank=True)),
                ('size_description', models.TextField(null=True, verbose_name=b'\xe5\xb0\xba\xe5\xaf\xb8\xe8\xaf\xb4\xe6\x98\x8e\xef\xbc\x8c|\xe5\x88\x86\xe5\x89\xb2', blank=True)),
                ('craft_description', models.TextField(null=True, verbose_name=b'\xe5\xb7\xa5\xe8\x89\xba\xe7\xbb\x86\xe8\x8a\x82\xef\xbc\x8c|\xe5\x88\x86\xe5\x89\xb2', blank=True)),
                ('custom_description', models.TextField(null=True, verbose_name=b'\xe5\xae\x9a\xe5\x88\xb6\xe8\xaf\xb4\xe6\x98\x8e\xe4\xb8\x8e\xe5\x8f\x91\xe8\xb4\xa7\xef\xbc\x8c|\xe5\x88\x86\xe5\x89\xb2', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('type', models.CharField(default=b'shirt', max_length=10, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'suit', b'\xe8\xa5\xbf\xe6\x9c\x8d'), (b'shirt', b'\xe8\xa1\xac\xe8\xa1\xab')])),
                ('img', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xb8\x80', blank=True)),
                ('img_thumbnail', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xb8\x80\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('img2', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xba\x8c', blank=True)),
                ('img2_thumbnail', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xba\x8c\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('img3', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xb8\x89', blank=True)),
                ('img3_thumbnail', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xb8\x89\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('img4', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe5\x9b\x9b', blank=True)),
                ('img4_thumbnail', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe5\x9b\x9b\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('img5', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xba\x94', blank=True)),
                ('img5_thumbnail', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe4\xba\x94\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('img6', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe5\x85\xad', blank=True)),
                ('img6_thumbnail', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe5\x9b\xbe\xe7\x89\x87\xe5\x85\xad\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True)),
                ('kouxing_sy', models.CharField(default=b'', choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'2*1', b'2*1'), (b'4*2', b'4*2'), (b'6*2', b'6*2')], max_length=16, blank=True, null=True, verbose_name=b'\xe6\x89\xa3\xe5\x9e\x8b\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('lingxing_sy', models.CharField(default=b'', choices=[(b'\xe5\xb9\xb3\xe9\xa9\xb3\xe5\xa4\xb4', b'\xe5\xb9\xb3\xe9\xa9\xb3\xe5\xa4\xb4'), (b'\xe6\x9e\xaa\xe9\xa9\xb3\xe5\xa4\xb4', b'\xe6\x9e\xaa\xe9\xa9\xb3\xe5\xa4\xb4'), (b'\xe7\xa4\xbc\xe6\x9c\x8d\xe9\xa2\x86', b'\xe7\xa4\xbc\xe6\x9c\x8d\xe9\xa2\x86')], max_length=16, blank=True, null=True, verbose_name=b'\xe9\xa2\x86\xe5\x9e\x8b\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('yaodou_sy', models.CharField(default=b'', choices=[(b'\xe6\x99\xae\xe9\x80\x9a', b'\xe6\x99\xae\xe9\x80\x9a'), (b'\xe6\x96\x9c\xe5\x85\x9c', b'\xe6\x96\x9c\xe5\x85\x9c'), (b'\xe5\x8f\x8c\xe7\x89\x99\xe5\x85\x9c', b'\xe5\x8f\x8c\xe7\x89\x99\xe5\x85\x9c')], max_length=16, blank=True, null=True, verbose_name=b'\xe8\x85\xb0\xe5\x85\x9c\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('kaiqi_sy', models.CharField(default=b'', choices=[(b'\xe5\x90\x8e\xe5\xbc\x80\xe6\xb0\x94', b'\xe5\x90\x8e\xe5\xbc\x80\xe6\xb0\x94'), (b'\xe4\xbe\xa7\xe5\xbc\x80\xe6\xb0\x94', b'\xe4\xbe\xa7\xe5\xbc\x80\xe6\xb0\x94'), (b'\xe6\x97\xa0', b'\xe6\x97\xa0')], max_length=16, blank=True, null=True, verbose_name=b'\xe5\xbc\x80\xe6\xb0\x94\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('xiukou_sy', models.CharField(default=b'', choices=[(b'3', b'3'), (b'4', b'4')], max_length=16, blank=True, null=True, verbose_name=b'\xe8\xa2\x96\xe6\x89\xa3\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('neibuzaoxing_sy', models.CharField(default=b'', choices=[(b'\xe6\x97\xb6\xe5\xb0\x9a\xe6\xac\xbe', b'\xe6\x97\xb6\xe5\xb0\x9a\xe6\xac\xbe'), (b'\xe4\xbc\xa0\xe7\xbb\x9f\xe6\xac\xbe', b'\xe4\xbc\xa0\xe7\xbb\x9f\xe6\xac\xbe')], max_length=16, blank=True, null=True, verbose_name=b'\xe5\x86\x85\xe9\x83\xa8\xe9\x80\xa0\xe5\x9e\x8b\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('neibudou_sy', models.CharField(default=b'', choices=[(b'\xe9\x87\x8c\xe5\x85\x9c', b'\xe9\x87\x8c\xe5\x85\x9c'), (b'\xe7\xac\x94\xe5\x85\x9c', b'\xe7\xac\x94\xe5\x85\x9c'), (b'\xe7\x83\x9f\xe5\x85\x9c', b'\xe7\x83\x9f\xe5\x85\x9c'), (b'\xe9\x87\x8c\xe5\x85\x9c|\xe7\xac\x94\xe5\x85\x9c', b'\xe9\x87\x8c\xe5\x85\x9c|\xe7\xac\x94\xe5\x85\x9c'), (b'\xe9\x87\x8c\xe5\x85\x9c|\xe7\x83\x9f\xe5\x85\x9c', b'\xe9\x87\x8c\xe5\x85\x9c|\xe7\x83\x9f\xe5\x85\x9c'), (b'\xe7\xac\x94\xe5\x85\x9c|\xe7\x83\x9f\xe5\x85\x9c', b'\xe7\xac\x94\xe5\x85\x9c|\xe7\x83\x9f\xe5\x85\x9c'), (b'\xe9\x87\x8c\xe5\x85\x9c|\xe7\xac\x94\xe5\x85\x9c|\xe7\x83\x9f\xe5\x85\x9c', b'\xe9\x87\x8c\xe5\x85\x9c|\xe7\xac\x94\xe5\x85\x9c|\xe7\x83\x9f\xe5\x85\x9c')], max_length=16, blank=True, null=True, verbose_name=b'\xe5\x86\x85\xe9\x83\xa8\xe5\x85\x9c( \xe5\xa4\x9a\xe9\x80\x89\xe7\x94\xa8  \xe2\x80\x98|\xe2\x80\x99 \xe7\xba\xbf\xe5\x88\x86\xe5\x89\xb2)\xef\xbc\x88\xe4\xb8\x8a\xe8\xa1\xa3\xef\xbc\x89')),
                ('kuzhe_xk', models.CharField(default=b'', choices=[(b'\xe6\x97\xa0\xe8\xa4\xb6', b'\xe6\x97\xa0\xe8\xa4\xb6'), (b'\xe5\x8d\x95\xe8\xa4\xb6', b'\xe5\x8d\x95\xe8\xa4\xb6'), (b'\xe5\x8f\x8c\xe8\xa4\xb6', b'\xe5\x8f\x8c\xe8\xa4\xb6')], max_length=16, blank=True, null=True, verbose_name=b'\xe8\xa3\xa4\xe8\xa4\xb6\xef\xbc\x88\xe8\xa5\xbf\xe8\xa3\xa4\xef\xbc\x89')),
                ('houdou_xk', models.CharField(default=b'', choices=[(b'\xe5\x8f\xb3\xe8\xbe\xb9', b'\xe5\x8f\xb3\xe8\xbe\xb9'), (b'\xe4\xb8\xa4\xe8\xbe\xb9', b'\xe4\xb8\xa4\xe8\xbe\xb9')], max_length=16, blank=True, null=True, verbose_name=b'\xe5\x90\x8e\xe5\x85\x9c\xef\xbc\x88\xe8\xa5\xbf\xe8\xa3\xa4\xef\xbc\x89')),
                ('kujiao_xk', models.CharField(default=b'', choices=[(b'\xe5\x86\x85\xe6\x8a\x98\xe8\xbe\xb9', b'\xe5\x86\x85\xe6\x8a\x98\xe8\xbe\xb9'), (b'\xe5\xa4\x96\xe7\xbf\xbb\xe8\xbe\xb9', b'\xe5\xa4\x96\xe7\xbf\xbb\xe8\xbe\xb9')], max_length=16, blank=True, null=True, verbose_name=b'\xe8\xa3\xa4\xe8\x84\x9a\xef\xbc\x88\xe8\xa5\xbf\xe8\xa3\xa4\xef\xbc\x89')),
                ('lingxing_cs', models.CharField(default=b'', choices=[(b'\xe6\xa0\x87\xe5\x87\x86', b'\xe6\xa0\x87\xe5\x87\x86'), (b'\xe5\x85\xab\xe5\xad\x97', b'\xe5\x85\xab\xe5\xad\x97'), (b'\xe4\xb8\x80\xe5\xad\x97', b'\xe4\xb8\x80\xe5\xad\x97'), (b'\xe9\xa2\x86\xe5\xb0\x96\xe6\x89\xa3\xe9\xa2\x86', b'\xe9\xa2\x86\xe5\xb0\x96\xe6\x89\xa3\xe9\xa2\x86'), (b'\xe5\xb0\x8f\xe6\x96\xb9\xe9\xa2\x86', b'\xe5\xb0\x8f\xe6\x96\xb9\xe9\xa2\x86'), (b'\xe7\xa4\xbc\xe6\x9c\x8d\xe9\xa2\x86', b'\xe7\xa4\xbc\xe6\x9c\x8d\xe9\xa2\x86')], max_length=16, blank=True, null=True, verbose_name=b'\xe9\xa2\x86\xe5\x9e\x8b\xef\xbc\x88\xe8\xa1\xac\xe8\xa1\xab\xef\xbc\x89')),
                ('xiukou_cs', models.CharField(default=b'', choices=[(b'2\xe7\xb2\x92\xe7\x9b\xb4\xe8\xa7\x92', b'2\xe7\xb2\x92\xe7\x9b\xb4\xe8\xa7\x92'), (b'2\xe7\xb2\x92\xe6\x96\x9c\xe8\xa7\x92', b'2\xe7\xb2\x92\xe6\x96\x9c\xe8\xa7\x92'), (b'2\xe7\xb2\x92\xe5\x9c\x86\xe8\xa7\x92', b'2\xe7\xb2\x92\xe5\x9c\x86\xe8\xa7\x92'), (b'\xe6\xb3\x95\xe5\xbc\x8f\xe7\x9b\xb4\xe8\xa7\x92', b'\xe6\xb3\x95\xe5\xbc\x8f\xe7\x9b\xb4\xe8\xa7\x92'), (b'\xe6\xb3\x95\xe5\xbc\x8f\xe6\x96\x9c\xe8\xa7\x92', b'\xe6\xb3\x95\xe5\xbc\x8f\xe6\x96\x9c\xe8\xa7\x92'), (b'\xe6\xb3\x95\xe5\xbc\x8f\xe5\x9c\x86\xe8\xa7\x92', b'\xe6\xb3\x95\xe5\xbc\x8f\xe5\x9c\x86\xe8\xa7\x92')], max_length=16, blank=True, null=True, verbose_name=b'\xe8\xa2\x96\xe5\x8f\xa3\xef\xbc\x88\xe8\xa1\xac\xe8\xa1\xab\xef\xbc\x89')),
                ('xiabai_cs', models.CharField(default=b'', choices=[(b'\xe7\x9b\xb4\xe4\xb8\x8b\xe6\x91\x86', b'\xe7\x9b\xb4\xe4\xb8\x8b\xe6\x91\x86'), (b'\xe5\xb0\x8f\xe5\x9c\x86\xe4\xb8\x8b\xe6\x91\x86', b'\xe5\xb0\x8f\xe5\x9c\x86\xe4\xb8\x8b\xe6\x91\x86'), (b'\xe5\xa4\xa7\xe5\x9c\x86\xe4\xb8\x8b\xe6\x91\x86', b'\xe5\xa4\xa7\xe5\x9c\x86\xe4\xb8\x8b\xe6\x91\x86')], max_length=16, blank=True, null=True, verbose_name=b'\xe4\xb8\x8b\xe6\x91\x86\xef\xbc\x88\xe8\xa1\xac\xe8\xa1\xab\xef\xbc\x89')),
                ('menjin_cs', models.CharField(default=b'', choices=[(b'\xe6\x98\x8e\xe9\x97\xa8\xe8\xa5\x9f', b'\xe6\x98\x8e\xe9\x97\xa8\xe8\xa5\x9f'), (b'\xe6\x9a\x97\xe9\x97\xa8\xe8\xa5\x9f', b'\xe6\x9a\x97\xe9\x97\xa8\xe8\xa5\x9f'), (b'\xe5\xb9\xb3\xe9\x97\xa8\xe8\xa5\x9f', b'\xe5\xb9\xb3\xe9\x97\xa8\xe8\xa5\x9f')], max_length=16, blank=True, null=True, verbose_name=b'\xe9\x97\xa8\xe8\xa5\x9f\xef\xbc\x88\xe8\xa1\xac\xe8\xa1\xab\xef\xbc\x89')),
                ('houbei_cs', models.CharField(default=b'', choices=[(b'\xe8\x82\xa9\xe9\x83\xa8\xe5\x8f\x8c\xe8\xa4\xb6', b'\xe8\x82\xa9\xe9\x83\xa8\xe5\x8f\x8c\xe8\xa4\xb6'), (b'\xe5\x90\x8e\xe8\x83\x8c\xe5\xb7\xa5\xe5\xad\x97\xe8\xa4\xb6', b'\xe5\x90\x8e\xe8\x83\x8c\xe5\xb7\xa5\xe5\xad\x97\xe8\xa4\xb6'), (b'\xe8\x85\xb0\xe9\x83\xa8\xe5\x8f\x8c\xe8\xa4\xb6', b'\xe8\x85\xb0\xe9\x83\xa8\xe5\x8f\x8c\xe8\xa4\xb6'), (b'\xe5\x90\x8e\xe8\x83\x8c\xe6\x97\xa0', b'\xe5\x90\x8e\xe8\x83\x8c\xe6\x97\xa0')], max_length=16, blank=True, null=True, verbose_name=b'\xe5\x90\x8e\xe8\x83\x8c\xef\xbc\x88\xe8\xa1\xac\xe8\xa1\xab\xef\xbc\x89')),
                ('koudai_cs', models.CharField(default=b'', choices=[(b'\xe6\x97\xa0\xe5\x8f\xa3\xe8\xa2\x8b', b'\xe6\x97\xa0\xe5\x8f\xa3\xe8\xa2\x8b'), (b'\xe5\x9b\xad\xe5\x8f\xa3\xe8\xa2\x8b', b'\xe5\x9b\xad\xe5\x8f\xa3\xe8\xa2\x8b'), (b'\xe5\x85\xad\xe8\xa7\x92\xe5\x8f\xa3\xe8\xa2\x8b', b'\xe5\x85\xad\xe8\xa7\x92\xe5\x8f\xa3\xe8\xa2\x8b'), (b'\xe5\xb0\x96\xe5\x8f\xa3\xe8\xa2\x8b', b'\xe5\xb0\x96\xe5\x8f\xa3\xe8\xa2\x8b')], max_length=16, blank=True, null=True, verbose_name=b'\xe5\x8f\xa3\xe8\xa2\x8b\xef\xbc\x88\xe8\xa1\xac\xe8\xa1\xab\xef\xbc\x89')),
                ('categorie', models.ForeignKey(verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', blank=True, to='web.Categorie', null=True)),
                ('fabric_web', models.ManyToManyField(related_name='fabric_web', null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99', to='web.Fabric_web', blank=True)),
                ('fabric_web_default', models.ForeignKey(related_name='fabric_web_default', verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe9\x9d\xa2\xe6\x96\x99', blank=True, to='web.Fabric_web', null=True)),
                ('menu', models.ForeignKey(verbose_name=b'\xe8\x8f\x9c\xe5\x8d\x95', blank=True, to='web.Menu', null=True)),
            ],
            options={
                'verbose_name': '\u4ea7\u54c1(\u7f51\u7ad9)',
                'verbose_name_plural': '\u4ea7\u54c1(\u7f51\u7ad9)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u5b50\u83dc\u5355',
                'verbose_name_plural': '\u5b50\u83dc\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product_web',
            name='submenu',
            field=models.ManyToManyField(to='web.Submenu', null=True, verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\xad\x90\xe8\x8f\x9c\xe5\x8d\x95', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poster',
            name='product_web',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe4\xba\xa7\xe5\x93\x81', blank=True, to='web.Product_web', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='submenu',
            field=models.ManyToManyField(to='web.Submenu', null=True, verbose_name=b'\xe5\xad\x90\xe8\x8f\x9c\xe5\x8d\x95', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='focus',
            name='product_web',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe4\xba\xa7\xe5\x93\x81', blank=True, to='web.Product_web', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cart_web',
            name='fabric',
            field=models.ForeignKey(verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99', blank=True, to='web.Fabric_web', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cart_web',
            name='product',
            field=models.ForeignKey(verbose_name=b'\xe4\xba\xa7\xe5\x93\x81', blank=True, to='web.Product_web'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cart_web',
            name='user',
            field=models.ForeignKey(related_name='user', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', blank=True, to='wap.User'),
            preserve_default=True,
        ),
    ]

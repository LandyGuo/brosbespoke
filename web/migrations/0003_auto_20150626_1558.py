# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_footer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand_fabric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('image_url', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe5\x93\x81\xe7\x89\x8clog', blank=True)),
                ('content', models.TextField(null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\x93\x81\xe7\x89\x8c\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('type', models.CharField(default=b'suit', max_length=10, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'suit', b'\xe8\xa5\xbf\xe6\x9c\x8d'), (b'shirt', b'\xe8\xa1\xac\xe8\xa1\xab')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u9762\u6599\u54c1\u724c',
                'verbose_name_plural': '\u9762\u6599\u54c1\u724c',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Secondarymenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u6b21\u7ea7\u83dc\u5355',
                'verbose_name_plural': '\u6b21\u7ea7\u83dc\u5355',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='submenu',
            options={'verbose_name': '\u6b21\u7ea7\u83dc\u5355\u5206\u7ec4', 'verbose_name_plural': '\u6b21\u7ea7\u83dc\u5355\u5206\u7ec4'},
        ),
        migrations.RemoveField(
            model_name='fabric_web',
            name='brand',
        ),
        migrations.AddField(
            model_name='fabric_web',
            name='brand_fabric',
            field=models.ForeignKey(verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\x93\x81\xe7\x89\x8c', to='web.Brand_fabric', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submenu',
            name='secondarymenu',
            field=models.ManyToManyField(to='web.Secondarymenu', null=True, verbose_name=b'\xe6\xac\xa1\xe7\xba\xa7\xe8\x8f\x9c\xe5\x8d\x95', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='image_url',
            field=models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\xa4\xa7\xe5\x9b\xbe'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='name',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='price',
            field=models.IntegerField(max_length=11, null=True, verbose_name=b'\xe4\xbb\xb7\xe6\xa0\xbc'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='thumbnail_url',
            field=models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='submenu',
            field=models.ManyToManyField(to='web.Submenu', null=True, verbose_name=b'\xe6\xac\xa1\xe7\xba\xa7\xe8\x8f\x9c\xe5\x8d\x95\xe5\x88\x86\xe7\xbb\x84', blank=True),
            preserve_default=True,
        ),
    ]

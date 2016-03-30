# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20150627_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_web',
            name='price',
            field=models.IntegerField(max_length=11, null=True, verbose_name=b'\xe5\x8d\x95\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='brand_fabric',
            name='type',
            field=models.CharField(default=b'suit', max_length=10, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\x93\x81\xe7\x89\x8c\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'suit', b'\xe8\xa5\xbf\xe6\x9c\x8d'), (b'shirt', b'\xe8\xa1\xac\xe8\xa1\xab'), (b'item', b'\xe5\x8d\x95\xe5\x93\x81'), (b'accessorie', b'\xe9\x85\x8d\xe9\xa5\xb0')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='brand_fabric',
            field=models.ForeignKey(verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\x93\x81\xe7\x89\x8c', blank=True, to='web.Brand_fabric', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='desigh',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Design', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fabric_web',
            name='thumbnail_url',
            field=models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product_web',
            name='type',
            field=models.CharField(default=b'shirt', max_length=10, verbose_name=b'\xe4\xba\xa7\xe5\x93\x81\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'suit', b'\xe8\xa5\xbf\xe6\x9c\x8d'), (b'shirt', b'\xe8\xa1\xac\xe8\xa1\xab'), (b'item', b'\xe5\x8d\x95\xe5\x93\x81'), (b'accessorie', b'\xe9\x85\x8d\xe9\xa5\xb0')]),
            preserve_default=True,
        ),
    ]

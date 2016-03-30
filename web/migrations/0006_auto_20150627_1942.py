# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20150627_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='focus',
            name='product_web',
        ),
        migrations.RemoveField(
            model_name='poster',
            name='product_web',
        ),
        migrations.AddField(
            model_name='fabric_web',
            name='color',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Color', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabric_web',
            name='composition',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Composition', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabric_web',
            name='desigh',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Desigh', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fabric_web',
            name='weight',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Weight', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='focus',
            name='sort',
            field=models.CharField(max_length=26, null=True, verbose_name=b'\xe8\xb7\xb3\xe8\xbd\xac\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'\xe4\xba\xa7\xe5\x93\x81', b'\xe4\xba\xa7\xe5\x93\x81'), (b'\xe4\xba\xa7\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8', b'\xe4\xba\xa7\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8'), (b'\xe7\xbd\x91\xe5\x9d\x80', b'\xe7\xbd\x91\xe5\x9d\x80')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poster',
            name='sort',
            field=models.CharField(max_length=26, null=True, verbose_name=b'\xe8\xb7\xb3\xe8\xbd\xac\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'\xe4\xba\xa7\xe5\x93\x81', b'\xe4\xba\xa7\xe5\x93\x81'), (b'\xe4\xba\xa7\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8', b'\xe4\xba\xa7\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8'), (b'\xe7\xbd\x91\xe5\x9d\x80', b'\xe7\xbd\x91\xe5\x9d\x80')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product_web',
            name='latest_product',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe6\x9c\x80\xe6\x96\xb0\xe4\xba\xa7\xe5\x93\x81'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='brand_fabric',
            name='type',
            field=models.CharField(default=b'suit', max_length=10, verbose_name=b'\xe9\x9d\xa2\xe6\x96\x99\xe5\x93\x81\xe7\x89\x8c\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'suit', b'\xe8\xa5\xbf\xe6\x9c\x8d'), (b'shirt', b'\xe8\xa1\xac\xe8\xa1\xab')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='focus',
            name='img_href',
            field=models.CharField(default=b'', max_length=256, null=True, verbose_name=b'\xe8\xb7\xb3\xe8\xbd\xac\xe9\x93\xbe\xe6\x8e\xa5|\xe7\xbd\x91\xe5\x9d\x80\xe4\xb8\x8d\xe5\xa1\xab:Http://,\xe4\xba\xa7\xe5\x93\x81\xe5\x90\x8d\xe5\xa1\xab\xe5\x85\xa8\xe7\xa7\xb0 ,\xe4\xba\xa7\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8\xe5\xa1\xab\xe5\x86\x99\xe8\x8f\x9c\xe5\x8d\x95\xe5\x90\x8d\xe6\x8c\x89\xe7\xba\xa7\xe5\x88\xab\xe7\x94\xa8|\xe5\x88\x86\xe5\x89\xb2', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poster',
            name='img_href',
            field=models.CharField(default=b'', max_length=256, null=True, verbose_name=b'\xe8\xb7\xb3\xe8\xbd\xac\xe9\x93\xbe\xe6\x8e\xa5|\xe7\xbd\x91\xe5\x9d\x80\xe4\xb8\x8d\xe5\xa1\xab:Http://,\xe4\xba\xa7\xe5\x93\x81\xe5\x90\x8d\xe5\xa1\xab\xe5\x85\xa8\xe7\xa7\xb0 ,\xe4\xba\xa7\xe5\x93\x81\xe5\x88\x97\xe8\xa1\xa8\xe5\xa1\xab\xe5\x86\x99\xe8\x8f\x9c\xe5\x8d\x95\xe5\x90\x8d\xe5\xa4\x9a\xe7\xba\xa7\xe5\x88\xab\xe7\x94\xa8|\xe5\x88\x86\xe5\x89\xb2', blank=True),
            preserve_default=True,
        ),
    ]

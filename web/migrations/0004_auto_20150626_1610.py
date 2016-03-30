# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150626_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_web',
            name='secondarymenu',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe6\xac\xa1\xe7\xba\xa7\xe8\x8f\x9c\xe5\x8d\x95', blank=True, to='web.Secondarymenu', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product_web',
            name='submenu',
            field=models.ManyToManyField(to='web.Submenu', null=True, verbose_name=b'\xe6\xac\xa1\xe7\xba\xa7\xe8\x8f\x9c\xe5\x8d\x95\xe5\x88\x86\xe7\xbb\x84', blank=True),
            preserve_default=True,
        ),
    ]

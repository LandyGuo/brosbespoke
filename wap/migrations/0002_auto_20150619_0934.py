# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.CharField(default=b'', max_length=32, null=True, verbose_name=b'\xe5\xb9\xb4\xe9\xbe\x84', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='job',
            field=models.CharField(default=b'', max_length=128, null=True, verbose_name=b'\xe8\x81\x8c\xe4\xb8\x9a', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(verbose_name=b'\xe4\xba\xa7\xe5\x93\x81', to='wap.Product'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to='wap.User'),
            preserve_default=True,
        ),
    ]

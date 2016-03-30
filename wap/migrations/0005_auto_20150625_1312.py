# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wap', '0004_auto_20150623_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gh',
            field=models.CharField(default=b'', max_length=32, null=True, verbose_name=b'\xe6\x96\xb0\xe5\xbb\xba\xe5\xb7\xa5\xe5\x8f\xb7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='gh',
            field=models.CharField(default=b'', max_length=32, null=True, verbose_name=b'\xe6\x96\xb0\xe5\xbb\xba\xe5\xb7\xa5\xe5\x8f\xb7', blank=True),
            preserve_default=True,
        ),
    ]

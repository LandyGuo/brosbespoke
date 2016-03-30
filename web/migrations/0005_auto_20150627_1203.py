# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20150626_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footer',
            name='content',
            field=models.TextField(null=True, verbose_name=b'\xe5\xbc\xb9\xe7\xaa\x97\xe5\x86\x85\xe5\xae\xb9\xef\xbc\x8c|\xe5\x88\x86\xe6\xae\xb5', blank=True),
            preserve_default=True,
        ),
    ]

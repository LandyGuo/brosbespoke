# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wap', '0003_measurereservation_reservation_time_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='address4order',
            name='default_address',
            field=models.BooleanField(default=False, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe5\x9c\xb0\xe5\x9d\x80'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address4order',
            name='sex',
            field=models.CharField(default=b'\xe7\x94\xb7', choices=[(b'\xe5\xa5\xb3', b'\xe5\xa5\xb3'), (b'\xe7\x94\xb7', b'\xe7\x94\xb7')], max_length=10, blank=True, null=True, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab'),
            preserve_default=True,
        ),
    ]

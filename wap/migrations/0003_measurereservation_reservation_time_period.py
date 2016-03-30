# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wap', '0002_auto_20150619_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurereservation',
            name='reservation_time_period',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe9\xa2\x84\xe7\xba\xa6\xe6\x97\xb6\xe9\x97\xb4\xe6\xae\xb5', blank=True),
            preserve_default=True,
        ),
    ]

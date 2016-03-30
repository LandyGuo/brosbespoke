# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('mz', models.CharField(max_length=32, null=True, verbose_name=b'\xe8\x8b\xb1\xe6\x96\x87\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('content', models.TextField(null=True, verbose_name=b'\xe5\xbc\xb9\xe7\xaa\x97\xe5\x86\x85\xe5\xae\xb9', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name': '\u5f39\u7a97',
                'verbose_name_plural': '\u5f39\u7a97',
            },
            bases=(models.Model,),
        ),
    ]

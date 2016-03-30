# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20150702_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, null=True, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', blank=True)),
                ('subtitle', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x89\xaf\xe6\xa0\x87\xe9\xa2\x98', blank=True)),
                ('img', models.ImageField(upload_to=web.models.get_uploadto_path, null=True, verbose_name=b'\xe5\xb1\x95\xe7\xa4\xba\xe5\x9b\xbe', blank=True)),
                ('content', DjangoUeditor.models.UEditorField(null=True, verbose_name=b'\xe4\xb8\xbb\xe6\x96\x87', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u671f\u520a',
                'verbose_name_plural': '\u671f\u520a',
            },
            bases=(models.Model,),
        ),
    ]

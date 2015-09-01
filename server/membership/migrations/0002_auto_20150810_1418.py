# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_premium_member',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
        migrations.AddField(
            model_name='user',
            name='resume',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default=b'Erkek', max_length=5,
                                   choices=[(b'Erkek', b'Erkek'), (b'Kad\xc4\xb1n', b'Kad\xc4\xb1n')]),
        ),
    ]

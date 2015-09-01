# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0004_auto_20150811_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default='Erkek', max_length=5,
                                   choices=[('Erkek', 'Erkek'), ('Kad\u0131n', 'Kad\u0131n')]),
        ),
    ]

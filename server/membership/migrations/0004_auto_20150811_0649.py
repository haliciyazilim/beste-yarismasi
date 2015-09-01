# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0003_auto_20150811_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default=b'Erkek', max_length=5,
                                   choices=[(b'Erkek', b'Erkek'), (b'Kad\xc4\xb1n', b'Kad\xc4\xb1n')]),
        ),
    ]

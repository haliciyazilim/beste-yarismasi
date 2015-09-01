# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0002_auto_20150810_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default=b'E', max_length=5, choices=[(b'E', b'E'), (b'K', b'K')]),
        ),
    ]

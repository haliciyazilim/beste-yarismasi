# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0008_auto_20150811_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='resume',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'eser', max_length=100)),
                ('url', models.URLField(default=b'')),
                ('is_qualified', models.BooleanField(default=False)),
                ('is_finalist', models.BooleanField(default=False)),
                ('order', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(null=True, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=30)),
                ('content', models.TextField(null=True, blank=True)),
                ('category_name', models.CharField(default=b'link', max_length=5, choices=[(b'link', b'link'), (b'index', b'index')])),
                ('update_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_for_static_content', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('year', models.IntegerField(unique=True)),
                ('theme', models.CharField(max_length=100, null=True)),
                ('poster', models.URLField(null=True)),
                ('start_date', models.DateField()),
                ('final_date', models.DateField()),
                ('finish_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StageMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TrackUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datafile', models.FileField(upload_to=b'')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_date', models.DateTimeField(auto_now_add=True, auto_created=True)),
                ('value', models.IntegerField()),
                ('ip', models.GenericIPAddressField()),
                ('composition', models.ForeignKey(related_name='composition', to='api.Composition')),
                ('contest', models.ForeignKey(to='api.Contest')),
            ],
        ),
        migrations.AddField(
            model_name='composition',
            name='contest',
            field=models.ForeignKey(to='api.Contest'),
        ),
        migrations.AddField(
            model_name='composition',
            name='devices',
            field=models.ManyToManyField(to='api.Device', blank=True),
        ),
        migrations.AddField(
            model_name='composition',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='composition',
            name='softwares',
            field=models.ManyToManyField(related_name='softwares', to='api.Software', blank=True),
        ),
        migrations.AddField(
            model_name='composition',
            name='stage_materials',
            field=models.ManyToManyField(to='api.StageMaterial', blank=True),
        ),
    ]

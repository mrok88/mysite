# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-25 00:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dq', '0016_auto_20180725_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vrfy_cmd',
            name='LAST_EXE_DTTM',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 25, 9, 2, 17, 14925), verbose_name='마지막수행일시'),
        ),
        migrations.AlterField(
            model_name='vrfylog',
            name='DB_NM',
            field=models.CharField(max_length=100, verbose_name='DB명'),
        ),
        migrations.AlterField(
            model_name='vrfylog',
            name='SCHEMA_NM',
            field=models.CharField(max_length=100, verbose_name='스키마명'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-16 05:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dq', '0004_auto_20180713_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vrfy',
            name='AUTO_CK_YN',
        ),
        migrations.AddField(
            model_name='vrfy',
            name='USE_YN',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1, verbose_name='사용여부'),
        ),
        migrations.AlterField(
            model_name='vrfy',
            name='CMD_TYPE_CD',
            field=models.CharField(choices=[('AURORA_SQL', 'AURORA_SQL'), ('ATHENA_SQL', 'ATHENA_SQL'), ('DYNAMODB_QRY', 'DYNAMODB_QRY'), ('RED_SHIFT_QRY', 'RED_SHIFT_QRY'), ('SHELL', 'SHELL'), ('ETC', 'ETC')], default='01', max_length=30, verbose_name='명령유형코드'),
        ),
        migrations.AlterField(
            model_name='vrfy',
            name='VRFY_EXPLN',
            field=models.TextField(blank=True, default=None, max_length=500, null=True, verbose_name='검증설명'),
        ),
        migrations.AlterField(
            model_name='vrfy_cmd',
            name='LAST_EXE_DTTM',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 16, 14, 43, 42, 206675), verbose_name='마지막수행일시'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-27 06:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dq', '0018_auto_20180725_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableCopy',
            fields=[
                ('TABLE_NO', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='원테이블번호')),
                ('TABLE_NM', models.CharField(max_length=100, verbose_name='테이블명')),
                ('TABLE_HANGL_NM', models.CharField(max_length=100, verbose_name='테이블한글명')),
                ('TABLE_COPY_EXPLN', models.TextField(blank=True, default=None, max_length=500, null=True, verbose_name='테이블복사설명')),
                ('USE_YN', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1, verbose_name='사용여부')),
                ('RGSTR_ID', models.CharField(default='DA', max_length=30, verbose_name='등록자ID')),
                ('RGST_DTTM', models.DateTimeField(auto_now_add=True, verbose_name='등록일시')),
                ('MODR_ID', models.CharField(default='DA', max_length=30, verbose_name='수정자ID')),
                ('MODI_DTTM', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
            ],
        ),
        migrations.AlterField(
            model_name='vrfy_cmd',
            name='LAST_EXE_DTTM',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 27, 15, 22, 28, 99668), verbose_name='마지막수행일시'),
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

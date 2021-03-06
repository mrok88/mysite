# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-13 07:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vrfy',
            fields=[
                ('VRFY_NO', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='검증번호')),
                ('DB_NM', models.CharField(max_length=100, verbose_name='DB명')),
                ('SCHEMA_NM', models.CharField(max_length=100, verbose_name='스키마명')),
                ('CLSF_NM1', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='대분류명')),
                ('CLSF_NM2', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='중분류명')),
                ('VRFY_TYPE_DTL_CD', models.CharField(choices=[('DMN', '도메인검증'), ('REF', '참조검증'), ('NT_NML', '비정규검증'), ('BIZ_RUL', '업무규칙검증')], default='BIZ_RUL', max_length=30, verbose_name='검증유형상세코드')),
                ('VRFY_NM', models.CharField(max_length=100, verbose_name='검증명')),
                ('VRFY_EXPLN', models.CharField(max_length=500, verbose_name='검증설명')),
                ('TABLE_NM', models.CharField(max_length=100, verbose_name='테이블명')),
                ('TABLE_HANGL_NM', models.CharField(max_length=100, verbose_name='테이블한글명')),
                ('REFRC_TABLE_NM', models.CharField(max_length=100, verbose_name='참조테이블명')),
                ('REFRC_TABLE_HANGL_NM', models.CharField(max_length=100, verbose_name='참조테이블한글명')),
                ('AUTO_CK_YN', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1, verbose_name='자동체크여부')),
                ('CMD_TYPE_CD', models.CharField(choices=[('01', 'AURORA_SQL'), ('02', 'ATHENA_SQL'), ('03', 'DynameDB_QRY'), ('04', 'RED_SHIFT_QRY'), ('05', 'SHELL'), ('99', '기타')], default='01', max_length=2, verbose_name='명령유형코드')),
                ('CMD_CNTS', models.TextField(blank=True, default=None, max_length=4000, null=True, verbose_name='검증내용')),
                ('RGSTR_ID', models.CharField(default='DA', max_length=30, verbose_name='등록자ID')),
                ('RGST_DTTM', models.DateTimeField(auto_now_add=True, verbose_name='등록일시')),
                ('MODR_ID', models.CharField(default='DA', max_length=30, verbose_name='수정자ID')),
                ('MODI_DTTM', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
            ],
        ),
        migrations.CreateModel(
            name='Vrfy_Cmd',
            fields=[
                ('VRFY_CMD_NO', models.AutoField(editable=False, primary_key=True, serialize=False, verbose_name='검증명령어번호')),
                ('VRFY_SEQ', models.IntegerField(verbose_name='검증순번')),
                ('AUTO_CK_YN', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=1, verbose_name='자동체크여부')),
                ('CMD_DVS_CD', models.CharField(choices=[('VRFY', '검증'), ('EXE', '실행')], default='VRFY', max_length=20, verbose_name='명령어구분코드')),
                ('CMD_TYPE_CD', models.CharField(choices=[('AURORA_SQL', 'AURORA_SQL'), ('SHELL', 'Shell'), ('AURORA_PROC', 'AURORA프로시져'), ('ATHENA_SQL', 'ATHENA_SQL')], default='AURORA_SQL', max_length=20, verbose_name='명령어유형코드')),
                ('CMD_CNTS', models.TextField(blank=True, default=None, max_length=4000, null=True, verbose_name='명령어내용')),
                ('DTL_VRFY_YN', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=1, verbose_name='상세검증여부')),
                ('LAST_EXE_DTTM', models.DateTimeField(default=datetime.datetime(2018, 7, 13, 16, 39, 50, 647155), verbose_name='마지막수행일시')),
                ('RGSTR_ID', models.CharField(default='DA', max_length=30, verbose_name='등록자ID')),
                ('RGST_DTTM', models.DateTimeField(auto_now_add=True, verbose_name='등록일시')),
                ('MODR_ID', models.CharField(default='DA', max_length=30, verbose_name='수정자ID')),
                ('MODI_DTTM', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('VRFY_NO', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dq.Vrfy')),
            ],
        ),
    ]

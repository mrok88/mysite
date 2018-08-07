# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms import ModelForm
from bootstrap3.tests import TestForm
############################## dbConn  ##############################
from .models import * 

###############################################################################
class VrfyForm(ModelForm):
    class Meta:
        model = Vrfy
        fields = ['DB_NM', 'SCHEMA_NM', 'CLSF_NM1', 'CLSF_NM2'
                 , 'VRFY_TYPE_CD','VRFY_NM','VRFY_EXPLN'
                 ,'TABLE_HANGL_NM','TABLE_NM', 'REFRC_TABLE_HANGL_NM','REFRC_TABLE_NM'
                 ,'USE_YN','CMD_TYPE_CD','CMD_CNTS'
        ,'RGSTR_ID'
        #,'RGST_DTTM'
        ,'MODR_ID'
        #,'MODI_DTTM'
        ]
        widgets = {
            'VRFY_EXPLN' : forms.Textarea(attrs={'rows':2}),
            'CMD_CNTS' : forms.Textarea(attrs={'rows':7}),
        }

###############################################################################
class TableCopyForm(ModelForm):
    class Meta:
        model = TableCopy
        fields = ['TABLE_NM'       
                    ,'TABLE_HANGL_NM'
                    ,'TABLE_COPY_EXPLN'
                    ,'USE_YN'
                    ,'RGSTR_ID'
                    #,'RGST_DTTM'
                    ,'MODR_ID'
                    #,'MODI_DTTM'
                    ]
        widgets = {
            'TABLE_COPY_EXPLN' : forms.Textarea(attrs={'rows':4})
        }

###############################################################################
class IlmForm(ModelForm):
    class Meta:
        model = Ilm
        fields = ['DB_NM', 'SCHEMA_NM', 'CLSF_NM1', 'CLSF_NM2'
                 , 'ILM_TYPE_CD','ILM_NM','ILM_EXPLN'
                 , 'TABLE_HANGL_NM','TABLE_NM','ILM_SEQ'
                 , 'EXPCT_CNT', 'PRESER_PRD_VAL'
                 ,'USE_YN','CMD_TYPE_CD','CMD_CNTS'
        ,'RGSTR_ID'
        #,'RGST_DTTM'
        ,'MODR_ID'
        #,'MODI_DTTM'
        ]
        widgets = {
            'ILM_EXPLN' : forms.Textarea(attrs={'rows':2}),
            'CMD_CNTS' : forms.Textarea(attrs={'rows':7}),
        }

###############################################################################
class vrfy_CmdForm(ModelForm):
    class Meta:
        model = Vrfy_Cmd
        fields = [ 'VRFY_NO','VRFY_SEQ', 'AUTO_CK_YN', 'CMD_DVS_CD', 'CMD_TYPE_CD', 'CMD_CNTS','DTL_VRFY_YN'
        ,'RGSTR_ID'
        #,'RGST_DTTM'
        ,'MODR_ID'
        #,'MODI_DTTM'
        ]      
###############################################################################
class EnvForm(forms.Form):
    ENV_DVS_CD = (
        ('all', '전체환경'),
        ('dev', '개발환경'),
        ('tst', '테스트환경'),
        ('prd', '운영환경'),
    )
    env = forms.ChoiceField(label = "환경",choices = ENV_DVS_CD)

###############################################################################
class vrfyLogForm(EnvForm):
    errYn = forms.BooleanField(
        label = '오류Only',
        required=False,
        help_text='수행결과가 오류가 있는 경우'
    )        
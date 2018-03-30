# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from bootstrap3.tests import TestForm
###############################################################################
from django.contrib.admin.widgets import AdminSplitDateTime
###############################################################################
RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)


MEDIA_CHOICES = (    
    ('개발', (    
        ('ellt', '개발전체'),         
        ('elltcc', '고객센터'),
        ('elltch', '채널제휴'),
        ('elltdp', '전시'),
        ('elltet', '거래처'),
        ('elltgd', '상품'),
        ('elltmb', '회원'),
        ('elltom', '주문'),        
        ('elltpy', '결제'),        
        ('elltlo', '배송'),        
        ('elltpr', '판촉'),
        ('elltsc', '검색'),     
    )),
    ('공통', (
        ('ltcm', '공통전체'),          
        ('ltcmst', '시스템공통'),
        ('ltcmpr', '판촉공통'),
        ('ltcmat', '상품속성'),        
    )),
)

class CompForm(forms.Form):
    """
    모델 과 테이블간 차이점을 비교하기 위해서 subject area를 선택한는 폼
    """

    subjArea = forms.ChoiceField(choices=MEDIA_CHOICES)

    # TODO: Re-enable this after Django 1.11 #28105 is available
    # polygon = gisforms.PointField()

    required_css_class = 'bootstrap3-req'

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data

class CapaForm(forms.Form):
    """
    모델 과 테이블간 차이점을 비교하기 위해서 subject area를 선택한는 폼
    """

    subjArea = forms.ChoiceField(choices=MEDIA_CHOICES)

    # TODO: Re-enable this after Django 1.11 #28105 is available
    # polygon = gisforms.PointField()

    required_css_class = 'bootstrap3-req'

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")


ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file5 = forms.ImageField()
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data



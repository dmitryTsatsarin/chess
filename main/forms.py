# -*- coding: utf-8 -*-
__author__ = 'dmitry'
from django.forms import ModelForm
from models import Member

class MemberForm(ModelForm):
    class Meta:
        model = Member
        exclude = ('elo_new',)
# -*- coding: utf-8 -*-
__author__ = 'dmitry'

from django.contrib import admin
from models import Member, Tournament

admin.site.register(Member)
admin.site.register(Tournament)


# -*- coding: utf-8 -*-
__author__ = 'dmitry'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^member/add/', views.add_member),
    url(r'^member/list/', views.show_list_members),
    url(r'^tournament/start/', views.tournament_start),
    url(r'^tournament/judge/', views.tournament_judge),
    url(r'^tournament/results/', views.tournament_results),
    url(r'^tournament/zeroing/', views.tournament_zeroing),
    url(r'^', views.show_list_members),
)

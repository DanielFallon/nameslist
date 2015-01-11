__author__ = 'peter@chinetti.me'

from django.conf.urls import patterns, url

from nameslist_app import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )

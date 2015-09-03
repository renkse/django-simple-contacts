__author__ = 'renkse'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.contacts_view, name='contacts'),
    url(r'^feedback/$', views.feedback_view, name='fbview'),
)

from django.conf.urls import patterns, url

from log_collector import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    )
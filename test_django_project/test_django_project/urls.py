from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^polls/', include('polls.urls',
                                               namespace="polls")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^blog/', include('blog.urls',
                                              namespace="blog")),
                       url(r'^log_collector/', include(
                           'log_collector.urls',
                           namespace="log_collector"))
                       )

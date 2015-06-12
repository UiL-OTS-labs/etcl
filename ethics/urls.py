from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/proposals/'}, name='logout'),

    url(r'^proposals/', include('proposals.urls', namespace='proposals')),
    url(r'^feedback/', include('feedback.urls', namespace='feedback')),

    url(r'^admin/', include(admin.site.urls)),
)

admin.site.site_header = 'ETCL'
admin.site.site_title = 'ETCL administratie'
admin.site.index_title = 'ETCL administratie'

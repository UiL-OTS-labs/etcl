"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

handler404 = 'core.error_views.error_404'
handler500 = 'core.error_views.error_500'
handler403 = 'core.error_views.error_403'
handler400 = 'core.error_views.error_400'


urlpatterns = [
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^', include('core.urls')),
    url(r'^proposals/', include('proposals.urls')),
    url(r'^studies/', include('studies.urls')),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^observations/', include('observations.urls')),
    url(r'^interventions/', include('interventions.urls')),
    url(r'^reviews/', include('reviews.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^faqs/', include('faqs.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^impersonate/', include('impersonate.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'FETC-GW'
admin.site.site_title = 'FETC-GW administratie'
admin.site.index_title = 'FETC-GW administratie'

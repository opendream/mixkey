from django.conf import settings

from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mixkey.views.home', name='home'),
    # url(r'^mixkey/', include('mixkey.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'domain.views.home', name='home'),
    url(r'^c/$', 'domain.views.data_create', name='data_create'),
    
    
    # Deprecate 
    url(r'^s.php$', 'domain.views.data_create'),
    url(r'^s.php/$', 'domain.views.data_create'),
    
    url(r'^language/$', 'domain.views.set_language', name='set_lang'),
    
    # Force to order end
    url(r'^(?P<project_code>[A-Za-z0-9_-]+)/(?P<sensor_code>[A-Za-z0-9_-]+)/$', 'domain.views.sensor_overview', name='sensor_overview'),
    url(r'^(?P<project_code>[A-Za-z0-9_-]+)/$', 'domain.views.project_overview', name='project_overview'),
    
    
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
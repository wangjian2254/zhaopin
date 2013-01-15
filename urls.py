from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from zhaopin import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zhaopin.views.home', name='home'),
    # url(r'^zhaopin/', include('zhaopin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

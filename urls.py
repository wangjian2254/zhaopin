from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
from pin.loginviews import reg, reg2
from zhaopin import settings
from zhaopin.pin.views import index,jianlilist,addjianli
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', index),
    (r'^jianlilist$', jianlilist),
    (r'^addjianli', addjianli),
    # url(r'^zhaopin/', include('zhaopin.foo.urls')),
    (r'^Reg/$',reg),
    (r'^Reg2/$',reg2),
    (r'^accounts/login/$',login,{'template_name':'login.html','redirect_field_name':'/'}),
    (r'^accounts/logout/$', logout,{'template_name':'logout.html'}),
    (r'^accounts/profile/$',index),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#s                       
)

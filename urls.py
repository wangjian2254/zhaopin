from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
from zhaopin.pin.loginviews import reg, reg2
from zhaopin import settings
from zhaopin.pin.views import index,jianlilist,addjianli,deljianli,savejianli,pubjianli,lookjianli,worklist,addwork,savework,pubwork,lookwork,updatecompany,savecompany
from zhaopin.pin.searchView import searchWork,searchPeople
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', index),
    (r'^SearchWork', searchWork),
    (r'^SearchPeople', searchPeople),
    (r'^jianlilist$', jianlilist),
    (r'^worklist$', worklist),
    (r'^addwork', addwork),
    (r'^savework', savework),
    (r'^addjianli', addjianli),
    (r'^deljianli', deljianli),

    (r'^pubjianli', pubjianli),
    (r'^pubwork', pubwork),
    (r'^updatecompany', updatecompany),
    (r'^savecompany', savecompany),
    (r'^lookjianli', lookjianli),
    (r'^lookwork', lookwork),
    (r'^savejianli', savejianli),
    # url(r'^zhaopin/', include('zhaopin.foo.urls')),
    (r'^Reg/$',reg),
    (r'^Reg2/$',reg2),
    (r'^accounts/login/$',login,{'template_name':'login1.html','redirect_field_name':'/'}),
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

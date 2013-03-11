from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
from zhaopin.pin.loginviews import reg, reg2
from zhaopin import settings
from zhaopin.pin.views import commentAdd,commentList,replay,newslist,newslook
from zhaopin.pin.views import index,toudijianli,toudilist,selectJianli,jianliRecodelook,jianlilist,addjianli,deljianli,savejianli,pubjianli,lookjianli,worklist,addwork,savework,pubwork,lookwork,updatecompany,savecompany,companylook
from zhaopin.pin.searchView import searchWork,searchPeople
from zhaopin.pin.weiboManage import Login_check,weiboLogin,pubWeibo,setWeibo
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', index),
    (r'^newslook', newslook),
    (r'^newslist', newslist),
    (r'^SearchWork', searchWork),
    (r'^SearchPeople', searchPeople),
    (r'^replay', replay),
    (r'^commentAdd', commentAdd),
    (r'^commentList', commentList),
    (r'^jianlilist$', jianlilist),
    (r'^worklist$', worklist),
    (r'^addwork', addwork),
    (r'^savework', savework),
    (r'^addjianli', addjianli),
    (r'^deljianli', deljianli),

    (r'^pubjianli', pubjianli),
    (r'^pubwork', pubwork),
    (r'^jianliRecodelook', jianliRecodelook),
    (r'^toudilist', toudilist),
    (r'^lookcompany', companylook),
    (r'^updatecompany', updatecompany),
    (r'^savecompany', savecompany),
    (r'^lookjianli', lookjianli),
    (r'^lookwork', lookwork),
    (r'^selectJianli', selectJianli),
    (r'^toudijianli', toudijianli),
    (r'^savejianli', savejianli),

    (r'^weibo/login_check', Login_check),
    (r'^weibo/login', weiboLogin),
    (r'^pubWeibo', pubWeibo),
    (r'^setWeibo', setWeibo),



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
    url(r'^ueditor/', include('zhaopin.ueditor.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#s                       
)

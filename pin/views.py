#coding=utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from pin.models import JianLi

def index(request):
    return render_to_response('index.html',RequestContext(request,{}))



def jianlilist(request):
    '''
    简历列表界面
    '''
    menuitem='jianlilist'
    list=JianLi.objects.filter(user=request.user)
    return render_to_response('jianlilist.html',{'menuitem':menuitem,'list':list},RequestContext(request,{}))
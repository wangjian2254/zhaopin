#coding=utf-8
#
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from pin.models import ZhiWei

__author__ = '张藐方'

def searchWork(request):
    searchValue=request.REQUEST.get('searchValue','')
    start=request.REQUEST.get('start',0)
    limit=request.REQUEST.get('limit',10)
    start=int(start)
    limit=int(limit)
    if not searchValue:
        return HttpResponseRedirect('/')
    zhiweiquery=ZhiWei.objects.filter(Q(zhiwei__contains=searchValue)|Q(desc__contains=searchValue))
    #其他条件

    total=zhiweiquery.count()
    return render_to_response('searchWork.html',{'pam':request.REQUEST,'start':start,'limit':limit,'total':total,'list':zhiweiquery[start:start+limit]},RequestContext(request,{}))
  
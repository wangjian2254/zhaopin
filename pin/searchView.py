#coding=utf-8
#
import urllib
import datetime
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from zhaopin.pin.tools import getSessionMsg
from zhaopin.pin.models import ZhiWei, JianLi

__author__ = '张藐方'

def searchWork(request):
    searchValue=request.REQUEST.get('searchValue','')
    start=request.REQUEST.get('start',1)
    limit=request.REQUEST.get('limit',20)
    start=int(start)
    limit=int(limit)
#    if not searchValue:
#        return HttpResponseRedirect('/')
    address=request.REQUEST.get('add','')
    type=request.REQUEST.get('type','')
    query={'searchValue':searchValue.encode('utf-8'),'add':address.encode('utf-8'),'type':type.encode('utf-8')}
    querystr=urllib.urlencode(query)

    zhiweiquery=ZhiWei.objects.filter(ispub=True).filter(Q(zhiwei__contains=searchValue)|Q(desc__contains=searchValue))
    #其他条件
    if address:
        zhiweiquery=zhiweiquery.filter(workadd__contains=address)
    if type:
        zhiweiquery=zhiweiquery.filter(Q(xingzhi=type)|Q(xingzhi=""))
    if not searchValue:
        zhiweiquery=[]
    page=Paginator(zhiweiquery,limit)
    currentpage=page.page(start)
    return render_to_response('searchWork.html',getSessionMsg(request,{'querystr':querystr,'pam':request.REQUEST,'start':start,'limit':limit,'page':page,'currentpage':currentpage}),RequestContext(request,{}))


def searchPeople(request):
    searchValue=request.REQUEST.get('searchValue','')
    start=request.REQUEST.get('start',1)
    limit=request.REQUEST.get('limit',20)
    start=int(start)
    limit=int(limit)
#    if not searchValue:
#        return HttpResponseRedirect('/')
    address=request.REQUEST.get('add','')
    sex=request.REQUEST.get('sex','')
    age=request.REQUEST.get('age','')
    maxage=age.split(',')[-1]
    minage=age.split(',')[0]
    workage=request.REQUEST.get('workage','')
    zhuanye=request.REQUEST.get('zhuanye','')
    xuewei=request.REQUEST.get('xuewei','')
    query={'searchValue':searchValue.encode('utf-8'),
           'add':address.encode('utf-8'),'sex':sex,'age':age,'workage':workage,'zhuanye':zhuanye.encode('utf-8'),'xuewei':xuewei.encode('utf-8')}
    querystr=urllib.urlencode(query)

    zhiweiquery=JianLi.objects.filter(ispub=True).filter(Q(name__contains=searchValue)|Q(desc__contains=searchValue))
    #其他条件
    if address:
        zhiweiquery=zhiweiquery.filter(workadd__contains=address)
    if sex:
        if '1'==sex:
            zhiweiquery=zhiweiquery.filter(sex=True)
        else:
            zhiweiquery=zhiweiquery.filter(sex=False)
    if minage:
        zhiweiquery=zhiweiquery.filter(age__lt=datetime.datetime.now()-datetime.timedelta(days=int(minage)*365))
    if maxage:
        zhiweiquery=zhiweiquery.filter(age__gt=datetime.datetime.now()-datetime.timedelta(days=int(maxage)*365))
    if workage:
        zhiweiquery=zhiweiquery.filter(workage__gte=int(workage))
    if zhuanye:
        zhiweiquery=zhiweiquery.filter(zhuanye__contains=zhuanye)
    if xuewei:
        zhiweiquery=zhiweiquery.filter(xuewei__gte=xuewei)
    if not searchValue:
        zhiweiquery=[]
    page=Paginator(zhiweiquery,limit)
    currentpage=page.page(start)
    return render_to_response('searchPeople.html',getSessionMsg(request,
            {'querystr':querystr,'pam':request.REQUEST,'start':start,'limit':limit,'page':page,'currentpage':currentpage}),RequestContext(request,{}))

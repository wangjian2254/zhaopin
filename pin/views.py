#coding=utf-8
# Create your views here.
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from zhaopin.pin.models import LookRecord, ZhiWei, WorkLookRecord, Business
from zhaopin.pin.models import JianLi, JiaoYu, WorkJingYan
RESULT='result'
MSG='msg'
SUCCESS='success'
WARN='warn'
def getSessionMsg(request,requestdic):
    requestdic[RESULT]=request.session.get(RESULT, '')
    requestdic[MSG]=request.session.get(MSG, '')
    if request.session.has_key(RESULT):
        del request.session[RESULT]
    if request.session.has_key(MSG):
        del request.session[MSG]
    return requestdic

def index(request):
    newzhiweilist=ZhiWei.objects.order_by('-updatetime')[:10]
    return render_to_response('index.html',{'newzhiweilist':newzhiweilist},RequestContext(request,{}))


@login_required
def worklist(request):
    '''
    简历列表界面
    '''
    list=ZhiWei.objects.filter(user=request.user)
    return render_to_response('worklist.html',getSessionMsg(request,{'list':list}),RequestContext(request,{}))

@login_required
def pubwork(request):
    '''
    简历列表界面
    '''
    workid=request.GET.get('work_id','')
    if workid and 0<ZhiWei.objects.filter(pk=workid).count():
        work=ZhiWei.objects.get(pk=workid)
        if work.ispub:
            work.ispub=False
        else:
            work.ispub=True
        work.save()
        request.session[RESULT]=SUCCESS
        request.session[MSG]=u'操作成功。'
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return HttpResponseRedirect('/worklist')
@login_required
def delwork(request):
    '''
    简历列表界面
    '''
    workid=request.GET.get('work_id','')
    if workid and 0<ZhiWei.objects.filter(pk=workid).count():
        work=ZhiWei.objects.get(pk=workid)
        WorkLookRecord.objects.filter(zhiwei=work).delete()
        work.delete()
        request.session[RESULT]=SUCCESS
        request.session[MSG]=u'操作成功。'
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return HttpResponseRedirect('/worklist')

def lookwork(request):
    '''
    简历列表界面
    '''
    workid=request.GET.get('work_id','')
    business={}
    work={}
    if workid and 0<ZhiWei.objects.filter(pk=workid).count():
        work=ZhiWei.objects.get(pk=workid)
        businesslist=Business.objects.filter(user=work.user)[:1]
        if 1==len(businesslist):
            business=businesslist[0]
        if request.user.is_authenticated() and request.user.person.type==1:
            lookrecord=WorkLookRecord()
            lookrecord.zhiwei=work
            lookrecord.user=request.user
            lookrecord.save()
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return render_to_response('worklook.html',getSessionMsg(request,{'work':work,'business':business}),RequestContext(request,{}))



@login_required
def jianlilist(request):
    '''
    简历列表界面
    '''
    list=JianLi.objects.filter(user=request.user)
    return render_to_response('jianlilist.html',getSessionMsg(request,{'list':list}),RequestContext(request,{}))


def lookjianli(request):
    '''
    简历列表界面
    '''
    jianliid=request.GET.get('jianli_id','')
    jiaoyulist=[]
    worklist=[]
    jianli={}
    if jianliid and 0<JianLi.objects.filter(pk=jianliid).count():
        jianli=JianLi.objects.get(pk=jianliid)
        for j in JiaoYu.objects.filter(jianli=jianli):
            jiaoyulist.append(j)
        for j in WorkJingYan.objects.filter(jianli=jianli):
            worklist.append(j)
        if request.user.is_authenticated() and request.user.person.type==2:
            lookrecord=LookRecord()
            lookrecord.jianli=jianli
            lookrecord.user=request.user
            lookrecord.save()
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return render_to_response('jianlilook.html',getSessionMsg(request,{'jianli':jianli,'jiaoyulist':jiaoyulist,'worklist':worklist}),RequestContext(request,{}))



@login_required
def pubjianli(request):
    '''
    简历列表界面
    '''
    jianliid=request.GET.get('jianli_id','')
    if jianliid and 0<JianLi.objects.filter(pk=jianliid).count():
        jianli=JianLi.objects.get(pk=jianliid)
        if jianli.ispub:
            jianli.ispub=False
        else:
            jianli.ispub=True
        jianli.save()
        request.session[RESULT]=SUCCESS
        request.session[MSG]=u'操作成功。'
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return HttpResponseRedirect('/jianlilist')
@login_required
def deljianli(request):
    '''
    简历列表界面
    '''
    jianliid=request.GET.get('jianli_id','')
    if jianliid and 0<JianLi.objects.filter(pk=jianliid).count():
        jianli=JianLi.objects.get(pk=jianliid)
        LookRecord.objects.filter(jianli=jianli).delete()
        jianli.delete()
        request.session[RESULT]=SUCCESS
        request.session[MSG]=u'操作成功。'
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return HttpResponseRedirect('/jianlilist')


@login_required
def addjianli(request):
    '''
    添加简历
    '''
    jianliid=request.GET.get('jianli_id','')
    if jianliid:
        jianli=JianLi.objects.get(pk=jianliid)
    else:
        jianli=JianLi()

    jiaoyulist=[]
    for j in JiaoYu.objects.filter(jianli=jianli):
        jiaoyulist.append(j)
    for j in range(5-len(jiaoyulist)):
        jiaoyulist.append({})
    worklist=[]
    for j in WorkJingYan.objects.filter(jianli=jianli):
        worklist.append(j)
    for j in range(5-len(worklist)):
        worklist.append({}.update())
    return render_to_response('jianli.html',getSessionMsg(request,{'jianli':jianli,'jiaoyulist':jiaoyulist,'worklist':worklist}),RequestContext(request,{}))

@login_required
def savejianli(request):
    '''
    保存简历
    '''
    menuitem='addjianli'
    id=request.POST.get('id','')
    user=request.user
    name=request.POST.get('name','')
    username=request.POST.get('username','')
    age=request.POST.get('age','')
    sex=request.POST.get('sex','')
    zhuanye=request.POST.get('zhuanye','')
    workage=request.POST.get('workage','')
    minzu=request.POST.get('minzu','')
    tel=request.POST.get('tel','')
    email=request.POST.get('email','')
    desc=request.POST.get('desc','')
    workadd=request.POST.get('workadd','')
    xuewei=request.POST.get('xuewei','')
    if id:
        jianli=JianLi.objects.get(pk=id)
    else:
        jianli=JianLi()
    jianli.user=user
    if name:
        jianli.name=name
    if workadd:
        jianli.workadd=workadd
    if xuewei:
        jianli.xuewei=xuewei
    if username:
        jianli.username=username
    if age:
        jianli.age=datetime.datetime.strptime(age,'%Y-%m-%d')
    if sex:
        if sex=='1':
            jianli.sex=True
        else:
            jianli.sex=False
    if zhuanye:
        jianli.zhuanye=zhuanye
    if workage:
        jianli.workage=int(workage)
    if minzu:
        jianli.minzu=minzu
    if tel:
        jianli.tel=tel
    if email:
        jianli.email=email
    if desc:
        jianli.desc=desc
    jianli.save()
    jiaoyulist=[]
    for i in range(5):
        jiaoyuid=request.POST.get('jiaoyuid'+str(i),'')
        jiaoyudateqj=request.POST.get('jiaoyudateqj'+str(i),'')
        jiaoyuindex=request.POST.get('jiaoyuindex'+str(i),'')
        jiaoyuworkcontent=request.POST.get('jiaoyuworkcontent'+str(i),'')
        if jiaoyuid:
            jiaoyu=JiaoYu.objects.get(pk=jiaoyuid)
        else:
            jiaoyu=JiaoYu()
        jiaoyu.jianli=jianli
        if jiaoyudateqj:
            jiaoyu.dateqj=jiaoyudateqj
        if jiaoyuindex:
            jiaoyu.index=str(i)
        if jiaoyuworkcontent:
            jiaoyu.workcontent=jiaoyuworkcontent
        if jiaoyudateqj and jiaoyuworkcontent:
            jiaoyu.save()
        jiaoyulist.append(jiaoyu)
    worklist=[]
    for i in range(5):
        workid=request.POST.get('workid'+str(i),'')
        workdateqj=request.POST.get('workdateqj'+str(i),'')
        workindex=request.POST.get('workindex'+str(i),'')
        workworkname=request.POST.get('workworkname'+str(i),'')
        workworkcontent=request.POST.get('workworkcontent'+str(i),'')
        if workid:
            work=WorkJingYan.objects.get(pk=workid)
        else:
            work=WorkJingYan()
        work.jianli=jianli
        if workdateqj:
            work.dateqj=workdateqj
        if workindex:
            work.index=str(i)
        if workworkcontent:
            work.workcontent=workworkcontent
        if workworkname:
            work.workname=workworkname
        if workdateqj and workworkname and workworkcontent:
            work.save()
        worklist.append(work)
    request.session[RESULT]=SUCCESS
    request.session[MSG]=u'保存成功。'
    return render_to_response('jianli.html',getSessionMsg(request,{'jianli':jianli,'jiaoyulist':jiaoyulist,'worklist':worklist}),RequestContext(request,{}))


@login_required
def addwork(request):
    '''
    添加职位
    '''
    workid=request.GET.get('work_id','')
    if workid:
        zhiwei=ZhiWei.objects.get(pk=workid)
    else:
        zhiwei=ZhiWei()
    return render_to_response('work.html',getSessionMsg(request,{'work':zhiwei}),RequestContext(request,{}))

@login_required
def savework(request):
    '''
    保存职位
    '''
    id=request.POST.get('id','')
    user=request.user
    zhiwei=request.POST.get('zhiwei','')
    workadd=request.POST.get('workadd','')
    xingzhi=request.POST.get('xingzhi','')
    num=request.POST.get('num','')
    price1=request.POST.get('price1','')
    price2=request.POST.get('price2','')
    workage=request.POST.get('workage','')
    desc=request.POST.get('desc','')
    if id:
        work=ZhiWei.objects.get(pk=id)
    else:
        work=ZhiWei()
    work.user=user
    if zhiwei:
        work.zhiwei=zhiwei
    if workadd:
        work.workadd=workadd
    if xingzhi:
        work.xingzhi=xingzhi
    else:
        work.xingzhi=''
    if workage:
        work.workage=int(workage)
    if num:
        work.num=int(num)
    if price1:
        work.price1=int(price1)
    if price2:
        work.price2=int(price2)
    if desc:
        work.desc=desc
    work.save()

    request.session[RESULT]=SUCCESS
    request.session[MSG]=u'保存成功。'
    return render_to_response('work.html',getSessionMsg(request,{'work':work}),RequestContext(request,{}))

@login_required
def updatecompany(request):
    '''
    公司信息
    '''
    user=request.user
    if hasattr(user,'business'):
        business=user.business
    else:
        business=Business()
    return render_to_response('business.html',getSessionMsg(request,{'business':business}),RequestContext(request,{}))

@login_required
def savecompany(request):
    '''
    保存公司信息
    '''
    #id=request.POST.get('id','')
    user=request.user
    name=request.POST.get('name','')
    type=request.POST.get('type','')
    num=request.POST.get('num','')
    url=request.POST.get('url','')

    desc=request.POST.get('desc','')
    if hasattr(user,'business'):
        business=user.business
    else:
        business=Business()
    business.user=user
    if name:
        business.name=name
    if type:
        business.type=type
    if url:
        business.url=url


    if num:
        business.num=int(num)

    if desc:
        business.desc=desc
    business.save()

    request.session[RESULT]=SUCCESS
    request.session[MSG]=u'保存成功。'
    return render_to_response('business.html',getSessionMsg(request,{'business':business}),RequestContext(request,{}))
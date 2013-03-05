#coding=utf-8
# Create your views here.
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from pin.models import LookRecord
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
    return render_to_response('index.html',RequestContext(request,{}))


@login_required
def jianlilist(request):
    '''
    简历列表界面
    '''
    list=JianLi.objects.filter(user=request.user)
    return render_to_response('jianlilist.html',getSessionMsg(request,{'list':list}),RequestContext(request,{}))

@login_required
def lookjianli(request):
    '''
    简历列表界面
    '''
    jianliid=request.GET.get('jianli_id','')
    jiaoyulist=[]
    worklist=[]

    if jianliid and 0<JianLi.objects.filter(pk=jianliid).count():
        jianli=JianLi.objects.get(pk=jianliid)
        for j in JiaoYu.objects.filter(jianli=jianli):
            jiaoyulist.append(j)
        for j in WorkJingYan.objects.filter(jianli=jianli):
            worklist.append(j)
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
    if id:
        jianli=JianLi.objects.get(pk=id)
    else:
        jianli=JianLi()
    jianli.user=user
    if name:
        jianli.name=name
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
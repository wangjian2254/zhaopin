#coding=utf-8
# Create your views here.
import datetime
import json
import urllib
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from zhaopin.pin.models import Column, News
from zhaopin.pin.tools import getSessionMsg, RESULT, SUCCESS, MSG, WARN
from zhaopin.pin.models import Replay
from zhaopin.pin.models import LookRecord, ZhiWei, WorkLookRecord, Business
from zhaopin.pin.models import JianLi, JiaoYu, WorkJingYan


def index(request):
    newzhiweilist=ZhiWei.objects.filter(ispub=True).order_by('-updatetime')[:13]
    newjianlilist=JianLi.objects.filter(ispub=True).order_by('-updatetime')[:10]
    responsedic={'newzhiweilist':newzhiweilist,'newjianlilist':newjianlilist}
    for column in Column.objects.all():
        responsedic[column.code]=column
        column.list=News.objects.filter(column=column).filter(ispub=True).order_by('-updatetime')[:10]
    return render_to_response('index.html',getSessionMsg(request,responsedic),RequestContext(request,{}))


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
    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return render_to_response('worklook.html',getSessionMsg(request,{'obj':work,'objtype':'work','business':business}),RequestContext(request,{}))


@login_required
@csrf_exempt
def toudijianli(request):
    uid=request.REQUEST.get('uid','')
    work_id=request.REQUEST.get('work_id','')
    jianli_id=request.REQUEST.get('jianli_id','')
    if 1==ZhiWei.objects.filter(pk=work_id).count() and 1==JianLi.objects.filter(pk=jianli_id).count():
        worklook=WorkLookRecord()
        worklook.jianli=JianLi.objects.get(pk=jianli_id)
        worklook.zhiwei=ZhiWei.objects.get(pk=work_id)
        if 0<WorkLookRecord.objects.filter(jianli=worklook.jianli).filter(zhiwei=worklook.zhiwei).count():
            return HttpResponse('{"success":false,"msg":"%s"}'%(u'已经投递过简历了。',))

        worklook.updatetime=datetime.datetime.now()
        worklook.save()
        zhiwei=ZhiWei.objects.get(pk=work_id)
        ZhiWei.objects.filter(pk=work_id).update(looknum=zhiwei.looknum+1)
        return HttpResponse('{"success":true,"msg":"%s"}'%(u'提交简历完成。',))
    else:
        return HttpResponse('{"success":false,"msg":"%s"}'%(u'职位或者简历不存在。',))


@login_required
def selectJianli(request):
    work_id=request.GET.get('work_id','')
    uid=request.GET.get('uid','')
    list=JianLi.objects.filter(user=request.user)
    return render_to_response('selectJianli.html',{'uid':uid,'work':work_id,'list':list})

@login_required
def toudilist(request):
    start=request.REQUEST.get('start',1)
    start=int(start)
    work_id=request.REQUEST.get('work_id','')
    work=ZhiWei.objects.get(pk=work_id)
    list=WorkLookRecord.objects.filter(zhiwei=work)
    page=Paginator(list,20)
    currentpage=page.page(start)
    query={'work_id':work_id}
    querystr=urllib.urlencode(query)

    return render_to_response('toudijianlilist.html',getSessionMsg(request,{'querystr':querystr,'work':work,'page':page,'currentpage':currentpage}),RequestContext(request,{}))

@login_required
def jianlilist(request):
    '''
    简历列表界面
    '''
    list=JianLi.objects.filter(user=request.user)
    return render_to_response('jianlilist.html',getSessionMsg(request,{'list':list}),RequestContext(request,{}))


def lookjianli(request):
    '''
    简历界面
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
        if request.user.is_authenticated() and hasattr(request.user,'person') and request.user.person.type==2:
            if jianli.pk not in  request.session.get('lookjianli',set()):
                lookrecord=LookRecord()
                lookrecord.jianli=jianli
                lookrecord.user=request.user
                lookrecord.updatetime=datetime.datetime.now()
                lookrecord.save()
                JianLi.objects.filter(pk=jianliid).update(looknum=jianli.looknum+1)
                s=request.session.get('lookjianli',set())
                s.add(jianli.pk)
                request.session['lookjianli']=s

    else:
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作失败，未找到简历，或简历已经被删除。'
    return render_to_response('jianlilook.html',getSessionMsg(request,{'obj':jianli,
                                                'objtype':'jianli','jiaoyulist':jiaoyulist,'worklist':worklist}),RequestContext(request,{}))



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
        if jiaoyuid and not (jiaoyudateqj or jiaoyuworkcontent):
            jiaoyu.delete()
            jiaoyu=JiaoYu()
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
        if workid and not (workdateqj or workworkname or workworkcontent):
            work.delete()
            work=WorkJingYan()
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


def jianliRecodelook(request):
    '''
    保存公司信息
    '''
    start=request.REQUEST.get('start',1)
    start=int(start)
    id=request.GET.get('jianli_id','')
    jianli=JianLi.objects.get(pk=id)
    list=LookRecord.objects.filter(jianli=jianli)
    page=Paginator(list,20)
    currentpage=page.page(start)
    query={'jianli_id':id}
    querystr=urllib.urlencode(query)


    return render_to_response('businesslist.html',getSessionMsg(request,{'querystr':querystr,'jianli':jianli,'start':start,'page':page,'currentpage':currentpage}),RequestContext(request,{}))



def companylook(request):
    '''
    查看公司信息
    '''
    id=request.GET.get('company_id','')
    business=Business.objects.get(pk=id)
    list=ZhiWei.objects.filter(user=business.user).filter(ispub=True)
    closelist=ZhiWei.objects.filter(user=business.user).filter(ispub=False)


    return render_to_response('businesslook.html',getSessionMsg(request,{'business':business,'obj':business,'objtype':'business','list':list,'closelist':closelist}),RequestContext(request,{}))


@login_required
def commentAdd(request):
    if hasattr(request,'environ'):
        fromurl=request.environ.get('HTTP_REFERER','/')
    if hasattr(request,'META'):
        fromurl=request.META.get('HTTP_REFERER','/')
    type=request.POST.get('type','')
    content=request.POST.get('content','')
#    content=content.replace('<','&lt;')
#    content=content.replace('>','&gt;')
    face=request.POST.get('face','')
    pk=request.POST.get('pk','')
    if pk and content and type:
        replay=Replay()
        replay.user=request.user
        replay.objid=int(pk)
        if face:
            replay.face=int(face)
        replay.content=content
        replay.type=type
        replay.save()
    return HttpResponseRedirect(fromurl)

@csrf_exempt
def replay(request):
    objid=request.POST.get('pk','')
    type=request.POST.get('type','')
    replaynum=Replay.objects.filter(objid=int(objid)).filter(type=type).count()
    return  HttpResponse('{"success":true,"replaynum":%s}'%replaynum)

@csrf_exempt
def commentList(request):
    type=request.POST.get('type','')
    objid=request.POST.get('pk','')
    replaylist=[]
    for replay in Replay.objects.filter(type=type).filter(objid=objid).order_by('-updatetime'):
        rmap={}
        rmap['id']=replay.pk
        rmap['face']=replay.face
        rmap['content']=replay.content
        rmap['createDate']=replay.updatetime.strftime('%Y年%m月%d日 %H:%M:%S')
        rmap['fatherid']=replay.father_id
        rmap['userid']=replay.user.pk
        rmap['username']=replay.user.username
        replaylist.append(rmap)
    html=json.dumps(replaylist)
    return  HttpResponse(html)


def newslist(request):
    '''
    栏目下新闻列表
    '''
    start=request.REQUEST.get('start',1)
    start=int(start)
    id=request.GET.get('column_id','')
    column=Column.objects.get(pk=id)
    list=News.objects.filter(column=column).filter(ispub=True)
    page=Paginator(list,20)
    currentpage=page.page(start)
    query={'column_id':id}
    querystr=urllib.urlencode(query)

    return render_to_response('newslist.html',getSessionMsg(request,{'querystr':querystr,'column':column,'start':start,'page':page,'currentpage':currentpage}),RequestContext(request,{}))

def newslook(request):
    '''
    新闻内容查看
    '''
    id=request.GET.get('news_id','')

    if 0==News.objects.filter(pk=id).count() or not News.objects.get(pk=id).ispub:
        request.session[RESULT]=WARN
        request.session[MSG]=u'新闻不存在。'
        if hasattr(request,'environ'):
            fromurl=request.environ.get('HTTP_REFERER','/')
        if hasattr(request,'META'):
            fromurl=request.META.get('HTTP_REFERER','/')
        return  HttpResponseRedirect(fromurl)

    news=News.objects.get(pk=id)
    column=news.column

    return render_to_response('newslook.html',getSessionMsg(request,{'column':column,'obj':news,'objtype':'news'}),RequestContext(request,{}))

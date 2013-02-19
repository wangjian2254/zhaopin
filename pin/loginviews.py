#coding=utf-8
# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = '王健'



def reg(request):
    return render_to_response('reg.html',{},RequestContext(request))

def reg2(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    r_password=request.POST.get('r_password','')
    fail_dict= {'msg': '', 'username': username}
    if username and password and r_password:
        if len(password)<6:
            fail_dict['msg']=u'密码长度应该大于6位字符串'
        elif password==r_password:
            if username.find('@')==-1:
                fail_dict['msg']=u'电子邮箱格式不正确'
            elif 1==User.objects.filter(username=username).count():
                fail_dict['msg']=u'电子邮箱已经被注册过了'
            else:
                user=User()
                user.username=username
                user.set_password(password)
                user.is_active=True
                user.email=username
                user.save()
                return render_to_response('reg_success.html',{'msg':u'注册成功'},RequestContext(request,{}))
        else:
            fail_dict['msg']=u'密码与确认密码不一致'
    else:
        fail_dict['msg']=u'请输入完整信息'
    return render_to_response('reg.html',RequestContext(request,fail_dict))
    #

  
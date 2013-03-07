#coding=utf-8
# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth import  login as auth_login, authenticate
from pin.models import Person

__author__ = '张藐方'



def reg(request):
    return render_to_response('reg.html',{},RequestContext(request))

def reg2(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    r_password=request.POST.get('r_password','')
    type=request.POST.get('type','')
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
                person=Person()
                person.user=user
                person.type=int(type)
                person.save()
                auth_login(request,authenticate(username=user.username,password=password))
                return render_to_response('reg_success.html',{'msg':u'注册成功'},RequestContext(request,{}))
        else:
            fail_dict['msg']=u'密码与确认密码不一致'
    else:
        fail_dict['msg']=u'请输入完整信息'
    return render_to_response('reg.html',RequestContext(request,fail_dict))
    #

  
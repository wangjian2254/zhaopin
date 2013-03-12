#coding=utf-8
import logging
import urllib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from zhaopin.pin.tools import getSessionMsg
from zhaopin.pin.tools import SUCCESS, MSG, RESULT,WARN
from zhaopin.pin.models import WeiBo
#from zhaopin.weibo import APIClient

#from t4py.tblog.tblog import TBlog
#from weibopy.api import API
#from t4py.http.oauth import OAuthToken
#from t4py.example import json

__author__ = 'wangjian2254'

#from weibopy import OAuthHandler, oauth, WeibopError
from qqweibo.auth import  OAuthHandler as qqOAuthHandler
from qqweibo.api import  API as qqAPI
import HTMLParser
html_parser = HTMLParser.HTMLParser()


#########新浪设置
xlconsumer_key = '3881792210' # 设置你申请的appkey
xlconsumer_secret = '4b6f5934f4787fb3f4a4d5aec5e79809' # 设置你申请的appkey对于的secret
#
#xlconsumer_key = '1163119853' # 设置你申请的appkey
#xlconsumer_secret = 'ba8e8dcf0994005fbeb1da3d45eef786' # 设置你申请的appkey对于的secret

######163网易
wyconsumer_key='qge2uc8ewt5nPwhI'
wyconsumer_secret='tl0WetROJtdqHXvqUp41WAIFKxRiwEgh'

#qq微博
qqconsumer_key='801095361'
qqconsumer_secret='f373f4aa6389ba8e3b0eae209d655f68'


#
#sinawebtext=u'[来自 @现在的生活就是个笑话 '+WEIBOURL+']'
#wywebtext=u'[来自 @这个生活就是个笑话 '+WEIBOURL+']'
#tengwebtext=u'[来自 @jokeinlive '+WEIBOURL+']'

'''
class WebOAuthHandler(OAuthHandler):
    user_id=None
    def get_authorization_url_with_callback(self, callback, signin_with_twitter=False):
        """Get the authorization URL to redirect the user"""
        try:
            # get the request token
            self.request_token = self._get_request_token()

            # build auth request and return as url
            if signin_with_twitter:
                url = self._get_oauth_url('authenticate')
            else:
                url = self._get_oauth_url('authorize')
            request = oauth.OAuthRequest.from_token_and_callback(
                token=self.request_token, callback=callback, http_url=url
            )
            return request.to_url()
        except Exception, e:
            raise WeibopError(e)


def _oauth():
    """获取oauth认证类"""
    return WebOAuthHandler(xlconsumer_key, xlconsumer_secret)
'''
def setWeibo(request):
    content=request.GET.get("content","")
    if hasattr(request,'environ'):
        fromurl=request.environ.get('HTTP_REFERER','/')
    if hasattr(request,'META'):
        fromurl=request.META.get('HTTP_REFERER','/')
    return render_to_response('pubweibo.html',getSessionMsg(request,{'fromurl':fromurl,'content':content}),RequestContext(request,{}))
def pubWeibo(request):
    try:
        fromurl=request.REQUEST.get('fromurl','/')
        sendWeibo(request,"%s %s"%(fromurl,request.REQUEST.get("content","")))
        request.session[RESULT]=SUCCESS
        request.session[MSG]=u'微博发布成功。'
        return render_to_response('pubweibo_result.html',getSessionMsg(request,{}),RequestContext(request,{}))
#        return HttpResponse('{"success":true,"msg":%s}'%(u'微博发布成功。',))
    except Exception,e:
        logging.info('empty'+str(e))
        request.session[RESULT]=WARN
        request.session[MSG]=u'操作成功。'
        return render_to_response('pubweibo_result.html',getSessionMsg(request,{}),RequestContext(request,{}))
#        return HttpResponse('{"success":false,"msg":%s}'%(u'微博发布失败。',))





@login_required
def weiboLogin(request):
    # 保存最初的登录url，以便认证成功后跳转回来
#    back_to_url = _get_referer_url(request)
#    request.session['login_back_to_url'] = back_to_url
    website=request.REQUEST.get('website')
    if hasattr(request,'environ'):
        host_url='http://'+request.environ.get('HTTP_HOST','/')
    if hasattr(request,'META'):
        host_url='http://'+request.META.get('HTTP_HOST','/')
    fromurl=request.REQUEST.get('fromurl',None)
    if not fromurl:
        if hasattr(request,'environ'):
            fromurl=request.environ.get('HTTP_REFERER','/')
        if hasattr(request,'META'):
            fromurl=request.META.get('HTTP_REFERER','/')
#    fromurl=''
    fromurl=urllib.urlencode({'fromurl':fromurl})
    # 获取oauth认证url
#    setting=Setting().all().fetch(1)
#    if setting:
#        setting=setting[0]
#    else:
#        return
    if 'sina'==website:
        return
#        login_backurl =host_url+'/weibo/login_check?website=sina'
#        login_backurl+="&uid=%s&%s"%(request.user.pk,fromurl)
#        auth_client = APIClient(xlconsumer_key,xlconsumer_secret,login_backurl)
#        auth_url = auth_client.get_authorize_url()
#        # 保存request_token，用户登录后需要使用它来获取access_token
##        user_request_token=request.session.get(website+"_request_token1","")
##        if not user_request_token:
##            user_request_token= auth_client.request_token
##            request.session[website+"_request_token1"]=user_request_token
#        # 跳转到登录页面
#        return HttpResponseRedirect(auth_url)
    elif 'wy'==website:
        return
#        login_backurl =host_url+'/weibo/login_check?website=wy'
#        login_backurl+="&uid=%s&%s"%(request.user.pk,fromurl)
#        t = TBlog(wyconsumer_key, wyconsumer_secret)
#        t.get_request_token()
#        url=t.get_auth_url(login_backurl)
#        # 保存request_token，用户登录后需要使用它来获取access_token
#        user_request_token=request.session.get(website+"_request_token3")
#        if not user_request_token:
#            user_request_token= t
#            request.session[website+"_request_token3"]=user_request_token
#        return HttpResponseRedirect(url)
    elif 'teng'==website:
        login_backurl=host_url+'/weibo/login_check?website=teng'
        login_backurl+="&uid=%s&%s"%(request.user.pk,fromurl)
        auth=qqOAuthHandler(qqconsumer_key,qqconsumer_secret,callback=login_backurl)
        url=auth.get_authorization_url()
        # 保存request_token，用户登录后需要使用它来获取access_token
        request.session[website+"_request_token4"]=auth
        return HttpResponseRedirect(url)

def Login_check(request):
    """
    验证 授权
    """
    website=request.GET.get('website')
    fromurl=request.GET.get('fromurl')
    uid=request.GET.get('uid')
    request.session[RESULT]=WARN
    from django.contrib.auth.models import User
    if 0== User.objects.filter(pk=uid).count():
        request.session[MSG]=u'微博授权失败，用户不存在。'
        return
    user=User.objects.get(pk=uid)
    weibolist=WeiBo.objects.filter(user=user).filter(type=website)[:1]
    if 1==len(weibolist):
        weibo=weibolist[0]
    else:
        weibo=WeiBo()
        weibo.type=website
        weibo.user=user
    if 'sina'==website:
        return
        """用户成功登录授权后，会回调此方法，获取access_token，完成授权"""
        # http://mk2.com/?oauth_token=c30fa6d693ae9c23dd0982dae6a1c5f9&oauth_verifier=603896
#        code = request.GET.get('code', None)
#        auth_client = APIClient(xlconsumer_key,xlconsumer_secret)
#        r=auth_client.request_access_token(code)
#        access_token=r.access_token
#        # 设置之前保存在session的request_token
#    #    request_token = request.session['oauth_request_token']
##        request_token=request.session.get(website+"_request_token1",None)
##        if not request_token:
##            return
##        memcache.Client().delete(website+"_request_token1")
#    #    del request.session['oauth_request_token']
#
##        auth_client.set_request_token(request_token.key, request_token.secret)
##        access_token = auth_client.get_access_token(verifier)
#        # 保存access_token，以后访问只需使用access_token即可
#
#        weibo.token0=access_token.secret
#        weibo.token1=access_token.key
#        weibo.token2=auth_client.user_id
#        weibo.save()
#        request.session[MSG]=u'新浪微博授权完成。'
    elif 'wy'==website:
        return
#        t = TBlog(weboSetting.wyconsumer_key, weboSetting.wyconsumer_secret)
#        request_token=request.session.get(website+"_request_token3")
#        if not request_token:
#            return
##        memcache.Client().delete(website+"_request_token3")
##        t._request_handler.request_token=request_token
##        request_token.get_auth_url()
##        pin=self.request.get('pin', None)
#        pin=request.GET.get('oauth_token', None)
#        s=request_token.get_access_token(pin)
#        weibo.token0=s.secret
#        weibo.token1=s.key
#        weibo.save()
#        request.session[MSG]=u'网易微博授权完成。'
    elif 'teng'==website:
        request_token=request.session.get(website+"_request_token4")
        if not request_token:
            return
        verifier = request.GET.get('oauth_verifier', None)
        access_token = request_token.get_access_token(verifier)
        weibo.token0=access_token.secret
        weibo.token1=access_token.key
        #userAccessToken.qquserid=auth_client.user_id
        weibo.save()
        request.session[MSG]=u'腾讯微博授权完成。'
    request.session[RESULT]=SUCCESS
    return HttpResponseRedirect(fromurl)

def sendWeibo(request,text,imgno=None):
#    if 'sina' in request.REQUEST.get('website','').split(',') and not sendSinaWeibo(request,text,imgno):
#        sendSinaWeibo(request,text)
#    if  'wy' in request.REQUEST.get('website','').split(',') and  not sendWangYiWeibo(request,text,imgno):
#        sendWangYiWeibo(serequestlf,text)
    if  'teng' in request.REQUEST.get('website','').split(',') and  not sendQQWeibo(request,text,imgno):
        sendQQWeibo(request,text)
#def sendSinaWeibo(request,text,imgno=None):
#    weiboquery=WeiBo.objects.filter(user=request.user).filter(type="sina")
#    if 0==weiboquery.count():
#        return True
#    weibo=weiboquery[0]
#    auth = OAuthHandler(xlconsumer_key, xlconsumer_secret)
#    auth.setToken(weibo.token1, weibo.token0)
#    api = API(auth)
#
#
#
#    try:
#        if imgno:
##                image = urlfetch.fetch(
##                    url =imgno,
##                    payload = {},
##                    method = urlfetch.GET,
##                    headers = {'Content-Type':'application/x-www-form-urlencoded',
##                               'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6'},
##                    follow_redirects = True,deadline=10)
##                if image.status_code==200:
##                    bf=db.Blob(image.content)
#                    result=api.upload(filename=imgno,status=text.encode('utf-8'))
##                else:
##                    result=self.api.update_status(status=text[:139].encode('utf-8'))
#        else:
#            result=api.update_status(status=text.encode('utf-8'))
#    except Exception,e:
#        logging.info('sina'+str(e))
#        if str(e).find('40025')==-1:
##            self.error(500)
#            return False
#    else:
#        return True
#
#def sendWangYiWeibo(request,text,imgno=None):
#    weiboquery=WeiBo.objects.filter(user=request.user).filter(type="wy")
#    if 0==weiboquery.count():
#        return True
#    weibo=weiboquery[0]
#    t = TBlog(wyconsumer_key,  wyconsumer_secret)
#    t._request_handler.access_token = OAuthToken(weibo.token1, weibo.token0)
#    try:
#        imgdata=''
##        if imgno:
##                image = urlfetch.fetch(url=setting[0].dbphotoWebSite+'/s/'+imgno,deadline=10)
##
##                if image.status_code == 200:
##                    logging.info(setting[0].dbphotoWebSite+'/s/'+imgno)
##                    bf=db.Blob(image.content)
#        if imgno:
#            imgulr=json.read(t.statuses_upload(imgno))
#            upload_image_url=imgulr['upload_image_url']
#            text=upload_image_url+' '+text
#
#        result=t.statuses_update({'status':text.encode('utf-8')})
#    except Exception,e:
#        logging.info('wy:'+str(e))
##        logging.info('wy'+str(result))
##        if str(result).find('40025')==-1:
##        self.error(500)
#        return False
#    else:
#        return True
def sendQQWeibo(request,text,imgno=None):
    weiboquery=WeiBo.objects.filter(user=request.user).filter(type="teng")
    if 0==weiboquery.count():
        return True
    weibo=weiboquery[0]
    auth = qqOAuthHandler(qqconsumer_key, qqconsumer_secret)
    auth.setToken(weibo.token1, weibo.token0)
    api = qqAPI(auth)



    try:
        if imgno:
#                image = urlfetch.fetch(
#                    url =setting[0].dbphotoWebSite+'/s/'+imgno,
#                    payload = {},
#                    method = urlfetch.GET,
#                    headers = {'Content-Type':'application/x-www-form-urlencoded',
#                               'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6'},
#                    follow_redirects = True,deadline=10)
#                if image.status_code==200:
#                    bf=db.Blob(image.content)
            result=api._t_add_pic(filename=imgno,content=text.encode('utf-8'),clientip='64.233.172.33')
#                else:
#                    result=self.api.update_status(status=text[:139].encode('utf-8'))
        else:
            result=api._t_add(content=text.encode('utf-8'),clientip='64.233.172.33')
    except Exception,e:
        logging.info('qq'+str(e))
        if str(e).find('40025')==-1:
            return False
    else:
        return True
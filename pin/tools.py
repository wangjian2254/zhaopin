#coding=utf-8
#author:u'王健'
#Date: 13-3-10
#Time: 上午12:08
__author__ = u'王健'
RESULT='result'
MSG='msg'
SUCCESS='succeed'
WARN='warning'
def getSessionMsg(request,requestdic):
    requestdic[RESULT]=request.session.get(RESULT, '')
    requestdic[MSG]=request.session.get(MSG, '')
    if request.session.has_key(RESULT):
        del request.session[RESULT]
    if request.session.has_key(MSG):
        del request.session[MSG]
    return requestdic

  
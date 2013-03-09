#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class UeditorFile(models.Model):
    filename=models.CharField(max_length=200,verbose_name=u'原文件名')
    realfilename=models.CharField(max_length=400,verbose_name=u'实际存储的文件名')
    title=models.CharField(max_length=100,null=True,blank=True,verbose_name=u'文件描述')
    createTime=models.DateTimeField(auto_now_add=True,verbose_name=u'文件添加时间')
    type=models.CharField(default='image',max_length=10,verbose_name=u'文件类型',help_text=u'文件类型：图片(image)、附件(att)')
    user=models.ForeignKey(User,verbose_name=u'上传人员')
    size=models.IntegerField(verbose_name=u'文件大小')

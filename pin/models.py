from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    user=models.OneToOneField(User,verbose_name=u'用户身份')
    type=models.CharField(default='search',max_length=10)



class JianLi(models.Model):#简历
    user=models.ForeignKey(User,verbose_name=u'简历人')
    username=models.CharField(max_length=10,verbose_name=u'姓名')
    age=models.DateField(verbose_name=u'出生年月日')
    sex=models.BooleanField(default=False,verbose_name=u'性别')
    zhuanye=models.CharField(max_length=10)
    workage=models.IntegerField()
    minzu=models.CharField(max_length=10)
    tel=models.CharField(max_length=11)
    email=models.EmailField()
    jiguan=models.CharField(max_length=10)


class ZhiWei(models.Model):
    workadd=models.CharField(max_length=10,verbose_name=u'工作地点')
    zhiwei=models.CharField(max_length=20,verbose_name=u'应聘职位')
    xingzhi=models.CharField(max_length=10,verbose_name=u'工作性质')

class WorkJingYan(models.Model):
    index=models.IntegerField(default=0,verbose_name=u'排序')
    dateqj=models.CharField(max_length=30,verbose_name=u'日期区间')
    workcontent=models.CharField(max_length=200,verbose_name=u'工作内容')




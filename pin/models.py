#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    user=models.OneToOneField(User,verbose_name=u'用户身份')
    type=models.IntegerField(default=1,max_length=10,verbose_name=u'用户类别',help_text=u'1 是找工作的，2 是企业用户 提供工作')


class Business(models.Model):
    user=models.OneToOneField(User,verbose_name=u'用户身份')
    name=models.CharField(max_length=50,verbose_name=u'企业名称',help_text=u'企业的名称')
    type=models.CharField(max_length=10,verbose_name=u'企业类型',help_text=u'私企、国企、外企')
    desc=models.CharField(max_length=1000,verbose_name=u'企业描述',help_text=u'描述企业性质、经营范围')
    num=models.CharField(max_length=10,verbose_name=u'公司规模',help_text=u'人数规模')
    url=models.URLField(verbose_name=u'公司网站',blank=True,null=True,help_text=u'人数规模')

class WeiBo(models.Model):
    user=models.OneToOneField(User,verbose_name=u'用户身份')
    type=models.CharField(max_length=10,blank=True,null=True,verbose_name=u'微博类型',help_text=u'新浪、腾讯等等')
    token0=models.CharField(max_length=200,blank=True,null=True,verbose_name=u'微博授权1')
    token1=models.CharField(max_length=200,blank=True,null=True,verbose_name=u'微博授权2')
    token3=models.CharField(max_length=200,blank=True,null=True,verbose_name=u'微博授权3')

class JianLi(models.Model):#简历
    user=models.ForeignKey(User,verbose_name=u'简历人')
    name=models.CharField(max_length=10,verbose_name=u'职位名称')
    updatetime=models.DateTimeField(auto_now=True)
    username=models.CharField(max_length=10,verbose_name=u'姓名')
    age=models.DateField(verbose_name=u'出生年月日')
    sex=models.BooleanField(default=False,verbose_name=u'性别')
    zhuanye=models.CharField(max_length=10,verbose_name=u'专业')
    workage=models.IntegerField(verbose_name=u'工作年龄')
    minzu=models.CharField(max_length=10,verbose_name=u'民族')
    tel=models.CharField(max_length=11,verbose_name=u'联系方式，手机')
    email=models.EmailField(verbose_name=u'电子邮件')
    xuewei=models.CharField(max_length=10,verbose_name=u'学位')
    workadd=models.CharField(max_length=10,verbose_name=u'工作地点')
    desc=models.CharField(max_length=2000,verbose_name=u'自我描述')
    looknum=models.IntegerField(default=0,verbose_name=u'被浏览次数')
    ispub=models.BooleanField(default=True,verbose_name=u'是否公开')

class LookRecord(models.Model):
    jianli=models.ForeignKey(JianLi)
    user=models.ForeignKey(User,verbose_name=u'浏览者')
    updatetime=models.DateTimeField(auto_created=True)

class JiaoYu(models.Model):
    '''
    简历相关的教育经历
    '''
    jianli=models.ForeignKey(JianLi)
    index=models.IntegerField(default=0,verbose_name=u'排序',help_text=u'')
    dateqj=models.CharField(max_length=30,verbose_name=u'日期区间',help_text=u'教育开始和结束的日期')
    workcontent=models.CharField(max_length=200,verbose_name=u'受教育内容',help_text=u'受教育的描述，高中、大学、培训……')

class WorkJingYan(models.Model):
    '''
    简历相关的工作经历
    '''
    jianli=models.ForeignKey(JianLi)
    index=models.IntegerField(default=0,verbose_name=u'排序',help_text=u'')
    dateqj=models.CharField(max_length=30,verbose_name=u'日期区间',help_text=u'工作开始和结束的日期')
    workname=models.CharField(max_length=30,verbose_name=u'公司名称',help_text=u'公司名称')
    workcontent=models.CharField(max_length=200,verbose_name=u'工作内容',help_text=u'工作的描述')

class ZhiWei(models.Model):
    user=models.ForeignKey(User,verbose_name=u'职位发布人')
    workadd=models.CharField(max_length=10,verbose_name=u'工作地点',help_text=u'工作地点')
    zhiwei=models.CharField(max_length=20,verbose_name=u'工作职位',help_text=u'提供的工作职位')
    xingzhi=models.CharField(max_length=10,verbose_name=u'工作性质',help_text=u'工作的性质，兼职、全职')
    num=models.IntegerField(verbose_name=u'需要人数',help_text=u'该职位需要招聘的人数')
    workage=models.IntegerField(verbose_name=u'最低工作年龄',help_text=u'该职位需要最低工作年龄')
    price1=models.IntegerField(verbose_name=u'薪水范围起',blank=True,null=True,help_text=u'提供的薪水范围')
    price2=models.IntegerField(verbose_name=u'薪水范围止',blank=True,null=True,help_text=u'提供的薪水范围')
    desc=models.CharField(max_length=2000,verbose_name=u'自我描述')
    looknum=models.IntegerField(default=0,verbose_name=u'被浏览次数')
    ispub=models.BooleanField(default=True,verbose_name=u'是否公开')
    updatetime=models.DateTimeField(auto_now=True,verbose_name=u'最后修改时间')


class WorkLookRecord(models.Model):
    zhiwei=models.ForeignKey(ZhiWei)
    user=models.ForeignKey(User,verbose_name=u'浏览者')
    updatetime=models.DateTimeField(auto_created=True)

class Replay(models.Model):
    user=models.ForeignKey(User)
    face=models.IntegerField(default=1,verbose_name=u'表情')
    objid=models.IntegerField(verbose_name=u'评论的目标id')
    type=models.CharField(max_length=10,verbose_name=u'评论主体',help_text=u'jianli、work')
    content=models.CharField(max_length=500,verbose_name=u'评论内容')
    updatetime=models.DateTimeField(auto_now=True,verbose_name=u'评论时间')



class Column(models.Model):
    name=models.CharField(max_length=10,verbose_name=u'栏目名称')
    code=models.CharField(max_length=10,verbose_name=u'栏目代码',help_text=u'templates 中使用')
    class Admin():
        pass
    class Meta():
        verbose_name='栏目'
        verbose_name_plural='栏目'

    def __unicode__(self):
        return self.name
class News(models.Model):
    title=models.CharField(max_length=50,verbose_name=u'标题')
    column=models.ForeignKey(Column)
    content=models.TextField(verbose_name=u'内容',blank=True,null=True)
    updatetime=models.DateTimeField(auto_created=True,verbose_name=u'最后修改日期')
    ispub=models.BooleanField(default=True,verbose_name=u'是否公开')
    class Admin():
        pass
    class Meta():
        verbose_name='文章'

#        verbose_name_plural='项目组'
    def __unicode__(self):
        return self.title


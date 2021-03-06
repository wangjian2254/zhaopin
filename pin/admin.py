#coding=utf-8
__author__ = '王健'
from zhaopin.pin.models import   Column,News
__author__ = 'WangJian'

from django.contrib import admin

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name','code')
class NewsAdmin(admin.ModelAdmin):
    ordering = ('-updatetime',)
    search_fields=('title',)
    list_display = ('title','updatetime','ispub')
    list_filter = ('column',)


admin.site.register(Column,ColumnAdmin)
admin.site.register(News,NewsAdmin)
#coding=utf-8
__author__ = '王健'

from django import template
from zhaopin.settings import MEDIA_URL
register=template.Library()

@register.filter(name='ueditorAll')
def ueditorAll(content,name):
    html='''
    <script type="text/javascript">
            <!--
            window.UEDITOR_HOME_URL = '%sueditor/';
            //-->
        </script>
        <script type="text/javascript" src="%sueditor/editor.min.js"></script>
        <script type="text/javascript" src="%sueditor/editor_config.js"></script>

        <link rel="stylesheet" href="%sueditor/themes/default/ueditor.css" />
    <script type="text/plain" id="id_%s" style="width:100%%" name="%s">%s</script><script type="text/javascript">
            var editor = new UE.ui.Editor();
            editor.render('id_%s');
        </script>'''%(MEDIA_URL,MEDIA_URL,MEDIA_URL,MEDIA_URL,name,name,(content.value() and [content.value()] or [''])[0],name)
    return html



@register.filter(name='ueditorReplay')
def ueditorReplay(content,name):
    html='''
    <script type="text/javascript">
            <!--
            window.UEDITOR_HOME_URL = '%sueditor/';
            //-->
        </script>
        <script type="text/javascript" src="%sueditor/editor.min.js"></script>
        <script type="text/javascript" src="%sueditor/editor_comment_config.js"></script>

        <link rel="stylesheet" href="%sueditor/themes/default/ueditor.css" />
    <script type="text/plain" id="u_editor" style="width:100%%" name="%s">%s</script><script type="text/javascript">
            var editor = new UE.ui.Editor();
            editor.render('u_editor');
        </script>'''%(MEDIA_URL,MEDIA_URL,MEDIA_URL,MEDIA_URL,name,content)
    return html

var ps='';
function register(e){
	e = e ? e : window.event;
	if(!validate_r()){
    	return;		
    }
    document.getElementById('RegDiv').style.display='none';
    ps='{username:"'+document.getElementById('username_r').value;
    ps+='",password:"'+document.getElementById('password_r').value;
    ps+='",newPassword:"'+document.getElementById('newPassword_r').value;
    ps+='",email:"'+document.getElementById('email').value;
    ps+='",telephone:"'+document.getElementById('telephone').value;
    ps+='",yzm:"'+document.getElementById('code_r').value;
    ps+='"}';
	sendRequest('HomePageAction.do?method=saveRegister','post',ps,register_handler,true,true);
}
function register_handler(xmlHttp){
	document.getElementById('bg').style.display='none';
	var o=eval("("+xmlHttp.responseText+")");
	if(o.success){
		document.getElementById('messageReg').innerHTML='注册成功,正在登陆...';
		
		document.getElementById('register_form').submit();
	}else{
		document.getElementById('RegDiv').style.display='block';
		alert(o.message);
	}
}
function registerKeySubmit(event){
	var evt = (event) ? event : ((window.event) ? window.event : "") //兼容IE和Firefox获得keyBoardEvent对象
	var key = event.keyCode?evt.keyCode:event.which; //兼容IE和Firefox获得keyBoardEvent对象的键值
	if (evt.keyCode == 13) {
		register(evt);       
	} 
}
function isEmail(strEmail) {
if (strEmail.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) != -1)
return true;
else
return false;
}
function validate_r(){
	if(document.getElementById('username_r').value==''){
		alert('用户名不能为空');
		return false
	}
	if(document.getElementById('password_r').value==''){
		alert('密码不能为空');
		return false
	}
	if(document.getElementById('newPassword_r').value==''){
		alert('确认密码不能为空');
		return false
	}
	if(document.getElementById('newPassword_r').value!=document.getElementById('password_r').value){
		alert('两次密码不一致');
		return false
	}
	if(document.getElementById('email').value==''){
		alert('电子邮箱不能为空');
		return false
	}
	if(!isEmail(document.getElementById('email').value)){
		alert('电子邮箱格式不正确');
		return false
	}
	if(document.getElementById('telephone').value==''){
		alert('电话不能为空');
		return false
	}
	if(document.getElementById('code_r').value==''){
		alert('验证码不能为空');
		return false
	}
	return true;
}
function input_over(e){
	e = e ? e : window.event; 
	if(!e){
		return;
	}
	var s= e.target ? e.target : e.srcElement;
	if(s.className.indexOf("input_focus")==-1){
		s.className="input_over";
	}
}
function input_out(e){
	e = e ? e : window.event;
	if(!e){
		return;
	}
	var s= e.target ? e.target : e.srcElement;
	if(s.className.indexOf("input_focus")==-1){
		s.className="";
	}
}
function input_focus(e){
	e = e ? e : window.event; 
	if(!e){
		return;
	}
	var s= e.target ? e.target : e.srcElement;
	s.className="input_focus";
}
function input_blur(e){
	e = e ? e : window.event; 
	if(!e){
		return;
	}
	var s= e.target ? e.target : e.srcElement;
	s.className="";
}
function showRegisterWin(){
	$('#dialog').dialog('open');
	
}

function restRegisterWin(){
	$('#register_form')[0].reset();
}
$(document).ready(function() {
		    $("#dialog").dialog({
		    	bgiframe:true,
				height:372,
				width:380,
//				hide: 'slide',
				resizable:false,
				modal: true,
				autoOpen: false,
				close:function(event,ui){
					$('#register_form')[0].reset();
				}
		    });
		    if($.browser.msie&&$.browser.version=='6.0'){
		    	$("#dialog").dialog({
					height:393
			    });
		    }
		    if($.browser.msie&&$.browser.version=='7.0'||$.browser.version=='8.0'){
		    	$("#dialog").dialog({
			    	height:380,
					width:384
			    });
		    }
		    $("#dialog").parent('.ui-widget').removeClass('ui-widget');
//		    document.getElementById('bg').style.display='block';
		 });
//HomePageAction.do?method=sendMail

var ps='';
function steppassword(e){
	e = e ? e : window.event;
	if(!validate_r()){
    	return;		
    }
//    document.getElementById('RegDiv').style.display='none';
    ps='{username:"'+document.getElementById('username').value;
    ps+='",email:"'+document.getElementById('email').value;
    ps+='",yzm:"'+document.getElementById('code').value;
    ps+='"}';
	sendRequest('HomePageAction.do?method=sendMail','post',ps,steppassword_handler,true,true);
}

function steppassword_handler(xmlHttp){
	document.getElementById('bg').style.display='none';
	var o=eval("("+xmlHttp.responseText+")");
	if(o.success){
		
		
		document.getElementById('email_form').submit();
	}else{
		document.getElementById('messageReg').innerHTML=o.message;
	}
}
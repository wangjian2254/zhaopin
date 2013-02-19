function createHttpRequest(){
   if(window.XMLHttpRequest){
        this.xmlHttp=new XMLHttpRequest();
    }
    else if(window.ActiveXObject){
       try{
           this.xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
       }
       catch(e){
          try{
            this.xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
           }
          catch(e){}
      }
   }
}
function sendRequest(url,method,data,handle,flag,mask){
   url= url ? url : "";
   if(url==""){
   	return;
   }
   if(mask){
   	document.getElementById('bg').style.display='block';
   }
   flag= flag===false ? false : true;
   method= method ? method : "get";
   data= data ? data : null;
   var xmlHttp=new createHttpRequest();
   var handleResponse= handle ? function(){
   	if(xmlHttp.xmlHttp.readyState==4){
	    if(xmlHttp.xmlHttp.status==200){
	    	//alert(xmlHttp.xmlHttp.responseText);
	    	try{
	    		var o=eval("("+xmlHttp.xmlHttp.responseText+")");
	    	}catch(e){
	    		alert(url);
	    	}
	    	//alert(o.message.message);
	    	handle(xmlHttp.xmlHttp);
	    }
	    else{
	       //alert("您的页面有异常");
	    }
  	}
   } : function(){
   	if(xmlHttp.xmlHttp.readyState==4){
	    if(xmlHttp.xmlHttp.status==200){
	    	try{
	    		var o=eval("("+xmlHttp.xmlHttp.responseText+")");
		    	if(o.message.success){
		    	}else{
		    		//alert(o.message.message);
		    	}
	    	}catch(e){
	    		alert(xmlHttp.xmlHttp.responseText);
	    	}
	    	
	    }
	    else{
	       //alert("您的页面有异常");
	    }
  	}
   };
   xmlHttp.xmlHttp.onreadystatechange=handleResponse;
   xmlHttp.xmlHttp.open(method,url,flag);
   xmlHttp.xmlHttp.setRequestHeader('Content-Type','application/application/json');
   xmlHttp.xmlHttp.setRequestHeader('X-Requested-With','XMLHttpRequest');
   setTimeout(function(){xmlHttp.xmlHttp.send(data)},0);
}
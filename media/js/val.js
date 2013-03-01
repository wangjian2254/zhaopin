function valSubmit(formid){
	var input_arr=[];
	if(formid){
		input_arr=$j('#'+formid+' input');
	}else{
		input_arr=$j('input');
	}
	if(input_arr.length==0){
		return true;
	}
	var input=null;
	var valdict=null;
	for(var i=0;i<input_arr.length;i++){
		input=input_arr[i];
		if(input.attributes.getNamedItem('val')==undefined){
			continue;
		}
		valdict=JSON2.parse(input.attributes.getNamedItem('val').value.replace(/'/g,'"'));
		if(valdict.required&&input.value==''){
			art.dialog({title:'提示',content:valdict.title+' 不能为空！',icon:'warning',lock: true,ok:true});
			return false;
		}else if(valdict.type=='int'&& input.value!=''&&isNaN(input.value)){
			art.dialog({title:'提示',content:valdict.title+' 必须为数字！',icon:'warning',lock: true,ok:true});
			return false;
		}else if(valdict.hasOwnProperty('min')&& input.value!=''&&Number(input.value)<valdict.min){
			art.dialog({title:'提示',content:valdict.title+' 必须大于 '+valdict.min+' ！',icon:'warning',lock: true,ok:true});
			return false;
		}else if(valdict.hasOwnProperty('max')&& input.value!=''&&Number(input.value)>valdict.max){
			art.dialog({title:'提示',content:valdict.title+' 必须小于 '+valdict.max+' ！',icon:'warning',lock: true,ok:true});
			return false;
		}
	}
	return true;
}

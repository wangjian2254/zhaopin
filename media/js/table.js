//隔行颜色
function senfe(o, a, b, c, d) {
	var t = document.getElementById(o).getElementsByTagName("tr");
	for (var i = 0; i < t.length; i++) {
		t[i].style.backgroundColor = (t[i].sectionRowIndex % 2 == 0) ? a : b;
		t[i].onclick = function() {
			if (this.x != "1") {
				this.x = "1";
				this.style.backgroundColor = d;
			} else {
				this.x = "0";
				this.style.backgroundColor = (this.sectionRowIndex % 2 == 0)
						? a
						: b;
			}
		}
		t[i].onmouseover = function() {
			if (this.x != "1")
				this.style.backgroundColor = c;
		}
		t[i].onmouseout = function() {
			if (this.x != "1")
				this.style.backgroundColor = (this.sectionRowIndex % 2 == 0)
						? a
						: b;
		}
	}
}

function delRow(e,attr_name){
	var tr=null;
	var table=null;
	try{
		
		tr=e.target.parentNode.parentNode;
		table=tr.parentNode.parentNode;
	}catch(ev){
//		alert(e.srcElement);
		tr=e.srcElement.parentNode.parentNode;
		table=tr.parentNode.parentNode;
		
	}
	
	if(attr_name==null){
		art.dialog({title:'提示',content:table.attributes.getNamedItem('warn_text').value,icon:'warning',lock: true,cancel:true,ok:function(){
			table.deleteRow(tr.rowIndex);
		}});
	}else{
		art.dialog({title:'提示',content:table.attributes.getNamedItem('warn_text').value,icon:'warning',lock: true,cancel:true,ok:function(){
			window.location.href=tr.attributes.getNamedItem(attr_name).value;
		}});
	}
	
}
function getTable(data_table){
	if(typeof(data_table)=="string"){
		data_table=document.getElementById(data_table);
	}
	return data_table;
}
//动态添加数据
function addTableRow(data_table,data,index_arr,value_p,need_del,attr_name){
	if(data==null||data=="null"){
		return;
	}
	data_table=getTable(data_table);
	
	var tr = document.createElement("tr");	
	var td = null;	
	var k='';
	for(var m=0;m< value_p.length;m++){
		k=value_p[m];
		if(k=='id'){
			k='tr_data_id';
			tr.setAttribute(k,data['id']);
		}else{
			if(data[k]!=undefined){
				tr.setAttribute(k,data[k]);
			}
			
		}
		
	}
	for(var i=0;i<index_arr.length;i++){
	
		td=document.createElement("td");
		td['class']='table1_top';
		td.appendChild(document.createTextNode(data[index_arr[i]]));
		tr.appendChild(td);
	}
	if(need_del==true){
	
		td=document.createElement("td");
		td['class']='table1_top';
		if(attr_name!=null){
			td.innerHTML="<label class='del_button_lbl' onClick='"+'delRow(event,"'+attr_name+'");'+"'>删除</label>";
//			if(typeof(attr_name)=="string"){
//			}else if (typeof(attr_name)==""){
//				for(var j=0;j<attr_name.length;j++){
//					td.innerHTML+=attr_name;
//				}
//			}
		}else{
			td.innerHTML="<label class='del_button_lbl' onClick='delRow(event);'>删除</label>";
			
		}
		
		tr.appendChild(td);
	}
	data_table.children[0].appendChild(tr);
	
	
}
function getTableRowValue(data_table,p_arr){
	var arr=[];
	
	data_table=getTable(data_table);
	data_table=data_table.children[0];
	
	
	var b=true;
	for(var i=0;i<data_table.rows.length;i++){
		
			var o={};
			b=true;
			for(var k=0;k<p_arr.length;k++){
				
				if([p_arr[k]]=='id'){
					if(data_table.rows[i].attributes.getNamedItem('tr_data_id')==null){
						continue;
					}
					o[p_arr[k]]=data_table.rows[i].attributes.getNamedItem('tr_data_id').nodeValue;
					b=false;
				}else{
					if(data_table.rows[i].attributes.getNamedItem(p_arr[k])==null){
						continue;
					}
					o[p_arr[k]]=data_table.rows[i].attributes.getNamedItem(p_arr[k]).nodeValue;
					b=false;
				}
			}
			if(!b){
			arr.push(o);
			}
	}
	return arr;
}

function getLXRDatas(url,data_table,index_arr,value_p,need_del){
	data_table=getTable(data_table);
	$j.get(url+'&noCacheForRefresh=' + Math.random(),{},function(data,textStatus){
		if(data.indexOf("Rows")<10){
			data=data.replace("Rows",'"Rows"');
		}
		var data2=JSON2.parse(data);
		for(var i=0;i<data2.Rows.length;i++){
			addTableRow(data_table,data2.Rows[i],index_arr,value_p,need_del);
		}
	})
}


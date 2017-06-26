function Tag_show(){
  this.ajax_method = 'GET';
}
Tag_show.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_tag:function(data){
	//console.log(data);
	var item;
	var name;
	var value;
	var attrTag = [];
	var attributeNames = [];
	var attributeValues = [];
    for(var key in data){
		item = data[key];
	}
	//console.log(item);
    for(i=0;i<item.length;i++){
		attrTag.push(item[i].split(':'));
	}
	//console.log(attrTag);
	for(i=0;i<attrTag.length;i++){
		attributeNames.push(attrTag[i][0]);
		attributeValues.push(attrTag[i][1]);
		//console.log(attrTag[i][0]);
	}
	//console.log(attributeNames);
	$('#ptag').empty();
	var html = '';
	for(i=0;i<item.length;i++){
		html += '<div class="tagClo fleft" ><span class="ptagName" style="color:red;">'+attributeNames[i]+'</span>：<span class="tagbg"><span>'+attributeValues[i]+'<span><a id="d_delIcon"></a></span></div>';	
	}
	$('#ptag').append(html);
  }
}
var url ="/tag/show_user_tag/?uid_list=" + uid + '&user=' + $('#d_useremail').text();
var Tag_show = new Tag_show();
Tag_show.call_sync_ajax_request(url, Tag_show.ajax_method, Tag_show.Draw_tag);
//选择类别
function Show_name(){
  this.ajax_method = 'GET';
}
Show_name.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_name:function(data){
	//console.log(data);
	$('#d_attribute_name_zh').empty();
	var html = '';
	html += '<select id="d_select_attribute_name">';
	if(data==""){
		html += '<option value="">暂无</option>';
	}
	else{
		for(i=0;i<data.length;i++){
		html += '<option value="'+data[i]+'">'+data[i]+'</option>';
	}
	}
	
	$('#d_attribute_name_zh').append(html);
  }
}
url_attribute_name = "/tag/show_attribute_name/?user=" + $('#d_useremail').text();
//console.log(url_attribute_name);
var Show_name = new Show_name();
Show_name.call_sync_ajax_request(url_attribute_name, Show_name.ajax_method, Show_name.Draw_name);
//标签名
function Show_value(){
  this.ajax_method = 'GET';
}
Show_value.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_value:function(data){
	//console.log(data);
	$('#d_attribute_value_zh').empty();
	var html = '';
	html += '<select id="d_select_attribute_value">';
        if(data=="no attribute"){
            html +='<option value="">暂无</option>';
            document.getElementById('select_attribute_name').style.width='53px';
        }else{
	    for(i=0;i<data.length;i++){
		html += '<option value="'+data[i]+'">'+data[i]+'</option>';
	    }
	   }
	    $('#d_attribute_value_zh').append(html); 
}   
}
var select_attribute_name = $("#d_select_attribute_name").val();
if(select_attribute_name != '[]'){
    url_attribute_value = "/tag/show_attribute_value/?user=" + $('#d_useremail').text() + "&attribute_name="+select_attribute_name;
    //console.log(url_attribute_value);
    var Show_value = new Show_value();
    Show_value.call_sync_ajax_request(url_attribute_value, Show_value.ajax_method, Show_value.Draw_value);
}else{
	$('#d_attribute_value_zh').empty();
	var html = '';
	html += '<select id="d_select_attribute_value" >';
	html += '<option value="null">暂无</option>';
	$('#d_attribute_value_zh').append(html);
}


$('#d_select_attribute_name').change(function(){
    var select_attribute_name = $("#d_select_attribute_name").val();
    if(select_attribute_name !=''){
        var url_attribute_value = '';
        url_attribute_value = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name + '&user=' + $('#d_useremail').text();
        Show_value.call_sync_ajax_request(url_attribute_value, Show_value.ajax_method, Show_value.Draw_value);
    }else{
	    $('#d_attribute_value_zh').empty();
	    var html = '';
	    html += '<select id="d_select_attribute_value" >';
	    html += '<option value="null">暂无</option>';
	    $('#d_attribute_value_zh').append(html);
  }
    
});

//添加
function Tag_add(){
  this.ajax_method = 'GET';
}
Tag_add.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_tag_add:function(data){
	//刷新页面
	url ="/tag/show_user_tag/?user="+ $('#d_useremail').text() +"&uid_list=" + uid;
	Tag_show.call_sync_ajax_request(url, Tag_show.ajax_method, Tag_show.Draw_tag);
  }
}
var Tag_add = new Tag_add();
//编辑
function Tag_change(){
  this.ajax_method = 'GET';
}
Tag_change.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_tag_change:function(data){
	//console.log(data);
	url ="/tag/show_user_tag/?uid_list=" + uid + '&user=' + $('#d_useremail').text();
	Tag_show.call_sync_ajax_request(url, Tag_show.ajax_method, Tag_show.Draw_tag);
	//刷新页面
	//location.reload();
  }
}
var Tag_change = new Tag_change();


function d_add_person_tag(){
	//获取所有类别名
	var new_attribute_name = $("#d_select_attribute_name").val();
	var new_attribute_value = $("#d_select_attribute_value").val();
    if(new_attribute_name !=''){
        var attributeNames = [];
	    var  tagnames = $('.ptagName').length;
	    for(i=0;i<tagnames;i++){
		    attributeNames.push($('.ptagName').eq(i).html());
	    }
	     //判断是否重复
	    var count = 0;
	    for(i=0;i<attributeNames.length;i++){
		    if(new_attribute_name==attributeNames[i]){
			    count += 0;
		    }else{
			    count ++;
		    }
	    }
	    if(count==attributeNames.length){
		    //添加新tag
		    var add_url = '';
                    var admin = $('#d_useremail').text();
		    add_url = '/tag/add_attribute/?uid=' + uid + '&attribute_name='+new_attribute_name+'&attribute_value='+new_attribute_value + '&user='+admin;
            Tag_add.call_sync_ajax_request(add_url, Tag_add.ajax_method, Tag_add.Draw_tag_add);
	    }else{
		    alert("已经存在相同的标签类型，新的标签名将替换原有的标签名！");
		    var change_url = '';
                    var admin = $('#d_useremail').text();
		    change_url = '/tag/change_attribute_portrait/?uid=' + uid + '&attribute_name='+new_attribute_name+'&attribute_value='+new_attribute_value+'&user='+admin;
		    //console.log(change_url);
		    Tag_change.call_sync_ajax_request(change_url, Tag_change.ajax_method, Tag_change.Draw_tag_change);
	    }
	}else{
        alert("标签类别不能为空，请先到自定义标签页面添加标签类别！");
	}
	
}
//删除
function Tag_del(){
  this.url = '/tag/delete_user_tag/?';
}
Tag_del.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_tag_del:function(data){
	//刷新页面
	url ="/tag/show_user_tag/?uid_list=" + uid + '&user=' + $('#d_useremail').text();
	Tag_show.call_sync_ajax_request(url, Tag_show.ajax_method, Tag_show.Draw_tag);
  }
}

function deleteTag(that){
	$('a[id^=d_delIcon]').live('click', function(){
		var del_url = that.url;
		var temp = $(this).parent().parent().parent().parent().remove();
		var delname = $(this).parent().parent().parent().prev().html();
		del_url = del_url +'uid=' + uid + '&attribute_name='+delname+'&user=admit';
		that.call_sync_ajax_request(del_url, Tag_del.ajax_method, Tag_del.Draw_tag_del);
	});
}
var Tag_del = new Tag_del();
deleteTag(Tag_del);


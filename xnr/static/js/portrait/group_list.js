function Group_identify_task(){
  this.ajax_method = 'GET';
}
Group_identify_task.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_resultTable: function(data){
    //console.log(data);
    $('#content_manage').empty();
    var item = data;
	var html = '';
	html += '<a id="turnback" onclick="redraw_result();" style="cursor:pointer;float:right;margin-right:40px;margin-top:12px;">查看全部任务</a><a data-toggle="modal" id="searchTable" href="#task_search" style="margin-bottom:10px;margin-top:12px;float: right;margin-right: 20px;"">表单搜索</a>';
	html += '<table id="group_analysis_body" class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	';
    html += '<th style="width:160px;">群组名称</th>';
    html += '<th style="width:170px;">时间</th><th>群组人数</th>';
    html += '<th style="width:200px;">备注</th><th>计算状态</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
		html += '<tr>';
		var time0 = new Date(item[i][1]*1000).format('yyyy/MM/dd hh:mm')
		html += '<td name="task_name">'+item[i][0]+'</td>';
		html += '<td>'+time0+'</td>';
		html += '<td>'+item[i][2]+'</td>';
		html += '<td>'+item[i][3]+'</td>';
		if(item[i][4]==1){
			html += '<td><a style="cursor:hand;" href="/index/group_analysis/?name=' + item[i][0]+ '">已完成</a></td>';
		}else{
			html += '<td>正在计算</td>';
		}
		html +='<td><a href="javascript:void(0)" id="commit_control">提交监控</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="analyze_del">删除</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
    html += '</table>';
	$('#content_manage').append(html);
	control_click();
    $('#group_analysis_body').dataTable({
       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
       "sPaginationType": "bootstrap",
       "aaSorting": [[ 1, "desc" ]],
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[5]}],
       "oLanguage": {
           "sLengthMenu": "_MENU_ 每页"
       }
    });
  },
}
function redraw_result(){
    //console.log('iiiii');
	var url = '/group/show_task/';
    url += '?submit_user=' + $('#useremail').text();
	Group_identify_task.call_sync_ajax_request(url, Group_identify_task.ajax_method, Group_identify_task.Draw_resultTable);
}

var current_date = new Date().format('yyyy/MM/dd hh:mm');
var max_date = '+1970/01/30';
var min_date = '-1970/01/30';
$('input[name="con_end_time"]').datetimepicker({value:current_date,minDate:current_date,step:10});
var Group_identify_task = new Group_identify_task();
redraw_result();
/*
var con_sen_word_url='/social_sensing/get_sensitive_words';
Group_identify_task.call_sync_ajax_request(con_sen_word_url,Group_identify_task.ajax_method,draw_con_sen_more);
var con_nor_word_url='/social_sensing/get_sensing_words';
Group_identify_task.call_sync_ajax_request(con_nor_word_url,Group_identify_task.ajax_method,draw_con_nor_more);
*/

$('#group_control_confirm_button').click(function(){
	group_control_data();
});
function group_control_check(){             // check validation 
    //group_information check starts  
    var group_name = $('input[name="con_group_name"]').val();
    var remark = $('input[name="con_remark"]').val();
    var sensors = '';
    //console.log(group_name, remark); 
    if (group_name.length == 0){
        alert('群体名称不能为空');
        return false;
    }
    var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
    if (!group_name.match(reg)){
        alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
        return false;
    }
    if ((remark.length > 0) && (!remark.match(reg))){
        alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
        return false;
    }
    //other form check starts
  return true;

}
function group_control_data(){
	var flag = group_control_check();
	var a = new Array();
    a['task_name'] = $('input[name="con_group_name"]').val();
    a['remark'] = $('input[name="con_remark"]').val();
	a['stop_time'] = Date.parse($('input[name="con_end_time"]').val())/1000;
	//a['keywords'] = '';
	//a['sensitive_words'] = '';
	a['create_at'] =  Date.parse(new Date())/1000;
	a['social_sensors'] ='';
	var url0 = [];
	var url1 = '';
	var url_create = '/social_sensing/create_task/?';
	if(flag = true){
        /*
	   a['keywords'] = $('input[name="con_nor_keywords"]').val();
	    if(a['keywords'].length){
		 	a['keywords'] = a['keywords'].split(/\s+/g);
	    }else{
	    	a['keywords'] = [];
	    }
	    $('[name="con_more_option_0"]:checked').each(function(){
		  	    a['keywords'].push($(this).val());
		  	});
	    a['sensitive_words'] = $('input[name="con_keywords"]').val();
	    if(a['sensitive_words'].length){
		 	a['sensitive_words'] = a['sensitive_words'].split(/\s+/g);
	    }else{
	    	a['sensitive_words'] = [];
	    }
	    $('[name="con_more_option_1"]:checked').each(function(){
		  	    a['sensitive_words'].push($(this).val());
		  	});
        */
    	$('[name="control_list_option"]:checked').each(function(){
	  	    a['social_sensors'].push($(this).parent().prev().prev().prev().prev().prev().prev().prev().attr('name'));
	  	});
		for(var k in a){
			if(a[k]){
				url0.push(k +'='+a[k]);
			}
		}
		if(url0.length > 1){
			url1 = url0.join('&');
		}else{
			url1 = url0;
		}
		url_create += url1;
        url_create += '&create_by=' + $('#useremail').text();
		//console.log(url_create);
	    $.ajax({
	        type:'GET',
	        url: url_create,
	        contentType:"application/json",
	        dataType: "json",
	        success: con_callback
	    });
        function con_callback(data){
            if(data==1){
                alert('操作成功！');
                //window.location.reload();
            }else if(data==0){
                alert('已存在相同名称的监控任务，请重试！');
            }else if(data ==-1){
                alert('请将信息补充完整！');
            }
        }
	}
}

function del(data){
		//console.log(data);
		if(data==true){
			alert('操作成功！');
			location.reload();
			//window.location.href=window.location.href;
		}
}
/*
function draw_con_sen_more(data){
	var item = data;
	//$('#so_more_content').empty();
	$('#con_sen_content').empty();
	var html = '';
    for (var i=0;i<item.length;i++){
		html += '<input  name="con_more_option_1" class="search_result_option" value="'+item[i]+'" type="checkbox"/><span style="margin-left:10px;margin-right:20px;">'+item[i]+'</span> ';
	}

	$('#con_sen_content').append(html);
}

function draw_con_nor_more(data){
	var item = data;
	$('#con_nor_content').empty();
	var html = '';
	for (var i=0;i<item.length;i++){
		html += '<input  name="con_more_option_0" class="search_result_option" value="'+item[i]+'" type="checkbox"/><span style="margin-left:10px;margin-right:20px;">'+item[i]+'</span> ';
	}
	$('#con_nor_content').append(html);
}
function con_more_all_0(){
  $('input[name="con_more_option_0"]').prop('checked', $("#con_more_all_0").prop('checked'));
}

function con_more_all_1(){
  $('input[name="con_more_option_1"]').prop('checked', $("#con_more_all_1").prop('checked'));
}
*/
function control_click(){
	$('a[id^="commit_control"]').click(function(){
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		var remark0 =  $(this).parent().prev().prev().html();
		url = '/social_sensing/get_group_detail/?task_name='+temp;
        url += '&user='+$('#useremail').text();
		Group_identify_task.call_sync_ajax_request(url,Group_identify_task.ajax_method,draw_control_table);
		$('input[name="con_group_name"]').val(temp);
		$('input[name="con_remark"]').val(remark0);
		$('#group_control').modal();
	});
    $('a[id="analyze_del"]').click(function(e){
		var a = confirm('确定要删除吗？');
    	if (a == true){
    		var url = '/detect/delete_task/?';
			var temp = $(this).parent().prev().prev().prev().prev().prev().html();
			url = url + 'task_name=' + temp;
            url += '&submit_user=' + $('#useremail').text();
			Group_identify_task.call_sync_ajax_request(url,Group_identify_task.ajax_method,del);
		}
	});	
}
var current_date = new Date().format('yyyy/MM/dd hh:mm');
var max_date = '+1970/01/30';
var min_date = '-1970/01/30';
$('input[name="so_end_time"]').datetimepicker({value:current_date,minDate:current_date,step:10});

function draw_control_table(data){
	if(data[0] == undefined){
		$('#group_control_confirm').empty();
		var html = '无满足条件用户';
		$('#group_control_confirm').append(html);

	}else{
        $('#group_control_confirm').empty();
        var html='';
        var item =data;
        var item_name = '';
        var html='';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;max-height:300px;">';
        html += '<tr><th style="text-align:center;width:50px">头像</th><th style="text-align:center">昵称</th>';
        html += '<th style="text-align:center;width:75px;">领域</th><th style="text-align:center">话题</th>';
        html += '<th style="text-align:center;width:60px;">重要度</th>';
        html += '<th style="text-align:center;width:60px;">影响力</th>';
        html += '<th style="text-align:center;width:60px;">活跃度</th><th><input name="control_choose_all" id="control_choose_all" type="checkbox" value="" onclick="control_choose_all()" /></th></tr>';//<th><input name="so_user_choose_all" id="so_user_choose_all" type="checkbox" value="" onclick="so_user_choose_all()" /></th>
        html += '<div style="overflow-y:auto;max-height:300px;">'
        for (var i=0;i<data.length;i++) {
            if(item[i][1]=='unknown'){
                item_name = '未知';
            }else{
                item_name = item[i][1];
            }
            if(item[i][2]=='unknown'){
                item_img = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
            }else{
                item_img = item[i][2];
            }
            // if(item[i][5]==undefined){
            // 	item_num = '无';
            // }else{
            // 	item_num = item[i][5].toFixed(2);
            // }
            html += '<tr><td name="'+item[i][0]+'" style="text-align:center"><img style="height:25px;" class="img-circle shadow-5"  title="'+item[i][0]+'"  src="' + item_img + '" ></td><td style="text-align:center">' + item_name + '</td><td style="text-align:center">' + item[i][3]+ '</td><td style="text-align:center">' + item[i][4] + '</td><td style="text-align:center">' + item[i][6] + '</td><td style="text-align:center">' + item[i][7] + '</td><td style="text-align:center">' + item[i][8] + '</td><td><input name="control_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></td></tr>';
        }
        html += '</div>'
        html += '</table>'; 
      //   html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" >';
      //   html += '<tr><th style="text-align:center">用户ID</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th><input name="control_choose_all" id="control_choose_all" type="checkbox" value="" onclick="control_choose_all()" /></th></tr>';
      //   for (var i=0;i<data.length;i++) {
      //       html += '<tr><td style="text-align:center">' + data[i][0] + '</td><td style="text-align:center">' + data[i][1] + '</td><td style="text-align:center">' + data[i][2].toFixed(2) + '</td><td style="text-align:center">' + data[i][3].toFixed(2) + '</td><td style="text-align:center">' + data[i][4].toFixed(2) + '</td><td><input name="control_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></td></tr>';
        // }
      //   html += '</table>'; 
        $('#group_control_confirm').append(html);
    }
}


function control_choose_all(){
	$('input[name="control_list_option"]').prop('checked', $("#control_choose_all").prop('checked'));
}

function task_search_button(){ //表单搜索
	var a = new Array();
	var url0 = [];
	var url1 = '';
	a['task_name'] = $('input[name="task_name0"]').val();
	a['submit_date'] = $('input[name="submit_date0"]').val();
	a['state'] = $('input[name="state0"]').val();
	var status =  $('input[name="status0"]').val();
	a['status'] = $('select[name="task_type"] option:selected').val();
	for(var k in a){
		if(a[k]){
			url0.push(k +'='+a[k]);
		}
	}
	if(url0.length > 1){
		url1 = url0.join('&');
	}else{
		url1 = url0;
	}
	var search_url = '/group/show_task/?'+url1;
    search_url += '&submit_user=' + $('#useremail').text();
	//console.log(search_url);
	$.ajax({
  	    type:'GET',
  	    url: search_url,
  	    contentType:"application/json",
  	    dataType: "json",
  	    success: Group_identify_task.Draw_resultTable
  	});
}

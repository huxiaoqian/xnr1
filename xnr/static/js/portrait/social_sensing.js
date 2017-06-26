function Social_sense(){
  this.ajax_method = 'GET';
}
Social_sense.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_group_table: function(data){
 	$('#so_group_task').empty();
    var item = data;
	var html = '';
	var item_time = '';
  console.log(item);
	if (item.length == 0){
		html += '<div style="color:grey;">暂无数据</div>'
	}else{
		html += '<table id="so_group_task_body" class="table table-bordered table-striped table-condensed datatable" >';
		html += '<thead><tr style="text-align:center;"><th>群组名称</th><th>提交人</th><th>时间</th><th>群组人数</th><th>备注</th><th>查看详情</th><th><input name="so_user_choose_all" id="so_user_choose_all" type="checkbox" value="" onclick="so_user_choose_all()" /></th></tr></thead>';
		html += '<tbody>';
		for (i=0;i<item.length;i++){
			item_time = new Date(item[i][2]*1000).format('yyyy/MM/dd hh:mm')
			html += '<tr><td name="'+item[i][5]+'">'+item[i][0]+'</td><td>'+item[i][1]+'</td><td>'+item_time+'</td><td>'+item[i][3]+'</td><td>'+item[i][4]+'</td>';
			html += '<td><a href=javascript:void(0)  id="so_users">查看详情<a/></td>';
			html += '<td><input name="so_user_list_option" class="search_result_option" type="checkbox"  /></td>'
			html += '</tr>';	
		}
		html += '</tbody>';
	    html += '</table>';
	}
	$('#so_group_task').append(html);
	// $('#so_group_task_body').dataTable({
 //       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
 //       "sPaginationType": "bootstrap",
 //       "oLanguage": {
 //           "sLengthMenu": "_MENU_ 每页"
 //       }
 //    });
  },
  Draw_task_table: function(data){
  	$('#so_task_table').empty();
  	var item = data;
  	var html = '';
  	var warn = '';
  	var flag = '';
  	var so_flag = '';
  	var time_pro = '';
  	var operate = '';
  	var f_color = '';
  	var time_now =  Date.parse(new Date())/1000;
	html += '<table id="so_task_table_body" class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;width:115px;"><th>任务名称</th><th style="width: 60px;">创建人</th><th>创建时间</th><th>终止时间</th><th  style="width: 140px;">监控进度&nbsp;&nbsp;<i style="font-size:15px;" class="glyphicon glyphicon-question-sign" data-placement="right" title="红色表示任务处于终止状态"></i></th><th>预警提示</th><th>监控浏览</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
	  	var create_d = new Date(item[i]['create_at']*1000).format('yyyy/MM/dd hh:mm'); 
      console.log(item[i]['stop_time'],item[i]['stop_time'].length);
	  	if(item[i]['stop_time']!= 'default'){
      var end_d = new Date(item[i]['stop_time']*1000).format('yyyy/MM/dd hh:mm'); 
      time_pro = (((time_now-item[i]['create_at'])/(item[i]['stop_time']-item[i]['create_at']))*100).toFixed(0);
	  	}else{
        var end_d = '无';
        time_pro = '----';
      }
      // var keys = [];
	  	// for(var j=0;j<item[i]['keywords'].length;j++){
	  	// 	keys.push(item[i]['keywords'][j]);
	  	// }
	  	// keys.join(',');
	  			if(item[i]['warning_status']==0){
			warn = '无事件';
			//$('#pro').replaceWith('<progress id="pro" progress ::webkit-progress-value{ background: #0064B4; }');
		}else if (item[i]['warning_status']==1){
			warn = '事件爆发';
			//$('progress').removeClass('webkit-progress-value').addClass('webkit-progress-value{ background: #333; }');
		}else {
			warn = '事件跟踪';
		}
		if(item[i]['finish'] == 0){
			if(item[i]['processing_status']==0){
				f_color = 'style="color:red"';
				operate = '<a href="javascript:void(0)" id="so_revise_task">修改</a>';
			}else{
				f_color = '';
				operate = '<a href="javascript:void(0)" id="so_revise_task">修改</a>&nbsp;&nbsp;<a href="javascript:void(0)" id="so_stop_task">终止</a>';
			}
		}else{
			operate = '<a href="javascript:void(0)" id="so_revise_task">修改</a>';
			f_color = '';
		}
		if(time_pro>=100.00){
	  		time_pro=100;
	  		operate = '<a href="javascript:void(0)" id="so_revise_task">修改</a>';
	  	}
	  	if(time_pro<=0){
	  		time_pro=0;
	  	}
		html += '<tr>';
		html += '<td><a href="javascript:void(0)" id="so_keys">'+item[i]['task_name']+'</a></td>';
		html += '<td style="width: 60px;">'+item[i]['create_by']+'</td>';
		html += '<td>'+create_d+'</td>';
		html += '<td>'+end_d+'</td>';
		html += '<td "><progress id="pro" style="width:60%"   value="'+time_pro+'" max="100"></progress><span '+f_color+'>'+time_pro+'%</span></td>';
		html += '<td>'+warn+'</a></td>';
		//<a href="/index/sensing_analysis/?task_name='+item[i]['task_name']+'&keywords='+keys+'&ts='+item[i]['history_status'][0][0]+'" id="so_warn">
		//html += '<td><a href="javascript:void(0)" id="so_keys">更多信息&nbsp;&nbsp;</a>';
		html += '<td><a href="javascript:void(0)" id="so_history">历史状态</a></td><td>'+operate+'&nbsp;&nbsp;<a href="javascript:void(0)" id="so_task_del">删除</a></td>';
		html += '</tr>';		
	}
	html += '</tbody>';
    html += '</table>';
	$('#so_task_table').append(html);
	so_ready();
	$('#so_task_table_body').dataTable({
       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
       "sPaginationType": "bootstrap",
       "oLanguage": {
           "sLengthMenu": "_MENU_ 每页"
       }
    });
  }
}

// $('input[name="so_mode_choose"]').change(function(){
//     var so_user_option = $('input[name="so_mode_choose"]:checked').val();
//     if (so_user_option == 'so_have_users'){
//         $('#so_have_users_ext').css('display','block').siblings().css({"display":"none"});
//     }
//     else if(so_user_option == 'so_search_users'){
//         $('#so_search_users_ext').css('display','block').siblings().css({"display":"none"});
//     }else{
//     	$('#so_up_users_ext').css('display','block').siblings().css({"display":"none"});
//     }
// });
var current_date0 = new Date();
//var current_date = current_date0.format('yyyy/MM/dd hh:mm')
current_date0.setDate(current_date0.getDate()+1);
var v_date = current_date0.format('yyyy/MM/dd hh:mm');
//var max_date = '+1970/01/30';
var min_date = '-1970/01/01';
$('input[name="so_end_time"]').datetimepicker({value:v_date,minDate:min_date,step:10});
$('input[id="so_re_end_time"]').datetimepicker({value:v_date,minDate:min_date,step:10});

function so_draw_control_table(data){
	$('#so_control_confirm').empty();
	var item =data;
	var item_name = '';
	var html='';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;">';
    html += '<tr><th style="text-align:center">头像</th><th style="text-align:center">昵称</th><th style="text-align:center">领域</th><th style="text-align:center">话题</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th style="text-align:center">活跃度</th></tr>';//<th><input name="so_user_choose_all" id="so_user_choose_all" type="checkbox" value="" onclick="so_user_choose_all()" /></th>
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
        html += '<tr><td name="'+item[i][0]+'" style="text-align:center"><img class="img-circle shadow-5"  style="height:30px;" title="'+item[i][0]+'"  src="' + item_img + '" ></td><td style="text-align:center">' + item_name + '</td><td style="text-align:center">' + item[i][3]+ '</td><td style="text-align:center">' + item[i][4] + '</td><td style="text-align:center">' + item[i][6] + '</td><td style="text-align:center">' + item[i][7] + '</td><td style="text-align:center">' + item[i][8] + '</td></tr>';
  	}
    html += '</table>'; 
	$('#so_control_confirm').append(html);
}


var Social_sense= new Social_sense();
//prepare(Social_sense);
var user= $('#so_useremail').text();
var user='admin';
function draw_result(){
	url = '/social_sensing/get_group_list/?user='+user; 
	Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, Social_sense.Draw_group_table);
}
draw_result();
show_url='/social_sensing/show_task/?user='+user;
Social_sense.call_sync_ajax_request(show_url, Social_sense.ajax_method, Social_sense.Draw_task_table);

//window.setInterval(so_redraw,30000);
function so_redraw(){
	show_url='/social_sensing/show_task/?user='+user;
	Social_sense.call_sync_ajax_request(show_url, Social_sense.ajax_method, Social_sense.Draw_task_table);
}

//Social_sense.Draw_task_table();
function so_choose_all(){
  $('input[name="so_list_option"]').prop('checked', $("#so_choose_all").prop('checked'));
}

function so_user_choose_all(){
  $('input[name="so_user_list_option"]').prop('checked', $("#so_user_choose_all").prop('checked'));
}

function keys_choose_all(){
  $('input[name="keys_list_option"]').prop('checked', $("#keys_choose_all").prop('checked'));
}

function so_more_all_0(){
  $('input[name="so_more_option_0"]').prop('checked', $("#so_more_all_0").prop('checked'));
}

function so_more_all_1(){
  $('input[name="so_more_option_1"]').prop('checked', $("#so_more_all_1").prop('checked'));
}


function draw_sensor(data){
	$('#so_sensor_content').empty();
	if(data['remark']){
		$('span[id^="so_remark0"]').html(data['remark']);
	}else{
		$('span[id^="so_remark0"]').html('无');
	}
	var item = data['social_sensors_portrait'];
	var html = '';
	var item_name = '';
	var item_img = '';
	var item_num = '';
	var item_keys = data['keywords'];
	var item_sen_keys = data['sensitive_words'];
	var item_sensor = data['social_sensors'];
 //    html += '<div style="width:100%"><div  style="float:left;display:inline-block">敏感传感词：</div>';
 //    if(item_keys.length > 0){
 //    	html += '<div style="margin-right: 9px;padding:0px;width: 83%;display:inline-block">';
	//     for (var j =0;j<item_sen_keys.length;j++){
	//     	html += '<span style="margin-right:20px;">'+item_sen_keys[j]+'</span>';
	//     }
	//     html += '</div>';
	// }else{html += '<span style="margin-right:20px;">无</span>'}
	// html += '<div style="width:100%;margin-top:10px;"><div  style="float:left;display:inline-block">普通传感词：</div>';
 //    if(item_keys.length > 0){
 //    	html += '<div style="margin-right: 9px;padding:0px;width: 83%;display:inline-block">';
	//     for (var j =0;j<item_keys.length;j++){
	//     	html += '<span style="margin-right:20px;">'+item_keys[j]+'</span>';
	//     }
	//     html += '</div>';  
 //    }else{html += '<span style="margin-right:20px;">无</span>'}
 //    html += '</div>';
    if (item_sensor.length == 0){
    	html += '<div style="margin-top:10px;">传感群：<span style="margin-left:28px;">全库用户</span></div>'
    }else{
    	html += '<div style="margin-top:10px;overflow-y:auto;height:300px;">';
	    html += '<table style="margin-top:10px;font-weight:lighter;" class="table table-striped table-bordered bootstrap-datatable datatable responsive" >';
	    html += '<tr><th style="text-align:center">头像</th><th style="text-align:center">昵称</th><th style="text-align:center">领域</th><th style="text-align:center">话题</th><th style="text-align:center">重要度</th></tr>';
        for (var i=0;i<item.length;i++) {
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
	    	if(item[i][5]==undefined){
	    		item_num = '无';
	    	}else{
	    		item_num = item[i][5].toFixed(2);
	    	}
	        html += '<tr><td style="text-align:center"><img class="img-circle shadow-5"  style="height:30px;" title="'+item[i][0]+'"  src="' + item_img + '" ></td>';
            html += '<td style="text-align:center">' + item_name + '</td><td style="text-align:center">' + item[i][3]+ '</td>';
            html += '<td style="text-align:center">' + item[i][4] + '</td><td style="text-align:center">' + item_num + '</td></tr>';
	 	}
	 	html += '</div>';
	    html += '</table>'; 
    }
    $('#so_sensor_content').append(html); 
}

function so_draw_search_results(data){
    //console.log(data);
    $('#search_result').empty();
    var user_url ;
    //console.log(user_url);
    var html = '';
    html += '<table id="search_result_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th>';
    html += '<th>操作</th><th><input  name="search_table_choose" id="search_table_choose" type="checkbox" value="" onclick="search_table_choose()" />全选</th></tr></thead>';
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      item = replace_space(item);
      if (item[1] == '未知'){
          item[1] = item[0];
      } 
      for(var j=3;j<7;j++){
        if(item[j]!='未知')
          item[j] = item[j].toFixed(2);
      }
      user_url = '/index/personal/?uid=' + item[0];
      html += '<tr id=' + item[0] +'>';
      html += '<td class="center" name="uids"><a href='+ user_url+ '  target="_blank">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] +'</td>';
      html += '<td class="center">'+ item[2] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[3] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[4] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[6] +'</td>';
      html += '<td class="center" style="width:120px;"><a class="portrait_href" href=' + user_url + ' target="_blank">查看人物属性页</a></td>';
      html += '<td class="center"><input name="search_table_choose_option" class="search_result_option" type="checkbox"  /></td>'
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#search_result').append(html);
    $('#search_result_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "aaSorting":[[5, 'desc']],
        //"aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "每页&nbsp; _MENU_ 条"
        }
    });
}

//上传文件交互、按钮
function bindOption(){
      $('#so_user_commit').click(function(){
          if ($('input[name="recommend_type"]:checked').val() == 'upload'){
              if (seed_user_files == undefined){
                  alert('请选择文件上传！');
                  return false;
              }

              var upload_job = {};
              var admin = $('#useremail').text();
              upload_job['user'] = admin;
              upload_job['type'] = $('#file_type').val();
              upload_job['date'] = new Date().format('yyyy-MM-dd');
              //upload_job['date'] = '2013-09-06';
              handleFileSelect(upload_job);
          }
      });

        $('#delete_file').click(function(){
            seed_user_files = undefined;
            $('#file_status').css('display', 'none');
        });
        $('#if_time').click(function(){
          if($(this).is(':checked')){
            $('input[name="so_end_time"]').attr('disabled',false);
          }
          else{
            $('input[name="so_end_time"]').attr('disabled',true);
          }
        });
        $('#uploadbtn').click(function(){
            var fileInput = document.getElementById('seed_file_upload');
            // 检查文件是否选择:
            if (!fileInput.value) {
                alert('没有选择文件。');
                return;
            }
            // 获取File引用:
            var file = fileInput.value;
            //alert(file);
            if ((file.endsWith('.csv')) || (file.endsWith('.txt'))) {
                seed_user_files = fileInput.files;
                $('#add_file').html(file);
                $('#file_status').css('display', 'block');
                return false;
            }else{
                alert('只能上传csv或txt文件。');
                return;
            }
        });
}
bindOption();
function draw_sen_more(data){
	var item = data;
	//$('#so_more_content').empty();
	$('#so_sen_content').empty();
	var html = '';
	//html += '<table id="so_more_body" class="table table-bordered table-striped table-condensed datatable" >';
	// html += '<div style="font-size:18px;font-weight:bold;">敏感词<input style="margin-left:50px;"margin-right:10px; name="so_more_all_1" id="so_more_all_1" type="checkbox" value="" onclick="so_more_all_1()" /><span>全选</span></div>';
	//html += '<div style="margin:8px 0px;">';
    for (var i=0;i<item.length;i++){
		html += '<input  name="so_more_option_1" class="search_result_option" value="'+item[i]+'" type="checkbox"/><span style="margin-left:10px;margin-right:20px;">'+item[i]+'</span> ';
	}
	//html += '</div><hr/>';
	//html += '<div style="font-size:18px;font-weight:bold;">一般关键词<input style="margin-left:21px;margin-right:10px;" name="so_more_all_0" id="so_more_all_0" type="checkbox" value="" onclick="so_more_all_0()" /><span>全选</span></div>';
	// html += '<div style="margin:8px 0px;">';
	// for (var j=0;j<item[1].length;j++){
	// 	html += '<input  name="so_more_option_0" class="search_result_option" value="'+item[1][j]+'" type="checkbox"/><span style="margin-left:10px;margin-right:20px;">'+item[1][j]+'</span> ';
	// }
	// html += '</div>';
	$('#so_sen_content').append(html);
}


function search_table_choose(){
  $('input[name="search_table_choose_option"]').prop('checked', $("#search_table_choose").prop('checked'));
}

function draw_nor_more(data){
	var item = data;
	$('#so_nor_content').empty();
	var html = '';
	for (var i=0;i<item.length;i++){
		html += '<input  name="so_more_option_0" class="search_result_option" value="'+item[i]+'" type="checkbox"/><span style="margin-left:10px;margin-right:20px;">'+item[i]+'</span> ';
	}
	$('#so_nor_content').append(html);
}
function so_ready(){
	$('a[id^="so_keys"]').click(function(e){
		var temp = $(this).parent().text();
		$('span[id^="so_group_name0"]').html(temp);
		$('#so_sensor_content').empty();
		$('span[id="so_remark0"]').html('');
		url = "/social_sensing/get_task_detail_info/?task_name=" + temp+'&user='+user;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_sensor);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().html();
		$('#so_keys_block').modal();
	});
	
	$('a[id^="so_history"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().text();
		$('span[id^="so_group_name0"]').html(temp);
		$('#so_his_content').empty();
		$('span[id="so_remark0"]').html('');
		url = "/social_sensing/get_task_detail_info/?task_name=" + temp+'&user='+user;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_history);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().prev().prev().html();
		$('#so_his_block').modal();
	});

	$('a[id^="so_stop_task"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().text();
		var a = confirm('确定要终止任务吗？');
		if (a== true){
			url = "/social_sensing/stop_task/?task_name=" + temp+'&user='+user;
			Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, callback);
		}
	});	

	$('a[id^="so_revise_task"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().text();
		//url = "/social_sensing/revise_task/?task_name=" + temp;
		//Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, callback);
		$('span[id^="so_re_group_name"]').html(temp);
		$('#so_revise').modal();
	});

	$('a[id^="so_users"]').click(function(){
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		var remark = $(this).parent().prev().html();
		url = "/social_sensing/get_group_detail/?task_name=" + temp+'&user='+user;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,so_draw_control_table);
		$('span[id^="have_sensor_name"]').html(temp);
		$('span[id^="have_sensor_remark"]').html(remark);
		$('#so_control').modal();
		});
	$('a[id^="so_task_del"]').click(function(e){
	var a = confirm('确定要删除吗？');
    	if (a == true){
			var url = '/social_sensing/delete_task/?';
			var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().text();
			url = url + 'task_name=' + temp;
			console.log(url);
			//window.location.href = url;
			Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,callback);
	}
	});
	// var sen_word_url='/social_sensing/get_sensitive_words';
	// Social_sense.call_sync_ajax_request(sen_word_url,Social_sense.ajax_method,draw_sen_more);
	// var nor_word_url='/social_sensing/get_sensing_words';
	// Social_sense.call_sync_ajax_request(nor_word_url,Social_sense.ajax_method,draw_nor_more);

	$('span[id^="so_more"]').click(function(e){
		$('#so_more_block').modal();
	 });
}

function callback(data){
	console.log(data);
	if(data.length>0){
		alert('操作成功！');
		window.location.href=window.location.href;
	}
		//window.location.href=window.location.href;
}




function draw_history(data){
	$('#so_his_content').empty();
	if(data['remark']){
		$('span[id^="so_remark0"]').html(data['remark']);
	}else{
		$('span[id^="so_remark0"]').html('无');
	}
	if(data['sensitive_words']){
		$('span[id^="so_sen_keys"]').empty();
		var s_html ='';
		for (var j =0;j<data['sensitive_words'].length;j++){
			s_html +=  '<span style="margin-right:20px;">'+data['sensitive_words'][j]+'</span>';
		}
		$('span[id^="so_sen_keys"]').append(s_html);
	}else{
		$('span[id^="so_sen_keys"]').html('无');
	}

	if(data['keywords']){
		$('span[id^="so_nor_keys"]').empty();
		var s_html ='';
		for (var j =0;j<data['keywords'].length;j++){
			s_html +=  '<span style="margin-right:20px;">'+data['keywords'][j]+'</span>';
		}
		$('span[id^="so_nor_keys"]').append(s_html);		
		//$('span[id^="so_nor_keys"]').html(data['keywords']);
	}else{
		$('span[id^="so_nor_keys"]').html('无');
	}
	//$('span[id="so_remark0"]').html('');
	//$('span[id="so_remark0"]').html(data['remark']);
    var item_his = data['history_status'];
	var html = '';
	var warn = '';
	var item_time = '';
	//console.log(item_his.length);
	if(item_his.length == 0){
		html += '<div>暂无历史状态</div>';
	}else{
		html += '<div style="overflow-y:auto;height:300px;">'
	    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;">';
	    html += '<tr><th style="text-align:center">时间</th><th style="text-align:center">预警状态</th><th style="text-align:center">查看详情</a></th></tr>';
	    for (var i=0;i<item_his.length ;i++) {
	    	if(item_his[i][2]==0){
				warn = '无事件';
			}else if (item_his[i][2]==1){
				warn = '事件爆发';
			}else {
				warn = '事件跟踪';
			}
			item_time = new Date(item_his[i][0]*1000).format('yyyy/MM/dd hh:mm');
	       html += '<tr><td style="text-align:center">' + item_time + '</td><td style="text-align:center">' + warn + '</td><td style="text-align:center"><a target="_blank" href="/index/sensing_analysis/?task_name='+data['task_name']+'&keywords='+data['keywords']+'&ts='+item_his[i][0]+'" id="show_detail">查看详情</a></td></tr>';
	 	}
	    html += '</table>'; 
	    html += '</div>';
	}
	$('#so_his_content').append(html);	
}

$('#so_user_commit').click(function(){
	so_group_data();
});

function revise_confirm_button(){
	var task_name=$('#so_re_group_name').html();
	var re_time=Date.parse($('#so_re_end_time').val())/1000;
	url = '/social_sensing/revise_task/?task_name='+task_name+'&stop_time='+re_time+'&finish=0';
	console.log(url);
	$.ajax({
	        type:'GET',
	        url: url,
	        contentType:"application/json",
	        dataType: "json",
	        success: callback
    });
}

var so_user_option = $('input[name="so_mode_choose"]:checked').val();
function so_user_check(){             // check validation 
    //group_information check starts  
    var group_name = $('#so_name').val();
    var remark = $('#so_remarks').val();
    var sensors = '';
    console.log(group_name, remark); 
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
function so_group_data(){
	var flag = so_user_check();
	var a = new Array();
	if(flag == true){
	    a['task_name'] = $('#so_name').val();
	    a['remark'] = $('#so_remarks').val();
    if($('#if_time').is(':checked')){
          a['stop_time'] = Date.parse($('input[name="so_end_time"]').val())/1000;  
      }
		else{
      a['stop_time']='default';
    }
		//a['keywords'] = '';
		//a['keywords0'] = '';
		a['create_at'] =  Date.parse(new Date())/1000;
		var so_user_option = $('input[name="so_mode_choose"]:checked').val();
		var url0 = [];
		var url1 = '';
		var url_create = '/social_sensing/create_task/?';
	  //   a['keywords'] = $('#so_keywords').val();
	 	// a['keywords'] = a['keywords'].split(/\s+/g);
	  //   a['sensitive_words'] = $('#so_keywords_nor').val();
	 	// a['sensitive_words'] = a['sensitive_words'].split(/\s+/g);
	  //   $('[name="so_more_option_0"]:checked').each(function(){
		 //  	    a['sensitive_words'].push($(this).val());
		 //  	});
	  //  	$('[name="so_more_option_1"]:checked').each(function(){
		 //  	    a['keywords'].push($(this).val());
		 //  	});
	    if (so_user_option == 'so_search_users'){
	    	a['social_sensors'] = '';
	    }else{              //single_user or multi_user with extension
	    	a['social_sensors'] = [];
		  	$('[name="so_user_list_option"]:checked').each(function(){
		  	    //group_names.push($(this).parent().prev().prev().prev().prev().prev().prev().text());
		  	     a['social_sensors'].push($(this).parent().prev().prev().prev().prev().prev().prev().attr('name'));
		  	});
		}
		console.log(a['social_sensors']);
		for(var k in a){
			if(a[k]){
				url0.push(k +'='+a[k]);
			}
		}
		if(url0.length > 1){
			url1 = url0.join('&');
		}else{
			url1 = url0.toString();
		}
		url_create += url1;
		console.log(url_create);
	    $.ajax({
	        type:'GET',
	        url: url_create,
	        contentType:"application/json",
	        dataType: "json",
	        success: so_callback
	    });
	}
}

function so_callback(data){
	if(data==1){
		alert('操作成功！');
		window.location.href=window.location.href;
	}else if(data==0){
		alert('已存在相同名称的监控任务，请重试！');
	}else if(data ==-1){
		alert('请将信息补充完整！');
	}
}


// have_keys(['sdfa','asdfasg','1231','asdfa','dsga4','12sdfa']);

// function have_keys(data){
// 	$('#show_keys').empty();
// 	html = '';
// 	for(var i=0;i<data.length;i++){
// 		html += '<input name="keys_list_option" class="search_result_option" value="'+data[i]+'" type="checkbox"/><span style="margin-left:10px;margin-right:20px;">'+data[i]+'</span> ';
// 	}
// 	$('#show_keys').append(html);
// }

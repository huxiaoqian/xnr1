//日期选择
var date = choose_time_for_mode();
var min_date_ms = new Date()
date.setHours(0,0,0,0);
var current_date = date.format('yyyy/MM/dd hh:mm');
var from_date_time = Math.floor(date.getTime()/1000) - 60*60*24;
min_date_ms.setTime(from_date_time*1000);
var from_date = min_date_ms.format('yyyy/MM/dd hh:mm');
if (global_test_mode == 0){
    $('#event_pattern #time_start').datetimepicker({value:from_date,step:10});
    $('#event_pattern #time_end').datetimepicker({value:current_date,step:10});
}
else{
    $('#event_pattern #time_start').datetimepicker({value:from_date,step:10,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
    $('#event_pattern #time_end').datetimepicker({value:current_date,step:10,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
}    
$('#event_pattern #show_advanced').click(function(){
    if($('#event_pattern #advanced_condition').is(':hidden')){
        $(this).html('收起');
        $('#event_pattern #advanced_condition').css('display', 'block');
    }
    else{
        $(this).html('高级');
        $('#event_pattern #advanced_condition').css('display', 'none');
    }
});

$('#event_pattern #num-range').change(function(){
    var num = $('#event_pattern #num-range').val();
    $('#event_pattern #show_num').empty();
    $('#event_pattern #show_num').append(num);    
});

function event_pattern_check(){             // check validation 
  //group_information check starts  
  var dt = new Date();
  dt.setHours(0,0,0,0);
  //console.log('max_date_limit',max_date_limit);
  var max_date_limit_stamp = Date.parse(dt)/1000;
  var group_name = $('#first_name').val();
  var remark = $('#first_remarks').val();
  var text = $('#event_pattern #text').val();
  var time_from = Date.parse($('#event_pattern #time_start').val())/1000;
  var time_to = Date.parse($('#event_pattern #time_end').val())/1000;
  var num_range_count = $('#event_pattern #num-range').val();
  var influ_from_num = parseFloat($('#event_pattern #influ_from').val());
  var influ_to_num =parseFloat($('#event_pattern #influ_to').val());
  var impor_from_num = parseFloat($('#event_pattern #impor_from').val());
  var impor_to_num = parseFloat($('#event_pattern #impor_to').val());
  if (text == ''){
      alert('关键词不能为空！');
      return false;
  }
  if (influ_from_num > influ_to_num){
    alert('影响力左侧输入值应小于右侧，请重新输入！')
    return false;
  }
  if (impor_from_num > impor_to_num){
    alert('重要度输入栏左侧输入值应小于右侧，请重新输入！')
    return false;
  }
  if(influ_from_num > 100 || influ_to_num > 100){
    alert('影响力输入值应在0到100之间，请重新输入！');
    return false;
  }
  if(impor_from_num>100 || impor_to_num>100){
    alert('重要度输入值应在0到100之间，请重新输入！');
    return false;
  }
  if(num_range_count ==0 ){
    alert('扩展规则中人数不能为0，请重新输入！');
    return false;
  }
  if(time_from > time_to){
    alert('起止时间错误，请重新选择！');
    return false;
  }
  if(max_date_limit_stamp < time_to ){
    alert('终止时间最晚不超过今日零点，请重新选择！');
    return false;
  }
  if (group_name.length == 0){
      alert('群体名称不能为空，请重新输入！');
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
  //other form check starts multi/single
  return true;

}

function submit_event(){
	if(event_pattern_check()){
		var event_pattern_url = '/detect/event/?';
		var event_all_url = new Array();

		var text_url = '';
		var text_id = $('#event_pattern #text').attr("id");
		var text_content = $('#event_pattern #text').val();
		if(text_content != ''){
			text_url = text_id +'='+ text_content;
			event_all_url.push(text_url);
		}

		var time_from = Date.parse($('#event_pattern #time_start').val())/1000;
		var time_to = Date.parse($('#event_pattern #time_end').val())/1000;
		var timestamp_from_url = '';
		timestamp_from_url = 'timestamp_from=' + time_from;
		event_all_url.push(timestamp_from_url);
		var timestamp_to_url = '';
		timestamp_to_url = 'timestamp_to=' + time_to;
		event_all_url.push(timestamp_to_url);

      	var domain_url = '';
		var domain = new Array();
		$('#event_pattern #domain .inline-checkbox').each(function(){
        	if($(this).is(':checked')){
          		domain.push($(this).next().text());
        	}
      	});
      	if(domain.length != 0 ){
       		domain_url += 'domain=' + domain.join(',');
        	event_all_url.push(domain_url);
      	}
      
		var topic_url = '';
		var topic_string = new Array();
		$('#event_pattern #topic_string .inline-checkbox').each(function(){
			if($(this).is(':checked')){
		  		topic_string.push($(this).next().text());
			}
		});
		if(topic_string.length != 0){
			topic_url += 'topic_string=' + topic_string.join(',');
			event_all_url.push(topic_url);
		}

		var num_range_url = '';
		var num_range_count = $('#event_pattern #num-range').val();
		num_range_url = 'count=' + num_range_count;
		event_all_url.push(num_range_url);

		var influ_from_url ='';
		var influ_from_val = $('#event_pattern #influ_from').val();
		influ_from_url = 'influence_from=' + influ_from_val;
		event_all_url.push(influ_from_url);

		var influ_to_url ='';
		var influ_to_val = $('#event_pattern #influ_to').val();
		influ_to_url = 'influence_to=' + influ_to_val;
		event_all_url.push(influ_to_url);

		var important_from_url ='';
		var important_from_val = $('#event_pattern #impor_from').val();
		important_from_url = 'important_from=' + important_from_val;
		event_all_url.push(important_from_url);

		var important_to_url ='';
		var important_to_val = $('#event_pattern #impor_to').val();
		important_to_url = 'important_to=' + important_to_val;
		event_all_url.push(important_to_url);

		var task_name_url = ''
		var task_name_id = 'task_name'
		var task_name_content = $('#first_name').val();
		if(task_name_content != ''){
		task_name_url =task_name_id +'='+ task_name_content;
		event_all_url.push(task_name_url);
		}

		var first_remarks_url = ''
		var first_remarks_id = 'state'
		var first_remarks_content = $('#first_remarks').val();
		if(first_remarks_content != ''){
		first_remarks_url = first_remarks_id +'='+ first_remarks_content;
		event_all_url.push(first_remarks_url);
		}

		event_pattern_url += event_all_url.join('&') + '&submit_user=' + $('#useremail').text();
		console.log(event_pattern_url);
	
		$.ajax({
			type:'GET',
			url: event_pattern_url,
			contentType:"application/json",
			dataType: "json",
			success: event_callback
      });
      
    }	
	}
  function event_callback(data){
    console.log(data);
    seed_user_callback(data);
}

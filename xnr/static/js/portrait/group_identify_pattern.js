function pattern_commit(){
    if(pattern_check()){
      var url_pattern = '/detect/new_pattern/?';
      var url_all = new Array();
      var geo_url = ''
      var geo_id = $('#pattern #geo').attr("id");
      var geo_content = $('#pattern #geo').val();
      if(geo_content != ''){
        geo_url = geo_id +'='+ geo_content;
        url_all.push(geo_url);
      }
      var ip_url = ''
      var ip_id = $('#pattern #ip').attr("id");
      var ip_content = $('#pattern #ip').val();
      if(ip_content != ''){
        ip_url = ip_id +'='+ ip_content;
        url_all.push(ip_url);
      }
      var message_url = '';
      message_url += 'message_type=' + $('#pattern #message_type').val();
      url_all.push(message_url);
      
      var sentiment_url = '';
      sentiment_url += 'sentiment=' + $('#pattern #sentiment').val();
      url_all.push(sentiment_url);

      var time_from = Date.parse($('#pattern #weibo_from').val())/1000;
      var time_to = Date.parse($('#pattern #weibo_to').val())/1000;
      var timestamp_from_url = '';
      timestamp_from_url = 'timestamp_from=' + time_from;
      url_all.push(timestamp_from_url);
      var timestamp_to_url = '';
      timestamp_to_url = 'timestamp_to=' + time_to;
      url_all.push(timestamp_to_url);

      var task_name_url = ''
      var task_name_id = 'task_name'
      var task_name_content = $('#first_name').val();
      if(task_name_content != ''){
        task_name_url =task_name_id +'='+ task_name_content;
        url_all.push(task_name_url);
      }

      var first_remarks_url = ''
      var first_remarks_id = 'state'
      var first_remarks_content = $('#first_remarks').val();
      if(first_remarks_content != ''){
        first_remarks_url = first_remarks_id +'='+ first_remarks_content;
        url_all.push(first_remarks_url);
      }
      var num_range_url = '';
      var num_range_count = $('#pattern #num-range').val();
      num_range_url = 'count=' + num_range_count;
      url_all.push(num_range_url);

      var influ_from_url ='';
      var influ_from_val = $('#pattern #influ_from').val();
      influ_from_url = 'influence_from=' + influ_from_val;
      url_all.push(influ_from_url);

      var influ_to_url ='';
      var influ_to_val = $('#pattern #influ_to').val();
      influ_to_url = 'influence_to=' + influ_to_val;
      url_all.push(influ_to_url);

      var important_from_url ='';
      var important_from_val = $('#pattern #impor_from').val();
      important_from_url = 'important_from=' + important_from_val;
      url_all.push(important_from_url);

      var important_to_url ='';
      var important_to_val = $('#pattern #impor_to').val();
      important_to_url = 'important_to=' + important_to_val;
      url_all.push(important_to_url);
      
      url_pattern += url_all.join('&') + '&submit_user=' + $('#useremail').text();
      console.log(url_pattern);

      $.ajax({
        type:'GET',
        url: url_pattern,
        contentType:"application/json",
        dataType: "json",
        success: pattern_callback
      });
      function pattern_callback(data){
          seed_user_callback(data);
      }
    }
}
function pattern_bind_click(){
    $('#pattern #show_advanced').click(function(){
        if($('#pattern #advanced_condition').is(':hidden')){
            $(this).html('收起');
            $('#pattern #advanced_condition').css('display', 'block');
        }
        else{
            $(this).html('高级');
            $('#pattern #advanced_condition').css('display', 'none');
        }
    });
    $('#pattern #num-range').change(function(){
        var num = $('#pattern #num-range').val();
        $('#pattern #show_num').empty();
        $('#pattern #show_num').append(num);    
    });
}
function pattern_check(){
  var group_name = $('#first_name').val();
  var remark = $('#first_remarks').val();
  var num_range_count = $('#pattern #num-range').val();
  var time_from = Date.parse($('#pattern #weibo_from').val())/1000;
  var time_to = Date.parse($('#pattern #weibo_to').val())/1000;
  if(time_from > time_to){
    alert('起止时间错误，请重新选择！');
    return false;
  }
  if(max_date_limit_stamp < time_to ){
    alert('终止时间最晚不超过今日零点，请重新选择！');
    return false;
  }
    var influ_from = parseFloat($('#pattern #influ_from').val());
    var influ_to = parseFloat($('#pattern #influ_to').val());
    if (influ_from > influ_to){
        alert('影响力左侧输入值应小于右侧输入值！');
        return false;
    }
    var impor_from = parseFloat($('#pattern #impor_from').val());
    var impor_to = parseFloat($('#pattern #impor_to').val());
    if (impor_from > impor_to){
        alert('重要度左侧输入值应小于右侧输入值！');
        return false;
    }
      if(num_range_count ==0 ){
        alert('扩展规则中人数不能为0，请重新输入！');
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
    return true;

}
//日期选择
var date = choose_time_for_mode();
var min_date_ms = new Date()
date.setHours(0,0,0,0);
var max_date_limit_stamp = date.getTime()/1000;
var current_date = date.format('yyyy/MM/dd hh:mm');
var from_date_time = Math.floor(date.getTime()/1000) - 60*60*24;
min_date_ms.setTime(from_date_time*1000);
var from_date = min_date_ms.format('yyyy/MM/dd hh:mm');
if (global_test_mode == 0){
    $('#pattern #weibo_from').datetimepicker({value:from_date,step:10});
    $('#pattern #weibo_to').datetimepicker({value:current_date,step:10});
}
else{
    $('#pattern #weibo_from').datetimepicker({value:from_date,step:10,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
    $('#pattern #weibo_to').datetimepicker({value:current_date,step:10,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
}   
pattern_bind_click();

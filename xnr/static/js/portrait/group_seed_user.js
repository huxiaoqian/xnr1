function seed_user_callback(data){
    console.log(data);
    //console.log(typeof(data));
    if (data == true) {
        alert('提交成功！');
    }
    else if (typeof(data) == 'string'){
        if (data == 'no seed user') {
            alert('用户列表为空！');
        }
        else if (data == 'task name invalid') {
            alert('任务名称已存在！');
        }
        else if (data == 'no query condition') {
            alert('请选择搜索条件！');
        }
        else if (data == 'seed user invalid') {
            alert('人物库中不存在该用户！');
        }
        else if (data == 'invalid seed user') {
            alert('无有效种子用户！');
        }
        else if(data =='invalid input for condition'){
          alert('请至少选择一个分析条件！');
        }
        else if(data == 'invalid input for query'){
          alert('请至少选择一个筛选条件！')
        }
        else if(data =='invalid input for range'){
          alert('请选择合理的时间范围！');
        }
        else if(data == 'invalid input for filter'){
          alert('请输入合理的影响力或重要度范围！');
        }
        else if(data == 'invalid input for count'){
          alert('请选择合理的人数！')
        }
    }
    else if(typeof(data) == 'object'){
        if (data[0] == 'invalid seed user'){
            alert('用户人数太少，无法提交任务！');
            return;
        }
        var out_list = data[1];
        if (out_list.length > 0){
            $('#group_out_list').empty();
            var html = '';
            html += '<table class="table table-bordered table-striped table-condensed datatable"><thead>';
            html += '<tr style="text-align:center;"><th>用户ID</th><th>昵称</th><th>粉丝数</th>';
            html += '<th>好友数</th><th>微博数</th><th>';
            html += '<input id="out_modal_all" type="checkbox" onclick="out_modal_all();"/></th></tr></thead>';
            html += '<tbody>';
            for (i=0;i<out_list.length;i++){
                html += '<tr><td class="center"><a target="_blank" href="http://weibo/com/u/' + out_list[i][0] + '">'+out_list[i][0]+'</a></td>';
                html += '<td class="center">'+out_list[i][1]+'</td>';
                html += '<td class="center">'+out_list[i][2]+'</td>';
                html += '<td class="center">'+out_list[i][4]+'</td>';
                html += '<td class="center">'+out_list[i][3]+'</td>';
                html += '<td><input name="group_recommend_in" type="checkbox" value="' + out_list[i][0] + '" /></td>';
                html += '</tr>';
            }
            html += '</tbody>';
            html += '</table>';
            $('#group_out_list').append(html);
            group_bind_recommend();
            $('#out_list_modal').modal();
        }
        alert('任务提交成功！');
    }
}
function seed_commit(){
    var valid = seed_user_check();
    if (valid){
        var user_mode = $('[name="user_choose"]:checked').val();
        if (user_mode == '1'){
            var seed_user_url = seed_single_user_data();
            console.log(seed_user_url);
            $.ajax({
                type:'GET',
                url:seed_user_url,
                dataType:'json',
                success:seed_user_callback
            });
        }
        else{
            seed_multi_user_data();
        }
    }
}
function bind_button_click(){
    $('#seed_user #show_advanced').click(function(){
        if($('#seed_user #advanced_condition').is(':hidden')){
            $(this).html('收起');
            $('#seed_user #advanced_condition').css('display', 'block');
        }
        else{
            $(this).html('高级');
            $('#seed_user #advanced_condition').css('display', 'none');
        }
    });
    $('#seed_user #time_checkbox').click(function(){
        if($(this).is(':checked')){
            $('#seed_user #events_from').attr('disabled',false);
            $('#seed_user #events_to').attr('disabled',false);
        }
        else{
            $('#seed_user #events_from').attr('disabled', true);
            $('#seed_user #events_to').attr('disabled', true);
        }
    });
    $('#seed_user #num-range').change(function(){
        var num = $('#seed_user #num-range').val();
        $('#seed_user #show_num').empty();
        $('#seed_user #show_num').append(num);    
    });
    $('#seed_user #delete_file').click(function(){
        seed_user_files = undefined;
        $('#seed_user #file_status').css('display', 'none');
    });
    $('#seed_user #uploadbtn').click(function(){
        var fileInput = document.getElementById('seed_file_upload');
        // 检查文件是否选择:
        if (!fileInput.value) {
            alert('没有选择文件');
            return;
        }
        // 获取File引用:
        var file = fileInput.value;
        //alert(file);
        if ((file.endsWith('.csv')) || (file.endsWith('.txt'))) {
            seed_user_files = fileInput.files;
            $('#seed_user #add_file').html(file);
            $('#seed_user #file_status').css('display', 'block');
            return false;
        }else{
            alert('Can only upload csv or txt file.');
            return;
        }
    });
}
function seed_user_init(){
    if (global_test_mode == 0){
        $('#seed_user #events_from').datetimepicker({value:seed_last_date,step:10});
        $('#seed_user #events_to').datetimepicker({value:seed_current_date,step:10});
    }
    else{
        $('#seed_user #events_from').datetimepicker({value:seed_last_date,minDate:min_date,maxDate:max_date,step:10});
        $('#seed_user #events_to').datetimepicker({value:seed_current_date,minDate:min_date,maxDate:max_date,step:10});
    }
    bind_button_click();
}

var seed_user_files = undefined;
var max_date = '+1970/01/01';
var min_date = '-1970/01/30';
var seed_current_date = choose_time_for_mode();
var seed_last_date = new Date();
seed_current_date.setHours(0,0,0);
var current_ts = seed_current_date.getTime();
seed_last_date.setTime(current_ts - 24*60*60*1000);
seed_current_date = seed_current_date.format('yyyy/MM/dd hh:mm');
seed_last_date = seed_last_date.format('yyyy/MM/dd hh:mm');

var seed_user_flag = false;
seed_user_init();

function seed_user_check(){             // check validation 
    var user_choose = $('[name="user_choose"]:checked').val();
    if (user_choose == '1'){
        if ($('#user_input').val() == ''){
            alert('请输入种子用户信息！');
            return false;
        }
    }
    else{
        if (seed_user_files == undefined){
            alert("请选择文件上传！");
            return false;
        }
    }
    //other form check starts
    var attr_weight = parseFloat($('#seed_user #attr_weight').val());
    var stru_weight = parseFloat($('#seed_user #stru_weight').val());
    if ((attr_weight < 0) || (attr_weight > 10) || (parseInt(attr_weight) != attr_weight)){
        alert('属性权重应该为0-10的整数！');
        return false;
    }
    if ((stru_weight < 0) || (stru_weight > 10) || (parseInt(stru_weight) != stru_weight)){
        alert('结构权重应该为0-10的整数！');
        return false;
    }
    var influ_from = parseFloat($('#seed_user #influ_from').val());
    var influ_to = parseFloat($('#seed_user #influ_to').val());
    if (influ_from > influ_to){
        alert('影响力左侧输入值应小于右侧输入值！');
        return false;
    }
    var impor_from = parseFloat($('#seed_user #impor_from').val());
    var impor_to = parseFloat($('#seed_user #impor_to').val());
    if (impor_from > impor_to){
        alert('重要度左侧输入值应小于右侧输入值！');
        return false;
    }
    if ($('#seed_user #time_checkbox').is(':checked')){
        var events_from = seed_user_timepicker($('#seed_user #events_from').val());
        var events_to = seed_user_timepicker($('#seed_user #events_to').val());
        if (events_from > events_to){
            alert('时间输入不合法！');
            return false;
        }
        if ((events_from > current_ts) || (events_to > current_ts)){
            alert('选择时间不能超过今日零时！');
            return false;
        }
    }
    if ($('#seed_user #num-range').val() == 0){
        alert('人数不能为0！');
        return false;
    }
    //group_information check starts  
    var group_name = $('#first_name').val();
    var remark = $('#first_remarks').val();
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
  return true;
}
function out_modal_all(){
  $('#seed_user input[name="group_recommend_in"]:not(:disabled)').prop('checked', $("#seed_user #out_modal_all").prop('checked'));
}
function group_bind_recommend(){
  $('#seed_user #group_recommend_confirm').click(function(){
      var cur_uids = [];
      $('#seed_user input[name="group_recommend_in"]:checked').each(function(){
        cur_uids.push($(this).attr('value'));
      })
      var recommend_date = new Date().format('yyyy-MM-dd');
      if(cur_uids.length == 0)
        alert("请选择至少一个用户！");
      else{
          var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + cur_uids.join(',') + '&submit_user=' + $('#useremail').text();
          $.ajax({
                type:'GET',
                url:recommend_confirm_url,
                dataType:'json',
                success:function(){
                    $('#out_list_modal').modal('hide');
                }
          });
        }
  });
}
//获取选择的条件，把参数传出获取返回值
function seed_single_user_data(){
    var url = '';
    url += '/detect/user_string/?';
    if ($('#content_choose').val() == 'url'){
        url += 'seed_user_type=uid';
        var url_string = $('#user_input').val();
        var string_list = url_string.split('http://weibo.com/p/');
        var uid_list = new Array();
        for (var i = 1; i < string_list.length; i++){
            uid_list.push(string_list[i].substring(6,16));
        }
        console.log(uid_list);
        url += '&seed_user_string=' + uid_list.join('/');
    }
    else{
        url += 'seed_user_type=' + $('#content_choose').val();
        url += '&seed_user_string=' + $('#user_input').val();
    }
    if ($('advanced_conditon').is(':hidden')){
        url += '&extend_mark=0';
        return url;
    }
    else{
        url += '&extend_mark=1';
        //attribute
        url += '&attribute_weight=' + $('#seed_user #attr_weight').val();
        $('#seed_user #attribute .inline-checkbox').each(function(){
            if($(this).is(':checked')){
                url += '&' + $(this).next().attr('id') + '=1';
            }
        });
        //structure
        url += '&structure_weight=' + $('#seed_user #stru_weight').val();
        url += '&hop=' + $('#seed_user [name="hop_choose"]:checked').val();
        $('#seed_user #structure .inline-checkbox').each(function(){
            if($(this).is(':checked')){
                url += '&' + $(this).next().attr('id') + '=1';
            }
        });
        //events
        url += '&text=' + $('#seed_user #events_keywords').val();
        if ($('#seed_user #time_checkbox').is(':checked')){
            url += '&timestamp_from=' + seed_user_timepicker($('#seed_user #events_from').val());
            url += '&timestamp_to=' + seed_user_timepicker($('#seed_user #events_to').val());
        }
        //extension
        url += '&count=' + $('#seed_user #num-range').val();
        url += '&influence_from=' + $('#seed_user #influ_from').val();
        url += '&influence_to=' + $('#seed_user #influ_to').val();
        url += '&importance_from=' + $('#seed_user #impor_from').val();
        url += '&importance_to=' + $('#seed_user #impor_to').val();
        // group_task
        url += '&task_name=' + $('#first_name').val();
        url += '&state=' + $('#first_remarks').val();
        url += '&submit_user=' + $('#useremail').text();
        return url;
    }
}
function seed_multi_user_data(){
    var upload_job = {};
    upload_job['seed_user_type'] = $('#content_choose').val();
    // group_task
    upload_job['task_name'] = $('#first_name').val();
    upload_job['state']  = $('#first_remarks').val();
    upload_job['submit_user'] = $('#useremail').text();
    if ($('#advanced_condition').is(':hidden')){
        upload_job['extend'] = '0';
    }
    else{
        upload_job['extend'] = '1';
        //attribute
        upload_job['attribute_weight'] = $('#seed_user #attr_weight').val();
        $('#seed_user #attribute .inline-checkbox').each(function(){
            var attr_id = $(this).next().attr('id');
            if($(this).is(':checked')){
                upload_job[attr_id] = '1';
            }
            else{
                upload_job[attr_id] = '0';
            }
        });
        //structure
        upload_job['structure_weight'] = $('#seed_user #stru_weight').val();
        upload_job['hop'] = $('#seed_user [name="hop_choose"]:checked').val();
        $('#seed_user #structure .inline-checkbox').each(function(){
            var attr_id = $(this).next().attr('id');
            if($(this).is(':checked')){
                upload_job[attr_id] = '1';
            }
            else{
                upload_job[attr_id] = '0';
            }
        });
        //events
        upload_job['text'] = $('#seed_user #events_keywords').val();
        if ($('#seed_user #time_checkbox').is(':checked')){
            upload_job['timestamp_from'] = seed_user_timepicker($('#seed_user #events_from').val());
            upload_job['timestamp_to'] = seed_user_timepicker($('#seed_user #events_to').val());
        }
        //extension
        upload_job['count'] = $('#seed_user #num-range').val();
        upload_job['influence_from'] = $('#seed_user #influ_from').val();
        upload_job['influence_to'] =  $('#seed_user #influ_to').val();
        upload_job['importance_from'] = $('#seed_user #impor_from').val();
        upload_job['importance_to'] = $('#seed_user #impor_to').val();
    }
    handleFileSelect(upload_job);
}
function seed_user_timepicker(str){
    var date_time = str.split(' ');
    var dates = date_time[0].split('/');
    var yy = parseInt(dates[0]);
    var mm = parseInt(dates[1]) - 1;
    var dd = parseInt(dates[2]);
    var times = date_time[1].split(':');
    var hh = parseInt(times[0]);
    var minute = parseInt(times[1]);
    var final_date = new Date();
    final_date.setFullYear(yy,mm,dd);
    final_date.setHours(hh,minute);
    final_date = Math.floor(final_date.getTime()/1000);
    return final_date;
}

function handleFileSelect(upload_job){
    var files = seed_user_files;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            upload_job['upload_data'] = a;
            console.log(upload_job);
            $.ajax({   
                type:"POST",  
                url:"/detect/user_file/",
                contentType:"application/json",
                data:JSON.stringify(upload_job),
                dataType: "json",
                success: seed_user_callback
            });
        };            
        reader.readAsText(f,'GB2312');                                                        
    }
}


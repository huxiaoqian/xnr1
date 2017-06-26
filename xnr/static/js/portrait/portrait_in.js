// Date format
Date.prototype.format = function(format){
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}
function Search_weibo_recommend(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_recommend.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Re_Draw_table: function(data){
    var div = that.div;
    $(div).empty();
    var user_url;
    html = '';
    html += '<table id="recommend_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="width:140px">用户ID</th><th>昵称</th><th>注册地</th><th style="width:100px">粉丝数</th><th style="width:100px">微博数</th><th style="width:100px">影响力</th><th style="width:100px">网民详情</th><th>' + '<input name="page_all" id="page_all" type="checkbox" value="" onclick="recommend_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if (item[i][1] == '未知'){
          item[i][1] = item[i][0];
      } 
      if(item[i][5]!='未知'){
        item[i][5] = item[i][5].toFixed(2);
      }
      else{
          item[i][5] = '';
      }
      if (item[i][3] == '未知'){
          item[i][3] = '';
      }
      if (item[i][4] == '未知'){
          item[i][4] = '';
      }
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][3] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][4] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][5] +'</td>';
      html += '<td class="center" style="width:100px"><a style="cursor:pointer;" name="details" id="'+ item[i][0] +'" title="'+ item[i][1] +'">详情</a></td>';
      html += '<td class="center"><input name="in_status" class="in_status" type="checkbox" value="' + item[i][0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);

    $('[name="details"]').click(function(){
      var detail_uid = $(this).attr('id');
      var detail_uname = $(this).attr('title');
      var detail_url = '/recommentation/show_in_more/?uid=' + detail_uid;
      $.ajax({
        url: detail_url,
        type: 'GET',
        dataType: 'json',
        async: false,
        success:show_details
      });
      function show_details(data){
        if(data['time_trend'].length==0){
          $('#line_chart').empty();
          $('#line_chart').append('<div style="text-align:center">暂无数据！</div>');
        }
        else{
          //$('#line_chart').empty();
          var line_chart_xaxis = [];
          for(var k in data['time_trend'][0])
            line_chart_xaxis.push(new Date(parseInt(data['time_trend'][0][k])*1000).format("MM-dd hh:mm"));
          var line_chart_yaxis = data['time_trend'][1];
          draw_line_chart(line_chart_xaxis.reverse(), line_chart_yaxis.reverse(), 'line_chart', detail_uname);
        }
        $('#place').empty();
        if(data['activity_geo'].length==0){
          $('#in_detail').css('height','70px');
          $('#place').append('<h4 style="text-align:center">活跃地点</h4><div style="text-align:center">暂无数据！</div>');
        }
        else{
          $('#in_detail').css('height','300px');
          var place_html = '';
          place_html += '<h4 style="text-align:center">活跃地点</h4>';
          place_html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
          place_html += '<thead><tr><th style="text-align:center;vertical-align:middle;width:80px">排名</th><th style="text-align:center;vertical-align:middle;width:200px">地点</th><th style="text-align:center;vertical-align:middle;width:80px">微博数</th></tr></thead>';
          place_html += '<tbody>';
          for(var m in data['activity_geo']){
            if(parseInt(m)<5){
              place_html += '<tr>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ (parseInt(m)+1) +'</td>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['activity_geo'][m][0] +'</td>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['activity_geo'][m][1] +'</td>';
              place_html += '</tr>';
            }
          }
          place_html += '</tbody>';
          place_html += '</table>';

          $('#place').append(place_html);
        }

        $('#hashtag').empty();
        if(data['hashtag'].length==0){
          $('#hashtag').append('<h4 style="text-align:center">微话题</h4><div style="text-align:center">暂无数据！</div>');
        }
        else{
          $('#in_detail').css('height','300px');
          var hashtag_html = '';
          hashtag_html += '<h4 style="text-align:center">微话题</h4>';
          hashtag_html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
          hashtag_html += '<thead><tr><th style="text-align:center;vertical-align:middle;width:80px">排名</th><th style="text-align:center;vertical-align:middle;width:200px">微话题</th><th style="text-align:center;vertical-align:middle;width:80px">微博数</th></tr></thead>';
          hashtag_html += '<tbody>';
          for(var n in data['hashtag']){
            if(parseInt(n)<5){
              hashtag_html += '<tr>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ (parseInt(n)+1) +'</td>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['hashtag'][n][0] +'</td>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['hashtag'][n][1] +'</td>';
              hashtag_html += '</tr>';
            }
          }
          hashtag_html += '</tbody>';
          hashtag_html += '</table>';
          $('#hashtag').append(hashtag_html);
        }

        $('#details_modal').modal();
      }
    });

    $('#recommend_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "custom_bootstrap",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页",
        }
    });
    // page control start
    global_pre_page = 1;
    global_choose_uids = new Array();
    // page control end
  }
}

function confirm_ok(data){
  if(data)
    alert('操作成功！');
}

function bindOption(){
      $('#recommend_button').click(function(){
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
          else{
		  var cur_uids = [];
		  $('input[name="in_status"]:checked').each(function(){
		    cur_uids.push($(this).attr('value'));
		  })
		  global_choose_uids[global_pre_page] = cur_uids;
		  var recommend_uids = [];
		  for (var key in global_choose_uids){
		      var temp_list = global_choose_uids[key];
		      for (var i = 0;i < temp_list.length;i++){
			  recommend_uids.push(temp_list[i]);
		      }
		  }
		  var recommend_date = $("#recommend_date_select").val()
		  var uids_trans = '';
		  for(var i in recommend_uids){
		      uids_trans += recommend_uids[i];
		      if(i<(recommend_uids.length-1))
			uids_trans += ',';
		  }
		  if(recommend_uids.length == 0){
		    alert("请选择至少一个用户！");
		  }
		  else{
		      $('#recommend').empty();
		      var waiting_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
		      $('#recommend').append(waiting_html);
		      var admin =$('#useremail').text();
		      var recommend_confirm_url = '/recommentation/identify_in/?submit_user='+admin+'&date=' + recommend_date + '&uid_list=' + uids_trans;
		      console.log(recommend_confirm_url);
		      draw_table_recommend.call_sync_ajax_request(recommend_confirm_url, draw_table_recommend.ajax_method, confirm_ok);
		      var recommend_type = $('input[name="recommend_type"]:checked').val();
		      
		      var url_recommend_new = '/recommentation/show_in/?submit_user='+admin+'&date=' + $("#recommend_date_select").val() + '&type=' + recommend_type;
		      draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
		      draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
		  }
          }
      });
      
      $('#recommend_date_button').click(function(){
          var recommend_type = $('input[name="recommend_type"]:checked').val();
          var admin =$('#useremail').text();
          var url_recommend_new = '/recommentation/show_in/?submit_user='+admin+'&date=' + $("#recommend_date_select").val() + '&type=' + recommend_type;
          draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
          draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
      });

       $('input[name="recommend_type"]').change(function(){
           if ($(this).val() == 'upload'){
               $('#upload_panel').css('display', 'block');
               $('#recommend_panel').css('display', 'none');
           }
           else{
               $('#upload_panel').css('display', 'none');
               $('#recommend_panel').css('display', 'block');
           }
       });
        
        $('#delete_file').click(function(){
            seed_user_files = undefined;
            $('#file_status').css('display', 'none');
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

// page control start
var global_pre_page = 1;
var global_choose_uids = new Array();
// page control end
var seed_user_files = undefined;

var now_date = choose_time_for_mode();
//var last_date = new Date(now_date - 24*60*60*1000)
var last_date = new Date(now_date)
var last = last_date.format('yyyy-MM-dd');
var recommend_type = $('input[name="recommend_type"]:checked').val();
var admin =$('#useremail').text();
var url_recommend = '/recommentation/show_in/?submit_user='+admin+'&date=' + last + '&type=' + recommend_type ;
date_initial();
bindOption();
draw_table_recommend = new Search_weibo_recommend(url_recommend, '#recommend');
draw_table_recommend.call_sync_ajax_request(url_recommend, draw_table_recommend.ajax_method, draw_table_recommend.Re_Draw_table);

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
                url:"/recommentation/submit_identify_in/",
                contentType:"application/json",
                data:JSON.stringify(upload_job),
                dataType: "json",
                success: file_callback,
            });
        };            
        reader.readAsText(f,'GB2312');                                                        
    }
}
function file_callback(data){
    console.log(data);
    if (data == 'uname list all in'){
        alert('用户已入库！');
    }
    else if(data == 'uname list valid'){
        alert('用户名不合法！');
    }
    else{
        alert('入库成功！');
    }
}

function date_initial(){
  var recommend_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(last_date-24*60*60*1000*(6-i));
    recommend_date[i] = today.format('yyyy-MM-dd');
  }
  $("#recommend_date_select").empty();
  var recommend_date_html = '';
  recommend_date_html += '<option value="' + recommend_date[0] + '">' + recommend_date[0] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[1] + '">' + recommend_date[1] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[2] + '">' + recommend_date[2] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[3] + '">' + recommend_date[3] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[4] + '">' + recommend_date[4] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[5] + '">' + recommend_date[5] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[6] + '" selected="selected">' + recommend_date[6] + '</option>';
  $("#recommend_date_select").append(recommend_date_html);
}


function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#page_all").prop('checked'));
}

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}

function draw_line_chart(xaxis, yaxis, div, uname){
  var uname_text = '"' + uname + '"的微博数';
  var line_chart_option = {
    title : {
        text: '用户微博走势图',
        subtext: '',
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:[uname_text]
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            axisLabel:{
              interval:5,
            },
            data : xaxis,
        }
    ],
    yAxis : [
        {
            type : 'value',
        }
    ],
    series : [
        {
            name:uname_text,
            type:'line',
            data:yaxis,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
    ]
  };
  var draw_init2 = echarts.init(document.getElementById(div));
  draw_init2.setOption(line_chart_option);
}


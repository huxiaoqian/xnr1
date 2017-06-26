 function Attention(){
  this.ajax_method = 'GET';
}
Attention.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
      person_call_ajax_request(url, callback);
  },
Draw_attention:function(data){
  var texts = '';
	var items = data;
  var UserName = document.getElementById('username').innerHTML;
	if(items==null){
		var say = document.getElementById('test1');
		say.innerHTML = '该用户暂无此数据';
	 }else{
		    attention(items,UserID,UserName,texts);
        draw_topic(items['in_portrait_result']);
        draw_field(items['in_portrait_result']);
        draw_more_topic(items['in_portrait_result']);        
        draw_more_field(items['in_portrait_result']);
        draw_out_list(items['out_portrait_list']);
        draw_in_list(items['in_portrait_list']);
	 }	
  }
}

function attention(data,UserID,UserName,texts){
    var out_data = data['out_portrait_list'];
    var in_data = data['in_portrait_list'];
    var personal_url = '/index/personal/?uid=';
    var nod = {};
    var linestyle = '';
    var select_graph = $('input[name="graph-type"]:checked').attr("title");
    nodeContent = []
    nod['category'] = 0;
    nod['name'] = UserName+'('+UserID+')';
    nod['label'] = UserName;
    nod['value'] = 10;
    nodeContent.push(nod);
    var linkline =[];
    var rename_out = '';
    for (var i=0;i<out_data.length;i++){
            nod = {};
            nod['category'] = 2;
            if(out_data[i][0]=='None'){
              var nod_name_out = '未知UID';
            }else{
              var nod_name_out = out_data[i][0];
            }
            if(out_data[i][1]=='unknown'||out_data[i][1]=='未知'){
              //rename_out = '未知';
              nod['name'] = nod_name_out;
              nod['label'] = nod_name_out;
            }else{
              rename_out = out_data[i][1];
              nod['name'] = rename_out +'('+nod_name_out+')';
              nod['label'] = rename_out;
            }
            //nod['name'] = nod_name_out;
            //nod['name'] = rename_out +'('+nod_name_out+')';
            //nod['label'] = rename_out;
            nod['value'] = 1;
            //nod['value'] = out_data[i][3];
            nodeContent.push(nod);
            var line ={};
            if( select_graph == '转发'||select_graph == '评论'){
              line['source'] = nod['name'];
              line['target'] = UserName+'('+UserID+')';
              line['weight'] = 1;
              linkline.push(line);
              linestyle = 'arrow'      
            }else if(select_graph == '被转发'||select_graph == '被评论'||select_graph == '提及'){
              line['source'] = UserName+'('+UserID+')' ;
              line['target'] = nod['name'];
              line['weight'] = 1;
              linkline.push(line);
              linestyle = 'arrow'  
            }else{
              line['source'] = nod['name'];
              line['target'] = UserName+'('+UserID+')';
              line['weight'] = 1;
              linkline.push(line);
              linestyle = 'none'         
            }
    }
    var rename_in = '';
    for (var i=0;i<in_data.length;i++){
      //console.log(in_data);
      nod = {};
      nod['category'] = 1;
      if(in_data[i][0]=='None'){
        var nod_name_in = '未知UID';
      }else{
        var nod_name_in = in_data[i][0];
      }
      if(in_data[i][1]=='unknown'){
        //var rename_in = '未知';
        nod['name'] = nod_name_in;
        nod['label'] = nod_name_in;
      }else{
        var rename_in = in_data[i][1];
        nod['name'] = rename_in +'('+nod_name_in+')';
        nod['label'] = rename_in;
      }
      //nod['name'] = nod_name_in;
      //nod['name'] = rename_in +'('+nod_name_in+')';
      //nod['label'] = rename_in;
      nod['value'] = 1;
      //nod['value'] = in_data[i][4];
      nodeContent.push(nod);
      var line ={};
      if( select_graph == '转发'||select_graph == '评论'){
        line['source'] = nod['name'];
        line['target'] = UserName+'('+UserID+')';
        line['weight'] = 1;
        linkline.push(line);
        linestyle = 'arrow'      
      }else if(select_graph == '被转发'||select_graph == '被评论'||select_graph == '提及'){
        line['source'] = UserName+'('+UserID+')' ;
        line['target'] = nod['name'];
        line['weight'] = 1;
        linkline.push(line);
        linestyle = 'arrow'  
      }else{
        line['source'] = nod['name'];
        line['target'] = UserName+'('+UserID+')';
        line['weight'] = 1;
        linkline.push(line);
        linestyle = 'none'         
      }

    }
	var myChart3 = echarts.init(document.getElementById('test1'));
	var option = {
            title : {
                text: texts,
                x:'left',
                y:'top'
            },
              tooltip : {
                  trigger: 'item',
                  formatter: ' {b}'
              },
            legend: {
                x: 'right',
                data:['用户','未入库','已入库']
            },
            series : [
                {
                    type:'force',
                    //name : "人物关系",
                    ribbonType: false,
                    categories : [
                        {
                            name: '用户'
                        },
                       {
                            name:'已入库'
                        },
						{
                            name:'未入库'
                        },
                    ],
                    itemStyle: {
                        normal: {
                            label: {
                                show: true,
                                textStyle: {
                                    color: '#333'
                                }
                            },
                            nodeStyle : {
                                brushType : 'both',
                                borderColor : 'rgba(255,215,0,0.4)',
                                borderWidth : 1
                            },
                            linkStyle: {
                                type: 'curve'
                            }
                        },
                        emphasis: {
                            label: {
                                show: false
                                // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                            },
                            nodeStyle : {
                                //r: 30
                            },
                            linkStyle : {}
                        }
                    },
                    useWorker: false,
                    minRadius : 15,
                    maxRadius : 25,
                    gravity: 1.1,
                    scaling: 1.1,
                    linkSymbol: linestyle,
                    roam: 'move',
                    nodes:nodeContent,
                    links : linkline
                }
            ]
    };  
	myChart3.setOption(option);	
    require([
            'echarts'
        ],
        function(ec){
            var ecConfig = require('echarts/config');
            function focus(param) {
                var data = param.data;
                var links = option.series[0].links;
                var nodes = option.series[0].nodes;
                if (
                    data.source != null
                    && data.target != null
                ) { //点击的是边
                    var sourceNode = nodes.filter(function (n) {return n.name == data.source})[0];
                    var targetNode = nodes.filter(function (n) {return n.name == data.target})[0];
                    } else {
                    var node_url;
                    var weibo_url ;
                    var ajax_url ;
                    if(data.category == 0){
                        ajax_url = '/attribute/identify_uid/?uid='+UserID;
                        weibo_url = 'http://weibo.com/u/'+ UserID;
                        node_url = personal_url + UserID;
                    }else{
                        ajax_url = '/attribute/identify_uid/?uid='+data.name; 
                        weibo_url = 'http://weibo.com/u/'+ data.name;
                        node_url = personal_url + data.name;
                    }                 
                    $.ajax({
                      url: ajax_url,
                      type: 'GET',
                      dataType: 'json',
                      async: false,
                      success:function(data){
                        if(data == 1){
                            window.open(node_url);
                        }
                        else{
                            window.open(weibo_url);
                        }
                      }
                    });
                    
                }
            }
                myChart3.on(ecConfig.EVENT.CLICK, focus)

                myChart3.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                });
            }
    )   
}


function draw_topic(data){
    $('#topic').empty();
    var datas = data['topic'];
    html = '';
    if(datas.length==0){
      html = '无入库用户';
    }else{
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">话题</th><th style="text-align:center">次数</th></tr>';
    var i = 1;
    for (var key in datas) {
       html += '<tr><th style="text-align:center">' + i + '</th><th style="text-align:center">' + datas[key][0] + '</th><th style="text-align:center">' + datas[key][1] +  '</th></tr>';
       i = i + 1;
       if(i >=6 ){
        break;
       }
    }
    html += '</table>'; 
  }
    $('#topic').append(html);                  
}

function draw_more_topic(data){
    $('#topic0').empty();
    var datas = data['topic'];
    html = '';
    if(datas.length==0){
      html = '无入库用户';
    }else{
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">话题</th><th style="text-align:center">次数</th></tr>';
    var i = 1;
    for (var key in datas) {
       html += '<tr><th style="text-align:center">' + i + '</th><th style="text-align:center">' + datas[key][0] + '</th><th style="text-align:center">' + datas[key][1] +  '</th></tr>';
    i = i + 1;
    }
    html += '</table>'; 
    }
    $('#topic0').append(html);                  
}

function draw_field(data){
    $('#field').empty();
    html = '';
    var datas = data['domain'];
    //console.log(datas.length);
    if(datas.length==0){
      html = '无入库用户';
    }else{
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">领域</th><th style="text-align:center">次数</th></tr>';
    var i = 1;
    for (var key in datas) {
       html += '<tr><th style="text-align:center">' + i + '</th><th style="text-align:center">' + datas[key][0] + '</th><th style="text-align:center">' + datas[key][1] +  '</th></tr>';
       i = i + 1;
       if(i >=6 ){
        break;
       }
     }
    }
    html += '</table>'; 
    $('#field').append(html);                  
}

function draw_more_field(data){
    $('#field0').empty();
    var datas = data['domain'];
    html = '';
    if(datas.length==0){
      html = '无入库用户';
    }else{
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">领域</th><th style="text-align:center">次数</th></tr>';
    var i = 1;
    for (var key in datas) {
       html += '<tr><th style="text-align:center">' + i + '</th><th style="text-align:center">' + datas[key][0] + '</th><th style="text-align:center">' + datas[key][1] +  '</th></tr>';
    i = i + 1;
     }
    html += '</table>'; 
    }
    $('#field0').append(html);                  
}


function draw_out_list(data){
    $('#out_list').empty();
    var select_graph = $('input[name="graph-type"]:checked').attr("title");
    html = '';
    if(data.length==0){html+='无未入库用户';}else{
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="width:90px;text-align:center;">用户ID</th><th style="width:150px;text-align:center;">昵称</th><th style="text-align:center;width:80px;">'+select_graph+'数</th><th style="text-align:center;">粉丝数</th><th style="text-align:center;">' + '<input name="out_choose_all" id="out_choose_all" type="checkbox" value="" onclick="out_choose_all()" />' + '</th></tr></thead>';
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      //item = replace_space(item);
      //global_data[item[0]] = item; // make global data\
      var list_id = '';
      if(item[0]=='None'){
        continue;
      }else if(item[0]=='' && item[1].length>0){
        var user_url = '<tr id="未知"><td style="text-align:center" style="width:150px;">未知</td>';
      }
      else{
        list_id = item[0];
        var user_url0 = 'http://weibo.com/u/'+ list_id;
        var user_url = '<tr id=' + list_id +'>';
        user_url+= '<td style="text-align:center" name="uids"><a href='+ user_url0+ '  target="_blank">'+ list_id +'</td>';
      }
        html += user_url;
        html += '<td style="text-align:center" style="width:150px;">'+ item[1] +'</td>';
        html += '<td style="text-align:center" style="width:100px;">'+ item[2] +'</td>';
        html += '<td style="text-align:center" style="width:100px;">'+ item[3] +'</td>';
        html += '<td style="text-align:center"><input name="out_list_option" class="search_result_option" type="checkbox" value="' + item[0] + '" /></td>';
        html += '</tr>';
      //}
    }
    html += '</tbody>';
    html += '</table>';
  }
    $('#out_list').append(html);
}


function draw_in_list(data){
  //console.log(personalData.uname);
  //console.log(uname);
    var select_graph = $('input[name="graph-type"]:checked').attr("title");
    if(personalData.uname == 'unknown'){
      var uname = '未知';
    }else if(personalData.uname == 'undefined'){
      var uname = '未知';
    }else{var uname = personalData.uname};
    $('#in_list').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th  style="/*width:90px;*/text-align:center;">用户ID</th><th style="/*width:150px;*/text-align:center;">昵称</th><th style="text-align:center;">影响力</th><th style="text-align:center;">重要度</th><th style="text-align:center;">'+select_graph+'数</th><th style="text-align:center;">' + '<input name="in_choose_all" id="in_choose_all" type="checkbox" value="" onclick="in_choose_all()" />' + '</th></tr></thead>';
    html += '<tbody>';
    var user_url = 'http://weibo.com/u/'+ uid;
    html += '<tr id=' + uid +'>';
    html += '<td style="text-align:center" name="uids"><a href='+ user_url+ '  target="_blank">'+ uid +'</td>';
    html += '<td style="text-align:center" style="width:150px;">'+ uname +'</td>';
    html += '<td style="text-align:center" style="width:70px;">'+ personalData.influence.toFixed(2) +'</td>';
    html += '<td style="text-align:center" style="width:70px;">'+ personalData.importance.toFixed(2) +'</td>';
    html += '<td style="text-align:center" style="width:70px;">-</td>';
    html += '<td style="text-align:center"><input name="in_list_option" class="search_result_option" type="checkbox" value="' + uid + '" /></td>';
    html += '</tr>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      //item = replace_space(item);
      //global_data[item[0]] = item; // make global data
      var user_url = 'http://weibo.com/u/'+ item[0];
      html += '<tr id=' + item[0] +'>';
      html += '<td style="text-align:center" name="uids"><a href='+ user_url+ '  target="_blank">'+ item[0] +'</td>';
      if(item[1] == 'unknown'){
        var user_name = '未知';
      }else if(item[1]  == 'undefined'){
      var user_name  = '未知';
     }else{ var user_name =item[1]};
     //console.log(item[1]);
      html += '<td style="text-align:center" style="width:150px;">'+ user_name +'</td>';
      html += '<td style="text-align:center" style="width:70px;">'+ item[2].toFixed(2) +'</td>';
      html += '<td style="text-align:center" style="width:70px;">'+ item[3].toFixed(2) +'</td>';
      html += '<td style="text-align:center" style="width:70px;">'+ item[4] +'</td>';
      html += '<td style="text-align:center"><input name="in_list_option" class="search_result_option" type="checkbox" value="' + item[0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#in_list').append(html);
}

function out_choose_all(){
  $('input[name="out_list_option"]').prop('checked', $("#out_choose_all").prop('checked'));
}
function in_choose_all(){
  $('input[name="in_list_option"]').prop('checked', $("#in_choose_all").prop('checked'));
}

function out_list_button(){
  var cur_uids = []
  var noneflag = true;
  $('input[name="out_list_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
      if($(this).parent().prev().prev().prev().prev().text()=='未知'){
        noneflag = false;
      }
  });
  //var compute_type = $('input[name="compute-type"]:checked').val();
 // var recommend_date = new Date().format('yyyy-MM-dd');
  var recommend_date0 = choose_time_for_mode();    // choose_time_for_mode().format('yyyy-MM-dd');
  recommend_date0.setDate(recommend_date0.getDate()-1);
  var recommend_date = recommend_date0.format('yyyy-MM-dd');
  if(noneflag==false){
    alert('ID未知用户不能推荐入库！');
  }else{
  if (cur_uids.length == 0){
    alert("请选择至少一个用户！");
  }
  else{
      /*
      if (compute_type==2){
        var a = confirm('您选择了预约计算，系统将在今日24:00自动启动计算！');
        if (a == true){
            var compute_url = '/recommentation/identify_in/?date='+recommend_date+'&uid_list='+cur_uids+'&status='+compute_type;
            console.log(compute_url);
            Attention.call_sync_ajax_request(compute_url, Attention.ajax_method, confirm_ok);
        }
      }
      else{
          var sure = confirm('立即计算会消耗系统较多资源，您确定要立即计算吗？');
          if(sure==true){
            // $('#out_list').empty();
            // var waiting_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
            // $('#out_list').append(waiting_html);
            var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + cur_uids + '&status=' + compute_type;
            console.log(recommend_confirm_url);
            Attention.call_sync_ajax_request(recommend_confirm_url, Attention.ajax_method, confirm_ok);
          }    
      }
      */
    var admin = $('#d_useremail').text();
    var compute_url = '/recommentation/identify_in/?submit_user='+admin+'&date='+recommend_date+'&uid_list='+cur_uids;
    Attention.call_sync_ajax_request(compute_url, Attention.ajax_method, confirm_ok);
  }
}
}

function in_list_button(){
  var group_confirm_uids = [];
  $('input[name="in_list_option"]:checked').each(function(){
      group_confirm_uids.push($(this).attr('value'));
  })
  var group_ajax_url = '/group/submit_task/';
  //var group_ajax_url = '/detect/add_detect2analysis/';
  //var group_url = '/index/group_result/';
  var group_url = '/index/group/#';
  var group_name = $('input[name="so_group_name"]').val();
  var remark = $('input[name="so_states"]').val();
  if (group_confirm_uids.length == 0){
      alert('请至少选择一名用户！');
      return;
  }
  if (group_name.length == 0){
      alert('群体名称不能为空');
      return;
  }
  var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
  if (!group_name.match(reg)){
    alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if ((remark.length > 0) && (!remark.match(reg))){
    alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if(group_confirm_uids.length <1){
    alert("请选择至少1个用户");
    return ;
  }
  var job = {"task_name":group_name, "uid_list":group_confirm_uids, "state":remark};
  $.ajax({
      type:'POST',
      url: group_ajax_url,
      contentType:"application/json",
      data: JSON.stringify(job),
      dataType: "json",
      success: callback
  });
  function callback(data){
      if (data == '1'){
          window.location.href = group_url;
      }
      else{
          alert('已存在相同名称的群体分析任务,请重试一次!');
      }
  }
}

function confirm_ok(data){
  if(data)
    alert('操作成功！');
}
function bind_social_mode_choose(){
    $('#graph_button').click(function(){
      var select_graph = $('input[name="graph-type"]:checked').val();
      var select_num=document.getElementById('num-range').value;
      var UserName = document.getElementById('username').innerHTML;
        $("#test1").empty();
        $("#test0").empty();
        $("#field").empty();
        $("#topic").empty();
        //console.log(uid);
      if (select_graph == 1){
          var test_html='转发情况 <hr style="margin-top:10px;margin-right:20px;" /> ';
        $("#test0").append(test_html);
        var url = '/attribute/attention/?uid='+uid+'&top_count='+select_num  ;
        Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
      }
      else if(select_graph == 2){
        var test_html='被转发情况 <hr style="margin-top:10px;margin-right:20px;" /> ';
        $("#test0").append(test_html);
        var url = '/attribute/follower/?uid='+uid+'&top_count='+select_num ;
        Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
      }
      else if(select_graph == 3){
        var test_html='提及情况 <hr style="margin-top:10px;margin-right:20px;" /> ';
        $("#test0").append(test_html);
        var url = '/attribute/mention/?uid='+uid+'&top_count='+select_num  ;
        Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
      }
      else if(select_graph == 4){
        var test_html='评论情况 <hr style="margin-top:10px;margin-right:20px;" /> ';
        $("#test0").append(test_html);
        var url = '/attribute/comment/?uid='+uid+'&top_count='+select_num  ;
        Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
        //Comment.call_sync_ajax_request(url, Comment.ajax_method, Comment.Draw_picture);
      }
      else if(select_graph == 5){
        var test_html='被评论情况 <hr style="margin-top:10px;margin-right:20px;" /> ';
        $("#test0").append(test_html);
        var url = '/attribute/be_comment/?uid='+uid+'&top_count='+select_num  ;
        Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
        //Comment.call_sync_ajax_request(url, Comment.ajax_method, Comment.Draw_picture);
      }
      else if(select_graph == 6){
        var test_html='互动情况 <hr style="margin-top:10px;margin-right:20px;" /> ';
        $("#test0").append(test_html);
        var url = '/attribute/bidirect_interaction/?uid='+uid+'&top_count='+select_num  ;
        Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
      }      
    }); 
  }
function social_load(){
    var url = '/attribute/attention/?uid='+uid+'&top_count='+select_num ;
    Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);
    bind_social_mode_choose();
}
var Attention = new Attention();


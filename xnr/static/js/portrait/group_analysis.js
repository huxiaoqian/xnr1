 function Search_weibo(){
  this.ajax_method = 'GET';
}

var global_pre_page = 1;
var global_choose_uids = new Array();

Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_attribute_name: function(data){
    $('#attribute_name').empty();
    html = '';
    html += '<select id="select_attribute_name" style="min-width:75px;" >';

    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        html += '<option value="' + data[s] + '">' + data[s] + '</option>';
    }
    $('#attribute_name').append(html);
  },

  Draw_attribute_value: function(data){
    // console.log(data);
    $('#attribute_value').empty();
    html = '';
    html += '<select id="select_attribute_value" style="min-width:75px;">';
    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        html += '<option value="' + data[s] + '">' + data[s] + '</option>';
} 
    $('#attribute_value').append(html);
  },
  Draw_add_group_tag: function(data){
    if(data == true){
        alert('操作成功');
        $('#myModal').modal('hide'); 
    }else{
        alert('提交失败，请检查后重试');
    }

  },
  Draw_group_tag: function(data){
    var height = '';
    height = (data.length*50).toFixed(0) + 'px'; 
    //document.getElementById("lable").style.height=height; 
    key_container = [];
    value_container = [];
    for (i=0;i<data.length;i++){
        s=i.toString();
        key_container.push(data[s]['0']);
        value_container.push(data[s]['1']);
    }
    
},

Draw_overview: function(data){
    //画星星
    if(data.importance_star==undefined){
        importance_star = '无此数据';
    }else{
    var importance_star = '';
    for(var i=0;i<data.importance_star;i++){
        importance_star += '<img src="/static/img/star-yellow.png" style="width:23px;">'
    };}
    if(data.activeness_star==undefined){
        activeness_star = '无此数据';
    }else{
     var activeness_star = '';
    for(var i=0;i<data.activeness_star;i++){
        activeness_star += '<img src="/static/img/star-yellow.png" style="width:23px;">'
    };}
    if(data.density_star==undefined){
        density_star = '无此数据';
    }else{
     var density_star = '';
    for(var i=0;i<data.density_star;i++){
        density_star += '<img src="/static/img/star-yellow.png" style="width:23px;" >'
    };}
    if(data.influence_star==undefined){
        influence_star = '无此数据';
    }else{    
     var influence_star = '';
    for(var i=0;i<data.influence_star;i++){
        influence_star += '<img src="/static/img/star-yellow.png" style="width:23px;" >'
    };}
    // if(data.importance_star==undefined){
    //     importance_star = '无此数据';
    // }else{
    //     importance_star = data.importance_star;
    // }
    // if(data.activeness_star==undefined){
    //     activeness_star = '无此数据';
    // }else{
    //     activeness_star = data.activeness_star;
    // }
    // if(data.density_star==undefined){
    //     density_star = '无此数据';
    // }else{
    //     density_star = data.density_star;
    // }
    // if(data.influence_star==undefined){
    //     influence_star = '无此数据';
    // }else{
    //     influence_star = data.influence_star;
    // }
    group_tag_vector(data.tag_vector);

    var task_name_2;
    var submit_date;
    var state;
    var submit_user;

    if(data.submit_date == undefined){
        submit_date = '无此数据';
    }else{
        submit_date = data.submit_date;
    };
    if(data.submit_user == undefined){
        submit_user = '无此数据';
    }else{
        submit_user = data.submit_user;
    };
    if(data.state == undefined){
        state = '无此数据';
    }else{
        state = data.state;
    };
    if(data.domain== undefined){
        domain = '无此数据';
    }else{
        domain = data.domain;
    };
    if(data.topic == undefined){
        topic = '无此数据';
    }else{
        topic = data.topic;
    };
    $('#overview').empty();
    html = '';
    html += '<p style="font-size:13px;padding: 5px 5px 5px 5px;">群体名称：<a style="cursor:pointer;" onclick="group_table();">' + name +'</a></p><p style="font-size:13px;padding: 5px 5px 5px 5px;">创建时间：' + submit_date +'</p><p style="font-size:13px;padding: 5px 5px 5px 5px;">创建人员：' + submit_user +'</p><p style="font-size:13px;padding: 5px 5px 5px 5px;" id="group_states">群体备注：<span id="g_states">' + state +'</p>';
    html += '</a></li></ul></div>';
    $('#overview').append(html);
    $('#g_tag').empty();
    var html = '';
    html += '<table style="height:100px;width:100%;">';//border-bottom:1px solid #ccc;
    html += '<tr><td style="padding:5px;text-align:center;vertical-align:middle"><img src="/static/img/closeness.png" style="height:60px"></td>';
    html += '<td style="padding:5px;text-align:center;vertical-align:middle"><img src="/static/img/activeness.png" style="height:60px"></td>';
    html += '<td style="padding:5px;text-align:center;vertical-align:middle"><img src="/static/img/importance.png" style="height:60px"></td>';
    html += '<td style="padding:5px;text-align:center;vertical-align:middle"><img src="/static/img/influence.png" style="height:60px"></td></tr>';
    html += '<tr><td style="text-align:center;vertical-align:middle;padding: 0px;/* width: 100px; */">' + density_star + '</td><td style="text-align:center;vertical-align:middle;padding: 0px;/* width: 100px; */">' + activeness_star + '</td>';
    html += '<td style="text-align:center;vertical-align:middle;padding: 0px;/* width: 100px; */">' + importance_star + '</td><td style="text-align:center;vertical-align:middle;padding: 0px;/* width: 100px; */">' + influence_star + '</td></tr>';
    html += '<tr><td style="padding:0px;font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;紧密度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员相互转发行为的多少程度，通过聚类系数、微博转发频率及参与转发的成员比例计算得到"></i>&nbsp;&nbsp;</</td>';
    html += '<td style="padding:0px;font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;活跃度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员线上线下的活跃程度，通过发布微博综述、活跃地区数、发布微博的时间走势计算得到"></i>&nbsp;&nbsp;</b></td>';
    html += '<td style="padding:0px;font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;重要度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员对社会网络安全业务的重要程度，通过群体成员的所属领域和偏好话题计算得到"></i>&nbsp;&nbsp;</b></td>';
    html += '<td style="padding:0px;font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;影响力<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员整体的影响力，通过群体成员原创微博、转发微博的评论和转发的最高值、均值、总量计算得到"></i>&nbsp;&nbsp;</b></td></tr>';

    //html += '<tr style="padding:2px;"><td><span style="color:red;margin-left:20px;font-size:13px;">紧密度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员相互转发行为的多少程度，通过聚类系数、微博转发频率及参与转发的成员比例计算得到"></i></span><span>&nbsp;'+importance_star+'</span></td>';
    //html += '<td><span style="color:red;margin-left:20px;font-size:13px;">活跃度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员线上线下的活跃程度，通过发布微博综述、活跃地区数、发布微博的时间走势计算得到"></i></span><span>&nbsp;'+activeness_star+'</span></td>';
    //html += '<tr><td><span style="color:red;margin-left:20px;font-size:13px;">重要度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员对社会网络安全业务的重要程度，通过群体成员的所属领域和偏好话题计算得到"></i></span><span>&nbsp;'+density_star+'</span></td>';
    //html += '<td ><span style="color:red;margin-left:20px;font-size:13px;">影响力<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员整体的影响力，通过群体成员原创微博、转发微博的评论和转发的最高值、均值、总量计算得到"></i></span><span>&nbsp;'+influence_star+'</span></td></tr>';
    $('#g_tag').append(html);
},

Draw_personal_tag: function(data){
    for (key in data){
        personal_tag =  data[key];
        document.getElementById(key).title=personal_tag;
    }
},
Draw_group_weibo: function(data){
    page_num = 10;
    if (data.length < page_num) {
          page_num = data.length
          page_group_weibo( 0, page_num, data);
      }
      else {
          page_group_weibo( 0, page_num, data);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>5){
        page_icon(1,5,0);
    }else{
        page_icon(1,pageCount,0);
    }
    
    $("#pageGro li").live("click",function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      page = parseInt($("#pageGro li.on").html())  
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        page_group_weibo(start_row,end_row,data);
    });

    $("#pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());
            pageUp(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index > 0){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html())  
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data);
    });
    

    $("#pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());

            pageDown(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html()) 
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data);
    });
    }
}
 
var Search_weibo = new Search_weibo(); 

function page_group_weibo(start_row,end_row,data){
    weibo_num = end_row - start_row;
    $('#group_weibo').empty();
    var html = "";
    html += '<div class="group_weibo_font">';
    for (var i = start_row; i < end_row; i += 1){
        s=i.toString();
        uid = data[s]['uid'];
        text = data[s]['text'];
        uname = data[s]['uname'];
        timestamp = data[s]['timestamp'];
        date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="background:whitesmoke;font-size:13px">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>'
    }
        else{
            html += '<div>';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';    
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>';
        }
    }
    html += '</div>'; 
    $('#group_weibo').append(html);
}

function show_personal_tag(uid){
    var show_personal_tag_url = '/tag/show_user_tag/?uid_list=' + uid;
    Search_weibo.call_sync_ajax_request(show_personal_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_personal_tag);
}

function recommend_all(){
    $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function add_group_tag(){
    var cur_uids = []
    $('input[name="in_status"]:checked').each(function(){
        cur_uids.push($(this).attr('value'));
    });
    global_choose_uids[global_pre_page] = cur_uids;
    var select_uids = [];
    var select_uids_string = '';
    for (var key in global_choose_uids){
        var temp_list = global_choose_uids[key];
        for (var i = 0; i < temp_list.length; i++){
            select_uids.push(temp_list[i]);
        }
    }
    for (var i = 0; i < select_uids.length; i++) {
        s=i.toString();
        select_uids_string += select_uids[s] + ',';
    };
    //console.log(select_uids_string);
    add_tag_attribute_name = $("#select_attribute_name").val();
    add_tag_attribute_value = $("#select_attribute_value").val();
    add_group_tag_url = '/tag/add_group_tag/?uid_list=' + select_uids + "&attribute_name=" + add_tag_attribute_name + "&attribute_value=" + add_tag_attribute_value;
    //console.log(add_group_tag_url);
    if(select_uids.length!=0){
        Search_weibo.call_sync_ajax_request(add_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_add_group_tag);
    }else{
        alert('请至少选择一名用户！')
    }

}



$(document).ready(function(){
	var downloadurl = window.location.host;


    var group_overview_url = '/group/show_group_result/?module=overview&task_name=' + name;
     Search_weibo.call_sync_ajax_request(group_overview_url, Search_weibo.ajax_method, Search_weibo.Draw_overview);
    var tag_url =  'http://' + downloadurl + "/tag/show_attribute_name/";
    Search_weibo.call_sync_ajax_request(tag_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_name);
    var select_attribute_name =document.getElementById("select_attribute_name").value;
    var attribute_value_url = '';
    attribute_value_url = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
    Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);
g_bind_remark_edit(Search_weibo);
    $('#select_attribute_name').change(function(){
            var attribute_value_url = '/tag/show_attribute_value/?attribute_name=' ;
            attribute_value_url += $(this).val();
            Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);
        });    
})

function group_tag_vector(data){
    $('#group_tag_vector').empty();
    var html = '';
    html += '<table class="table table-striped">';
    html += '<tr>';
    for(var key in data){
        html += '<tr>';
        html += '<th style="font-weight:normal;">'+ data[key][0] + '</th>';
        if(data[key][0] == '主要消极情绪'){
            var value_emotion='';
            // console.log('情绪',data[key][0])
            switch(data[key][1])
            {
            case '2': value_emotion = "生气";break;
            case '3': value_emotion = "焦虑";break;
            case '4': value_emotion = "悲伤";break;
            case '5': value_emotion = "厌恶";break;
            case '6': value_emotion = "消极其他";break;
            } 
            html += '<th>'+ value_emotion + '</th>';
        }else{
            html += '<th>'+ data[key][1] + '</th>';
        }
        html += '</tr>'
    }
    html += '</table>'
    $('#group_tag_vector').html(html);
}

function g_bind_remark_edit(Search_weibo){
    $('#g_states').click(function(){
        console.log('ddd');
        var td = $(this);
        var txt = td.html();
        var input = "<input id='g_editremark' style='width:100px;' type='text' value='" + txt + "'/>";
        td.html(input);
        $('#g_editremark').click(function(){
            return false;
        });
        $('#g_editremark').trigger('focus');
        $('#g_editremark').bind('keyup', function(e){
            var ev = document.all?window.event:e;
            if (ev.keyCode == 13){
                var newtxt = $(this).val();
                if (newtxt == ''){
                    td.html('暂无');
                }
                else{    
                    td.html(newtxt);
                }
                if (newtxt != txt){
                    var url = '/group/edit_states/?task_name=' + name + '&submit_user='+$('#g_useremail').text()+'&new_state=' + newtxt;
                    Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, confirm_edit);
                    //console.log('diff');
                }
            }
        }).bind('keydown', function(e){
            var ev = document.all?window.event:e;
            if (ev.keyCode == 13){
                return false;
            }
        });
        $('#g_editremark').blur(function(){
            var newtxt = $(this).val();
            if (newtxt == ''){
                td.html('暂无');
            }
            else{    
                td.html(newtxt);
            }
            if (newtxt != txt){
                var url = '/group/edit_states/?task_name=' + name + '&submit_user='+$('#g_useremail').text()+'&new_state=' + newtxt;
                Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, confirm_edit);
                console.log('dif');
            }
        });
        function confirm_edit(data){
            //alert(data);
        }
    });
}
// g_bind_remark_edit(Search_weibo);

function group_table(){
    var model_url =   "/group/show_group_list/?task_name=" + name;
    Search_weibo.call_sync_ajax_request(model_url,Search_weibo.ajax_method, Draw_model);
    $("#g_myModal_group").modal();
    function Draw_model(data){
        $("#g_group_member_user").empty();
        html = '';
        html += '<table id="g_modal_table" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
        html += '<thead><tr><th class="center" style="text-align:center">用户ID</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center;width：auto;">性别</th>';
        html += '<th class="center" style="text-align:center">注册地</th><th class="center" style="text-align:center">重要度</th><th class="center" style="text-align:center;width:72px">影响力</th>';
        html += '<th class="center" style="text-align:center"><input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()"></th>';
        //html += '<th class="center" style="text-align:center">添加标签</th>';
        html += '</tr></thead>';
        html += '<tbody>';
        for ( i=0 ; i<data.length; i++){
            s = i.toString();
            if (data[s]['2'] == 1){
                sex = '男';
            }else{
                sex = '女';
            }
        if(data[s]['1']=='unknown'){
            data[s]['1'] = '未知';
        }
        if(data[s]['3']=='unknown'){
            data[s]['3'] = '未知';
        }
          html += '<th class="center" style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data[s]['0']+ '">' + data[s]['0']+ '</a></th><th class="center" style="text-align:center">' + data[s]['1']+ '<img data-toggle="tooltip" data-placement="right" title="" id=' + data[s]['0'] + ' src="/static/img/tag.png" class="tag" onmouseover="show_personal_tag(' + data[s]['0'] + ')"; style="height:20px"></th><th class="center" style="text-align:center">' + sex+ '</th>';
          html += '<th class="center" style="text-align:center">' + data[s]['3']+ '</th><th class="center" style="text-align:center">' + data[s]['4'].toFixed(2) + '</th><th class="center" style="text-align:center;width:72px">' + data[s]['5'].toFixed(2) + '</th>';  
          html += '<th class="center" style="text-align:center"><input name="in_status" class="in_status" type="checkbox" value="' + data[s]['0'] + '"/></th>';
          //html += '<th><span id="attribute_name" style="min-width:75px;margin-left:10px" ></span><span id="attribute_value" style="min-width:75px;margin-left:10px"></span><button class="btn btn-primary btn-sm" style="width:80px;height:30px" id="add_group_tag_button" title="确定选择" onclick="add_group_tag()">添加</button></th>';
          html += '</tr>';
        };
        html += '</tbody>';
        html += '</table>';
        $("#g_group_member_user").append(html);
        $('#g_modal_table').dataTable({
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
            "sPaginationType": "bootstrap",
            "aaSorting": [[ 4, "desc" ]],
            "aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}],
            "oLanguage": {
                "sLengthMenu": "_MENU_ 每页"
            }
        });

    }

  

}
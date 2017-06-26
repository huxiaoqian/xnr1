//draw function
function Search_weibo(){
  this.ajax_method = 'GET';
  that = this ;
}

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

    
    Return_data: function(data){
        return data;
    },

    Draw_user_tag: function(data){
      //console.log(data);
      $('#user_lable').empty();
      user_lable_html = '';
      user_lable_html += '<table id="" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
      user_lable_html += '<thead><tr><th class="center" style="text-align:center">用户ID</th>';
      user_lable_html += '<th class="center" style="text-align:center">用户昵称</th>';
      user_lable_html += '<th class="center" style="text-align:center">用户标签</th>';
      user_lable_html += '<th class="center" style="text-align:center">全选<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()"></th>';
      user_lable_html += '</tr></thead>';
      user_lable_html += '<tbody>';
      for (var i=1;i < Search_weibo.data.length - 1; i++){
           var key = Search_weibo.data[i][0];
           var uname = Search_weibo.data[i][1];
           user_lable_html += '<tr>';
           user_lable_html += '<th class="center" style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + key + '">' + key +'</a></th>'; 
           user_lable_html += '<th class="center" style="text-align:center">' + uname +'</th>'; 
           user_lable_html += '<th class="center" style="text-align:center">' + data[key] + '</th>';
           user_lable_html += '<th class="center" style="text-align:center"><input name="in_status" class="in_status" type="checkbox" value="' + key + '"/></th>';
           user_lable_html += '</tr>';
      }    
      user_lable_html += '</tbody>';
      user_lable_html += '</table>';     
      $('#user_lable').append(user_lable_html);
    },

    Draw_add_group_tag: function(data){
      var downloadurl = window.location.host;
      show_group_tag_url = 'http://' + downloadurl + '/tag/show_user_tag/?uid_list=' + id_string;
      Search_weibo.call_sync_ajax_request(show_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_user_tag);
    },

    Draw_table: function(data){
        //console.log(data);
        that.data = data;
        if(data.length == 2){
            alert("没有相关人物推荐");
            return false;
        }
        $('#table').empty();
        var html = '';
        var height = 39 * (data.length-1);
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive" style="table-layout:fixed">';
        html += '<thead><tr><th class="center" style="text-align:center">用户ID</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center; ">活跃度</th><th class="center" style="text-align:center;">重要度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">相关度</th><th style="width:40px"><input name="choose_all" id="choose_all" type="checkbox" value="" onclick="choose_all()" /></th></tr></thead>';
        html += '<tbody>';
        for(var item = 1; item < data.length-1; item++){
            html += '<tr style="border-bottom:1px solid #ddd">';
            var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
            for(var i =0; i < data[item].length; i++){  
                if(data[item][i] == 'unknown'){
                    data[item][i] = '未知'
                }
                if (data[item][1] == '未知'){
                    data[item][1] = data[item][0];
                }
                if(i >= 2) {
                    html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data[item][i].toFixed(2) +'</td>';
                }
                else{
			if(i == 0){
			   var user_url = personal_url + data[item][0];
			   save_id.push(data[item][0]);
			    html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+user_url +' target="_blank">'+ data[item][i] +'</a></td>';
			}else{
			   html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data[item][i] +'</td>'; 
			}
                }            
            }
            html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item + '" /></td>';
            html += '</tr>';
        }
        html += '</tbody>';
        html += '</table>';
        document.getElementById('relatednum').innerHTML = data.length-1;
        $('#table').css('height',height);
        $('#table').append(html);
        for (var i = 0; i < save_id.length; i++) {
            s=i.toString();
            id_string += save_id[s] + ',';
        };
        id_string=id_string.substring(0,id_string.length-1)
    },

  Draw_attribute_name: function(data){
    $('#attribute_name').empty();
    html = '';
    html += '<select id="select_attribute_name">';
    if (data.length > 0){
	    for (var i = 0; i < data.length-1; i++) {
	      var s = i.toString();
	      html += '<option value="' + data[s] + '">' + data[s] + '</option>';
	    }
	    var t = (data.length-1).toString();
	    html += '<option value="' + data[t] + '" selected="selected">' + data[t] + '</option>';
    }
    html += '</select>';
    $('#attribute_name').append(html);
  },

  Draw_attribute_value: function(data){
    console.log(data);
    $('#attribute_value').empty();
    html = '';
    html += '';
    html += '<select id="select_attribute_value">';
    if (data != 'no attribute'){
	    for (var i = 0; i < data.length-1; i++) {
	      var s = i.toString();
	      html += '<option value="' + data[s] + '">' + data[s] + '</option>';
	    }
	    var t = (data.length-1).toString();
	    html += '<option value="' + data[t] + '" selected="selected">' + data[t] + '</option>';
    }
    html += '</select>';
    $('#attribute_value').append(html);
  },

    Draw_picture: function(data){
        /*
        if(data.length == 2){
            //alert("");
            return false;
        }
        */
        var Related_Node = new Array();
        var Related_Link = new Array();
        if (data[0][1] == 'unknown'){
            data[0][1] = data[0][0];
        }
        Related_Node.push({'name':data[0][0],'value':data[0][4],'label':data[0][1],'category':0,'symbolSize':2*Math.sqrt(data[0][4]),'itemStyle':{'normal':{'color':'rgba(255,215,0,0.4)'}}});
        var user_name = data[0][0];
         var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
        for(var item =1; item < data.length-1; item++){
            if(data[item][1]=='unknown'){
                data[item][1] = data[item][0];
                Related_Node.push({'name':data[item][0], 'value':data[item][4], 'label':data[item][1],'category':1,'symbolSize':2*Math.sqrt(data[item][4])});
                Related_Link.push({'source':user_name, 'target':data[item][0], 'weight':data[item][4],'itemStyle':{'normal':{'width':Math.sqrt(data[item][4])}}});
            }
            else{
                Related_Node.push({'name':data[item][0], 'value':data[item][4], 'label':data[item][1],'category':1,'symbolSize':2*Math.sqrt(data[item][4])});
                Related_Link.push({'source':user_name, 'target':data[item][0], 'weight':data[item][4],'itemStyle':{'normal':{'width':Math.sqrt(data[item][4])}}});
            }
        }
        var option = {
                title : {
                    text: '',
                    subtext: '',
                    x:'right',
                    y:'bottom'
                },
                color:['#B0E0E6','#FFC0CB'],
                tooltip : {
                    trigger: 'item',
                    formatter: '{a} : {b}'
                },
                toolbox: {
                    show : true,
                    feature : {
                        restore : {show: true},
                        magicType: {show: true, type: ['force', 'chord']},
                        saveAsImage : {show: true}
                    }
                },
                series : [
                    {
                        type:'force',
                        name : "用户ID",
                        ribbonType: false,
                        categories:[
                            {
                                name:'',
                                symbol:'circle',
                            },
                            {
                                name:'',
                                symbol:'circle',
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
                        linkSymbol:'arrow',
                        gravity: 1.1,
                        scaling: 1.1,
                        roam: 'move',
                        nodes: Related_Node,
                        links : Related_Link,
                    }
                ]
        };  

        var myChart = echarts.init(document.getElementById('echart'));
        myChart.setOption(option);
        //回调函数，添加监听事件
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
                        var node_url = personal_url + data.name;
                        window.open(node_url);
                    }
                }
                    myChart.on(ecConfig.EVENT.CLICK, focus)

                    myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                    });
                }
        )     
    }
}
var save_id = [];
var id_string = '';
var test_uids = [];
var test_uids_string = '';
var Search_weibo = new Search_weibo();
//get tag
var user_tag = '/tag/show_user_attribute_name/?uid='+ uid;
Search_weibo.call_sync_ajax_request(user_tag, Search_weibo.ajax_method, Show_tag);

Search_weibo.call_sync_ajax_request(get_choose_data(uid), Search_weibo.ajax_method, Search_weibo.Draw_table);
Search_weibo.Draw_picture(Search_weibo.data);
var show_user_tag_url = '/tag/show_user_tag/?uid_list=' + id_string;
Search_weibo.call_sync_ajax_request(show_user_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_user_tag);
var tag_url = "/tag/show_attribute_name/";
Search_weibo.call_sync_ajax_request(tag_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_name);
var select_attribute_name = $("#select_attribute_name").val()
var attribute_value_url = '';
attribute_value_url = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);

var global_data = Search_weibo.data;

function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function Show_tag(data){
    var height = $('#box-height').height();
    var unit = Math.ceil(data.length / 4);
    $('#box-height').css('height',height+20*unit);

    /*
    if(data.length <=4 && data.length > 0 ){
        $('#box-height').css('height',height+20);
    }
    else if(data.length >4 && data.length <=8){
        $('#box-height').css('height',height+20*2);
    }
    else{
        $('#box-height').css('height',height+20*3);
    }
    */
    var html = '';
    if(data.length == 0){
      return false;
    }
    else{
      for(var i = 0; i < data.length; i++){
        if (data[i] != ''){
		html += '<div class="col-lg-3" >';
		html += '<span class="input-group-addon" style="width:96px;border:1px solid white; background-color:white;display:inline-block" id="'+ data[i] +'">'+ data[i] +'</span>';
		html += '<input type="text" class="form-control" style="width:40%; display:inline;height:25px;margin-left:4px" value="0">';
		html += '</div>';
        }
      }
      $('#tag').append(html);
    }
}

function add_group_tag(){
    var select_uids = [];
    $('input[name="in_status"]:checked').each(function(){
        select_uids.push($(this).attr('value'));
    })
    //console.log(select_uids);
    var select_uids_string = select_uids.join(',');

    add_tag_attribute_name = $("#select_attribute_name").val();
    add_tag_attribute_value = $("#select_attribute_value").val();
    console.log(add_tag_attribute_value);
    if (!add_tag_attribute_value){
        alert('不能添加空白标签！');
        return;
    }
    add_group_tag_url = '/tag/add_group_tag/?uid_list=' + select_uids_string + "&attribute_name=" + add_tag_attribute_name + "&attribute_value=" + add_tag_attribute_value;
    Search_weibo.call_sync_ajax_request(add_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_add_group_tag);
}

$('.label-success').click(function(){
    var url = get_choose_data(uid);
    //console.log(url);
    if(url == ''){
        return false;
    }
    else{
    Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, Search_weibo.Draw_table);
    Search_weibo.Draw_picture(Search_weibo.data);
    //Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, Search_weibo.Draw_picture);
    }
});

$('.inline-checkbox').click(function(){
    console.log('dddd');
    if($(this).is(':checked')){
        $(this).next().next().val('1');
        $(this).next().next().attr('disabled',false);
    }
    else{
        $(this).next().next().val('');
        $(this).next().next().attr('disabled',true);
    }
});

//获取选择的条件，把参数传出获取返回值
function get_choose_data(uid){
    var url = '/manage/imagine/?uid=' + uid + '&keywords=';
    var keywords = new Array();
    var weight = new Array();
    //var field ;
    var isflag = 1;
    $('.input-group-addon').each(function(){
        if ($(this).attr('id') != ''){ 
		keywords.push($(this).attr('id'));
		var value = $(this).next().val();
		if((parseInt(value) != value) || (value > 10) || (value < 0 )){
		    alert("请输入0-10的整数");
		    isflag = 0;
		    return false;
		}else{
		    weight.push(value);
		}
        }
    });
    /*
    $('[type="radio"]').each(function(){
        if($(this).is(':checked')){
            field = $(this).attr('id');
        }
    });
    */
    if(isflag == 1){
        url = url + keywords.join(',') + '&weight=' + weight.join(',');
    }
    else{
        url = '';
    }
    console.log(url);
    return url;
}

// 保留原有的html代码
var origin_html = $('#ADD').html();

function diy_button(){
 // $('#ADD').html(origin_html);
  // var cur_uids = []
  // $('input[name="search_result_option"]:checked').each(function(){
  //     cur_uids.push($(this).attr('value'));
  // });
  // if(cur_uids.length < 1){
  //   alert('请选择至少1个用户');
  // }
  // else{
      $('#Diymodal').modal();
  // }
  $(".addIcon").off("click").click(function(){
    var html = '';
    html += '<div class="tagCols"><span >标签名</span><input name="tagname" class="inputbox " type="text" value="" style="margin-left:35px;line-height:36px;"></div>';
    $('#ADD').append(html);
  });

}


function compare_button(){
  var compare_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      compare_uids.push($(this).attr('value'));
  });
  //console.log(compare_uids);
  var len = compare_uids.length;
  if(len>3 || len<2){
    alert("请选择2至3个用户！");
  }
  else{
      draw_table_compare_confirm(compare_uids, "#compare_comfirm");
      $('#compare').modal();
  }
}

function group_button(){
  var group_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      group_uids.push($(this).attr('value'));
  });
  var group_uids = [];
  //console.log(group_uids);
  var len = group_uids.length;
  if (len < 1){
      alert("请选择至少1个用户!");
  }
  else{
      draw_table_group_confirm(group_uids, "#group_comfirm");
      $("#group").modal();
  }
}

function delete_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var delete_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        delete_uids.push(temp_list[i]);
      }
  }
  console.log(delete_uids);
  var len = delete_uids.length;
  if (len < 1){
      alert("请选择至少1个用户!");
  }
  else{
      draw_table_delete_confirm(delete_uids, "#delete_comfirm");
      $('#delete').modal();
  }
}

function choose_all(){
  $('input[name="search_result_option"]').prop('checked', $("#choose_all").prop('checked'));
}

function draw_table_compare_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="compare_cofirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">活跃度</th><th class="center" style="text-align:center;width:72px">重要度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="compare_confirm_uids">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ item[2].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[3].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] + '</td>';
      html += '<td class="center" style="width:80px;"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function draw_table_group_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="group_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">活跃度</th><th class="center" style="text-align:center;width:72px">重要度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="group_confirm_uids">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ item[2].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[3].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] + '</td>';
      html += '<td class="center" style="width:80px;"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function draw_table_delete_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="delete_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th>d>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr id=' + uids[1] +'>';
      html += '<td class="center" name="delete_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ item[2] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[3] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[4] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[6] + '</td>';
      html += '<td class="center" style="width:80px;"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function delRow(obj){
  var Row = obj.parentNode;
  while(Row.tagName.toLowerCase()!="tr"){
    Row = Row.parentNode;
  }
  Row.parentNode.removeChild(Row);
}

function compare_confirm_button(){
  var compare_confirm_uids = [];
  $('[name="compare_confirm_uids"]').each(function(){
      compare_confirm_uids.push($(this).text());
  })
  if (compare_confirm_uids.length <= 1){
      alert('对比的用户至少需要2名!');
      return;
  }
  var compare_url = '/index/contrast/?uid_list='+ compare_confirm_uids.join(',');
  console.log(compare_url);
  window.open(compare_url);
}

function group_confirm_button(){
  var group_confirm_uids = [];
  $('[name="group_confirm_uids"]').each(function(){
      group_confirm_uids.push($(this).text());
  })
  console.log(group_confirm_uids);
  var group_ajax_url = '/group/submit_task/';
  var group_url = '/index/group/';
  var group_name = $('input[name="group_name"]').val();
  var remark = $('input[name="remark"]').val();
  console.log(group_name, remark);
  if (group_name.length == 0){
      alert('群体名称不能为空');
      return;
  }
  //console.log(group_url);
  var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
  if (!group_name.match(reg)){
    alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if ((remark.length > 0) && (!remark.match(reg))){
    alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if(group_confirm_uids.length <=1){
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
      //console.log(data);
      if (data == '1'){
          //console.log('seceed',group_ajax_url)
          window.location.href = group_url;
      }
      else{
          alert('已存在相同名称的群体分析任务,请重试一次!');
      }
  }
}

function delete_confirm_button(){
  var now_date = new Date();
  var now = now_date.getFullYear()+"-"+((now_date.getMonth()+1)<10?"0":"")+(now_date.getMonth()+1)+"-"+((now_date.getDate())<10?"0":"")+(now_date.getDate());
  var delete_confirm_uids = [];
  $('[name="delete_confirm_uids"]').each(function(){
      delete_confirm_uids.push($(this).text());
  })
  console.log(delete_confirm_uids);
  var delete_uid_list = '';
  for(var i in delete_confirm_uids){
      delete_uid_list += delete_confirm_uids[i];
      if(i<(delete_confirm_uids.length-1))
        delete_uid_list += ',';
  }
  if(confirm("确认要删除吗?")){
      var delete_url = '/recommentation/search_delete/?date=' + now + '&uid_list=' + delete_uid_list;
      console.log(delete_url);
      $.ajax({
          type:'get',
          url: delete_url,
          dataType: "json",
          success: callback
      });
      function callback(data){
           console.log(data);
           if (data == '1'){
               for (var i = 0; i < delete_confirm_uids.length; i++){
                   global_data[delete_confirm_uids[i]] = '';
               }
               alert('出库成功！');
               draw_table_search_result.Re_Draw_table(global_data);
           }
           else{
               alert('fail');
           }
      }
  }
}

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}

function Search_weibo_result(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_result.prototype = {
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
    //console.log(data);
    var div = that.div
    //console.log(div);
    $(div).empty();
    var user_url ;
    //console.log(user_url);
    html = '';
    html += '<table id="result_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th>' + '<input name="choose_all" id="choose_all" type="checkbox" value="" onclick="choose_all()" />' + '</th></tr></thead>';
    html += '<tbody>';
    for(var key in data){
      var item = data[key];
      if (item != ''){ // remain in global_data
          user_url = '/index/personal/?uid=' + item[0];
          html += '<tr id=' + item[0] +'>';
          html += '<td class="center" name="uids"><a href='+ user_url+ '>'+ item[0] +'</td>';
          html += '<td class="center">'+ item[1] +'</td>';
          html += '<td class="center">'+ item[2] +'</td>';
          html += '<td class="center" style="width:100px;">'+ item[3] +'</td>';
          html += '<td class="center" style="width:100px;">'+ item[4] +'</td>';
          html += '<td class="center" style="width:100px;">'+ item[5] +'</td>';
          html += '<td class="center" style="width:100px;">'+ item[6] +'</td>';
          html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item[0] + '" /></td>';
          html += '</tr>';
      }
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    //datatable
    $('#result_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

var global_pre_page = 1;
var global_choose_uids = new Array();
var global_data = new Array();

//console.log(url_search_result);
var draw_table_search_result = new Search_weibo_result(url_search_result, '#search_result');
draw_table_search_result.call_sync_ajax_request(url_search_result, draw_table_search_result.ajax_method, draw_table_search_result.Draw_table);


function get_custom_value(data){
    //console.log(data);
    if (data == 'no attribute'){
        data = [];
    }
    $('[name=attribute_value]').empty();
    var html = '';
    for (var i=0;i<data.length;i++){
        html += '<option value="' + data[i] + '">' + data[i] + '</option>';
    }
    $('[name=attribute_value]').html(html);
}

function get_custom_name(){
    var attribute_name_url = '/tag/show_attribute_name/';
    base_call_ajax_request(attribute_name_url, draw_name_option);
    
    function draw_name_option(data){
        // console.log(data);
        $('[name=attribute_name]').empty();
        var html = '';
        for (var i=0;i<data.length;i++){
            html += '<option value="' + data[i] + '">' + data[i] + '</option>';
        }
        $('[name=attribute_name]').html(html);

        var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
        attribute_value_url += data[0];
        base_call_ajax_request(attribute_value_url, get_custom_value);

        $('[name=attribute_name]').change(function(){
            // console.log($(this).val());
            var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
            attribute_value_url += $(this).val();
            base_call_ajax_request(attribute_value_url, get_custom_value);
        });
    }

}

function custom_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var custom_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        custom_uids.push(temp_list[i]);
      }
  }
  //console.log(custom_uids);
  var len = custom_uids.length;
  if(len<1){
    alert("请至少选择1个用户！");
  }
  else{
      draw_table_custom_confirm(custom_uids, "#custom_confirm");
      get_custom_name();
      $('#custom').modal();
  }
}
function compare_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var compare_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        compare_uids.push(temp_list[i]);
      }
  }
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
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var group_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        group_uids.push(temp_list[i]);
      }
  }
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
  //console.log(delete_uids);
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

function draw_table_custom_confirm(uids, div){
    $(div).empty();
    var html = '';
    html += '<table id="custom_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="custom_confirm_uids">'+ uids[i] +'</td>';
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
function draw_table_compare_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="compare_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="compare_confirm_uids">'+ uids[i] +'</td>';
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

function draw_table_group_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="group_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr>';
      html += '<td class="center" name="group_confirm_uids">'+ uids[i] +'</td>';
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

function draw_table_delete_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="delete_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th></th></tr></thead>';
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

function custom_confirm_button(){
  var custom_confirm_uids = [];
  $('[name="custom_confirm_uids"]').each(function(){
      custom_confirm_uids.push($(this).text());
  })
  if (custom_confirm_uids.length < 1){
      alert('至少需要选择1名用户!');
      return;
  }
  var attribute_name = $('[name=attribute_name]').val();
  var attribute_value = $('[name=attribute_value]').val();
  var custom_url = '/tag/add_group_tag/?uid_list='+ custom_confirm_uids.join(',');
  custom_url += '&attribute_name=' + attribute_name + '&attribute_value=' + attribute_value;
  //console.log(custom_url);
  base_call_ajax_request(custom_url, callback);
  function callback(data){
       //console.log(data);
  }
}
function compare_confirm_button(){
  var compare_confirm_uids = [];
  $('[name="compare_confirm_uids"]').each(function(){
      compare_confirm_uids.push($(this).text());
  })
  if (compare_confirm_uids.length < 2){
      alert('对比的用户至少需要2名!');
      return;
  }
  var compare_url = '/index/contrast/?uid_list='+ compare_confirm_uids.join(',');
  //console.log(compare_url);
  window.open(compare_url);
}

function group_confirm_button(){
  var group_confirm_uids = [];
  $('[name="group_confirm_uids"]').each(function(){
      group_confirm_uids.push($(this).text());
  })
  if (group_confirm_uids.length < 1){
      alert('至少需要选择1名用户!');
      return;
  }
  //console.log(group_confirm_uids);/group/submit_task/
  var group_ajax_url = '/group/submit_task/'; ///detect/add_detect2analysis/';
  var group_url = '/index/group/#';
 // var group_url = '/index/group_result/';
  var group_name = $('input[name="group_name"]').val();
  var remark = $('input[name="remark"]').val();
  //console.log(group_name, remark);
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
  var job = {"task_name":group_name, "uid_list":group_confirm_uids,"state":remark};//"state":remark
  $.ajax({
      type:'POST',
      url: group_ajax_url,
      contentType:"application/json",
      data: JSON.stringify(job),
      dataType: "json",
      success: callback
  });
  function callback(data){
      console.log(data);
      if (data == '1'){
          window.location.href = group_url;
      }
      else{
          alert('已存在相同名称的群体分析任务,请重试一次!');
      }
  }
}


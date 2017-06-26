function Search_weibo_total(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_total.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    var select_index = $('input[name="index_select"]:checked').val();
    $(div).empty();
    html = '';
    html += '<table id="total_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    if(select_index==1)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">影响力</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==2)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">转发量</th><th style="text-align:center;vertical-align:middle">微博链接</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==3)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">评论量</th><th style="text-align:center;vertical-align:middle">微博链接</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==4)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">转发爆发度</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==5)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">评论爆发度</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知' && select_index!=2 && select_index!=3)
        item[i][4] = item[i][4].toFixed(2);
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="http://weibo.com/u/'+ item[i][2] +'" target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][3] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][4] +'</td>';
      if(select_index==2 || select_index==3){
        html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="'+ item[i][5] +'" target="_blank">查看微博</a></td>';
        if(item[i][6]==0)
          html += '<td class="center" style="text-align:center;vertical-align:middle">未入库</td>';
        else if(item[i][6]==1)
          html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][2] +'" target="_blank">已入库</a></td>';
      }
      else{
        if(item[i][5]==0)
          html += '<td class="center" style="text-align:center;vertical-align:middle">未入库</td>';
        else if(item[i][5]==1)
          html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][2] +'" target="_blank">已入库</a></td>';
      }
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#total_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function Search_weibo_domain(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_domain.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    html = '';
    html += '<table id="domain_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">影响力</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][2] +'" target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][3] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][4] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#domain_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function Search_weibo_change(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_change.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    html = '';
    html += '<table id="change_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">变动名次</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      var pic = '';
      if(item[i][4]>0)
        pic = '/static/img/up.png';
      else if(item[i][4]<0)
        pic = '/static/img/down.png';
      else
        pic = '';
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="http://weibo.com/u/'+ item[i][2] +'" target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][3] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][4] +'<img src="'+ pic +'" style="width:20px;height:25px"></td>';
      if(item[i][5]==0)
        html += '<td class="center" style="text-align:center;vertical-align:middle">未入库</td>';
      else if(item[i][5]==1)
        html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][2] +'" target="_blank">已入库</a></td>';
      else
        html += '<td class="center" style="text-align:center;vertical-align:middle">error!</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#change_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function Search_weibo_detail_trans(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

/*
Search_weibo_detail_trans.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="detail_trans_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">微博ID</th><th style="text-align:center;vertical-align:middle">转发量</th></tr></thead>';
    var item = data[0];
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      user_url = '/index/personal/?uid=';
      user_url = user_url + item[i][2];
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+ user_url + ' target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][3] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+ item[i][7] + ' target="_blank">'+ item[i][4] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][5] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#detail_trans_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function Search_weibo_detail_comment(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_detail_comment.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="detail_comment_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">微博ID</th><th style="text-align:center;vertical-align:middle">评论量</th></tr></thead>';
    var item = data[1];
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      user_url = '/index/personal/?uid=';
      user_url = user_url + item[i][2];
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+ user_url + ' target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][3] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+ item[i][7] + ' target="_blank">'+ item[i][4] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][5] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#detail_comment_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}
*/

$("#range").empty();
var range_html = '';
range_html += '<input type="radio" name="range_select" checked value="0" /> 全网';
range_html += '<input type="radio" name="range_select" value="1" style="margin-left:5px" /> 人物库';
$("#range").append(range_html);

$("#change").empty();
var change_html = '';
change_html += '<input type="radio" name="change_select" checked value="0" /> 全网';
change_html += '<input type="radio" name="change_select" value="1" style="margin-left:5px" /> 人物库';
$("#change").append(change_html);

$("#index").empty();
var index_html = '';
index_html += '<input type="radio" name="index_select" checked value="1" /> 影响力';
index_html += '<input type="radio" name="index_select" value="2" style="margin-left:5px" /> 转发量';
index_html += '<input type="radio" name="index_select" value="3" style="margin-left:5px" /> 评论量';
index_html += '<input type="radio" name="index_select" value="4" style="margin-left:5px" /> 转发爆发度';
index_html += '<input type="radio" name="index_select" value="5" style="margin-left:5px" /> 评论爆发度';
$("#index").append(index_html);

/*
$("#detail").empty();
var detail_html = '';
detail_html += '<input type="radio" name="detail_select" checked value="0" /> 转发量';
detail_html += '<input type="radio" name="detail_select" value="1" style="margin-left:5px" /> 评论量';
$("#detail").append(detail_html);
*/

$("#domain").empty();
var domain_html = '';
domain_html += '<select id="domain_select">';
domain_html += '<option value="1" selected="selected">高校微博</option>';
domain_html += '<option value="2">境内机构</option>';
domain_html += '<option value="3">境外机构</option>';
domain_html += '<option value="4">媒体</option>';
domain_html += '<option value="5">境外媒体</option>';
domain_html += '<option value="6">民间组织</option>';
domain_html += '<option value="7">律师</option>';
domain_html += '<option value="8">政府机构人士</option>';
domain_html += '<option value="9">媒体人士</option>';
domain_html += '<option value="10">活跃人士</option>';
domain_html += '<option value="11">草根</option>';
domain_html += '<option value="12">商业人士</option>';
domain_html += '<option value="13">其他</option>';
domain_html += '</select>';
$("#domain").append(domain_html);

$('input[name="range_select"]').click(function(){
  var select_range = $('input[name="range_select"]:checked').val();
  var select_index = $('input[name="index_select"]:checked').val();
  var select_total_date = $("#total_date_select").val()
  var url_total_new = '';
  url_total_new = '/influence_application/search_influence/?date=' + select_total_date + '&index=' + select_index + '&domain=' + select_range;
  draw_table_total_new = new Search_weibo_total(url_total_new, '#total_rank');
  draw_table_total_new.call_sync_ajax_request(url_total_new, draw_table_total_new.ajax_method, draw_table_total_new.Draw_table);
});

$('input[name="index_select"]').click(function(){
  var select_range = $('input[name="range_select"]:checked').val();
  var select_index = $('input[name="index_select"]:checked').val();
  var select_total_date = $("#total_date_select").val()
  var url_total_new = '';
  url_total_new = '/influence_application/search_influence/?date=' + select_total_date + '&index=' + select_index + '&domain=' + select_range;
  draw_table_total_new = new Search_weibo_total(url_total_new, '#total_rank');
  draw_table_total_new.call_sync_ajax_request(url_total_new, draw_table_total_new.ajax_method, draw_table_total_new.Draw_table);
});

$('input[name="change_select"]').click(function(){
  var select_change = $('input[name="change_select"]:checked').val();
  var url_change_new = '';
  if(select_change==0)
    url_change_new = '/influence_application/vary_top_k/';
  else
    url_change_new = '/influence_application/portrait_user_in_vary/';
  //console.log(url_change_new);
  draw_table_change_new = new Search_weibo_change(url_change_new, '#change_rank');
  draw_table_change_new.call_sync_ajax_request(url_change_new, draw_table_change_new.ajax_method, draw_table_change_new.Draw_table);
});

/*
$('input[name="detail_select"]').click(function(){
  var url_detail_new = '/influence_application/hot_origin_weibo/?date=' + $("#detail_date_select").val() + '&number=10';
  var detail_status = $('input[name="detail_select"]:checked').val();
  if(detail_status==0){
    draw_table_detail_trans_new = new Search_weibo_detail_trans(url_detail_new, '#detail_rank');
    draw_table_detail_trans_new.call_sync_ajax_request(url_detail_new, draw_table_detail_trans_new.ajax_method, draw_table_detail_trans_new.Draw_table);
  }
  else{
    draw_table_detail_comment_new = new Search_weibo_detail_comment(url_detail_new, '#detail_rank');
    draw_table_detail_comment_new.call_sync_ajax_request(url_detail_new, draw_table_detail_comment_new.ajax_method, draw_table_detail_comment_new.Draw_table);
  }
});
*/

/*
$('#domain_button').click(function(){
  var url_domain_new = '/influence_application/domain_rank/?date=' + $("#domain_date_select").val() + '&domain=' + $("#domain_select").val();
  draw_table_domain_new = new Search_weibo_domain(url_domain_new, '#domain_rank');
  draw_table_domain_new.call_sync_ajax_request(url_domain_new, draw_table_domain_new.ajax_method, draw_table_domain_new.Draw_table);
});
*/

var tomorrow = new Date(2013,8,8);
var now_date = new Date(tomorrow-24*60*60*1000);
var now = now_date.getFullYear()+"-"+((now_date.getMonth()+1)<10?"0":"")+(now_date.getMonth()+1)+"-"+((now_date.getDate())<10?"0":"")+(now_date.getDate());

var url_total = '/influence_application/search_influence/?date=' + now;
draw_table_total = new Search_weibo_total(url_total, '#total_rank');
draw_table_total.call_sync_ajax_request(url_total, draw_table_total.ajax_method, draw_table_total.Draw_table);

/*
var url_domain = '/influence_application/domain_rank/?date=' + now;
draw_table_domain = new Search_weibo_domain(url_domain, '#domain_rank');
draw_table_domain.call_sync_ajax_request(url_domain, draw_table_domain.ajax_method, draw_table_domain.Draw_table);
*/

var url_change = '/influence_application/vary_top_k/';
draw_table_change = new Search_weibo_change(url_change, '#change_rank');
draw_table_change.call_sync_ajax_request(url_change, draw_table_change.ajax_method, draw_table_change.Draw_table);

/*
var url_detail = '/influence_application/hot_origin_weibo/?date=' + now + '&number=10';
draw_table_detail_trans = new Search_weibo_detail_trans(url_detail, '#detail_rank');
draw_table_detail_trans.call_sync_ajax_request(url_detail, draw_table_detail_trans.ajax_method, draw_table_detail_trans.Draw_table);
*/

function date_initial(){
  var total_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(tomorrow-24*60*60*1000*(7-i));
    total_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
  }
  $("#total_date").empty();
  var total_date_html = '';
  total_date_html += '<select id="total_date_select">';
  total_date_html += '<option value="' + total_date[0] + '">' + total_date[0] + '</option>';
  total_date_html += '<option value="' + total_date[1] + '">' + total_date[1] + '</option>';
  total_date_html += '<option value="' + total_date[2] + '">' + total_date[2] + '</option>';
  total_date_html += '<option value="' + total_date[3] + '">' + total_date[3] + '</option>';
  total_date_html += '<option value="' + total_date[4] + '">' + total_date[4] + '</option>';
  total_date_html += '<option value="' + total_date[5] + '">' + total_date[5] + '</option>';
  total_date_html += '<option value="' + total_date[6] + '" selected="selected">' + total_date[6] + '</option>';
  total_date_html += '</select>';
  $("#total_date").append(total_date_html);

  var domain_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(tomorrow-24*60*60*1000*(7-i));
    domain_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
  }
  $("#domain_date").empty();
  var domain_date_html = '';
  domain_date_html += '<select id="domain_date_select">';
  domain_date_html += '<option value="' + domain_date[0] + '">' + domain_date[0] + '</option>';
  domain_date_html += '<option value="' + domain_date[1] + '">' + domain_date[1] + '</option>';
  domain_date_html += '<option value="' + domain_date[2] + '">' + domain_date[2] + '</option>';
  domain_date_html += '<option value="' + domain_date[3] + '">' + domain_date[3] + '</option>';
  domain_date_html += '<option value="' + domain_date[4] + '">' + domain_date[4] + '</option>';
  domain_date_html += '<option value="' + domain_date[5] + '">' + domain_date[5] + '</option>';
  domain_date_html += '<option value="' + domain_date[6] + '" selected="selected">' + domain_date[6] + '</option>';
  domain_date_html += '</select>';
  $("#domain_date").append(domain_date_html);

  /*
  var detail_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(tomorrow-24*60*60*1000*(7-i));
    detail_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
  }
  $("#detail_date").empty();
  var detail_date_html = '';
  detail_date_html += '<select id="detail_date_select">';
  detail_date_html += '<option value="' + detail_date[0] + '">' + detail_date[0] + '</option>';
  detail_date_html += '<option value="' + detail_date[1] + '">' + detail_date[1] + '</option>';
  detail_date_html += '<option value="' + detail_date[2] + '">' + detail_date[2] + '</option>';
  detail_date_html += '<option value="' + detail_date[3] + '">' + detail_date[3] + '</option>';
  detail_date_html += '<option value="' + detail_date[4] + '">' + detail_date[4] + '</option>';
  detail_date_html += '<option value="' + detail_date[5] + '">' + detail_date[5] + '</option>';
  detail_date_html += '<option value="' + detail_date[6] + '" selected="selected">' + detail_date[6] + '</option>';
  detail_date_html += '</select>';
  $("#detail_date").append(detail_date_html);
  */
}

date_initial();

$('#total_date_button').click(function(){
  var select_range = $('input[name="range_select"]:checked').val();
  var select_index = $('input[name="index_select"]:checked').val();
  var select_total_date = $("#total_date_select").val()
  var url_total_new = '';
  url_total_new = '/influence_application/search_influence/?date=' + select_total_date + '&index=' + select_index + '&domain=' + select_range;
  draw_table_total_new = new Search_weibo_total(url_total_new, '#total_rank');
  draw_table_total_new.call_sync_ajax_request(url_total_new, draw_table_total_new.ajax_method, draw_table_total_new.Draw_table);
  prepare_rank_distribution();
});

/*
$('#detail_date_button').click(function(){
  //console.log($("#total_date_select").val());
  var url_detail_new = '/influence_application/hot_origin_weibo/?date=' + $("#detail_date_select").val() + '&number=10';
  var detail_status = $('input[name="detail_select"]:checked').val();
  if(detail_status==0){
    draw_table_detail_trans_new = new Search_weibo_detail_trans(url_detail_new, '#detail_rank');
    draw_table_detail_trans_new.call_sync_ajax_request(url_detail_new, draw_table_detail_trans_new.ajax_method, draw_table_detail_trans_new.Draw_table);
  }
  else{
    draw_table_detail_comment_new = new Search_weibo_detail_comment(url_detail_new, '#detail_rank');
    draw_table_detail_comment_new.call_sync_ajax_request(url_detail_new, draw_table_detail_comment_new.ajax_method, draw_table_detail_comment_new.Draw_table);
  }
  draw_hot_users();
});
*/

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}

prepare_rank_distribution();

//画柱状图
function draw_rank_distribution(axis, data1, data2, div, number_all, number_in){
  var option = {
    title : {
        text: '用户影响力分布',
        subtext: '较低影响力(<500)的人数：全网:' + number_all + '人，人物库:3034人',
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['全网','人物库']
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
    grid:{
        y:80,
    },
    xAxis : [
        {
            type : 'category',
            data : axis,
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'全网',
            type:'bar',
            data:data1,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
        },
        {
            name:'人物库',
            type:'bar',
            data:data2,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
        }
    ]
  };
  var draw_init = echarts.init(document.getElementById(div));
  draw_init.setOption(option);
}

//柱状图数据
function prepare_rank_distribution(){
  var influence_bar_axis = [];
  var influence_bar_all = [];
  var influence_bar_in = [];
  var low_number_all = 0;
  var low_number_in = 0;

  var url_rank_distribution_all = '/influence_application/user_index_distribution/?date=' + $("#total_date_select").val();
  $.ajax({
    url: url_rank_distribution_all,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:callback_all
  });

  function callback_all(data1){
    for(var i=3;i<(data1[0].length-1);i++)
      influence_bar_axis.push(data1[0][i]+'-'+data1[0][i+1]);
    low_number_all = data1[1][0]+data1[1][1]+data1[1][2];
    for(var j=3;j<data1[1].length;j++)
      influence_bar_all.push(data1[1][j]);
  }

  var url_rank_distribution_in = '/influence_application/portrait_user_index_distribution/?date=' + $("#total_date_select").val();
  $.ajax({
    url: url_rank_distribution_in,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:callback_in
  });

  function callback_in(data2){
    low_number_in = data2[1][0]+data2[1][1]+data2[1][2];
    for(var k=3;k<data2[1].length;k++)
      influence_bar_in.push(data2[1][k]);
  }

  //console.log(influence_bar_axis, influence_bar_all, influence_bar_in, low_number_all, low_number_in);
  draw_rank_distribution(influence_bar_axis, influence_bar_all, influence_bar_in, 'rank_distribution', low_number_all, low_number_in);
}

/*
//热门人物信息
function get_hot_users_details(){
  var url_hot_users = '/influence_application/hot_origin_weibo_brust/?date=' + $("#detail_date_select").val() + '&number=6';
  $.ajax({
    url: url_hot_users,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:hot_users_details
  }); 
  function hot_users_details(data){
    //console.log(url_hot_users);
    //console.log(data);
    for(var i=0;i<2;i++){
      for(var j=0;j<6;j++){
        var user_id = data[i][j][2];
        var details = [];
        if(data[i][j][3]=="")
          data[i][j][3] = "未知";
        details.push(data[i][j][3],data[i][j][4].toFixed(0),data[i][j][6].toFixed(0));
        details.push(data[i][j][7],data[i][j][8].toFixed(0),data[i][j][9],data[i][j][10].toFixed(0));
        details.push(data[i][j][11],data[i][j][12].toFixed(0),data[i][j][13],data[i][j][14].toFixed(0));
        details.push(data[i][j][15],data[i][j][16].toFixed(0),data[i][j][17],data[i][j][18].toFixed(0));
        details.push(data[i][j][19],data[i][j][20].toFixed(0),data[i][j][21],data[i][j][22].toFixed(0));
        user_details[user_id] = details;
      }
    }
  }
}
    
function draw_hot_users_details(uid){
    $('#hot_users_details').empty(); 
    var html_details = '';
    html_details += '<div style="font-size:medium"><span class="pt_title">用户ID： <a href="/index/personal/?uid='+ uid +'" target="_blank">'+ uid +'</a></span>';
    html_details += '<span class="pt_title" style="margin-left:10px">昵称： '+ user_details[uid][0] +'</span>';
    html_details += '<span class="pt_title" style="margin-left:10px">影响力： '+ user_details[uid][1] +'</span>';
    html_details += '<span class="pt_title" style="margin-left:10px">爆发度： '+ user_details[uid][2] +'</span></div>';
    html_details += '<div style="margin-top:10px;margin-bottom:20px;margin-left:150px;width:700px">';
    html_details += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html_details += '<thead><tr><th colspan="2"></th><th style="text-align:center;vertical-align:middle;width:110px">总数</th><th style="text-align:center;vertical-align:middle;width:110px">平均数</th><th style="text-align:center;vertical-align:middle;width:110px">最大值</th><th style="text-align:center;vertical-align:middle;width:110px">爆发度</th></tr></thead>';
    html_details += '<tbody>';
    html_details += '<tr>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle;width:100px" rowspan="2">原创微博</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle;width:80px">转发</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][3] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][4] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][5] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][6] +'</td>';
    html_details += '</tr>';
    html_details += '<tr>';
    //html_details += '<td class="center" style="text-align:center;vertical-align:middle"></td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle;width:80px">评论</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][7] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][8] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][9] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][10] +'</td>';
    html_details += '</tr>';
    html_details += '<tr>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle;width:100px" rowspan="2">转发微博</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle;width:80px">转发</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][11] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][12] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][13] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][14] +'</td>';
    html_details += '</tr>';
    html_details += '<tr>';
    //html_details += '<td class="center" style="text-align:center;vertical-align:middle"></td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">评论</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][15] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][16] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][17] +'</td>';
    html_details += '<td class="center" style="text-align:center;vertical-align:middle">'+ user_details[uid][18] +'</td>';
    html_details += '</tr>';
    html_details += '</tbody>';
    html_details += '</table>';
    html_details += '</div>';
    $('#hot_users_details').append(html_details);
}

//画折线图
function draw_line_chart(xaxis, influence_data, div, uid){
  var uname = user_details[uid][0];
  //console.log(uname);
  var uname_text = '"' + uname + '"的影响力';
  var line_chart_option = {
    title : {
        text: '用户影响力走势图',
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
            data : xaxis,
        }
    ],
    yAxis : [
        {
            type : 'value',
            max : 2000,
            min : 0,
            splitNumber : 4,
        }
    ],
    series : [
        {
            name:uname_text,
            type:'line',
            data:influence_data,
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
  //$('#'+div).empty();
  var draw_init2 = echarts.init(document.getElementById(div));
  draw_init2.setOption(line_chart_option);
}

//折线图数据
function prepare_line_chart(uid){
  var url_line_chart = '/influence_application/portrait_history_active/?date=2013-09-07&uid=' + uid;
  //console.log(url_line_chart);
  $.ajax({
    url: url_line_chart,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:callback_line_chart
  });
  function callback_line_chart(data){
    var line_chart_dates = [];
    var line_chart_tomorrow = new Date(2013,8,8);
    for(var i=0;i<7;i++){
      var today = new Date(line_chart_tomorrow-24*60*60*1000*(7-i));
      line_chart_dates[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
    }
    //console.log(line_chart_dates);
    //console.log(data);
    var line_chart_data = [];
    if (data != 'NotFound'){
        for(var j=0;j<data.length;j++)
            line_chart_data.push(parseFloat(data[j].toFixed(2)));
        //console.log(line_chart_data);
    }
    draw_line_chart(line_chart_dates, line_chart_data, 'hot_users_line_chart', uid);
  }
}

//画头像
function draw_hot_users(){
  var url_hot_users = '/influence_application/hot_origin_weibo_brust/?date=' + $("#detail_date_select").val() + '&number=6';
  $.ajax({
    url: url_hot_users,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:hot_users_img
  });
  function hot_users_img(data){
    $('#hot_users').empty(); 
    var html = '';
    html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope" style="width:480px"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
    html += '<h3 class="no-margin" style="text-align:center"><small>转发量排序</small></h3>';
    html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
    html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:80px" class="list-inline">';
    for(var i in data[0]){
      if(data[0][i][1]=="")
        data[0][i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(data[0][i][3]=="")
        data[0][i][3]="未知";
      html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom:10px;margin-right:9px" class="index-small-photo-wrap no-padding ng-scope">';
      html += '<div class="small-photo shadow-5"><img style="cursor:hand;" src="' + data[0][i][1] + '" alt="' + data[0][i][3] +'" title="' + data[0][i][3] +'" class="hot_users" name="' + data[0][i][2] + '"></div></li>';
    }
    html += '</ul></div></div>';

    html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope" style="float:right;width:480px"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
    html += '<h3 class="no-margin" style="text-align:center"><small>评论量排序</small></h3>';
    html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
    html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:80px" class="list-inline">';
    for(var j in data[1]){
      if(data[1][j][1]=="")
        data[1][j][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(data[0][j][3]=="")
        data[0][j][3]="未知";
      html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom:10px;margin-right:9px" class="index-small-photo-wrap no-padding ng-scope">';
      html += '<div class="small-photo shadow-5"><img style="cursor:hand;" src="' + data[1][j][1] + '" alt="' + data[1][j][3] +'" title="' + data[1][j][3] +'" class="hot_users" name="' + data[1][j][2] + '"></div></li>';
    }
    html += '</ul></div></div>';
    $('#hot_users').append(html);
    $('.hot_users').click(function(){
      var user_id_choose = $(this).attr('name');
      //console.log('choose'+user_id_choose);
      draw_hot_users_details(user_id_choose);
      prepare_line_chart(user_id_choose);
    });

    user_details = new Array();
    get_hot_users_details();
    draw_hot_users_details(data[0][0][2]);
    prepare_line_chart(data[0][0][2]);
  }
}

var user_details;
draw_hot_users();
*/

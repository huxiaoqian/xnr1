//影响力分布
function draw_influ_distribution(data,radar_div, title){
    //console.log(data);
    var mychart1 = echarts.init(document.getElementById(radar_div));
    var y_axi = data[0];
    var x_axi = data[1];
    var xdata = [];
    var ydata = [];
    var count_sum = 0;
    for (var i =0; i < y_axi.length;i++){
        count_sum += y_axi[i];
        if(y_axi[i]!=0){
            xdata.push(data[1][i] + '-' + data[1][i+1]);
            ydata.push(data[0][i]);
        }
    }
    /*
    for (i = 0; i< data[1].length-1; i++){
        xdata.push(data[1][i] + '-' + data[1][i+1]);
    };
    */
    var option = {
    tooltip : {
        trigger: 'axis',
        formatter: "{a}<br/>{b} : {c}"
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            //scale: true,
            name : title,
            data : xdata
        }
    ],
    series : [
        {
            name:title,
            type:'bar',
            data:ydata
        }
    ]
    };
    mychart1.setOption(option);
}

//粉丝数分布
function draw_fans_distribution(data,radar_div, title){
    //console.log(data);
    var y_name = title+'（/百万人）';
    var mychart1 = echarts.init(document.getElementById(radar_div));
    var y_axi = data[0];
    var x_axi = data[1];
    var xdata = [];

    for (i = 0; i< data[1].length-1; i++){
        xdata.push((data[1][i]/1000000).toFixed(2) + '-' + (data[1][i+1]/1000000).toFixed(2))
    };

    var option = {
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            name : y_name,
            data : xdata
        }
    ],
    series : [
        {
            name:title,
            type:'bar',
            data:data[0]
        }
    ]
    };
    mychart1.setOption(option);
}

//微博数分布
function draw_status_distribution(data,radar_div, title){
    //console.log(data);
    var y_name = title + '（/万）';
    var mychart1 = echarts.init(document.getElementById(radar_div));
    var y_axi = data[0];
    var x_axi = data[1];
    var xdata = [];

    for (i = 0; i< data[1].length-1; i++){
        xdata.push((data[1][i]/10000).toFixed(2) + '-' + (data[1][i+1]/10000).toFixed(2))
    };

    var option = {
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            name : y_name,
            data : xdata
        }
    ],
    series : [
        {
            name:title,
            type:'bar',
            data:data[0]
        }
    ]
    };
    mychart1.setOption(option);
}

//朋友数分布
function draw_friends_distribution(data, radar_div, title){
    //console.log(data);
    var y_name = title + '（/千人）';
    var mychart1 = echarts.init(document.getElementById(radar_div));
    var y_axi = data[0];
    var x_axi = data[1];
    var xdata = [];

    for (i = 0; i< data[1].length-1; i++){
        xdata.push((data[1][i]/1000).toFixed(2) + '-' + (data[1][i+1]/1000).toFixed(2))
    };

    var option = {
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            name : y_name,
            data : xdata
        }
    ],
    series : [
        {
            name:title,
            type:'bar',
            data:data[0]
        }
    ]
    };
    mychart1.setOption(option);
}


function Show_influ(url,div){
    that = this;
    this.ajax_method = 'GET';
    this.div = div;
}

Show_influ.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_table:function(data){
   // console.log(data);
    var influ_his = data['influence_his'];
    var influ_in_user = data['influence_in_user'];
    var influ_out_user = data['influence_out_user'];
    var influ_trend = data['influence_trend'];
    //console.log('influ_his',influ_his);
    if(influ_his[1][1] == 0 & influ_his[1][5] == 1){
        $('#influ_distribution').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        draw_influ_distribution(influ_his,'influ_distribution', '影响力排名');
    }
    show_influ_users('influ_active_users',influ_trend['main_max']);
    show_influ_users('influ_unactive_users',influ_trend['main_min']);
    //console.log(influ_trend['main_max']);
    //console.log(influ_out_user);
    group_influ(influ_trend);
    var influ_in = data['influence_in_user'];
    var topics = [];
    for(var key in influ_in['topic']){
        var tt = [];
        tt.push(key,influ_in['topic'][key])
        topics.push(tt);
    }
    var domains = [];
    for(var key in influ_in['domain']){
        var dd = [];
        dd.push(key,influ_in['domain'][key])
        domains.push(dd);
    }
    //console.log(domains);
    if(topics.length == 0){
        $('#showmore_topic_influ').css('display', 'none');
        $('#influence_topic').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(topics,'influence_topic', 'influ_topic_WordList','showmore_topic_influ');
    };
    if(domains.length == 0){
        $('#showmore_domain_influ').css('display', 'none');
        $('#influence_domain').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(domains,'influence_domain', 'influ_domain_WordList','showmore_domain_influ');
    }
    if(influ_in['influence'][1][1] == 0 & influ_in['influence'][1][5] == 1){
        $('#group_influ_distribution').append('<div style="padding-top: 30%;margin-left:30%;">暂无数据</div>');
    }else{
        //console.log('influ_in["influence"]',influ_in['influence']);
        draw_influ_distribution(influ_in['influence'],'group_influ_distribution', '影响力排名');
    }
    if(influ_in['importance'][1][1] == 0 & influ_in['importance'][1][5] == 1){
        $('#group_impor_distribution').append('<div style="padding-top: 30%;margin-left:30%;">暂无数据</div>');
    }else{
        draw_influ_distribution(influ_in['importance'],'group_impor_distribution', '重要度排名');
    }
    var influ_out = data['influence_out_user'];
    //Draw_top_location2(influ_out['out_fansnum_his'], influ_out['out_friendsnum_his'], influ_out['out_statusnum_his']);

    if(influ_out['out_fansnum_his'][1][1] == 0 & influ_out['out_fansnum_his'][1][5] == 1){
        $('#group_fans_distribution').append('<div style="padding-top: 30%;margin-left:30%;">暂无数据</div>');
    }else{
        draw_fans_distribution(influ_out['out_fansnum_his'],'group_fans_distribution', '粉丝数');
    };
    if(influ_out['out_friendsnum_his'][1][1] == 0 & influ_out['out_friendsnum_his'][1][5] == 1){
        $('#group_friends_distribution').append('<div style="padding-top: 30%;margin-left:30%;">暂无数据</div>');
    }else{
        draw_friends_distribution(influ_out['out_friendsnum_his'],'group_friends_distribution', '朋友数');
    };
    if(influ_out['out_statusnum_his'][1][1] == 0 & influ_out['out_statusnum_his'][1][5] == 1){
        $('#group_weiboshu_distribution').append('<div style="padding-top: 30%;margin-left:30%;">暂无数据</div>');
    }else{
    draw_status_distribution(influ_out['out_statusnum_his'],'group_weiboshu_distribution', '微博数');
    };
  }
}

//影响用户
function show_influ_users(div_name,data){
    $('#' + div_name).empty();
    
    var html = '';
    html += '<table class="table table-striped" style="font-size:10px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">频数</th></tr>';
    for (var i = 0; i < data.length; i++) {
       var s = i.toString();
       var m = i + 1;
       var inid =  data[i][0].split('&')[0]
       var uname = data[i][0].split('&')[1];
       if(uname == 'unknown'){
          uname = '未知('+inid+')';
       }
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid='+inid+'">' + uname + '</a></th><th style="text-align:center">' + data[i][1] + '</th></tr>';
    };
    /*
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    */
    html += '</table>'; 
    $('#'+div_name).append(html);
}
//更多影响用户
function show_more_influ_active_users(div_name){
    $('#' + div_name).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < 1; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + 'web' + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#'+div_name).append(html);
}

//群体影响力走势图

function group_influ(data){
   var mychart = echarts.init(document.getElementById('group_influ'));
   var mind = []
   var maxd = []
   ave_data = data['ave_list'];
   max_data = data['max_list'];
   min_data = data['min_list'];
  // console.log(min_data);
   for(var i=0;i<min_data.length;i++){
      mind.push(min_data[i][1]);
   }
   // console.log('min',mind);
   for(var i=0;i<max_data.length;i++){
	  
      maxd.push(max_data[i][1]);
   }
   // console.log('max',maxd);
   time_data = data['time_list'];
   var option = {
    tooltip : {
        trigger: 'axis',
        formatter: function (params) {
        var max_user_name = [];
        var min_user_name = [];
        for(var i=0; i<max_data.length;i++){
            if(max_data[i][2]=='unknown'){
                max_data[i][2] = '未知('+max_data[i][0]+')';
            }
            if(min_data[i][2]=='unknown'){
                min_data[i][2] = '未知('+min_data[i][0]+')';
            }
            max_user_name.push(max_data[i][2]);
            min_user_name.push(min_data[i][2]);

        };
            var res = '' + params[0].name;
            var index = params[0].dataIndex;
            res +=  '<br/>最高值用户: ' + max_user_name[index] ;
            res +=  '<br/>最低值用户: ' + min_user_name[index] ;
            return res
        }
    },
    legend: {
        data:['最高值','平均值','最低值']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : time_data
        }
    ],
    yAxis : [
        {
            type : 'value',
            scale: true,
            name : '影响力'
        }
    ],
    series : [
        {
            name:'最高值',
            type:'line',
            data:maxd
        },
        {
            name:'平均值',
            type:'line',
            data:ave_data
        },
        {
            name:'最低值',
            type:'line',
            data:mind
        }
        
    ]
};
  mychart.setOption(option);
}

//显示成员微博信息
function Draw_group_influ_weibo(data, div_name, sub_div_name){
    page_num = 5;
    //console.log(div_name);
    if (data.length < page_num) {
        //console.log('data_length', data.length);
        $('#'+ div_name + ' #pageGro').css('display', 'none');
        $('#'+ div_name + ' #pageGro .pageUp').css('display', 'none');
        $('#'+ div_name + ' #pageGro .pageList').css('display', 'none'); 
        $('#'+ div_name + ' #pageGro .pageDown').css('display', 'none'); 
        if (data.length == 0) {
            $('#' + sub_div_name).empty();
            $('#' + sub_div_name).append('此条件下没有与此事件相关的微博！');
        }else{
            //$('#'+ div_name + ' #pageGro').css('display', 'block');
            page_num = data.length
            page_group_influ_weibo( 0, page_num, data, sub_div_name);
        }
      }
      else {
          $('#'+ div_name + ' #pageGro').css('display', 'block');
          $('#'+ div_name + ' #pageGro .pageUp').css('display', 'block');
          $('#'+ div_name + ' #pageGro .pageList').css('display', 'block'); 
          $('#'+ div_name + ' #pageGro .pageDown').css('display', 'block'); 
          page_group_influ_weibo( 0, page_num, data, sub_div_name);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>10){
        page_icon(1,10,0, div_name);
    }else{
        page_icon(1,pageCount,0, div_name);
    }
    
    $("#"+div_name+" #pageGro li").live("click", function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      //console.log('page', page);         
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        // console.log('start', start_row);
        // console.log('end', end_row);
        // console.log('data',data);
        page_group_influ_weibo(start_row,end_row,data, sub_div_name);
    });

    $("#"+div_name+" #pageGro .pageUp").off('click').click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());
            pageUp(pageNum,pageCount);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index > 0){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      //console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_influ_weibo(start_row,end_row,data, sub_div_name);
    });
    

    $("#" + div_name + " #pageGro .pageDown").off('click').click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());

            pageDown(pageNum,pageCount);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html()) 
      //console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_influ_weibo(start_row,end_row,data, sub_div_name);
    });
}

function page_group_influ_weibo(start_row,end_row,data, sub_div_name){
    weibo_num = end_row - start_row;
    $('#'+ sub_div_name).empty();
    var html = "";
    html += '<div class="group_weibo_font" style="margin-right:5px;">';
    for (var i = start_row; i < end_row; i += 1){
        s=i.toString();
        //uid = data[s]['uid'];
        uid = document.getElementById('select_group_weibo_user').value;
        text = data[s]['text'];
        //uname = data[s]['uname'];
        var selectIndex  = document.getElementById('select_group_weibo_user').selectedIndex
        uname = document.getElementById('select_group_weibo_user').options[selectIndex].text;
        timestamp = data[s]['timestamp'];
        //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="padding:5px;background:whitesmoke;font-size:14px">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + timestamp + '</font></p>';
            html += '</div>'
    }
        else{
            html += '<div style="padding;5px;">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';    
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + timestamp + '</font></p>';
            html += '</div>';
        }
    }
    html += '</div>'; 
    $('#'+sub_div_name).append(html);
}

//获取微博成员信息
function Draw_group_weibo_user(uids,unames){
    
    $('#group_influ_weibo_user').empty();
    html = '';
    html += '<select id="select_group_weibo_user" style="max-width:150px;">';
    // var timestamp = Date.parse(new Date());
    // date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
    //var all= '全部用户'
    //html += '<option value="' + all + '" selected="selected">' + all + '</option>';      
    for (var i = 0; i < unames.length; i++) {
        // timestamp = timestamp-24*3600*1000;
        // date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
        if(unames[i] == 'unknown'){
            unames[i] = '未知('+uids[i]+')';
        }
        html += '<option value="' + uids[i] + '">' + unames[i] + '</option>';
    }
    html += '</select>';
    $('#group_influ_weibo_user').append(html);
}

//显示群组成员微博
function submit_date_user(){
    var timestamp_from = $('#group_influ_weibo #weibo_from').val();
    var timestamp_to = $('#group_influ_weibo #weibo_to').val();
    timestamp_from = new Date(timestamp_from);
    timestamp_from = Math.floor(timestamp_from.getTime()/1000);
    timestamp_to = new Date(timestamp_to);
    timestamp_to = Math.floor(timestamp_to.getTime()/1000);
    var select_uid = document.getElementById('select_group_weibo_user').value;
    var submit_date_user_url = '/group/influence_content/?uid=' + select_uid + '&timestamp_from=' + timestamp_from + '&timestamp_to=' + timestamp_to;
    //console.log(submit_date_user_url);
    function Weibo(){
        this.ajax_method = 'GET';
    }
    Weibo.prototype = {
      call_sync_ajax_request:function(url, method, callback){
        $.ajax({
          url: url,
          type: method,
          dataType: 'json',
          async: false,
          success:callback
        });
       },
       Draw:function(data){
	    //console.log(data);
		Draw_group_influ_weibo(data,'group_influ_weibo', 'group_influ_weibo_result');
        }
      
     }
    var Weibo = new Weibo();
    Weibo.call_sync_ajax_request(submit_date_user_url, Weibo.ajax_method, Weibo.Draw);
}

function get_radar_data (data) {
  var topic = data;
  var topic_name = [];
  var topic_value = [];
  for(var i=0; i<topic[0].length;i++){
    topic_value.push(topic[1][i].toFixed(2)*10)
    topic_name.push(topic[0][i]);
  };
  // var topic_value2 = [];
  // var topic_name2 = [];
  // for(var i=0; i<8;i++){ //取前8个最大值
  //   a=topic_value.indexOf(Math.max.apply(Math, topic_value));
  //   topic_value2.push(topic_value[a].toFixed(3));
  //   topic_name2.push(topic_name[a]);
  //   topic_value[a]=0;
  // }
  var topic_name3 = [];
  var max_topic = 8;
  if(topic_value.length<8){
    max_topic = topic_value.length;
  }
  for(var i=0;i<max_topic;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name[i];
    name_dict["text"] = index;
    name_dict["max"] = Math.max.apply(Math, topic_value).toFixed(3)+1;
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value);
  return topic_result;
}
function Draw_topic_group_spread(data, radar_div, motal_div, show_more){
  var topic = [];
  var html = '';
    if(data[0][1] == 0){
      $('#'+ motal_div).empty();
      $('#'+ motal_div).empty();
      html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      $('#'+ radar_div).append(html);
      $('#'+ motal_div).append(html);
    }else{
      var topic_sta = [];
      var topic_name_sta = [];
      for(var i=0;i<data.length;i++){
        if(data[i][1] != 0){
          topic_sta.push(data[i][1]/data[0][1]);
          topic_name_sta.push(data[i][0]);
        }
      };
      $('#'+ motal_div).empty();
  if(topic_sta.length == 0){
      $('#'+ motal_div).empty();
      html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      //$('#'+ more_div).append(html);
      $('#'+ radar_div).append(html);
      $('#'+ motal_div).append(html);
      $('#'+ show_more).empty();
  }else{
      html = '';
      html += '<table class="table table-striped table-bordered">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">概率</th></tr>';
      for (var i = 0; i < topic_sta.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + topic_name_sta[i] +  '&psycho_status=&domain&topic" target="_blank">' + topic_name_sta[i] +  '</a></th><th style="text-align:center">' + topic_sta[i].toFixed(2) + '</th></tr>';
      };
      html += '</table>'; 
      $('#'+ motal_div).append(html);
    };
    var topic_val = [];
    topic_val.push(topic_name_sta);
    topic_val.push(topic_sta);
    var topic_result = [];
    topic_result = get_radar_data(topic_val);
  var topic_name = topic_result[0];
  var topic_value = topic_result[1];
  var myChart2 = echarts.init(document.getElementById(radar_div));
  var option = {
    // title : {
    //   text: '用户话题分布',
    //   subtext: ''
    // },
      tooltip : {
        show: true,
        trigger: 'axis',
        formatter:  function (params){
          var res  = '';
          var indicator = params.indicator;
          //console.log(params);
          res += params['0'][3]+' : '+(params['0'][2]/10).toFixed(2);
          return res;
          }
        },
      toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
      },
      calculable : true,
      polar : [
       {
        indicator :topic_name,
        radius : 90
       }
      ],
      series : [
       {
        name: '话题分布情况',
        type: 'radar',
        itemStyle: {
         normal: {
          areaStyle: {
            type: 'default'
          }
         }
        },
       data : [
        {
         value : topic_value,
         //name : '用户话题分布'
        }
       ]
      }]
  };
  myChart2.setOption(option);
}
}


var Show_influ = new Show_influ();
var group_influ_url = '/group/show_group_result/?task_name='+name+'&submit_user=admin&module=influence';
//console.log(group_influ_url);
Show_influ.call_sync_ajax_request(group_influ_url, Show_influ.ajax_method, Show_influ.Draw_table);
//日期选择


//影响力内容：用户微博
    //选择用户
function Weibo_user(){
    this.ajax_method = 'GET';
}
Weibo_user.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_user:function(data){
	  //console.log(data);
	  var unames = [];
	  var uids = [];
	  for(var key in data){
        uids.push(key);
        unames.push(data[key]);
	  }
      Draw_group_weibo_user(uids,unames);
  }
      
}
function bind_spread_click(){
    //波及用户
    $(' input[name="user_select"]').click(function(){
        if($('input[name="user_select"]:checked').val()=='1'){       
            $('#influence_in_user').css('display', 'none');
            $('#influence_out_user').css('display', 'block');
        }else{
            $('#influence_in_user').css('display', 'block');
            $('#influence_out_user').css('display', 'none');
        }
    });
}

var weibo_user_url = '/group/group_member/?task_name=mytest030303&submit_user=admin';
var Weibo_user = new Weibo_user();
Weibo_user.call_sync_ajax_request(weibo_user_url,Weibo_user.ajax_method,Weibo_user.Draw_user)
function spread_load(){
    if (!global_spread_flag){
        if(global_test_mode==0){
            $('#group_influ_weibo #weibo_from').datetimepicker({value:from_date,step:60});
            $('#group_influ_weibo #weibo_to').datetimepicker({value:current_date,step:60});
        }else{
            $('#group_influ_weibo #weibo_from').datetimepicker({value:from_date,step:60,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
            $('#group_influ_weibo #weibo_to').datetimepicker({value:current_date,step:60,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
        }
        bind_spread_click();
        // show_more_influ_active_users('show_rank_influ_users');
        // show_more_influ_active_users('show_rank_uninflu_users');
        //$('#group_influence_conclusion').append('结论结论结论结论');
        
        //var weibo_user_url = '/group/group_member/?task_name=' + name;
		var weibo_user_url = '/group/group_member/?task_name=mytest030303';
        Weibo_user.call_sync_ajax_request(weibo_user_url,Weibo_user.ajax_method,Weibo_user.Draw_user)
        global_spread_flag = true;
    }
}

var date = choose_time_for_mode();
date.setHours(0,0,0,0);
var max_date = date.format('yyyyMMdd hh:mm');
var current_date = date.format('yyyy/MM/dd hh:mm');
var from_date_time = Math.floor(date.getTime()/1000) - 60*60*24*30;
var min_date_ms = new Date()
min_date_ms.setTime(from_date_time*1000);
var from_date = min_date_ms.format('yyyy/MM/dd hh:mm');
//var Weibo_user = new Weibo_user();
var global_spread_flag = false;
$(function(){
	spread_load();
})
    //选择时间
/*
var url_all = [];
var time_from = Date.parse($('#group_influ_weibo #weibo_from').val())/1000;
var time_to = Date.parse($('#group_influ_weibo #weibo_to').val())/1000;
var timestamp_from_url = '';
timestamp_from_url = 'timestamp_from=' + time_from;
url_all.push(timestamp_from_url);
var timestamp_to_url = '';
timestamp_to_url = 'timestamp_to=' + time_to;
url_all.push(timestamp_to_url);
*/



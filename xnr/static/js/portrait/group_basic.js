function g_basic(){
  this.ajax_method = 'GET';
}
g_basic.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  }
}
function draw_basic(data){
    //console.log(data);
	draw_sex(data);
	draw_verify(data);
	Draw_totalnumber(data);
	draw_tag(data);
	g_info(data);
	//draw_tag({'user_tag':{'好':13,'中':21,'坏':9}});
}

function weiboData(data){
		DrawBasicWeibo(data,'group_basic_weibo', 'group_basic_weibo_result');
}

function g_info(data){
	$('#group_num').html(data.count);
	//console.log(data.topic);
	//console.log(data.domain);
	
	if(data.topic.length == 0){
        $('#showmore_topic').css('display', 'none');
        $('#topic').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(data.topic,'topic', 'topicWordList','showmore_topic');
    };
	
    if(data.domain.length == 0){
        $('#showmore_domain').css('display', 'none');
        $('#domain').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(data.domain,'domain', 'domainWordList','showmore_domain');
    }
}
function draw_sex(data){
	var mychart1 =  echarts.init(document.getElementById('group_sex')); 
	var option = {
	    tooltip : {
	        trigger: 'item',
	        formatter: "{a} <br/>{b} : {c} ({d}%)"
	    },
	    legend: {
	        orient : 'vertical',
	        x : 'left',
	        data:['男','女']
	    },
	    toolbox: {
	        show : false,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            magicType : {
	                show: true, 
	                type: ['pie', 'funnel'],
	                option: {
	                    funnel: {
	                        x: '25%',
	                        width: '25%',
	                        funnelAlign: 'center',
	                        max: 1548
	                    }
	                }
	            },
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    calculable : true,
	    series : [
	        {
	            name:'性别',
	            type:'pie',
	            radius : ['50%', '70%'],
	            itemStyle : {
	                normal : {
	                    label : {
	                        show : false
	                    },
	                    labelLine : {
	                        show : false
	                    }
	                },
	                emphasis : {
	                    label : {
	                        show : true,
	                        position : 'center',
	                        textStyle : {
	                            fontSize : '30',
	                            fontWeight : 'bold'
	                        }
	                    }
	                }
	            },
	            data:[
	                {value:data['gender']['1'], name:'男'},
	                {value:data['gender']['2'], name:'女'}
	            ]
	        }
	    ]
	};
	                  
  mychart1.setOption(option);
}
function draw_verify(data){
	var veri = data['verified'];
	var yes = 0;
	var no = 0;
	for (var k in veri){
		if (k == ''){
			no = veri[k];
		}else{
			yes = veri[k];
		}
	}
	var mychart1 =  echarts.init(document.getElementById('group_verify')); 
	var option = {
	    tooltip : {
	        trigger: 'item',
	        formatter: "{a} <br/>{b} : {c} ({d}%)"
	    },
	    legend: {
	        orient : 'vertical',
	        x : 'left',
	        data:['已认证','未认证']
	    },
	    toolbox: {
	        show : false,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            magicType : {
	                show: true, 
	                type: ['pie', 'funnel'],
	                option: {
	                    funnel: {
	                        x: '25%',
	                        width: '50%',
	                        funnelAlign: 'center',
	                        max: 1548
	                    }
	                }
	            },
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    calculable : true,
	    series : [
	        {
	            name:'认证情况',
	            type:'pie',
	            radius : ['50%', '70%'],
	            itemStyle : {
	                normal : {
	                    label : {
	                        show : false
	                    },
	                    labelLine : {
	                        show : false
	                    }
	                },
	                emphasis : {
	                    label : {
	                        show : true,
	                        position : 'center',
	                        textStyle : {
	                            fontSize : '20',
	                            fontWeight : 'bold'
	                        }
	                    }
	                }
	            },
	            data:[
	                {value:yes, name:'已认证'},
	                {value:no, name:'未认证'}
	            ]
	        }
	    ]
	};
  mychart1.setOption(option);
}
function Draw_totalnumber(data){
    $('#totalnumber').empty();
    html = '';
    html += '<a class="well top-block" style="height: 200px;width: 200px;border-radius: 450px;margin-top: 40px;margin-left: 50px;">';
    html += '<div><img src="/static/img/user_group.png" style="height:40px;margin-top:40px"></div>';
    html += '<div>群组总人数</div>'
    html += '<div>' + data['count'] + '</div></a>';
    $('#totalnumber').append(html);
}
function toarray(a,b){
	this.names=a;
	this.num=b;
}
function draw_tag(data){
	var mychart1 = echarts.init(document.getElementById('group_tag'));
	var item = data['user_tag'];
	var items = [];
	var tagname= [];
	var tagvalue = [];
	for (var k in item){
		items.push(new toarray(k,item[k]));
	}
	items.sort(function(a,b){return a.num-b.num});
	//console.log(items);
	for (var i=0;i< items.length;i++){
		tagname.push(items[i].names);
		tagvalue.push(items[i].num);
	}
	var option = {
    tooltip : {
        trigger: 'axis',
        formatter:"{b} : {c}",
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
            data :tagname
        }
    ],
    series : [
        {
            // name:'2011年',
            type:'bar',
            data:tagvalue
        }
    ]
};
  mychart1.setOption(option);
}


function DrawMore(data,div,option){
    if (option =="topic"){
	    var theme = '话题';
	}else{
	    var theme = '身份';
	}
	var html = '';
    $('#'+div).empty();
	html += '<table class="table table-striped table-bordered" style="width:450px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">'+theme+'</th><th style="text-align:center">频数</th></tr>';
    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        var m = i + 1;
		if(data[i][1]=="unknown"){
		    data[i][1] = "未知";
		}
        html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data[i][0] +  '</th><th style="text-align:center">' + data[i][1] + '</th></tr>';
    };
    html += '</table>'; 
    $('#'+ div).append(html);
}



//var basic_name=document.getElementById('').text();
//var basic_name=$("#stickynote").text();
var g_basic = new g_basic();
var basic_url='/group/show_group_result/?task_name='+name+'&submit_user=admin&module=basic';
//var basic_url='/group/show_group_result/?task_name=mytest030303&submit_user=admin&module=basic';
//console.log(basic_url);
g_basic.call_sync_ajax_request(basic_url,g_basic.ajax_method,draw_basic);

var url = "/group/group_user_weibo/?task_name="+name+"&submit_user=admin&sort_type=timestamp";
g_basic.call_sync_ajax_request(url, g_basic.ajax_method,weiboData);
bind_basic_click();

function bind_basic_click(){
	$('[name="mode_choose"]').change(function(){
        // var url = "group/group_user_weibo/?task_name="+name+"&submit_user=admin&sort_type="+$(this).val();
        var url = "/group/group_user_weibo/?task_name="+name+"&submit_user=admin&sort_type=timestamp";
        //console.log(url);
        g_basic.call_sync_ajax_request(url, g_basic.ajax_method,weiboData);
	});
}

function DrawBasicWeibo(data, div_name, sub_div_name){
    //console.log(data);
    page_num = 5;
	//console.log(data);	
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
            page_group_basic_weibo( 0, page_num, data, sub_div_name);
        }
    }else {
          $('#'+ div_name + ' #pageGro').css('display', 'block');
          $('#'+ div_name + ' #pageGro .pageUp').css('display', 'block');
          $('#'+ div_name + ' #pageGro .pageList').css('display', 'block'); 
          $('#'+ div_name + ' #pageGro .pageDown').css('display', 'block'); 
          page_group_basic_weibo( 0, page_num, data, sub_div_name);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
    }
    var pageCount = total_pages;
    //console.log(pageCount);
    if(pageCount>5){
        page_icon(1,5,0, div_name);
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
      //console.log('start', start_row);
      //console.log('end', end_row);
      //console.log('data',data);
      page_group_basic_weibo(start_row,end_row,data, sub_div_name);
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
        page_group_basic_weibo(start_row,end_row,data, sub_div_name);
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
        page_group_basic_weibo(start_row,end_row,data, sub_div_name);
    });

}


function page_group_basic_weibo(start_row,end_row,data, sub_div_name){
    //console.log(data);
    weibo_num = end_row - start_row;
    $('#'+ sub_div_name).empty();
    var html = "";
    html += '<div class="group_weibo_font" style="margin-right:5px;">';
    for (var i = start_row; i < end_row; i += 1){
        s=i.toString();
		var mid = data[s][0];
		var uid = data[s][1];
		var uname = data[s][2];
        if(uname=='unknown'){
            uname = '未知('+uid+')';
        }
        var text = data[s][3];
		var retweet_count = data[s][8];
		var comment_count = data[s][9];
        //var location = data[s][2];
        var date = data[s][7];
        var tweet_ulr = data[s][11];
        //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="padding:5px;background:whitesmoke;">';
            html += '<p style="margin-left:10px;"><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:-5px;margin-left:10px;"><a color:#e0e0e0 target="_blank" style="text-decoration: underline;" href="'+tweet_ulr+'">' + date + '</a>-<a target="_blank" href="/index/personal_detail/?uid=' + uid + '">用户详情</a>-<a>转发树</a>';
            html += '<span style="margin-left:500px;"><a>转发数（'+ retweet_count +'）</a><a>评论数（'+ comment_count +'）</a></span></p>';
			html += '</div>'
    }
        else{
            html += '<div style="padding;5px;">';
            html += '<p style="margin-left:10px;"><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';    
            html += '<p style="margin-top:-5px;margin-left:10px;"><a color:#e0e0e0 target="_blank" style="text-decoration: underline;" href="'+tweet_ulr+'">' + date + '</a>-<a target="_blank" href="/index/personal_detail/?uid=' + uid + '">用户详情</a>-<a>转发树</a>';
            html += '<span style="margin-left:500px;"><a>转发数（'+ retweet_count +'）</a><a>评论数（'+ comment_count +'）</a></span></p>';
			html += '</div>';
        }
    }
    html += '</div>'; 
    $('#'+sub_div_name).append(html);
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


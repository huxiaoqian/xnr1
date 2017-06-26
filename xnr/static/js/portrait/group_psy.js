function g_psy(){
  this.ajax_method = 'GET';
}
g_psy.prototype = {   //获取数据，重新画表
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
var psy_url='/group/show_group_result/?task_name='+name+'&module=think';
var g_psy = new g_psy();
g_psy.call_sync_ajax_request(psy_url,g_psy.ajax_method,draw_think_all);
function draw_think_all(data){
    draw_group_kind(data);
    Draw_group_think(data);
    Draw_group_trend(data);
}
function Draw_group_think(data){
	var g_think = data['sentiment_pie'];
	var content1 = [];
	var content2 = [];
	var nod = {};
	var planb={'0':'中性','1':'积极','2':'生气','3':'焦虑','4':'悲伤','5':'厌恶','6':'消极其他','7':'消极'};
	var all_think = 0;
	var neg = 0;
	for(var key in g_think){
		var nod = {};
		all_think += g_think[key];
		if (key != '0' && key != '1'){
			neg += g_think[key];
		}
	}
	//console.log(all_think+'  '+neg);
	for(var key in g_think){
		var nod = {};
		if(key =='0' || key == '1'){
			nod['name'] = planb[key];
			nod['value'] = (g_think[key]/all_think).toFixed(2);		
			content1.push(nod);	
		}
		nod['name'] = planb[key];
		nod['value'] = (g_think[key]/all_think).toFixed(2);
		content2.push(nod);
	}
	content1.push({'name':'消极','value':(neg/all_think).toFixed(2)});
    var myChart = echarts.init(document.getElementById('group_think')); 
    var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: false},
            dataView : {show: false, readOnly: false},
            magicType : {
                show: false, 
                type: ['pie', 'funnel']
            },
            restore : {show: false},
            saveAsImage : {show: true}
        }
    },
    calculable : false,
    series : [
        {
            name:'',
            type:'pie',
            selectedMode: 'single',
            radius : [0, 35],
            
            // for funnel
            x: '20%',
            width: '40%',
            funnelAlign: 'right',
            max: 1548,
            
            itemStyle : {
                normal : {
                    label : {
                        position : 'inner'
                    },
                    labelLine : {
                        show : false
                    }
                }
            },
            data:content1
        },
        {
            name:'',
            type:'pie',
            radius : [50, 70],
            
            // for funnel
            x: '60%',
            width: '35%',
            funnelAlign: 'left',
            max: 1048,
            
            data:content2
        }
    ]
}
    myChart.setOption(option);                    
}
function draw_group_kind(data){
	var g_text = data['character']['character_text'];
	var g_sen = data['character']['character_sentiment'];
	var content1 = [];
	var content2 = [];
	var nod = {};
	var all_text = 0;
	var all_sen = 0;
	for(var key in g_text){
		all_text += g_text[key];
	}
	for(var key in g_text){
		var nod = {};
		nod['name'] = key;
		nod['value'] = (g_text[key]/all_text).toFixed(2);
		content1.push(nod);
	}
	for(var key in g_sen){
		all_sen += g_sen[key];
	}
	for(var key in g_sen){
		var nod = {};
		nod['name'] = key;
		nod['value'] = (g_sen[key]/all_text).toFixed(2);
		content2.push(nod);
	}
	var myChart1 = echarts.init(document.getElementById('group_kind')); 
    var option = {
    title : {
        text: '语言特征                                   情绪特征',
        textStyle:{fontSize:14},
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: false},
            dataView : {show: false, readOnly: false},
            magicType : {
                show: false, 
                type: ['pie', 'funnel']
            },
            restore : {show: false},
            saveAsImage : {show: true}
        }
    },
    calculable : false,
    series : [
        {
            name:'',
            type:'pie',
            itemStyle:{
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                         '#FFB980','#87CEFA','#B6A2DE','#FFB980','#F3A43B','#B6A2DE','#9BCA63','#FE8463'
                        ];
                        return colorList[params.dataIndex]
                    } 
                }
            },
            selectedMode: 'single',
            radius : [0, 60],
            center:['25%','50%'],
            // for funnel
            x: '20%',
            width: '40%',
            funnelAlign: 'right',
            max: 1548,
            
            data:content1
        },
        {
            name:'',
            type:'pie',
            itemStyle:{
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                         '#FFB980','#87CEFA','#B6A2DE','#FFB980','#F3A43B','#B6A2DE','#9BCA63','#FE8463'
                        ];
                        return colorList[params.dataIndex]
                    } 
                }
            },
            radius : [0, 60],
            center:['70%','50%'],
            // for funnel
            x: '60%',
            width: '35%',
            funnelAlign: 'left',
            max: 1048,
            
            data:content2
        }
    ]
}
	myChart1.setOption(option);    
}
function group_draw_content(data){
	//console.log('asdfadf');
    var html_c = '';
    $('#group_weibo_text_1').empty();
    //$('#group_select_time').empty();
    if(data==''){
        html_c += "<div style='width:100%;'><span style='margin-left:20px;'>该时段群组用户未发布任何微博</span></div>";
    }else{
        for(i=0;i<data.length;i++){
            html_c += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i]['text']+"</span></div>";
        }
    }
    $('#group_weibo_text_1').append(html_c);
}
function group_emotions(data){
    var times = [];
    var time_name = [];
    times = data['sentiment_trend']['time_list'];
    time_name = data['sentiment_trend']['time_list'];
    //console.log(times);
    var names = ['中性','积极','消极']; 
    var data0 = data['sentiment_trend']['0'];
    var data1 = data['sentiment_trend']['1'];
    var data2 = data['sentiment_trend']['2'];
    var datas = [data0,data1,data2];
    var nods = {};
    var nodcontent = [];
    for(i=0;i<3;i++){
        nods = {};
        nods['name'] = names[i];
        nods['type'] = 'line';
        nods['data'] = datas[i];
        nodcontent.push(nods);
    }
    //console.log(nodcontent[0]);

    var myChart1 = echarts.init(document.getElementById('group_emotion'));
    var option = {
    tooltip : {
        trigger: 'axis'
    },
    grid:{
        width:'80%'
    },
    legend: {
        data:names
    },
    toolbox: {
        show : false,
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
            data : times
        }
    ],
    yAxis : [
        {
            type : 'value',
        }
    ],
    series : nodcontent
    };
    myChart1.setOption(option); 
    require([
            'echarts'
        ],
        function(ec){
            var ecConfig = require('echarts/config');
            function focus(param) {
                var sentiment = param.seriesIndex;
                var date = new Date(time_name[param.dataIndex]);
                var starts_ts = date.getTime().toString().substr(0,10);
                var start_ts = parseInt(starts_ts)-28800;    
                //console.log(start_ts);             
                var ajax_url = '/group/group_sentiment_weibo/?task_name='+name+'&sentiment='+sentiment+'&start_ts='+start_ts;
                // ajax_url = '/attribute/sentiment_weibo/?uid='+uid+'&start_ts='+start_ts+'&time_type='+index+'&sentiment='+sentiment;
                $.ajax({
                      url: ajax_url,
                      type: 'GET',
                      dataType: 'json',
                      async: false,
                      success:group_draw_content
                    });
                var html0 = '';
                $('#group_select_time').empty();  
                html0 += "<div style='float:left'>当前选择时间段：</div><div style='color:brown;'>"+time_name[param.dataIndex]+"</div><br><div style='float:left'>当前选择情绪：</div><div style='color:brown;'>"+names[sentiment]+'</div>';
                $('#group_select_time').append(html0);
                }
            myChart1.on(ecConfig.EVENT.CLICK, focus);
            }
            
    )
}

function Draw_group_trend(data){
    var items = data;
    if(items==null){
        var say = document.getElementById('group_emotion');
        say.innerHTML = '该用户暂无此数据';
    }else{
        group_emotions(items);
        var time_init = new Date(items['sentiment_trend']['time_list'][0]);
        var times_init = time_init.getTime().toString().substr(0,10);
        var html0 = '';
        var url_content = '/group/group_sentiment_weibo/?task_name='+name+'&sentiment=0&start_ts='+times_init;
        g_psy.call_sync_ajax_request(url_content,g_psy.ajax_method,group_draw_content);
        $('#group_select_time').empty();  
        html0 += "<div style='float:left'>当前选择日期：</div><div style='color:brown;'>"+items['sentiment_trend']['time_list'][0]+"</div><br><div style='float:left' >当前选择情绪：</div><div style='color:brown;'>中性</div>";
        $('#group_select_time').append(html0);
    }   
}

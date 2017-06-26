function Thought(){
}
Thought.prototype = {   //获取数据，重新画表
    Draw_emotion:function(data){
        var items = data;
        if(items==null){
            var say = document.getElementById('emotion');
            say.innerHTML = '该用户暂无此数据';
        }else{
            // var con0 = document.getElementById('con_emotion0');
            // con0.innerHTML = items['description'][0];
            // var con = document.getElementById('con_emotion');
            // con.innerHTML = items['description'][1];
            emotions(items);
            var time_init = new Date(items['time_list'][0]);
            var times_init = time_init.getTime().toString().substr(0,10);
            //console .log(times_init);    
            var html0 = '';
            //console.log(url_content);
            $('#select_time').empty();  
            html0 += "<div>当前选择时间段：</div><div style='color:brown;'>"+items['time_list'][0]+"</div><br><div>当前选择情绪：</div><div style='color:brown;'>中性</div>";
            $('#select_time').append(html0);
            var index = $('input[name="time-type"]:checked').val();
            var url_content = '/attribute/sentiment_weibo/?uid='+uid+'&start_ts='+times_init+'&time_type='+index+'&sentiment=0';
            person_call_ajax_request(url_content,th_draw_content);
        }   
    }
}
function choose_time(){            
    var index = $('input[name="time-type"]:checked').val();
    var url = '/attribute/sentiment_trend/?uid='+uid+'&time_type='+index;
    person_call_ajax_request(url, Thought.Draw_emotion);
    //$('#emotion').empty();
  }
function th_draw_content(data){
    var html = '';
    $('#thought_weibo_text').empty();
    //console.log(data);
   // console.log(data.length);
    if(data.length==0){
        html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
    }else{
        for(i=0;i<data.length;i++){
            //console.log(data[i].text);
            html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i]['text']+"</span></div>";
        }
    }
    $('#thought_weibo_text').append(html);
}
function emotions(data){
    var times = [];
    var time_name = [];
    var index = $('input[name="time-type"]:checked').val();
    if (index =='week'){
        times = data['time_list'];
    }
    else{
        for (var t in data['time_list']){
            //console.log(data['time_list'][t]);
            times.push(data['time_list'][t].substr(11,5));
        }
    }
    time_name = data['time_list'];
    //console.log(times);
    var names = ['中性','积极','消极']; 
    var data0 = data['trend_result']['0'];
    var data1 = data['trend_result']['1'];
    var data2 = data['trend_result']['2'];
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
    var myChart1 = echarts.init(document.getElementById('emotion'));
    var option = {
    tooltip : {
        trigger: 'axis'
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
                if(index == 'week'){
                var start_ts = parseInt(starts_ts)-28800;                   
                }
                else if(index == 'day'){var start_ts = starts_ts;}
                ajax_url = '/attribute/sentiment_weibo/?uid='+uid+'&start_ts='+start_ts+'&time_type='+index+'&sentiment='+sentiment;
                $.ajax({
                      url: ajax_url,
                      type: 'GET',
                      dataType: 'json',
                      async: false,
                      success:th_draw_content
                    });
                var html0 = '';
                $('#select_time').empty();  
                html0 += "<div>当前选择时间段：</div><div style='color:brown;'>"+time_name[param.dataIndex]+"</div><br><div>当前选择情绪：</div><div style='color:brown;'>"+names[sentiment]+'</div>';
                $('#select_time').append(html0);
                }
            myChart1.on(ecConfig.EVENT.CLICK, focus);
            }
            
    )
}
function draw_character(data){
    //console.log(data);
    var sentiment_dict = ['冲动', '抑郁', '未知'];
    var text_dict = ['批判', '未知'];
    var character_sent = data['character_sentiment'];
    var character_text = data['character_text'];
    var html = '';
    html += '<div>根据情绪特征划分为：</div>';
    for (var i = 0; i < sentiment_dict.length; i++){
        var key = sentiment_dict[i]
        if (key == character_sent){
            html += '<span class="group_block">' + key + '</span>';
        }
        else{
            html += '<span style="background-color:gray;" class="group_block">' + key + '</span>';
        }
    }
    $('#character_sent').html(html);
    var html = '';
    html += '<div>根据语言特征划分为：</div>';
    for (var i = 0; i < text_dict.length; i++){
        var key = text_dict[i];
        if (key == character_text){
            html += '<span class="group_block">' + key + '</span>';
        }
        else{
            html += '<span style="background-color:gray;" class="group_block">' + key + '</span>';
        }
    }
    $('#character_text').html(html);


    var pie_data = data['sentiment_pie'];
    var character_dict = {0:'中性', 1:'积极', 2:'生气', 3:'焦虑', 4:'悲伤', 5:'厌恶', 6:'消极其他'};
    var neg = 0;
    var first_content = [];
    var second_content = [];
    for (var i = 0;i < 7; i++){
        if (pie_data[i] && pie_data[i] != 0){
            //console.log(i,pie_data[i]);
            var nod = {};
            nod['name'] = character_dict[i];
            nod['value'] = pie_data[i];
            second_content.push(nod);
            if ((i == 0 ) || (i == 1)){
                //console.log(2,nod);
                first_content.push(nod);
            }
            else{
                neg += pie_data[i];
                //console.log(neg);
            }
        }
    }
    var nod = {};
    //console.log(neg);
    nod['name'] = '消极';
    nod['value'] = neg;
    if (neg != 0){
        first_content.push(nod);    
    }
    var myChart = echarts.init(document.getElementById('pie_emotion'));
    var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true, 
                type: ['pie', 'funnel']
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : false,
    series : [
        {
            name:'心理状态',
            type:'pie',
            selectedMode: 'single',
            radius : [0, 50],
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
            data:first_content
        },
        {
            name:'心理状态',
            type:'pie',
            radius : [70, 110],
            // for funnel
            x: '60%',
            width: '35%',
            funnelAlign: 'left',
            max: 1048,
            data:second_content
        }
    ]
    };
    myChart.setOption(option);
}
function thought_load(){
    var url = '/attribute/sentiment_trend/?uid='+uid+'&time_type='+index;
    person_call_ajax_request(url, Thought.Draw_emotion);
    var url_character = '/attribute/character_psy/?uid='+uid;
    person_call_ajax_request(url_character,draw_character);
}
var Thought = new Thought();
var index = $('input[name="time-type"]:checked').val();

 function Field_topic(){
  this.ajax_method = 'GET';
}
Field_topic.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
    Draw_field_topic:function(data){
	console.log(data);	
    Draw_topic();
    Draw_field();
}
}

var Field_topic = new Field_topic();

$(document).ready(function(){
    var downloadurl = window.location.host;
    weibo_url =  'http://' + downloadurl + "/overview/show/?date=2013-09-07";
    Field_topic.call_sync_ajax_request(weibo_url, Field_topic.ajax_method, Field_topic.Draw_field_topic);
})

function Draw_topic(){
    var myChart = echarts.init(document.getElementById('topic')); 
        
    var option = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'话题',
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:435, name:'娱乐'},
                {value:310, name:'计算机'},
                {value:234, name:'经济'},
                {value:135, name:'自然'},
                {value:548, name:'健康'},
                {value:235, name:'教育'},
                {value:110, name:'军事'},
                {value:135, name:'政治'},
                {value:248, name:'体育'},
                {value:234, name:'交通'},
                {value:435, name:'民生'},
                {value:448, name:'生活'}
            ]
        }
    ]
};                    
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}

function Draw_field(){
    var myChart = echarts.init(document.getElementById('field')); 
        
    var option = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'领域',
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:235, name:'高校微博'},
                {value:110, name:'境内机构'},
                {value:134, name:'境外机构'},
                {value:335, name:'媒体'},
                {value:248, name:'律师'},
                {value:148, name:'草根'},
                {value:210, name:'民间组织'},
                {value:134, name:'政府机构人士'},
                {value:335, name:'媒体人士'},
                {value:248, name:'活跃人士'},
                {value:198, name:'其他'},
                {value:148, name:'商业人士'},
                {value:48, name:'境外媒体'}
            ]
        }
    ]
};
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}
ajax_method = 'GET';
function call_sync_ajax_request(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  }


// $(function() {
//     $( '#dl-menu' ).dlmenu();
//   });
$(".closeList").off("click").click(function(){
    $("#float-wrap").addClass("hidden");
    $("#more_topic").addClass("hidden");
    return false;
  });

$("#showmore_topic").off("click").click(function(){
    $("#float-wrap").removeClass("hidden");
    $("#more_topic").removeClass("hidden");
    return false;
  });



function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')'
        }
    };
}

function get_radar_data (data) {
  var topic = data;
  var topic_name = [];
  var topic_value = [];

  for(var i=0; i<topic[0].length;i++){
    if(topic[1][i].toFixed(3) != 0){
      topic_value.push(topic[1][i].toFixed(3)*10);
      topic_name.push(topic[0][i]);
    }
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
  if(topic_value.length <8){
    max_topic = topic_value.length;
  }
  //Math.min.apply(7, topic_value.length);
  for(var i=0;i<max_topic;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name[i];
    name_dict["text"] = index;
    name_dict["max"] = Math.max.apply(Math, topic_value).toFixed(3)+0.2;
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value);
  return topic_result;
}

function Draw_topic0(data){
  if(data[0][1].toFixed(3) == 0){
      $('#user_topic').append('<h4 style="text-align:center;margin-top:50%;">暂无数据</h4>');
      $('#showmore_topic').css('display', 'none');      
  }else{
      var topic_sta = [];
      var topic_name_sta = [];
      for(var i=0;i<data.length;i++){
        if(data[i][1] != 0){
          topic_sta.push(data[i][1]/data[0][1]);
          topic_name_sta.push(data[i][0]);
        }
      };

      var topic = [];
      var html = '';
      $('#topic_WordList').empty();
      if(topic_sta.length == 0){
         //console.log(div_name);
          html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
          //$('#'+ more_div).append(html);
          $('#more_topic').append(html);
          $('#showmore_topic').empty();
      }else{
          html = '';
          html += '<table class="table table-striped table-bordered" style="width:450px;">';
          html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">用户领域分布</th><th style="text-align:center">概率</th></tr>';
          for (var i = 0; i < topic_sta.length; i++) {
             var s = i.toString();
             var m = i + 1;
             html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + topic_name_sta[i] +  '&psycho_status=&domain&topic" target="_blank">' + topic_name_sta[i] +  '</a></th><th style="text-align:center">' + topic_sta[i].toFixed(3) + '</th></tr>';
          };
          html += '</table>'; 
          $('#topic_WordList').append(html);
      };
      var topic_val = [];
      topic_val.push(topic_name_sta);
      topic_val.push(topic_sta);
      var topic_result = [];
      topic_result = get_radar_data(topic_val);
      var topic_name = topic_result[0];
      //console.log(topic_name);
      var topic_value = topic_result[1];
     // console.log(topic_value)
      var myChart2 = echarts.init(document.getElementById('user_topic'));
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
              res += params['0'][3]+' : '+(params['0'][2]/10).toFixed(3);
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

function show_domain0(data){

  // var html = '';
  //html += '<h3>用户领域分析</h3>';
  data1 = '根据注册信息分类：\n'+data[0][0];
  data2 = '根据转发结构分类：\n'+data[0][1];
  data3 = '根据发帖内容分类：\n'+data[0][2];
  data4 = data[1];
var myChart1 = echarts.init(document.getElementById('preference_domain')); 
var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{b}"
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
    calculable : false,

    series : [
        {
            name:'树图',
            type:'tree',
            orient: 'horizontal',  // vertical horizontal
            rootLocation: {x: 240, y: 'center'}, // 根节点位置  {x: 'center',y: 10}
            nodePadding: 50,
            symbol: 'circle',
            symbolSize: 30,
            itemStyle: {
                normal: {
                    color: '#FF7F50',
                    label: {
                        show: true,
                        position: 'right',
                        formatter: "{b}",
                        textStyle: {
                            color: '#000',
                            fontSize: 5
                        }
                    },
                    lineStyle: {
                        color: '#ccc',
                        width: 5,
                        type: 'curve' // 'curve'|'broken'|'solid'|'dotted'|'dashed'

                    }
                },
                emphasis: {
                    color: '#FF7F50',
                    label: {
                        show: false
                    },
                    borderWidth: 0
                }
            },
            
            data: [
                {name:data4 ,itemStyle:{normal:{label:{textStyle:{fontWeight:'bold',fontSize:14}}}},
		children:[{name:data1},{name:data2},{name:data3}]}
            ]
        }
    ]
};
   myChart1.setOption(option);               
}


function show_results0(data){
  //console.log(data.results.keywords);
  var topic = data.results.topic;
  var domain = data.results.domain;
  Draw_topic0(topic);
  //show_conclusion(conclusion);
  show_domain0(domain);
}

function preference_load(){
  var prefrence_url = '/attribute/preference/?uid=' + uid;
  //console.log(prefrence_url);
  call_sync_ajax_request(prefrence_url, ajax_method, show_results0);
}

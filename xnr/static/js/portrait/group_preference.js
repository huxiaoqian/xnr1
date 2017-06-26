
function Show_pref(url,div){
    that = this;
    this.ajax_method = 'GET';
    this.div = div;
}
Show_pref.prototype = {
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
    console.log(data);
    var keywords_data = data['keywords'];
    var keywords_name = 'Language';
    var keywords_more = 'key_WordList';
    var hashtag_data = data['hashtag'];
    var hashtag_name = 'hashtag_words';
    var hashtag_more = 'hashtag_WordList';
    var topic_data = data['topic'];
    var domain_data = data['domain'];
    Draw_keyword(keywords_data, keywords_name, keywords_more, showmore_keyWords);
    Draw_keyword(hashtag_data, hashtag_name, hashtag_more, showmore_hashtagWords);
    Draw_topic(topic_data,'preference_topic', 'topic_WordList');
    Draw_topic(domain_data,'preference_domain', 'domain_WordList');
  }
}

function show_conclusion(data){
  var html = '';
  html += '<span class="fleft" style="margin-right:10px;width:32px;height:32px;background-image:url(/static/img/warning.png);margin-top:5px;display:black;"></span>';
  //html += '<h4>'+data[0]+'<span style="color:red;">'+data[1]+'</span>，'+data[2]+'<span style="color:red;">'+data[3]+'</span>。</h4>';
  html += data;
  $("#preference_conclusion").append(html);
}

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
function Draw_keyword(data, div_name, more_div, hide_more){
  var keyword = [];
  var html = '';
  $('#'+ more_div).empty();
  if(data.length == 0){
     //console.log(div_name);
      html = '<h4 style="text-align:center;margin-top:50%;">暂无数据</h4>';
      //$('#'+ more_div).append(html);
      $('#'+ div_name).append(html);
      $('#'+ hide_more).empty();
  }else{
   
      html = '';
      html += '<table class="table table-striped table-bordered" style="width:450px;">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">频数</th></tr>';
      for (var i = 0; i < data.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data[i][0] +  '&psycho_status=&domain&topic" target="_blank">' + data[i][0] +  '</a></th><th style="text-align:center">' + data[i][1] + '</th></tr>';
      };
      html += '</table>'; 
      $('#'+ more_div).append(html);

     //最大是50
    var key_value = [];
    var key_name = [];
    for(var i=0;i<data.length;i++){
      key_value.push(data[i][1]+Math.random());
      key_name.push(data[i][0]);
    };

    var word_num = Math.min(20, data.length);
    var key_value2 = [];
    var key_name2 = [];
    for(var i=0; i<word_num; i++){ //最多取前50个最大值
      a=key_value.indexOf(Math.max.apply(Math, key_value));
      key_value2.push(key_value[a]);
      key_name2.push(key_name[a]);
      key_value[a]=0;
    }      
    //console.log(key_value);
    for (i=0;i<word_num;i++){
      var word = {};

      word['name'] = key_name2[i];
      word['value'] =key_value2[i]*100;
      //console.log(word['value']);
      word['itemStyle'] = createRandomItemStyle();
      keyword.push(word);
    }

    var myChart = echarts.init(document.getElementById(div_name)); 
    var option = {
      tooltip: {
          show: true,
          formatter:  function (params){
            var res  = '';
            var value_after = parseInt(params.value/100);
            res += params.name+' : '+value_after;
            return res;
          }
      },
      series: [{
          type: 'wordCloud',
          size: ['100%', '100%'],
          textRotation : [0, 45, 90, -45],
          textPadding: 0,
          autoSize: {
              enable: true,
              minSize: 14
          },
          data: keyword
      }]
    };
        myChart.setOption(option);  
  }
}

function get_radar_data_pre (data) {
  var topic = data;
  var topic_name = [];
  var topic_value = [];
  for(var i=0; i<topic[0].length;i++){
    topic_value.push(topic[1][i].toFixed(2)*10)
    topic_name.push(topic[0][i]);
  };
  //console.log(topic_name);
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
    name_dict["max"] = Math.max.apply(Math, topic_value).toFixed(3);
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value);
  return topic_result;
}
function Draw_topic(data, radar_div, motal_div){
  //console.log(data);
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
          //$('#'+ show_more).empty();
      }else{
          html = '';
          html += '<table class="table table-striped table-bordered" style="width:450px;">';
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
      //console.log(topic_val);
      topic_result = get_radar_data_pre(topic_val);
      //console.log(topic_result);
      var topic_name = topic_result[0];
      //console.log(topic_name);
      var topic_value_final = topic_result[1];
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
         value : topic_value_final,
         //name : '用户话题分布'
       }
       ]
      }]
  };
  myChart2.setOption(option);
  }
}

function show_results(data){
  show_conclusion(conclusion);
}
function preference_load(){
    if (!global_preference_flag){
        var prefrence_url = '/group/show_group_result/?task_name='+ name +'&module=preference&submit_user=admin';
        Show_pref.call_sync_ajax_request(prefrence_url, Show_pref.ajax_method, Show_pref.Draw_table);
        global_preference_flag = true;
    }
}
var Show_pref = new Show_pref();
var global_preference_flag = false;


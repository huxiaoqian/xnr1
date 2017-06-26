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
    $("#more_keyWords").addClass("hidden");
    $("#more_hashtagWords").addClass("hidden");
    $("#more_senWords").addClass("hidden");
    $("#more_topic").addClass("hidden");
    return false;
  });
$("#showmore_keyWords").off("click").click(function(){
    $("#float-wrap").removeClass("hidden");
    $("#more_keyWords").removeClass("hidden");
    return false;
  });
$("#showmore_topic").off("click").click(function(){
    $("#float-wrap").removeClass("hidden");
    $("#more_topic").removeClass("hidden");
    return false;
  });

$("#showmore_hashtagWords").off("click").click(function(){
        $("#float-wrap").removeClass("hidden");
        $("#more_hashtagWords").removeClass("hidden");
        return false;
    });
$("#showsen_keyWords").off("click").click(function(){
        $("#float-wrap").removeClass("hidden");
        $("#more_senWords").removeClass("hidden");
        return false;
    });

function show_conclusion(data){
  var html = '';
  html += '<span class="fleft" style="margin-right:10px;width:32px;height:32px;background-image:url(/static/img/warning.png);margin-top:5px;display:black;"></span>';
  html += '<h4>'+data[0]+'<span style="color:red;">'+data[1]+'</span>，'+data[2]+'<span style="color:red;">'+data[3]+'</span>。</h4>';
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
function Draw_keyword(data, div_name, more_div, more,title){
	var keyword = [];
  var html = '';
	$('#'+ more_div).empty();
  if(data.length == 0||data[0]==undefined){
     //console.log(div_name);
      html = '<h4 style="text-align:center;margin-top:50%;">暂无数据</h4>';
      //$('#'+ more_div).append(html);
      $('#'+ div_name).append(html);
      $('#'+ more).empty();
  }else{
   
      html = '';
      html += '<table class="table table-striped table-bordered" style="width:450px;">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">'+title+'</th><th style="text-align:center">频数</th></tr>';
      for (var i = 0; i < data.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data[i][0] +  '&psycho_status=&domain&topic" target="_blank">' + data[i][0] +  '</a></th><th style="text-align:center">' + data[i][1] + '</th></tr>';
      };
      html += '</table>'; 
      $('#'+ more_div).append(html);

    var key_value = [];
    var key_name = [];
    for(var i=0;i<data.length;i++){
      key_value.push(data[i][1]+Math.random());
      key_name.push(data[i][0]);
    };

    var word_num = Math.min(50, data.length);
    var key_value2 = [];
    var key_name2 = [];
    for(var i=0; i<word_num; i++){ //最多取前50个最大值
      a=key_value.indexOf(Math.max.apply(Math, key_value));
      key_value2.push(key_value[a]);
      key_name2.push(key_name[a]);
      key_value[a]=0;
    }
    
  	for (var i=0;i<word_num;i++){
  		var word = {};
  		word['name'] = key_name2[i];
  		word['value'] = key_value2[i]*100;
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


function show_results(data){
  //console.log(data.results.keywords);
  var keywordsCloud = data.results.keywords;
  //console.log(keywordsCloud);
  var hashtag = data.results.hashtag;
  var topic = data.results.topic;
  var senword = data.results.hashtag;
  var conclusion = data.description;
  var domain = data.results.domain;
  var keywords_name = 'Language';
  var hashtag_name = 'hashtag_words';
  var keywords_more = 'key_WordList';
  var hashtag_more = 'hashtag_WordList';
  var key_more = 'key_more';
  var hash_more = 'hash_more';
  var sen_name = 'sen_Language';
  var senwords_more = 'sen_WordList';
  var sen_more = 'sen_more';

  Draw_keyword(keywordsCloud, keywords_name, keywords_more, key_more,'关键词');
  Draw_keyword(hashtag, hashtag_name, hashtag_more, hash_more,'微话题');
  //show_conclusion(conclusion);

  var tag_vector = data.tag_vector;
  //console.log(tag_vector);
  for(var i=0; i<tag_vector.length;i++){
    if(tag_vector[i][1] == ''){
      tag_vector[i][1] = '暂无数据'
    }
    global_tag_vector.push(tag_vector[i]);
  }
  }
// function show_results0(data){
//   //console.log(data.results.keywords);
//   var topic = data.results.topic;
//   var domain = data.results.domain;
//   Draw_topic0(topic);
//   //show_conclusion(conclusion);
//   show_domain0(domain);
// }
function show_results1(data){
  //console.log(data.results.keywords);
  var senword = data;
  var sen_name = 'sen_Language';
  var senwords_more = 'sen_WordList';
  var sen_more = 'sen_more';
  Draw_keyword(senword, sen_name, senwords_more, sen_more,'敏感词');
  //show_conclusion(conclusion);
  }

function language_load(){
  var prefrence_url = '/attribute/preference/?uid=' + uid;
  var sen_url = '/attribute/new_sensitive_words/?uid=' +uid;
  //console.log(prefrence_url);
  call_sync_ajax_request(prefrence_url, ajax_method, show_results);
  // call_sync_ajax_request(prefrence_url, ajax_method, show_results0);
  call_sync_ajax_request(sen_url, ajax_method, show_results1);  
}

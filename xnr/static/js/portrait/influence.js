function Influence(){
  this.ajax_method = 'GET';
}
function getDate_in(tm){
    var tt = new Date(parseInt(tm)*1000).format("MM-dd");
    return tt;
}
Influence.prototype = {   //获取数据，重新画表
  call_async_ajax_request:function(url, method, callback){
      person_call_ajax_request(url, callback);
  },
  call_ajax_request:function(url, method, callback){
      $.ajax({
          url:url,
          type:"GET",
          dataType:'json',
          async:false,
          success:callback,
      });
  },
  Draw_influence:function(data){
    //console.log(data);
  var item_x = [];
  for (var t=0;t<data.timeline.length;t++){
    item_x.push(getDate_in(data.timeline[t]));
  }
  //var item_y = data.influence;
	var item_y = data.evaluate_index;
  // var conclusion = data.description;
if(data.evaluate_index){
	var dataFixed = [];
	for(i=0;i<item_y.length;i++){
		dataFixed.push(parseFloat(item_y[i].toFixed(2)));
	}
    var myChart = echarts.init(document.getElementById('influence_chart')); 
    var option = {

      tooltip : {
          trigger: 'axis'
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
      calculable : false,
      xAxis : [
          {
              type : 'category',
              boundaryGap : true,
              data : item_x
          }
      ],
      yAxis : [
          {
              type : 'value',
              axisLabel : {
                  formatter: '{value} '
              }
          }
      ],
      series : [
          {
              type:'line',
              data:dataFixed,
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
          }
          
      ]
    };
        // 为echarts对象加载数据 
        myChart.setOption(option); 
  }
else{
  $('#influence_chart').append('<h4 style="text-align:center;margin-top:50%;">暂无数据</h4>')
}
},

 Draw_get_top_weibo1:function(data){
  var div_name = 'influence_weibo1';
  Draw_get_top_weibo(data, div_name);
},
 Draw_get_top_weibo2:function(data){
  var div_name = 'influence_weibo2';
  Draw_get_top_weibo(data, div_name);

},
 Draw_get_top_weibo3:function(data){
  var div_name = 'influence_weibo3';
  Draw_get_top_weibo(data, div_name);
},
 Draw_get_top_weibo4:function(data){
  var div_name = 'influence_weibo4';
  Draw_get_top_weibo(data, div_name);
},
Draw_pie_all0:function(data){
  //console.log(data);
  a=$('#sum_yc_zf').text();
  b=$('#sum_zf_zf').text();
  total = parseInt(a)+parseInt(b);
    $('#all_re_conclusion').empty();
    var html = '';
    html += '该类用户共有<span style="color:red">'+data.total_number+'</span>人，';
    html += '平均影响力为<span style="color:red">'+data.influence.toFixed(2)+'</span>';
    $('#all_re_conclusion').append(html);
    var div_name = ['re_user_domain_all','re_user_topic_all','re_user_geo_all'];
    Draw_pie(data.domian, div_name[0]);
    Draw_pie(data.geo, div_name[2]);
    Draw_pie(data.topic, div_name[1]);
    var data_set = [];
    data_set.push(data.in_portrait);
    data_set.push(data.out_portrait);
    data_set.push(data.in_portrait_number);
    data_set.push(data.out_portrait_number);
    Influence_motal(data_set, 're_user_in_all', 're_user_out_all', 're_three_pie_all', 're_user_content_all')

    
  },
  Draw_pie_all1:function(data){
  a=$('#sum_yc_pl').text();
  b=$('#sum_zf_pl').text();
  total = parseInt(a)+parseInt(b);
    var div_name = ['cmt_user_domain_all','cmt_user_topic_all','cmt_user_geo_all'];
    $('#all_cmt_conclusion').empty();
    var html = '';
    html += '该类用户共有<span style="color:red">'+data.total_number+'</span>人，';
    html += '平均影响力为<span style="color:red">'+data.influence.toFixed(2)+'</span>';
    $('#all_cmt_conclusion').append(html);
    Draw_pie(data.domian, div_name[0]);
    Draw_pie(data.topic, div_name[1]);
    Draw_pie(data.geo, div_name[2]);
    var data_set = [];
    data_set.push(data.in_portrait);
    data_set.push(data.out_portrait);
    data_set.push(data.in_portrait_number);
    data_set.push(data.out_portrait_number);
    Influence_motal(data_set, 'cmt_user_in_all', 'cmt_user_out_all', 'cmt_three_pie_all', 'cmt_user_content_all')
  },

  Draw_basic_influence:function(data){
    //console.log(data);
    $('#influence_conclusion_c').empty();
    var html='';
    if(data[0][0] != ''){
      html += '该用户<span style="color:red">'+data[0][0]+'</span>。';
    }
    var conclu_s1 = [];
    // conclu_s.push()
    if(data[0][1] != ''){
      conclu_s1.push(data[0][1]);
      //html += data[0][1]+'，'+data[0][2]+'，';
      //html += '<span >'+data[0][1]+'，</span>';
    }
    if(data[0][2] != ''){
      conclu_s1.push(data[0][2]);
      //html += data[0][1]+'，'+data[0][2]+'，';
      //html += '<span>'+data[0][2]+'，</span>';
    }
    if(data[1][0] != ''){
      var data1_0 = '属于<span style="color:red">'+data[1][0]+'</span>';
      conclu_s1.push(data1_0);
      //html += '属于<span style="color:red">'+data[1][0]+'。</span>';
    }
    var conclu_s2 = [];
    if(data[0][3]!= ''){
      conclu_s2.push(data[0][3]);
      //html += '<span>'+data[0][3]+'，</span>';
    }
    if(data[0][4] != ''){
      conclu_s2.push(data[0][4]);
      //html += '<span>'+data[0][4]+'，</span>';
    }
    if(data[1][1] != ''){
      var data1_1 = '属于<span style="color:red">'+data[1][1]+'</span>';
      conclu_s2.push(data1_1);
      //html += '属于<span style="color:red">'+data[1][1]+'。</span>';
    }
    var conclu_s3 = [];
    if(data[0][5]!= ''){
      conclu_s3.push(data[0][5]);
      //html += '<span>'+data[0][5]+'，</span>';
    }
    if(data[0][6]!= ''){
      conclu_s3.push(data[0][6]);
      //html += '<span>'+data[0][6]+'，</span>';
    }
    if(data[1][2] != ''){
      var data1_2 = '<span style="color:red">'+data[1][2]+'</span>';
      conclu_s3.push(data1_2);
      //html += '属于<span style="color:red">'+data[1][2]+'。</span>';
    }
    var conclu_s4 = [];
    if(data[0][7]!= ''){
      conclu_s4.push(data[0][7]);
      //html += '<span>'+data[0][7]+'，</span>';
    }
    if(data[0][8]!= ''){
      conclu_s4.push(data[0][8]);
      //html += '<span>'+data[0][8]+'，</span>';
    }
    if(data[1][3] != ''){
      var data1_3 = '属于<span style="color:red">'+data[1][2]+'</span>';
      conclu_s4.push(data1_3);
      //html += '属于<span style="color:red">'+data[1][3]+'。</span>';
    }
    if (conclu_s1.length != 0){
      html+= conclu_s1.join('，')+'。';
    };
    if (conclu_s2.length != 0){
      html+= conclu_s2.join('，')+'。';
    };
    if (conclu_s3.length != 0){
      html+= conclu_s3.join('，')+'。';
    };
    if (conclu_s4.length != 0){
      //console.log(conclu_s4);
      html+= conclu_s4.join('，')+'。';
    };
    $('#influence_conclusion_c').append(html);  
  },
  
  Draw_user_influence_detail:function(data){
    $('#influence_table').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="font-size:14px;">';
    html += '<tr><th rowspan="2" style="text-align:center;vertical-align:middle;">&nbsp;类别</th>';
    html += '<th colspan="4" style="text-align:center;">转发情况<u id="retweet_distribution" style="font-size:12px;color:#555555;margin-left:20px;cursor: pointer">查看详情</u></th>';
    html += '<th colspan="4" style="text-align:center;">评论情况<u id="comment_distribution" style="font-size:12px;color:#555555;margin-left:20px;cursor: pointer">查看详情</u></th></tr>';
    html += '<tr><th style="text-align:center">总数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="所有发布微博被转发的总次数"></i></th>';
    html += '<th style="text-align:center">平均数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="平均每条发布微博被转发的平均数"></i></th>';
    html += '<th style="text-align:center">最高数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="单条发布微博被转发的最高次数"></i></th>';
    html += '<th style="text-align:center">爆发数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="所有微博在15分钟被转发的总次数"></i></th>';
    html += '<th style="text-align:center">总数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="所有发布微博被评论的总次数"></i></th>';
    html += '<th style="text-align:center">平均数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="平均每条发布微博被评论的平均数"></i></th>';
    html += '<th style="text-align:center">最高数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="单条发布微博被评论的最高次数"></i></th>';
    html += '<th style="text-align:center">爆发数<i class="glyphicon glyphicon-question-sign" data-toggle="tootlip" data-placement="right" title="所有微博在15分钟被评论的总次数"></i></th>';
    html += '</tr>';
    html += '<tr><th style="text-align:center">原创微博 ('+data['origin_weibo_number']+')</th>';
    html += '<th style="text-align:center" id="sum_yc_zf">'+data['origin_weibo_retweeted_total_number']+'</th>';
    html += '<th style="text-align:center" >'+data['origin_weibo_retweeted_average_number'].toFixed(0)+'</th>';
    html += '<th style="text-align:center">'+data['origin_weibo_retweeted_top_number']+'</th>';
    html += '<th style="text-align:center">'+data['origin_weibo_retweeted_brust_average'].toFixed(0)+'</th>';
    html += '<th style="text-align:center" id="sum_yc_pl">'+data['origin_weibo_comment_total_number']+'</th>';
    html += '<th style="text-align:center">'+data['origin_weibo_comment_average_number'].toFixed(0)+'</th>';
    html += '<th style="text-align:center">'+data['origin_weibo_comment_top_number']+'</th>';
    html += '<th style="text-align:center">'+data['origin_weibo_comment_brust_average'].toFixed(0)+'</th>';
    html += '</tr>';
    html += '<tr><th style="text-align:center">转发微博 ('+data['retweeted_weibo_number']+')</th>';
    html += '<th style="text-align:center" id="sum_zf_zf">'+data['retweeted_weibo_retweeted_total_number']+'</th>';
    html += '<th style="text-align:center">'+data['retweeted_weibo_retweeted_average_number'].toFixed(0)+'</th>';
    html += '<th style="text-align:center">'+data['retweeted_weibo_retweeted_top_number']+'</th>';
    html += '<th style="text-align:center">'+data['retweeted_weibo_retweeted_brust_average'].toFixed(0)+'</th>';
    html += '<th style="text-align:center" id="sum_zf_pl">'+data['retweeted_weibo_comment_total_number']+'</th>';
    html += '<th style="text-align:center">'+data['retweeted_weibo_comment_average_number'].toFixed(0)+'</th>';
    html += '<th style="text-align:center">'+data['retweeted_weibo_comment_top_number']+'</th>';
    html += '<th style="text-align:center">'+data['retweeted_weibo_comment_brust_average'].toFixed(0)+'</th>';
    html += '</tr>';
    html += '</table>';
    $('#influence_table').append(html);

    $('#influence_index').html(data['order_count']);
    var total_count;
    if (data['total_count'] > 10000){
        total_count = Math.floor(data['total_count'] / 10000) + '万';
    }
    else{
        total_count = data['total_count'];
    }
    $('#influence_total').html(total_count);
  },

  Influence_tag_vector:function(data){
    var tag_vector = []
    tag_vector.push('影响力类型');
    if (data == ''){
        tag_vector.push('暂无数据');
    }
    else{
        tag_vector.push(data);
    }
    global_tag_vector.push(tag_vector); 
  },

  Single_users_influence_re:function(data){
    var data_user_detail = [];
    data_user_detail.push(data.influence_users[0]);
    data_user_detail.push(data.influence_users[1]);
    data_user_detail.push(data.influence_distribution.in_portrait_number);
    data_user_detail.push(data.influence_distribution.out_portrait_number);

    Influence_motal(data_user_detail, 're_user_in', 're_user_out', 're_three_pie', 're_user_content');
    $('#re_conclusion').empty();
    var html = '该类用户的平均影响力为'+data.influence_distribution.influence;
    $('#re_conclusion').append(html);
    Draw_pie(data.influence_distribution.topic, 're_user_topic');
    Draw_pie(data.influence_distribution.domian, 're_user_domain');
    Draw_pie(data.influence_distribution.geo, 're_user_geo');
  },

  Draw_conclusion:function(data){
    $('#influence_conclusion_all').empty();
    var html = '';
    html += '该用户<span style="color:red">'+ data[0] +'</span>。';
    if(data[1][0]!= ''){
      html += '属于<span style="color:red">'+ data[1][0] +'</span>，';
    };
    if(data[1][1]!= ''){
      html +='<span style="color:red">'+ data[1][1] +'</span>，';
    };
    if(data[1][2]!= ''){
      html +='是<span style="color:red">'+ data[1][2] +'</span>，';
    };
    if(data[1][3]!= ''){
      html +='<span style="color:red">'+ data[1][3] +'</span>，';
    };
    if(data[2] != ''){
      html+= '所影响的领域为';
      var domain_len = data[2].length
      for(var i = 0; i<domain_len-1;i++){
       html += '<span style="color:red">'+ data[2][i]+'</span>、';
       }
      html +='<span style="color:red">'+ data[2][domain_len-1] +'</span>。';
    }
    if(data[3] != ''){
      html+= '影响的话题有';
      var topic_len = data[3].length
      for(var i = 0; i<topic_len-1;i++){
        html += '<span style="color:red">'+ data[3][i]+'</span>、';
      }
       html +='<span style="color:red">'+ data[3][topic_len-1] +'</span>。';
    }
    $('#influence_conclusion_all').append(html);
  },

  Single_users_influence_cmt:function(data){
    var data_user_detail = [];
    data_user_detail.push(data.influence_users[0]);
    data_user_detail.push(data.influence_users[1]);
    data_user_detail.push(data.influence_distribution.in_portrait_number);
    data_user_detail.push(data.influence_distribution.out_portrait_number);
    Influence_motal(data_user_detail, 'cmt_user_in','cmt_user_out', 'cmt_three_pie', 'cmt_user_content');
    $('#cmt_conclusion').empty();
    var html = '该类用户的平均影响力为'+data.influence_distribution.influence;
    $('#cmt_conclusion').append(html);
    Draw_pie(data.influence_distribution.topic, 'cmt_user_topic');
    Draw_pie(data.influence_distribution.domian, 'cmt_user_domain');
    Draw_pie(data.influence_distribution.geo, 'cmt_user_geo');  
  }
}

  function Influence_motal(data, div_name_in, div_name_out, del_div, del_div_attr){         
    $('#'+div_name_in).empty();

    var html = '';
    //console.log(data);
    //html += '<hr style="margin-top:-10px;">';
    html += '<h4>已入库用户('+data[2]+')</h4><p style="text-align:left;padding: 0px 10px;width:800px;">';
    if (data[2] == 0){
      //$('#'+del_div).append('<h4>test</h4>');
      $('#'+del_div).css('display', 'none');
      //$('#'+del_div).remove();
      $('#'+del_div_attr).css("height", "auto");
      $('#'+del_div_attr).css("overflow-y", "auto");
    }else{
      $('#'+del_div).css('display', 'block');
      for (i=0;i<data[0].length;i++){
       var img_src = ''
       if (data[0][i][0] == 'unknown'){
       img_src = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
       }else{
        img_src = data[0][i][0];
       };
       var user_name = '';
       if (data[0][i][1] == 'unknown'){
        user_name = '未知('+data[0][i][2]+')';
       }else{
         user_name = data[0][i][1];
       }
        var user_id = data[0][i][2];
      html += '<span><a target="_blank" href="/index/personal/?uid=' + user_id +'" title="' + user_name +'">';
      html += '<img class="small-photo shadow-5" style="margin:10px 0px 0px 25px;" src="' + img_src + '" title="' + user_name +'">';
      html += '</a></span>';
      }
    }

    html += '</p>';
    $('#'+div_name_in).append(html);

    $('#'+div_name_out).empty();
    var html2 = '';
    html2 += '<hr><h4 style="margin-left:10px;">未入库用户('+data[3]+')</h4><p style="text-align:left;padding: 0px 10px;width:800px;">';
    if (data[3] == 0){
    }else{
      for (i=0;i<data[1].length;i++){
        var img_src = ''
        if (data[1][i][0] == 'unknown'){
          img_src = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        }else{
          img_src = data[1][i][0];
        };
        var user_name = '';
        if (data[1][i][1] == 'unknown'){
          user_name = '未知('+data[1][i][2]+')';
        }else{
          user_name = data[1][i][1];
        }
        var user_id_out = data[1][i][2];
        html2 += '<span><a target="_blank" href="http://weibo.com/u/' + user_id_out +'" title="' + user_name +'">';
        html2 += '<img class="small-photo shadow-5" style="margin:10px 0px 0px 25px;" src="' + img_src + '" title="' + user_name +'">';
        html2 += '</a></span>';
      }
    }
    html2 += '</p>';
    $('#'+div_name_out).append(html2);
  }

 function Draw_pie(data, div_name){
    if (data.length == 0){
      $('#'+div_name).empty();
      $('#'+div_name).append('<h4 style="margin-top:50%;margin-left:41%;font-size:14px;">暂无数据</h4>');
    }else{
      var myChart = {};
      myChart = echarts.init(document.getElementById(div_name));
      //var data = {'type1':11,'type2':20,'type3':29,'type4':30,'type5':10};
      var data_list = [];
      var data_dict = {};
      for (var i=0; i<data.length; i++){
        data_dict.value = data[i][1].toFixed(2);
        data_dict.name = data[i][0];
        data_list.push(data_dict);
        data_dict = {};
      }
      var option = {
        tooltip : {
          trigger: 'item',
          formatter: "{b} <br/> 占比 {d}%"
        },

        calculable : true,
        series : [
        {
          name:'',
          type:'pie',
          radius : '30%',
          center: ['48%', '45%'],
          itemStyle : {
            normal : {
              label : {
                show : true
              },
              labelLine : {
                show : true,
                length : 5
              }
            },
            emphasis : {
              label : {
                show : false,
                position : 'bottom',
                textStyle : {
                  fontSize : '14',
                  fontWeight : 'bold'
                }
              }
            }
          },
          data:data_list
        }
        ]
      }; 
      myChart.setOption(option);
    }             
  }

function Draw_get_top_weibo(data,div_name){
  var html = '';
  $('#'+div_name).empty();
  //console.log(data[0]);
    if(data[0]==undefined){
        html += "<div style='margin-left:10px;width:100%;height:100px;'>用户在昨天未发布任何微博</div>";
    }else if(data[0][3]==''){
        html += "<div style='margin-left:10px;width:100%;height:100px;'>用户在昨天未发布任何微博</div>";
    }else{
      //html += '<div id="weibo_list" class="weibo_list weibo_list_height scrolls tang-scrollpanel" style="margin:0;">';
      //html += '<div id="content_control_height" class="tang-scrollpanel-wrapper" style="margin:0;">';
      html += '<div class="tang-scrollpanel-content" style="margin:0;">';
      html += '<ul>';
      for(var i=0;i<data.length;i++){
        s = (i+1).toString();
        var weibo = data[i]
        var mid = weibo[0];
        var uid = weibo[9];
        var name = weibo[10];
        if(name == 'unknown'){
          name = '未知('+weibo[9]+')';
        };
        var date = weibo[5];
        var text = weibo[3];
        var geo = weibo[4];
        var reposts_count = weibo[1];
        var comments_count = weibo[2];
        var weibo_link = weibo[7];
        var user_link = weibo[8];
        var profile_image_url = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        var repost_tree_link = 'http://219.224.135.60:8080/show_graph/' + mid;
        if (geo==''){
           geo = '未知';
        }else{
          var geo_s = geo.split('&');
          geo_s = geo_s.join(' ');
        }
        var user_link = 'http://weibo.com/u/' + uid;
        html += '<li class="item">';
        html += '<div class="weibo_detail" style="width:800px">';
        html += '<p style="text-align:left;margin-bottom:0;">' +s + '、昵称:<a class="undlin" target="_blank" href="' + user_link  + '">' + name + '</a>(' + geo_s + ')&nbsp;&nbsp;发布内容：&nbsp;&nbsp;' + text + '</p>';
        html += '<div class="weibo_info"style="width:100%">';
        html += '<div class="weibo_pz">';
        html += '<div id="topweibo_mid" class="hidden">'+mid+'</div>';
        html += '<a class="retweet_count" href="javascript:;" title='+reposts_count+' target="_blank">转发数(' + reposts_count + ')</a>&nbsp;&nbsp;|&nbsp;&nbsp;';
        html += '<a class="comment_count" href="javascript:;" title='+comments_count+' target="_blank">评论数(' + comments_count + ')</a></div>';
        html += '<div class="m">';
        html += '<u>' + date + '</u>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + weibo_link + '">微博</a>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + user_link + '">用户</a>;';
       // html += '<a target="_blank" href="' + repost_tree_link + '">转发树</a>';
        html += '</div>';
        // html += '</div>';
        // html += '</div>';
        html += '</li>';
            }
                                    
    html += '<div id="TANGRAM_54__slider" class="tang-ui tang-slider tang-slider-vtl" style="height: 100%;">';
    html += '<div id="TANGRAM_56__view" class="tang-view" style="width: 6px;">';
    html += '<div class="tang-content"><div id="TANGRAM_56__inner" class="tang-inner"><div id="TANGRAM_56__process" class="tang-process tang-process-undefined" style="height: 0px;"></div></div></div>';
    html += '<a id="TANGRAM_56__knob" href="javascript:;" class="tang-knob" style="top: 0%; left: 0px;"></a></div>';
    html += '<div class="tang-corner tang-start" id="TANGRAM_54__arrowTop"></div><div class="tang-corner tang-last" id="TANGRAM_54__arrowBottom"></div></div>';

    html += '</ul>';
    html += '</div>';
    html += '</div>';
    html += '</div>';   
    }
      $('#'+div_name).append(html);
  }


function click_action(){
  //console.log(date_str);
      // $(".closeList2").live('click',function(){
      //   $("#float-wrap").addClass("hidden");
      //   //$("#re_influence").addClass("hidden");
      //   $("#cmt_influence").addClass("hidden");
      //   $("#comment_distribution_content").addClass("hidden");
      //   $("#retweet_distribution_content").addClass("hidden");
      //   return false;
      // });
      $(".comment_count").live("click",function(){    
        var comment = $(this).attr("title"); 
        //$("#float-wrap").removeClass("hidden");
        //$("#cmt_influence").removeClass("hidden"); 
        var mid = $(this).prev().prev(".hidden").text();
        var influenced_users_url_cmt = '/attribute/influenced_users/?uid='+parent.personalData.uid+'&date='+date_str+'&style=1&mid='+mid+'&count='+comment;
        Influence.call_ajax_request(influenced_users_url_cmt, Influence.ajax_method, Influence.Single_users_influence_cmt);
        $('#cmt_influence').modal();
        return false;
      });
      $(".retweet_count").live("click",function(){
        var retweeted = $(this).attr("title");
        //$("#float-wrap").removeClass("hidden");
       // $("#re_influence").removeClass("hidden");
        var mid = $(this).prev(".hidden").text();
        var influenced_users_url_re = '/attribute/influenced_users/?uid='+parent.personalData.uid+'&date='+date_str+'&style=0&mid='+mid+'&count='+retweeted;
        //console.log(influenced_users_url_re);
        Influence.call_ajax_request(influenced_users_url_re, Influence.ajax_method, Influence.Single_users_influence_re);
        $('#re_influence').modal();
        return false;
      });
      $("#retweet_distribution").live("click",function(){
        //$("#float-wrap").removeClass("hidden");
        //$("#retweet_distribution_content").removeClass("hidden");
        var all_influenced_users_url_style0 = '/attribute/all_influenced_users/?uid='+parent.personalData.uid+'&date='+date_str+'&style=0';
        //console.log(all_influenced_users_url_style0);
        Influence.call_ajax_request(all_influenced_users_url_style0, Influence.ajax_method, Influence.Draw_pie_all0);
        $('#retweet_distribution_content').modal();
        return false;
      });
      $("#comment_distribution").live("click",function(){
        //$("#float-wrap").removeClass("hidden");
        //$("#comment_distribution_content").removeClass("hidden");
        var all_influenced_users_url_style1 = '/attribute/all_influenced_users/?uid='+parent.personalData.uid +'&date='+date_str+'&style=1';
        //console.log(all_influenced_users_url_style1);
        Influence.call_ajax_request(all_influenced_users_url_style1, Influence.ajax_method, Influence.Draw_pie_all1);
        $('#comment_distribution_content').modal();
        return false;
      });
    $('input[name="choose_module"]').live('click', function(){             
      var index = $('input[name="choose_module"]:checked').val();
      //console.log(index);
      if(index == 1){
        var influence_url = '/attribute/influence_trend/?uid='+uid + '&time_segment=7';
        Influence.call_ajax_request(influence_url, Influence.ajax_method, Influence.Draw_influence);
      }
      else{
        var influence_url = '/attribute/influence_trend/?uid='+uid + '&time_segment=30';
        Influence.call_ajax_request(influence_url, Influence.ajax_method, Influence.Draw_influence);    
      }
    });

}

function influence_load(){
    click_action();
    var influence_url = '/attribute/influence_trend/?uid='+uid + '&time_segment=7';
    Influence.call_async_ajax_request(influence_url, Influence.ajax_method, Influence.Draw_influence);
    //console.log(date_str);
    var user_influence_detail_url = '/attribute/user_influence_detail/?uid='+parent.personalData.uid+'&date='+date_str;
    Influence.call_async_ajax_request(user_influence_detail_url, Influence.ajax_method, Influence.Draw_user_influence_detail);

    var basic_influence_url = '/attribute/current_influence_comment/?uid='+parent.personalData.uid+'&date='+date_str;
    Influence.call_async_ajax_request(basic_influence_url, Influence.ajax_method, Influence.Draw_basic_influence);
    var all_influenced_users_url_style0 = '/attribute/all_influenced_users/?uid='+parent.personalData.uid+'&date='+date_str+'&style=0';
    Influence.call_async_ajax_request(all_influenced_users_url_style0, Influence.ajax_method, Influence.Draw_all_influenced_users_style0);
    var all_influenced_users_url_style1 = '/attribute/all_influenced_users/?uid='+parent.personalData.uid+'&date='+date_str+'&style=1';
    Influence.call_async_ajax_request(all_influenced_users_url_style1, Influence.ajax_method, Influence.Draw_all_influenced_users_style1);
    //$('#influence_weibo1').showLoading();
    var get_top_weibo_url_style0 = '/attribute/get_top_weibo/?uid='+parent.personalData.uid+'&date='+date_str+'&style=0';
    Influence.call_async_ajax_request(get_top_weibo_url_style0, Influence.ajax_method, Influence.Draw_get_top_weibo1);
    var get_top_weibo_url_style1 = '/attribute/get_top_weibo/?uid='+parent.personalData.uid+'&date='+date_str+'&style=1';
    Influence.call_async_ajax_request(get_top_weibo_url_style1, Influence.ajax_method, Influence.Draw_get_top_weibo2);
    //console.log(date_str);
    var get_top_weibo_url_style2 = '/attribute/get_top_weibo/?uid='+parent.personalData.uid+'&date='+date_str+'&style=2';
    Influence.call_async_ajax_request(get_top_weibo_url_style2, Influence.ajax_method, Influence.Draw_get_top_weibo3);
    var get_top_weibo_url_style3 = '/attribute/get_top_weibo/?uid='+parent.personalData.uid+'&date='+date_str+'&style=3';
    Influence.call_async_ajax_request(get_top_weibo_url_style3, Influence.ajax_method, Influence.Draw_get_top_weibo4);
    //$('.entry #myTabContent').hideLoading();
    var summary_influence_url = '/attribute/summary_influence/?uid='+parent.personalData.uid+'&date='+date_str;
    Influence.call_async_ajax_request(summary_influence_url, Influence.ajax_method, Influence.Draw_conclusion);
};

var Influence = new Influence();
var influence_date = choose_time_for_mode();
var pre_influence_date = new Date(influence_date - 24*60*60*1000);
var date_str = pre_influence_date.format('yyyy-MM-dd');

// var influence_tag_url = '/attribute/current_tag_vector/?uid='+parent.personalData.uid+'&date='+date_str;
// Influence.async_call_sync_ajax_request(influence_tag_url, Influence.ajax_method, Influence.Influence_tag_vector);



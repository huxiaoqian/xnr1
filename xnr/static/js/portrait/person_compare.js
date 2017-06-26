function Search_weibo(){
  this.ajax_method = 'GET';
  that = this;
}

Search_weibo.prototype = {
    call_sync_ajax_request:function(url, method, callback){
        $.ajax({
          url: url,
          type: method,
          dataType: 'json',
          async: false,
          success:callback,
        });
    },
    call_async_ajax_request:function(url, method, callback){
        $.ajax({
          url: url,
          type: method,
          dataType: 'json',
          async: true,
          beforeSend:function(){$('#compare_loading').showLoading();},
          complete:function(){$('#compare_loading').hideLoading();},
          success:callback,
        });
    },
    Total_callback:function(all_data){
        var data = all_data.user_portrait;
        var url_photo = data.photo_url;
        var portrait = data.portrait;
        var tag_data = portrait.tag;
        Compare(url_photo, portrait, tag_data);
        compare_extra(portrait);
        bind_close_click(portrait);
    },
    Get_Callback_data:function(data){
        that.call_data = data;
    },
    Return_data: function(){
        return that.call_data;
    },
    Draw_cloud_keywords:function(data, div){
        
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
        var keywords_data = data;
        //console.log(data);

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
        var keyword = [];
        for (var i=0;i<word_num;i++){
            var word = {};
            word['name'] = key_name2[i];
            word['value'] = key_value2[i]*1000;
            word['itemStyle'] = createRandomItemStyle();
            keyword.push(word);
        }        
        var keywords = new Array();
        for(i in keywords_data){
            keywords.push({'name':keywords_data[i][0], 'value':keywords_data[i][1]*1000, 'itemStyle':createRandomItemStyle()});
            if(keywords.length == 20){
                break;
            }
        }
        var option = {
            title: {
                text: '',
            },
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
                name: '',
                type: 'wordCloud',
                size: ['80%', '80%'],
                textRotation : [0, 45, 90, -45],
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 14,
                },
                data: keyword,
            }]
        }
        var myChart = echarts.init(document.getElementById(div));
        myChart.setOption(option);
    },
}


function Compare(url_photo, portrait, tag_data){
    var html = '';
    var num = 0;
    var j = 0;
    for(var k in url_photo){
        num += 1;
    }
    html += '<thead id="head_id">';
    html += '<tr style="background: #fafafa;"><th style="width:100px;font-size:20px;vertical-align:middle; text-align:center;"></th>';
    var i =0;
    var photos = '';
    for(var k in url_photo){
        var person_url = "http://"+window.location.host+"/index/personal/?uid=";
        person_url = person_url + k;
        i += 1;
        if(url_photo[k]['photo_url']=='unkown'){
            photos = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        }else{
            photos = url_photo[k]['photo_url'];
        }
        html += '<th name="line'+ i +'" id='+k +' value='+i+'>';
        html += '<div class="panel-heading text-center">';
        html += '<div class="col-md-12">';
        html += '<a href="'+ person_url +'" target="_blank">';
        html += '<img src='+photos+' alt="" class="img-circle">';
        html += '</a>';
        html += '</div>';
        html += '<div style="float:right;margin-top:-66px">';
        html += '<a  name="line'+i+'" class="btn btn-round btn-default" style="border-radius:40px;font-size:12px;padding-top:4px;padding-bottom:0px"><i class="glyphicon glyphicon-remove"></i></a>';
        html += '</div>'
        html += '</div>';
        html += '</th>';
    }
    html += '</tr></thead><tbody>';
    html += '<tr><td colspan="'+ (num +1) +'" name="list-1" class="cate_title" style="font-size:20px"><b>基本信息</b></td></tr>';
    j = 0;
    html += '<tr class="list-1"><td class="cate_title" style="width:90px;text-align:right">昵称</td>';
    for(var k in portrait){

        if(portrait[k]['uname'] == 'unknown'){
            portrait[k]['uname'] = k;
        }
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['uname'] +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-1"><td class="cate_title" style="width:90px;text-align:right">注册地</td>';
    for(var k in portrait){
        if(portrait[k]['location'] = 'unknown'){
            portrait[k]['location'] = '未知';
        }
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['location'] +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-2" class="cate_title" style="font-size:20px"><b>整体评价</b></td></tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">活跃度</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['activeness'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">重要度</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['importance'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">影响力</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['influence'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">敏感度</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['sensitive'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-3" class="cate_title" style="font-size:20px"><b>倾向特征</b></td></tr>';
    html += '<tr class="list-3"><td class="cate_title" style="width:90px;text-align:right">身份</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['domain'] +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-3"><td class="cate_title" style="width:90px;text-align:right">领域</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['topic'][0]+','+ portrait[k]['topic'][1]+','+portrait[k]['topic'][2]+ '</td>';
		
    }
    html += '</tr>';
    html += '<tr><td colspan="'+ (num+1) +'" name="list-5" class="cate_title" style="font-size:20px"><b>偏好特征</b></td></tr>';
    
    j = 0 ;
    html += '<tr class="list-5"><td class="cate_title" style="width:90px;text-align:right">微话题</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id = "hashtag'+ j +'" style="height:200px"></div></td>';
    }
    html += '</tr>';
    j = 0 ;
    html += '<tr class="list-5"><td class="cate_title" style="width:90px;text-align:right">敏感词</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id = "sensitiveword'+ j +'" style="height:200px"></div></td>';
    }
    html += '</tr>';    
    j = 0 ;
    html += '<tr class="list-5"><td class="cate_title" style="width:90px;text-align:right">关键词</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id="line'+ j +'" style="height:300px"></div></td>';
    }
    html += '</tr>';

    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-7" class="cate_title" style="font-size:20px"><b>自定义标签</b></td></tr>';
    html += '<tr class="list-7"><td class="cate_title" style="width:90px;text-align:right">标签</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">';
        if(portrait[k]['tag'].length == 0){
        	 html += '<div>暂无数据</div>';
        }
        else{
        	for(var i = 0; i < portrait[k]['tag'].length; i++){
        		if(i == portrait[k]['tag'].length -1){
        			html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ portrait[k]['tag'][i].replace('-',':') +'</span>';
        		}
        		else{
        			html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ portrait[k]['tag'][i].replace('-',':') +',</span>';
        		}
        	}
        }
    }
    html += '</tr>';
    html += '<tr class="list-7"><td class="cate_title" style="width:90px;text-align:right">群体标签</td>';
    var j = 0 ;
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">';
        if(portrait[k]['tag'].length == 0){
             html += '<div>暂无数据</div>';
        }
        else{
            for(var i = 0; i < portrait[k]['group_tag'].length; i++){
                if(i == portrait[k]['group_tag'].length -1){
                    html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ portrait[k]['group_tag'][i].replace('-',':') +'</span>';
                }
                else{
                    html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ portrait[k]['group_tag'][i].replace('-',':') +',</span>';
                }
            }
        }
    }
    html += '</tr>';



    html += '</tbody>';
    $('#table_compare').append(html);

    var html2 = '';
    j = 0;
    for(var k in portrait){
        j += 1;
        html2 += '<div id="activityb'+ j +'"; style="display:none;height:600px;width:1000px"></div>'
    }
    $('#picturebig').append(html2);
}

function compare_extra(portrait){
    var mark = 1;
    var div ='';
    for(var key in portrait){
        var div = 'line'+ mark;
        //console.log(portrait[key]['keywords'],'portrait[key]["keywords"]');
        if(portrait[key]['keywords'].length == 0){
            $('#'+div).empty();
            $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['keywords'], div);
        }
        //div = 'emotion'+ mark;
        //var psycho_status = portrait[key]['psycho_status']
        // Draw_think_emotion(psycho_status,div);
        var div = 'hashtag'+ mark;
        if(portrait[key]['hashtag'].length == 0){
            $('#'+div).empty();
            $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['hashtag'], div);
        }
        var div = 'sensitiveword'+ mark;
//console.log(portrait[key]['sensitive_words'],portrait[key]['sensitive_words'].length)
        if(portrait[key]['sensitive_words'].length == 0){
            $('#'+div).empty();
            $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['sensitive_words'], div);
        }

        mark = mark + 1;
    }
}
function bind_close_click(portrait){
     $('.btn-round').live('click', function(){
        var cell = $('#table_compare').find('th').prevAll().length;
 
        if (cell == 2){
            $('.btn-round').css('display', 'none');
        }
        $('#table_compare').css('table-layout', 'fixed');
        $('[name='+ $(this).attr("name") +']').remove();
        $('#table_compare').css('table-layout', 'auto');
        $("td[name^='list-']").attr('colspan',cell);
        $('#table_compare').css('table-layout', 'fixed');
        var length = $("#head_id").find('th').length;
        
        for(var i = 1; i < length; i++){
            var obj = $("#head_id").find('th').eq(i);
            var uid = obj.attr('id');
            var value = obj.attr("value");
            var cloud_div = 'line'+value;
            var topic_div = 'topic'+ value;
            var emotion_div = 'emotion' + value;
            var hashtag_div = 'hashtag'+ value ;
            var sen_div = 'sensitiveword' + value;
            if(portrait[uid]['keywords'].length == 0){
                $('#'+cloud_div).empty();
                $('#'+cloud_div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
            }else{
                Search_weibo.Draw_cloud_keywords(portrait[uid]['keywords'], cloud_div);
            }

            if(portrait[uid]['sensitive_words'].length == 0){
                $('#'+sen_div).empty();
                $('#'+sen_div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
            }else{
                Search_weibo.Draw_cloud_keywords(portrait[uid]['sensitive_words'], sen_div);
            }
            if(portrait[uid]['hashtag']){
                $('#'+hashtag_div).empty();
                $('#'+hashtag_div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
            }else{
                Search_weibo.Draw_cloud_keywords(portrait[uid]['hashtag'], hashtag_div);
            }
            //var psycho_status = portrait[uid]['psycho_status']
            // Draw_think_emotion(psycho_status,emotion_div);
        }

     });
}
var uid_list = window.location.search;
Search_weibo = new Search_weibo();
//心理状态
var SENTIMENT_DICT_NEW = {'0':'中性', '1':'积极', '2':'生气', '3':'焦虑', '4':'悲伤', '5':'厌恶', '6':'其他', '7':'消极'};
var user=$('#com_user').text();
var url_total = '/manage/all_user_portrait/' + uid_list+'&submit_user='+user;
Search_weibo.call_async_ajax_request(url_total, Search_weibo.ajax_method, Search_weibo.Total_callback);

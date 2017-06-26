Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}
function g_social(){
  this.ajax_method = 'GET';
}
g_social.prototype = {   //获取数据，重新画表
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
//点击跳转页面
function g_pageGroup(pageNum,pageCount,div_name){
	switch(pageNum){
		case 1:
			g_page_icon(1,5,0,div_name);
		break;
		case 2:
			g_page_icon(1,5,1,div_name);
		break;
		case pageCount-1:
			g_page_icon(pageCount-4,pageCount,3,div_name);
		break;
		case pageCount:
			g_page_icon(pageCount-4,pageCount,4,div_name);
		break;
		default:
			g_page_icon(pageNum-2,pageNum+2,2,div_name);
		break;
	}
}

//根据当前选中页生成页面点击按钮
function g_page_icon(page,count,eq,div_name){
	var ul_html = "";
	for(var i=page; i<=count; i++){
		ul_html += "<li>"+i+"</li>";
	}
	$("#"+div_name+" #pageGro ul").html(ul_html);
	$("#"+div_name+" #pageGro ul li").eq(eq).addClass("on");
}

//上一页
function g_pageUp(pageNum,pageCount,div_name){
	//console.log(div_name);
	switch(pageNum){
		case 1:
		break;
		case 2:
			g_page_icon(1,5,0,div_name);
		break;
		case pageCount-1:
			g_page_icon(pageCount-4,pageCount,2,div_name);
		break;
		case pageCount:
			g_page_icon(pageCount-4,pageCount,3,div_name);
		break;
		default:
			g_page_icon(pageNum-2,pageNum+2,1,div_name);
		break;
	}
}

//下一页
function g_pageDown(pageNum,pageCount,div_name){
	switch(pageNum){
		case 1:
			g_page_icon(1,5,1,div_name);
		break;
		case 2:
			g_page_icon(1,5,2,div_name);
		break;
		case pageCount-1:
			g_page_icon(pageCount-4,pageCount,4,div_name);
		break;
		case pageCount:
		break;
		default:
			g_page_icon(pageNum-2,pageNum+2,3,div_name);
		break;
	}
}
function g_page_group_weibo1(start_row,end_row,data,div_name,sub_div_name){
    var weibo_num = end_row - start_row;
    $("#"+div_name+" #group_weibo_text").empty();
    //$("#"+sub_div_name).empty();
    var html = "";
    html += '<div class="group_weibo_font">';
    for (var i = start_row; i < end_row; i += 1){
        var s=i.toString();
        var uid = data[s]['uid'];
        var text = data[s]['text'];
        var uname = data[s]['uname'];
        var timestamp = data[s]['timestamp'];
        var date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="background:whitesmoke;font-size:14px;padding:5px;">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>'
    }
        else{
            html += '<div style="padding:5px;">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';    
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>';
        }
    }
    html += '</div>'; 
    $("#"+div_name+" #group_weibo_text").append(html);
    //$("#"+sub_div_name).empty();
}
$('#weiboTab li a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

function Draw_group(data){
    $('#in_group').empty();
    var html = '';
    html += '<table><tr><th ">连接紧密度<i id="closeness_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内所有节点之间实际存在的边数与所有可能边数之比"></i>&nbsp;&nbsp;'+ data['in_density'].toFixed(2) +'</th>';
    html += '<th ">微博转发频率<i id="weibo_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内单个节点转发群体微博的平均次数"></i>&nbsp;&nbsp;'+ data['in_inter_weibo_ratio'].toFixed(2) +'</th>';
    html += '<th ">参与转发比例<i id="join_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内所有参与转发群体微博的人数占群体人数的比例"></i>&nbsp;&nbsp;'+ (Math.round(data['in_inter_user_ratio'] * 10000)/100).toFixed(0) + '%' +'</th></tr>';
    html += '</table>'; 
    $('#in_group').append(html);
}
function Draw_out_group(data){
    $('#out_group').empty();
    var html = '';
    html += '<table><tr><th ">交互外部用户转发频率<i id="closeness_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内部用户平均与外部用户交互的微博频率"></i>&nbsp;&nbsp;'+ data['out_inter_weibo_ratio'].toFixed(2) +'</th>';
    html += '<th ">外部用户数量<i id="weibo_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="与群体交互的外部用户数量"></i>&nbsp;&nbsp;'+ data['social_out_record'].length +'</th>';
    html += '<th ">外部用户入库占比<i id="join_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title=" 与群体存在交互的外部用户中，已入库用户所占的比例"></i>&nbsp;&nbsp;'+ (Math.round(data['out_inter_user_ratio'] * 10000)/100).toFixed(0) + '%' +'</th></tr>';
    html += '</table>'; 
    $('#out_group').append(html);
}

function draw_relation_net(data,name,symbols){
    var total_content = [];
    var source_content = []
    for (var i=0;i<data[name].length;i++){
        var s=i.toString();
        var content1 = {};
        content1['category'] = 1;
        if(data[name][s]['3']=='unknown'){
            content1['name'] = '未知\n'+'('+data[name][s]['0']+')';
            content1['label'] = '未知';
        }else{
            content1['name'] = data[name][s]['3']+'\n('+data[name][s]['0']+')';
            content1['label'] = data[name][s]['3'];
        };
        content1['id'] = data[name][s]['0'];
        content1['value'] = 7;
        content1['draggable'] = true;
        content1['symbolSize'] = [60, 30];
        total_content.push(content1);
        var content2 = {};
        content2['category'] = 1;
        if(data[name][s]['4']=='unknown'){
            content2['name'] = '未知'+'\n('+data[name][s]['1']+')';
            content2['label'] = '未知';
        }else{
            content2['name'] = data[name][s]['4']+'\n('+data[name][s]['1']+')';
            content2['label'] = data[name][s]['4'];
        };
        //console.log('name!2!',content['name']);
        content2['id'] = data[name][s]['1'];
        content2['value'] = 7;
        content2['draggable'] = true;
        content2['symbolSize'] = [60, 30];
        total_content.push(content2);

        var relation = {};
        //relation['source'] = data[name][s]['4']+'\n('+data[name][s]['1']+')';
        //relation['target'] = data[name][s]['3']+'\n('+data[name][s]['0']+')';
        relation['source'] = content2['name'];
        relation['target'] = content1['name'];
        relation['weight'] = data[name][s]['2'];
        //relation['name'] = data[name][s]['4'];

        var width = data[name][s]['2'];
        var normal = {'width':width};
        var itemStyle= {'normal':normal};
        relation['itemStyle'] = itemStyle;

        source_content.push(relation);
    }

    var option = {
    tooltip : {
        trigger: 'item',
        formatter: '{a} : {b}'
    },
    toolbox: {
        show : true,
        feature : {
            restore : {show: true},
            magicType: {show: true, type: ['force', 'chord']},
            saveAsImage : {show: true}
        }
    },
    legend: {
        x: 'left',
        data:['']
    },
    series : [
        {
            type:'force',
            name : "",
            size:'80%',
            ribbonType: false,
            categories : [
                {
                    name:'微博用户'
                }
            ],
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        textStyle: {
                            color: '#333'
                        }
                    },
                    nodeStyle : {
                        brushType : 'both',
                        borderColor : 'rgba(255,215,0,0.4)',
                        borderWidth : 1
                    }
                },
                emphasis: {
                    label: {
                        show: false
                        // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                    },
                    nodeStyle : {
                        //r: 30
                    },
                    linkStyle : {}
                }
            },
            minRadius : 15,
            maxRadius : 25,
            gravity: 1.1,
            scaling: 1.2,
            draggable: false,
            linkSymbol: symbols,
            steps: 10,
            coolDown: 0.9,
            //preventOverlap: true,
            nodes:total_content,
            links : source_content
        }
    ]
	};
    var myChart = echarts.init(document.getElementById('relation_net'));
    myChart.setOption(option);
    require([
            'echarts'
        ],
        function(ec){
            var ecConfig = require('echarts/config');
            function focus(param) {
                var data = param.data;
                var links = option.series[0].links;
                var nodes = option.series[0].nodes;
                if (
                    data.source != null
                    && data.target != null
                ) { //点击的是边
                    var sourceNode = nodes.filter(function (n) {return n.name == data.source})[0];
                    var targetNode = nodes.filter(function (n) {return n.name == data.target})[0];
                    // console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
                } else{
                        window.open("/index/personal/?uid=" + data.id);                 
                }
            }
                myChart.on(ecConfig.EVENT.CLICK, focus)

                myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                    //console.log(myChart.chart.force.getPosition());
                });
            }
    )
}
function draw_relation_out_net(data,name,symbols){
    var total_content = [];
    //var total_out_content = [];
    var source_content = []
    for (var i=0;i<data[name].length;i++){
        var s=i.toString();
        var content1 = {};
        content1['category'] = 1;
        if(data[name][s]['5']=='unknown'){
            content1['name'] = '未知\n'+'('+data[name][s]['1']+')';
            content1['label'] = '未知';
        }else{
            content1['name'] = data[name][s]['5']+'\n('+data[name][s]['1']+')';
            content1['label'] = data[name][s]['5'];
        };
        content1['id'] = data[name][s]['1'];
        content1['value'] = data[name][s]['3']/10;
        content1['draggable'] = true;
        total_content.push(content1);
        var content2 = {};

        content2['category'] = 0;
        if(data[name][s]['4']=='unknown'){
            content2['name'] = '未知\n'+'('+data[name][s]['0']+')';
            content2['label'] = '未知';
        }else{
            content2['name'] = data[name][s]['4']+'\n('+data[name][s]['0']+')';
            content2['label'] = data[name][s]['4'];  
        };
        //content['name'] = data[name][s]['4'];
        content2['id'] = data[name][s]['0'];     
        //content['value'] = data[name][s]['3'];
        content2['draggable'] = true;
        //content['symbolSize'] = [60, 30];
        total_content.push(content2);

        var relation = {};
        //relation['source'] = data[name][s]['4']+'\n('+data[name][s]['0']+')';
        //relation['target'] = data[name][s]['5']+'\n('+data[name][s]['1']+')';
        relation['source'] = content2['name'];
        relation['target'] = content1['name'];
        relation['weight'] = data[name][s]['2']*10;
        //relation['name'] = data[name][s]['4'];

        var width = data[name][s]['2'];
        var normal = {
              label : {
                show : true
              },
              labelLine : {
                show : true,
                length : 5
              }
            };
        var itemStyle= {'normal':normal};
        relation['itemStyle'] = itemStyle;

        source_content.push(relation);
    }

    var option = {
    tooltip : {
        trigger: 'item',
        formatter: '{a} : {b}'
    },
    toolbox: {
        show : true,
        feature : {
            restore : {show: true},
            magicType: {show: true, type: ['force', 'chord']},
            saveAsImage : {show: true}
        }
    },
    legend: {
        x: 'left',
        data:['群组内部用户','群组外部用户']
    },
    series : [
        {
            type:'force',
            name : "",
            size:'70%',
            ribbonType: false,
            categories : [
                {
                    name:'群组内部用户'
                },
                {
                    name:'群组外部用户'
                }
            ],
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        textStyle: {
                            color: '#333',
                            fontSize:12
                        },
                labelLine : {
                    show : true,
                    length : 1000
                  }
                    },
                    nodeStyle : {
                        brushType : 'both',
                        borderColor : 'rgba(255,215,0,0.4)',
                        borderWidth : 1
                    }
                },
                emphasis: {
                    label: {
                        show: false
                        // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                    },
                    nodeStyle : {
                        //r: 30
                    },
                    linkStyle : {}
                }
            },
            minRadius : 15,
            maxRadius : 25,
            gravity: 1.1,
            scaling: 1.2,
            draggable: false,
            linkSymbol: symbols,
            steps: 10,
            coolDown: 0.9,
            //preventOverlap: true,
            nodes:total_content,
            links : source_content
        }
    ]
	};
    var myChart = echarts.init(document.getElementById('relation_out_net'));
    myChart.setOption(option);
    require([
            'echarts'
        ],
        function(ec){
            var ecConfig = require('echarts/config');
            function focus(param) {
                var data = param.data;
                var links = option.series[0].links;
                var nodes = option.series[0].nodes;
                if (
                    data.source != null
                    && data.target != null
                ) { //点击的是边
                    var sourceNode = nodes.filter(function (n) {return n.name == data.source})[0];
                    var targetNode = nodes.filter(function (n) {return n.name == data.target})[0];
                    // console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
                } else{
                        window.open("/index/personal/?uid=" + data.id);                 
                }
            }
                myChart.on(ecConfig.EVENT.CLICK, focus)

                myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                    //console.log(myChart.chart.force.getPosition());
                });
            }
    )
}
function draw_in_table(data){
    $('#group_in_table').empty();
    var s = '';
    var html = '';
    html = '<table id="group_in_table_body" class="table table-striped table-bordered bootstrap-datatable datatable responsive" >';
    html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center"></td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">转发量</td></tr>';
    for (var i=0;i<data['social_in_record'].length;i++){
    s =i.toString();
    var uname1 = data['social_in_record'][s]['4'];
    var uname2 = data['social_in_record'][s]['3'];
    if (uname1 =='unknown'){
        uname1 = '未知';
    }
    if (uname2 =='unknown'){
        uname2 = '未知';
    }
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_in_record'][s]['1'] + '">' + data['social_in_record'][s]['1'] +'</a></td><td style="text-align:center">' + uname1 +'</td><td style="text-align:center"><img src="/static/img/arrow_geo.png" style="width:25px;"></td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_in_record'][s]['0'] + '">' + data['social_in_record'][s]['0'] +'</a></td><td style="text-align:center">' + uname2 +'</td>';
    html += '<td style="text-align:center">';
    // html += '<a href=javascript:void(0)  id="group_change_weibo">' +;
    html += data['social_in_record'][s]['2'] +'</td></tr>';
    };
    html += '</table>';
    $('#group_in_table').append(html);
    /*
    $('#group_in_table_body').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        // "aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
    */
}
function draw_out_table(data){
    $('#group_out_table').empty();
    var s = '';
    var html = '';
    html = '<table id="group_out_table_body" class="table table-bordered table-striped table-condensed datatable" >';
    html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td>';
    // html +='<td style="text-align:center">影响力</td>';
    html += '<td style="text-align:center">转发量</td></tr>';
    for (var i=0;i<data['social_out_record'].length;i++){
        s =i.toString();
            var uname1 = data['social_out_record'][s]['4'];
            var uname2 = data['social_out_record'][s]['5'];
            if (uname1 =='unknown'){
                uname1 = '未知';
            }
            if (uname2 =='unknown'){
                uname2 = '未知';
            }
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_out_record'][s]['0'] + '">' + data['social_out_record'][s]['0'] +'</a></td><td style="text-align:center">' + uname1 +'</td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_out_record'][s]['1'] + '">' + data['social_out_record'][s]['1'] +'</a></td><td style="text-align:center">' + uname2 +'</td>';
    // html+= '<td style="text-align:center">' + data['social_out_record'][s]['3'] +'</td>';
    html += '<td style="text-align:center">';
    // html +='<a href=javascript:void(0)  id="group_change_out_weibo">';
    html += data['social_out_record'][s]['2'] +'</td></tr>';
    };
    html += '</table>';
    $('#group_out_table').append(html);
    /*
    $('#group_out_table_body').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        // "aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    })
    */
}

function draw_more_in_table(data){
    $('#group_in_more_table').empty();
    var html = '';
    html = '<table id="group_more_in" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="height: 300px;    overflow-y: scroll;">';
    html += '<tr><td style="text-align:center">原始微博ID</td><td style="text-align:center">昵称</td><td style="text-align:center"></td><td style="text-align:center">转发微博ID</td><td style="text-align:center">昵称</td><td style="text-align:center">转发量</td></tr>';
    for (var i=0;i<data['social_in_record'].length;i++){
        s =i.toString();
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_in_record'][s]['1'] + '">' + data['social_in_record'][s]['1'] +'</a></td><td style="text-align:center">' + data['social_in_record'][s]['4'] +'</td><td style="text-align:center"><img src="/static/img/arrow_geo.png" style="width:30px;"></td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_in_record'][s]['0'] + '">' + data['social_in_record'][s]['0'] +'</a></td><td style="text-align:center">' + data['social_in_record'][s]['3'] +'</td><td style="text-align:center">' + data['social_in_record'][s]['2'] +'</td></tr>';
    };
    html += '</table>';
    $('#group_in_more_table').append(html);
    // $('#group_more_in').dataTable({
    //    "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
    //    "sPaginationType": "bootstrap",
    //    "oLanguage": {
    //        "sLengthMenu": "_MENU_ 每页"
    //    }
    // });
}
function draw_more_out_table(data){
    $('#group_out_more_table').empty();
    var html = '';
    html = '<table  class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="height: 300px;    overflow-y: scroll;">';
  	html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">影响力</td><td style="text-align:center">转发量</td></tr>';
    for (var i=0;i<data['social_out_record'].length;i++){
        s =i.toString();
        html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_out_record'][s]['0'] + '">' + data['social_out_record'][s]['0'] +'</a></td><td style="text-align:center">' + data['social_out_record'][s]['4'] +'</td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['social_out_record'][s]['1'] + '">' + data['social_out_record'][s]['1'] +'</a></td><td style="text-align:center">' + data['social_out_record'][s]['5'] +'</td><td style="text-align:center">' + data['social_out_record'][s]['3'] +'</td><td style="text-align:center">' + data['social_out_record'][s]['2'] +'</td></tr>';
    };
    html += '</table>';
    $('#group_out_more_table').append(html);
    // $('#group_more_out').dataTable({
    //    "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
    //    "sPaginationType": "bootstrap",
    //    "oLanguage": {
    //        "sLengthMenu": "_MENU_ 每页"
    //    }
    // });
}
function draw_group_weibo0(data,div_name,sub_div_name){
    var page_num = 5;
    //console.log(data);
    if (data.length < page_num) {
        $('#'+ div_name + ' #pageGro .pageUp').css('display', 'none');
        $('#'+ div_name + ' #pageGro .pageList').css('display', 'none'); 
        $('#'+ div_name + ' #pageGro .pageDown').css('display', 'none'); 
        if (data.length == 0) {
            $('#' + sub_div_name).empty();
            $('#' + sub_div_name).append('该时段没有与此事件相关的微博！')
        }else{
            page_num = data.length
            g_page_group_weibo1( 0, page_num, data, div_name, sub_div_name);
        }
      }
      else {
        $('#'+ div_name + ' #pageGro .pageUp').css('display', 'block');
        $('#'+ div_name + ' #pageGro .pageList').css('display', 'block'); 
        $('#'+ div_name + ' #pageGro .pageDown').css('display', 'block'); 
          g_page_group_weibo1( 0, page_num, data,div_name,sub_div_name);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>5){
        g_page_icon(1,5,0,div_name);
    }else{
        g_page_icon(1,pageCount,0,div_name);
    }
    
    //$("#"+div_name+" #pageGro ").on("click",'li',function(){
    $("#"+div_name+" #pageGro li").live("click",function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            g_pageGroup(pageNum,pageCount,div_name);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      var page = parseInt($("#"+div_name+" #pageGro li.on").html());
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;}
      g_page_group_weibo1(start_row,end_row,data,div_name,sub_div_name);
    });

    $("#"+div_name+" #pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());
            g_pageUp(pageNum,pageCount,div_name);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index > 0){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        g_page_group_weibo1(start_row,end_row,data,div_name,sub_div_name);
    });
    

    $("#"+div_name+" #pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());

            g_pageDown(pageNum,pageCount,div_name);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html()) 
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
       g_page_group_weibo1(start_row,end_row,data,div_name,sub_div_name);
    });
}
function draw_group_weibo1(data){
	var div_name = 'weiboTabContent';
    var sub_div_name = 'group_weibo_text';
    $('#' + div_name).css('display','block');
	draw_group_weibo0(data,div_name,sub_div_name);
}
function draw_group_weibo2(data){
	var div_name = 'outWeiboTabContent';
    var sub_div_name = 'group_weibo_text';
    $('#' + div_name).css('display','block');
	draw_group_weibo0(data,div_name,sub_div_name);
}

function show_conclusion(data){
  var html = '';
  html += '<span class="fleft" style="margin: 10px 5px 5px 15px;/* margin-right:10px; */width:32px;height:32px;background-image:url(/static/img/warning.png);/* margin-top:5px; */display:black;"></span>';
  //html += '<h4>'+data[0]+'<span style="color:red;">'+data[1]+'</span>，'+data[2]+'<span style="color:red;">'+data[3]+'</span>。</h4>';
  html += '<span  class="fleft" style="    margin-top: 15px;    margin-left: 10px;    font-size: 16px;">'+data['density_description']+'。</span>';
  $("#social_conclusion").append(html);
}

function social_click(){
   //  $('a[id^="group_change_weibo"]').click(function(){
   //  var uid1 = $(this).parent().prev().prev().text();
   //  var uid2 = $(this).parent().prev().prev().prev().prev().prev().text();
   //  var url = '/group/social_inter_content/?uid1='+uid1+'&uid2='+uid2;
   //  console.log(url);
   //  g_social.call_sync_ajax_request(url, g_social.ajax_method, draw_group_weibo1);

   // });
    // $('a[id^="group_change_out_weibo"]').click(function(){
    // var uid1 = $(this).parent().prev().prev().prev().text();
    // var uid2 = $(this).parent().prev().prev().prev().prev().prev().text();
    // var url = '/group/social_out_content/?uid1='+uid1+'&uid2='+uid2;
    // g_social.call_sync_ajax_request(url, g_social.ajax_method, draw_group_weibo2);
    // });
    /*
    var init_in_uid1 = $('#group_in_table tr:eq(1) td:eq(3)').text();
    var init_in_uid2 = $('#group_in_table tr:eq(1) td:eq(0)').text();
    g_social.call_sync_ajax_request('/group/social_inter_content/?uid1='+init_in_uid1+'&uid2='+init_in_uid2, g_social.ajax_method, draw_group_weibo1);

    var init_out_uid1 = $('#group_out_table tr:eq(1) td:eq(2)').text();
    var init_out_uid2 = $('#group_out_table tr:eq(1) td:eq(0)').text();
    console.log('/group/social_out_content/?uid1='+init_out_uid1+'&uid2='+init_out_uid2);
    g_social.call_sync_ajax_request('/group/social_out_content/?uid1='+init_out_uid1+'&uid2='+init_out_uid2, g_social.ajax_method, draw_group_weibo2);
    */
}

function draw_social(data){
	Draw_group(data);
	Draw_out_group(data);
	draw_in_table(data);
	draw_relation_net(data,'social_in_record','arrow');
	draw_out_table(data);
	draw_relation_out_net(data,'social_out_record','none');
    social_click();
	show_conclusion(data);
	//draw_more_in_table(data);
	//draw_more_out_table(data);
}


var social_url = '/group/show_group_result/?task_name='+name+'&module=social';
var g_social = new g_social();
var group_weibo_url = '/group/social_out_content/?uid1=3270561561&uid2=2656274875';
g_social.call_sync_ajax_request(social_url, g_social.ajax_method, draw_social);
//g_social.call_sync_ajax_request(group_weibo_url, g_social.ajax_method, draw_group_weibo1);

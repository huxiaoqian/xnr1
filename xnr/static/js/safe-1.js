var end_time=Date.parse(new Date())/1000;
var historyTotal_url='/weibo_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+'&type=today&start_time=0&end_time='+end_time;
public_ajax.call_request('get',historyTotal_url,historyTotal);
function historyTotal(dataTable) {
    var data=[dataTable[0]];
    $('#history p').show();
    $('#history').bootstrapTable('load', data);
    $('#history').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
        pageList: [15,20,25],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: false,//回车搜索
        showRefresh: false,//刷新按钮
        showColumns: false,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:false,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "名称",//标题
                field: "date_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.date_time==''||row.date_time=='null'||row.date_time=='unknown'||!row.date_time){
                        return '未知';
                    }else {
                        return row.date_time;
                    };
                }
            },
            {
                title: "总粉丝数",//标题
                field: "user_fansnum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "总发帖量",//标题
                field: "total_post_sum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "日常发帖",//标题
                field: "daily_post_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "热点跟随",//标题
                field: "hot_follower_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "业务发帖",//标题
                field: "business_post_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "渗透力",//标题
                field: "penetration",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "安全性",//标题
                field: "safe",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
        ],
    });
    $('#history p').slideUp(700);
};
$('.choosetime .demo-label input').on('click',function () {
    var _val=$(this).val();
    if (_val=='mize'){
        $('#start_1').show();
        $('#end_1').show();
        $('.sureTime').show();
    }else {
        $('#start_1').hide();
        $('#end_1').hide();
        $('.sureTime').hide();
        var startTime='',today='',startTime_2,midURL='safe_active',
            lastURL='';
        if (_val==0){
            startTime=todayTimetamp();
            startTime_2=0;
            today='today';
            midURL='safe_active_today';
        }else {
            startTime=getDaysBefore(_val);
            startTime_2=getDaysBefore(_val);
            lastURL='&start_time='+startTime+'&end_time='+end_time+'&assess_type=safe';
        }
        //表格
        var historyTotal_url='/weibo_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+'&type='+today+
            '&start_time='+startTime_2+'&end_time='+end_time;
        public_ajax.call_request('get',historyTotal_url,historyTotal);
        //曲线图 1
        var safe_7day_url='/weibo_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
            '&start_time='+startTime+'&end_time='+end_time+'&assess_type=safe';
        public_ajax.call_request('get',safe_7day_url,safe_7day);
        //曲线图 2
        var safe_url='/weibo_xnr_assessment/'+midURL+'/?xnr_user_no='+ID_Num+lastURL;
        public_ajax.call_request('get',safe_url,safe);
    }
});
$('.sureTime').on('click',function () {
    var s=$('#start_1').val();
    var d=$('#end_1').val();
    if (s==''||d==''){
        $('#successfail p').text('时间不能为空。');
        $('#successfail').modal('show');
    }else {
        var start =(Date.parse(new Date(s))/1000);
        var end = (Date.parse(new Date(d))/1000);
        //表格
        var historyTotal_url='/weibo_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+
            '&start_time='+start+'&end_time='+end;
        public_ajax.call_request('get',historyTotal_url,historyTotal);
        //曲线图 1
        var safe_7day_url='/weibo_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
            '&start_time='+start+'&end_time='+end+'&assess_type=safe';
        public_ajax.call_request('get',safe_7day_url,safe_7day);
        //曲线图 2
        var safe_url='/weibo_xnr_assessment/safe_active/?xnr_user_no='+ID_Num+
            '&start_time='+start+'&end_time='+end+'&assess_type=safe';
        public_ajax.call_request('get',safe_url,safe);
    }
});
//==============
var end=Date.parse(new Date())/1000;
var safe_7day_url='/weibo_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end+'&assess_type=safe';
public_ajax.call_request('get',safe_7day_url,safe_7day);
function safe_7day(data) {
    $('#near_7_day p').show();
    var nearTime=[],nearData=[];
    $.each(data,function (index,item) {
        nearTime.push(item['date_time'][0]);
        nearData.push(item['safe'][0]);
    })
    var myChart = echarts.init(document.getElementById('near_7_day'),'dark');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '安全性变化趋势图',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {
                    backgroundColor: 'rgba(8,23,44,0.8)',
                }
            }
        },
        xAxis:  {
            type: 'category',
            boundaryGap: false,
            data: nearTime
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        },
        series : [
            {
                name:'安全性分值',
                type:'line',
                data:nearData,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            },
        ]
    };
    myChart.setOption(option);
    $('#near_7_day p').slideUp(700);
};
var scoreUrl='/weibo_xnr_assessment/safe_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
var defaultUrl='/weibo_xnr_assessment/safe_active/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end_time+'&assess_type=safe';
public_ajax.call_request('get',defaultUrl,safe);
var t;
$('#container .type_page #myTabs li').on('click',function () {
    $('#postRelease p').show();
    var mid=$(this).attr('midurl');
    if (mid.indexOf('&')==-1){
        public_ajax.call_request('get',defaultUrl,safe);
    }else {
        var midTwo=mid.split('&');
        var readyChart_url='/weibo_xnr_assessment/'+midTwo[0]+'/?xnr_user_no='+ID_Num;
        public_ajax.call_request('get',readyChart_url,radar);
        var topic;
        if (midTwo[1]=='safe_tweets_topic'){
            topic=$('#field input:radio[name="theme2"]:checked').val();
        }else {
            topic=$('#userField input:radio[name="domain"]:checked').val();
        }
        var readyDoc_url='/weibo_xnr_assessment/'+midTwo[1]+'/?xnr_user_no='+ID_Num+'&topic='+topic+
            '&sort_item=timestamp';
        public_ajax.call_request('get',readyDoc_url,weiboData);
        t=$(this).attr('linktype');
        if (t=='area'){
            $('.pc-4 .center-1').show();
            $('.pc-4 .center-3').hide();
            $('#postContent-2 ._tit').text('虚拟人相关发帖');
        }else {
            $('.pc-4 .center-1').hide();
            $('.pc-4 .center-3').show();
            $('#postContent-2 ._tit').text('关注人群相关发帖');
        }
    }
});
//--活跃安全性
function safe(data) {
    //total_num、day_num、growth_rate
    $('#active-1 p').show();
    if (isEmptyObject(data)){
        $('#active-1').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var time=[],totData=[];
        for (var i in data){
            totData.push(data[i]);
            time.push(getLocalTime(i));
        };
        var myChart = echarts.init(document.getElementById('active-1'),'dark');
        var option = {
            backgroundColor:'transparent',
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['微博发布量']
            },
            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    magicType: {type: ['line', 'bar']},
                    restore: {},
                    saveAsImage: {
                        backgroundColor: 'rgba(8,23,44,0.8)',
                    }
                }
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: time
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            },
            series: [
                {
                    name:'微博发布量',
                    type:'line',
                    data:totData,
                    markPoint: {
                        data: [
                            {type: 'max', name: '最大值'},
                            {type: 'min', name: '最小值'}
                        ]
                    },
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    }
                },
            ]
        };
        myChart.setOption(option);
    }
    $('#safeContent p').slideUp(700);
};
// 雷达图
function radar(data) {
    var radarData=[],radarVal=[];
    for (var k in data){
        if (k=='radar'){
            if (isEmptyObject(data[k])){
                radarVal=[0,0,0,0,0];
                var p;
                if (t=='area'){p=$('#field input')}else {p=$('#userField input')};
                for(var s=0;s<5;s++){
                    radarData.push({name:$(p[s]).val(), max:1});
                }
            }else {
                for(var m in data[k]){
                    radarData.push({name:m, max:1});
                    radarVal.push(data[k][m]);
                }
            }
            for(var m in data[k]){
                radarData.push({name:m, max:1});
                radarVal.push(data[k][m]);
            }
        }else {
            dashBoard(data[k]);
        }
    };
    var myChart = echarts.init(document.getElementById('pc-1'),'dark');
    var option = {
        backgroundColor:'transparent',
        tooltip: {},
        radar: {
            // shape: 'circle',
            indicator:radarData,
        },
        series: [{
            //name: '渗透领域',
            type: 'radar',
            // areaStyle: {normal: {}},
            data : [
                {
                    value : radarVal,
                    name : '渗透领域'
                },
            ]
        }]
    };
    myChart.setOption(option);
}
// 仪表盘图
function dashBoard(dashVal) {
    dashVal=(dashVal*100).toFixed(4);
    var myChart = echarts.init(document.getElementById('pc-2'),'dark');
    var option = {
        backgroundColor:'transparent',
        tooltip : {
            formatter: "{a} <br/>{b} : {c}%"
        },
        toolbox: {
            feature: {
                restore: {},
                saveAsImage: {
                    backgroundColor: 'rgba(8,23,44,0.8)',
                }
            }
        },
        series: [
            {
                name: '渗透率',
                type: 'gauge',
                max:100,
                detail: {formatter:'{value}'},
                data: [{value:dashVal, name: '渗透率'}]
            }
        ]
    };
    myChart.setOption(option);
}
//发表内容
$('.pc-4 input').on('click',function () {
    $('#postRelease p').show();
    var name=$(this).attr('name'),theSort='',the='';
    if (name=='th'){
        if (t=='area'){
            the=$('#field input:radio[name="theme2"]:checked').val();
        }else {
            the=$('#userField input:radio[name="domain"]:checked').val();
        }
        theSort=$(this).val();
        if (!the){the=''};
    }else {
        the=$(this).val();
        theSort=$('.center-2 input:radio[name="th"]:checked').val();
    }
    var the_url='';
    if (t=='area'){
        the_url='/weibo_xnr_assessment/safe_tweets_topic/?xnr_user_no='+ID_Num+'&topic='+the+'&sort_item='+theSort;
    }else {
        the_url='/weibo_xnr_assessment/follow_group_tweets/?xnr_user_no='+ID_Num+'&domain='+the+'&sort_item='+theSort;
    }
    public_ajax.call_request('get',the_url,weiboData)
});
function weiboData(data) {
    $('#postRelease').bootstrapTable('load', data);
    $('#postRelease').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
        pageList: [15,20,25],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: false,//回车搜索
        showRefresh: false,//刷新按钮
        showColumns: false,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:false,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name,location,txt,txt2,all='',img;
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name=row.uid;
                    }else {
                        name=row.nick_name;
                    };
                    if (row.geo==''||row.geo=='null'||row.geo=='unknown'){
                        location='未知';
                    }else {
                        location=row.geo.replace(/&/g,' ');
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        if (row.sensitive_words_string||!isEmptyObject(row.sensitive_words_string)){
                            var keyword_d=row.sensitive_words_string.split('&');
                            for (var f of keyword_d){
                                txt=row.text.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                            var rrr=row.text;
                            if (rrr.length>=50){
                                rrr=rrr.substring(0,50)+'...';
                                all='inline-block';
                            }else {
                                rrr=row.text;
                                all='none';
                            }
                            for (var f of keyword_d){
                                rrr=rrr.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                            txt2=rrr;
                        }else {
                            txt=row.text;
                            if (txt.length>=160){
                                txt2=txt.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                txt2=txt;
                                all='none';
                            }
                        };
                    };
                    var str=
                        '<div class="post_center-every" style="text-align: left;">'+
                        '   <div class="post_center-hot">'+
                        '       <img src="'+img+'" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>'+
                        '           <span class="time" style="font-weight:700;color:#f6a38e;display: inline-block;margin-left:5px;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(row.timestamp)+'</span> '+
                        // '           <span class="location" style="font-weight:700;color:blanchedalmond;display: inline-block;margin-left:5px;"><i class="icon icon-screenshot"></i>&nbsp;&nbsp;'+location+'</span>  '+
                        '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                        '           <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                        '           <p class="allall1" style="display:none;">'+txt+'</p>'+
                        '           <p class="allall2" style="display:none;">'+txt2+'</p>'+
                        '           <span class="center_2" style="text-align: left;">'+txt2+'</span>'+
                        '           <div class="center_3">'+
                        '               <span class="cen3-1" onclick="retweet(this)" title="转发"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（'+row.retweeted+'）</span>'+
                        '               <span class="cen3-2" onclick="showInput(this)" title="评论"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（'+row.comment+'）</span>'+
                        '               <span class="cen3-3" onclick="thumbs(this)" title="赞"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '               <span class="cen3-9" onclick="robot(this)" title="机器人回复"><i class="icon icon-github-alt"></i>&nbsp;&nbsp;机器人回复</span>'+
                        '               <span class="cen3-4" onclick="joinlab(this)" title="加入语料库"><i class="icon icon-upload-alt"></i>&nbsp;&nbsp;加入语料库</span>'+
                        '           </div>'+
                        '           <div class="commentDown" style="width: 100%;display: none;">'+
                        '               <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '               <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '           </div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#postRelease p').slideUp(30);
    $('.postRelease .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}
//评论
function showInput(_this) {
    $(_this).parents('.post_center-every').find('.commentDown').show();
};
function comMent(_this){
    var txt = $(_this).prev().val().replace(/\&/g,'%26').replace(/\#/g,'%23');
    var mid = $(_this).parents('.post_center-every').find('.mid').text();
    if (txt!=''){
        var post_url_1='/weibo_xnr_operate/reply_comment/?text='+txt+'&xnr_user_no='+ID_Num+'&mid='+mid;
        public_ajax.call_request('get',post_url_1,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}
//转发
function retweet(_this) {
    var txt = $(_this).parent().prev().text().replace(/\&/g,'%26').replace(/\#/g,'%23');
    var mid = $(_this).parents('.post_center-every').find('.mid').text();
    var uid = $(_this).parents('.post_center-every').find('.uid').text();
    var post_url_2='/weibo_xnr_operate/reply_retweet/?tweet_type=行为评估'+'&xnr_user_no='+ID_Num+
        '&text='+txt+'&mid='+mid;
    public_ajax.call_request('get',post_url_2,postYES)
}
//点赞
function thumbs(_this) {
    var mid = $(_this).parents('.post_center-every').find('.mid').text();
    var post_url_3='/weibo_xnr_operate/like_operate/?mid='+mid+'&xnr_user_no='+ID_Num;
    public_ajax.call_request('get',post_url_3,postYES)
};
//操作返回结果
function postYES(data) {
    var f='';
    if (data[0]||data||data[0][0]){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}

var end_time=yesterday();
var historyTotal_url='/facebook_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+'&type=today&start_time=0&end_time='+end_time;
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
                title: "总发帖量",//标题
                field: "total_post_sum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "好友数",//标题
                field: "user_friendsnum",//键名
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
                title: "跟踪转发",//标题
                field: "trace_follow_tweet_num",//键名
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
        var startTime='',today='',startTime_2,midURL='penetration_total',lastURL='';
        if (_val==0){
            startTime=todayTimetamp();
            startTime_2=0;
            today='today';
            midURL='penetration_total_today';
        }else {
            startTime=getDaysBefore(_val);
            startTime_2=getDaysBefore(_val);
            lastURL='&start_time='+startTime+'&end_time='+end_time+'&assess_type=penetration';
        }
        //表格
        var historyTotal_url='/facebook_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+'&type='+today+
            '&start_time='+startTime_2+'&end_time='+end_time;
        public_ajax.call_request('get',historyTotal_url,historyTotal);
        //曲线图 1
        var penetration_7day_url='/facebook_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
            '&start_time='+startTime+'&end_time='+end_time+'&assess_type=penetration';
        public_ajax.call_request('get',penetration_7day_url,penetration_7day);
        //曲线图 2
        var penetration_url='/facebook_xnr_assessment/'+midURL+'/?xnr_user_no='+ID_Num+lastURL;
        public_ajax.call_request('get',penetration_url,penetration);
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
        var historyTotal_url='/facebook_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+
            '&start_time='+start+'&end_time='+end;
        public_ajax.call_request('get',historyTotal_url,historyTotal);
        //曲线图 1
        var penetration_7day_url='/facebook_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
            '&start_time='+start+'&end_time='+end+'&assess_type=penetration';
        public_ajax.call_request('get',penetration_7day_url,penetration_7day);
        //曲线图 2
        var penetration_url='/facebook_xnr_assessment/penetration_total/?xnr_user_no='+ID_Num+
            '&start_time='+start+'&end_time='+end+'&assess_type=penetration';
        public_ajax.call_request('get',penetration_url,penetration);
    }
});
//==============
var penetration_7day_url='/facebook_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end_time+'&assess_type=penetration';
public_ajax.call_request('get',penetration_7day_url,penetration_7day);
function penetration_7day(data) {
    $('#near_7_day p').show();
    var nearTime=[],nearData=[];
    if (data.length==0){
        // nearTime.push($_time);
        // nearData.push(0);
        $('#near_7_day h2').remove();
        $('#near_7_day p').slideUp(700);
        $('#near_7_day').height('40px').append('<h2 style="width:100%;text-align:center;">趋势图暂无数据</h2>');
        return false;
    }else {
        $('#near_7_day').height('400px');
        $.each(data,function (index,item) {
            nearTime.push(item['date_time'][0]);
            var hu=item['penetration']||item['influence'];
            nearData.push(hu[0]);
        })
    };
    var myChart = echarts.init(document.getElementById('near_7_day'),'dark');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '渗透力变化趋势图',
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
                name:'渗透力分值',
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
var scoreUrl='/facebook_xnr_assessment/penetration_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
var defaultUrl='/facebook_xnr_assessment/penetration_total/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end_time+'&assess_type=penetration';;
public_ajax.call_request('get',defaultUrl,penetration);
//=====
function publicData(data) {
    var a=[];
    for (var b in data){
        a.push(data[b])
    }
    return a;
}
//画图
function penetration(data) {
    $('#penetration p').show();
    //total_num、day_num、growth_rate
    if (isEmptyObject(data)){
        $('#penetration').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var time=[],fans_group=[];
        for (var i in data['friends_group']){
            fans_group.push(data['friends_group'][i]);
            time.push(getLocalTime(i));
        };
        var feedback_total=publicData(data['feedback_total']);
        var follow_group=publicData(data['follow_group']);
        var self_info=publicData(data['self_info']);
        var warning_report_total=publicData(data['warning_report_total']);
        var myChart = echarts.init(document.getElementById('penetration'),'dark');
        var option = {
            backgroundColor:'transparent',
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['好友群体敏感度','发布信息敏感度','社交反馈敏感度','预警上报敏感度'],
                width: '600',
                left:'center'
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
                    name:'好友群体敏感度',
                    type:'line',
                    data:fans_group,
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
                {
                    name:'社交反馈敏感度',
                    type:'line',
                    data:feedback_total,
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
                {
                    name:'发布信息敏感度',
                    type:'line',
                    data:self_info,
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
                {
                    name:'预警上报敏感度',
                    type:'line',
                    data:warning_report_total,
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
    $('#penetration p').slideUp(700);
}


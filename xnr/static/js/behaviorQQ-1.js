var end_time=Date.parse(new Date())/1000;
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
        var startTime='',midurl_1='influence_qq',midurl_2='penetration_qq',midurl_3='safe_qq',urlLast='';
        if (_val==0){
            startTime=todayTimetamp();
            midurl_1='influence_qq_today';
            midurl_2='penetration_qq_today';
            midurl_3='safe_qq_today';
        }else {
            startTime=getDaysBefore(_val);
            urlLast='&start_time='+startTime+'&end_time='+end_time;
        }
        //曲线图 1
        var influe_url='/qq_xnr_assessment/'+midurl_1+'/?xnr_user_no='+ID_Num+urlLast;
        public_ajax.call_request('get',influe_url,influe);
        //曲线图 2
        var penetration_url='/qq_xnr_assessment/'+midurl_2+'/?xnr_user_no='+ID_Num+urlLast;
        public_ajax.call_request('get',penetration_url,penetration);
        //曲线图 3
        var safe_url='/qq_xnr_assessment/'+midurl_3+'/?xnr_user_no='+ID_Num+urlLast;
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
        var startTime =(Date.parse(new Date(s))/1000);
        var end_time = (Date.parse(new Date(d))/1000);
        //曲线图 1
        var influe_url='/qq_xnr_assessment/influence_qq/?xnr_user_no='+ID_Num+
            '&start_time='+startTime+'&end_time='+end_time;
        public_ajax.call_request('get',influe_url,influe);
        //曲线图 2
        var penetration_url='/qq_xnr_assessment/penetration_qq/?xnr_user_no='+ID_Num+
            '&start_time='+startTime+'&end_time='+end_time;
        public_ajax.call_request('get',penetration_url,penetration);
        //曲线图 3
        var safe_url='/qq_xnr_assessment/safe_qq/?xnr_user_no='+ID_Num+
            '&start_time='+startTime+'&end_time='+end_time;
        public_ajax.call_request('get',safe_url,safe);
    }
});
//影响力
var influe_url='/qq_xnr_assessment/influence_qq/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end_time;
console.log('影响力=== '+influe_url)
public_ajax.call_request('get',influe_url,influe);
function influe(data) {
    console.log(data)
    var score=0;
    if (data.mark){score=data.mark}
    $('.influe-1 .score').text(score);
    var time=[],dayData=[],total=[];
    for(var a in data['at_day']){
        time.push(getLocalTime(a));
        dayData.push(data['at_day'][a]);
    };
    for(var a in data['at_total']){
        total.push(data['at_total'][a]);
    }
    var myChart = echarts.init(document.getElementById('influe-2'),'dark');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '影响力变化趋势图',
            left: 'center'
        },
        legend: {
            data: ['历史总被@数', '日被@数'],
            left:'left'
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
            data: time
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        },
        series : [
            {
                name:'历史总被@数',
                type:'line',
                data:total,
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
                name:'日被@数',
                type:'line',
                data:dayData,
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
};
//渗透力
var penetration_url='/qq_xnr_assessment/penetration_qq/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end_time;
public_ajax.call_request('get',penetration_url,penetration);
function penetration(data) {
    var score=0;
    if (data.mark){score=data.mark}
    $('.pen-1 .score').text(score);
    var time=[],dayData=[];
    for(var a in data['sensitive_info']){
        time.push(getLocalTime(a));
        dayData.push(data['sensitive_info'][a].toFixed(2));
    };
    var myChart = echarts.init(document.getElementById('pen-2'),'dark');
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
            data: time
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        },
        series : [
            {
                name:'渗透力指数',
                type:'line',
                data:dayData,
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
};
//安全性
var safe_url='/qq_xnr_assessment/safe_qq/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end_time;
public_ajax.call_request('get',safe_url,safe);
function safe(data) {
    var score=0;
    if (data.mark){score=data.mark}
    $('.safe-1 .score').text(score);
    var time=[],dayData=[],total=[];
    for(var a in data['speak_day']){
        time.push(getLocalTime(a));
        dayData.push(data['speak_day'][a]);
    };
    for(var a in data['speak_total']){
        total.push(data['speak_total'][a]);
    }
    var myChart = echarts.init(document.getElementById('safe-2'),'dark');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '安全性变化趋势图',
            left: 'center'
        },
        legend: {
            data: ['历史总发言数', '日发言数'],
            left:'left'
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
            data: time
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        },
        series : [
            {
                name:'历史总发言数',
                type:'line',
                data:total,
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
                name:'日发言数',
                type:'line',
                data:dayData,
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

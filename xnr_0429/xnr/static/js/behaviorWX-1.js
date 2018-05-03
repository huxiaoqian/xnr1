/*
* @Author: Marte
* @Date:   2017-10-26 11:34:30
* @Last Modified by:   Marte
* @Last Modified time: 2017-11-15 17:35:35
*/
console.log('===微信行为评估js===')
console.log(ID_Num)
// // 暂时展示数据用
// ID_Num = 'QXNR0001';


//时间戳转时间_修改版2017-11-15 LL(只保留日期，)
function getLocalTime_LL(nS) {
    // return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日|上午|下午/g, " ");  //2017/11/9  12:00:00
    return new Date(parseInt(nS) * 1000).toLocaleDateString();//2017/11/9 只要日期
}

// 时间选项
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
        // var startTime='',midurl_1='influence_qq',midurl_2='penetration_qq',midurl_3='safe_qq',urlLast='';
        var startTime='',midurl_1='influence',midurl_2='penetration',midurl_3='safe',urlLast='';
        if (_val==0){
            startTime=todayTimetamp();
            // midurl_1='influence_qq_today';
            // midurl_2='penetration_qq_today';
            // midurl_3='safe_qq_today';

            // urlLast='&start_time='+startTime+'&end_time='+end_time;
            urlLast='&period='+_val;
        }else {
            startTime=getDaysBefore(_val);
            // urlLast='&start_time='+startTime+'&end_time='+end_time;
            urlLast='&period='+_val;
        }
        //曲线图 1
        var influe_url='/wx_xnr_assessment/'+midurl_1+'/?wxbot_id='+ID_Num+urlLast;
        console.log(influe_url)
        public_ajax.call_request('get',influe_url,influe);
        //曲线图 2
        var penetration_url='/wx_xnr_assessment/'+midurl_2+'/?wxbot_id='+ID_Num+urlLast;
        console.log(penetration_url)
        public_ajax.call_request('get',penetration_url,penetration);
        //曲线图 3
        var safe_url='/wx_xnr_assessment/'+midurl_3+'/?wxbot_id='+ID_Num+urlLast;
        console.log(safe_url)
        public_ajax.call_request('get',safe_url,safe);
    }
});
// 确定时间搜索
$('.sureTime').on('click',function () {
    var s=$('#start_1').val();
    var d=$('#end_1').val();
    if (s==''||d==''){
        $('#successfail p').text('时间不能为空。');
        $('#successfail').modal('show');
    }else {
        // var startTime =(Date.parse(new Date(s))/1000);
        // var end_time = (Date.parse(new Date(d))/1000);
        // ===========改为上传日期 2017-11-15
        //曲线图 1
        // var influe_url='/qq_xnr_assessment/influence_qq/?xnr_user_no='+ID_Num+
        //     '&start_time='+startTime+'&end_time='+end_time;
        var influe_url='/wx_xnr_assessment/influence/?wxbot_id='+ID_Num+
            '&startdate='+s+'&enddate='+d;
        public_ajax.call_request('get',influe_url,influe);
        //曲线图 2
        var penetration_url='/wx_xnr_assessment/penetration/?wxbot_id='+ID_Num+
            '&startdate='+s+'&enddate='+d;
        public_ajax.call_request('get',penetration_url,penetration);
        //曲线图 3
        var safe_url='/wx_xnr_assessment/safe/?wxbot_id='+ID_Num+
            '&startdate='+s+'&enddate='+d;
        public_ajax.call_request('get',safe_url,safe);
    }
});

//影响力
// var influe_url='/qq_xnr_assessment/influence_qq/?xnr_user_no='+ID_Num+
//     '&start_time='+getDaysBefore('7')+'&end_time='+end_time;
// var influe_url='/wx_xnr_assessment/influence/?wxbot_id='+ID_Num+'&start_time='+getDaysBefore('7')+'&end_time='+end_time;
// var influe_url='/wx_xnr_assessment/influence/?wxbot_id='+ID_Num+'&startdate=2017-11-10&enddate=2017-11-15';
var influe_url='/wx_xnr_assessment/influence/?wxbot_id='+ID_Num+'&period=7';
console.log('影响力=== '+influe_url)
public_ajax.call_request('get',influe_url,influe);
function influe(data) {
    console.log('影响力数据')
    console.log(data)
    var score=0;
    if (data.mark){score=data.mark}
    $('.influe-1 .score').text(score);
    var time=[],dayData=[],total=[];
    for(var a in data['at_day']){
        time.push(getLocalTime_LL(a));
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
                dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
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
// var penetration_url='/wx_xnr_assessment/penetration/?wxbot_id='+ID_Num+
//     '&start_time='+getDaysBefore('7')+'&end_time='+end_time;
var penetration_url='/wx_xnr_assessment/penetration/?wxbot_id='+ID_Num+'&period=7';
console.log('渗透力=== '+penetration_url)
public_ajax.call_request('get',penetration_url,penetration);
function penetration(data) {
    console.log(data)
    var score=0;
    if (data.mark){score=data.mark}
    $('.pen-1 .score').text(score);
    var time=[],dayData=[];
    for(var a in data['sensitive_info']){
        time.push(getLocalTime_LL(a));
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
                dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
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
// var safe_url='/wx_xnr_assessment/safe/?wxbot_id='+ID_Num+
//     '&start_time='+getDaysBefore('7')+'&end_time='+end_time;
var safe_url='/wx_xnr_assessment/safe/?wxbot_id='+ID_Num+'&period=7';
console.log('安全性=== '+penetration_url)
public_ajax.call_request('get',safe_url,safe);
function safe(data) {
    console.log(data);
    var score=0;
    if (data.mark){score=data.mark}
    $('.safe-1 .score').text(score);
    var time=[],dayData=[],total=[];
    for(var a in data['speak_day']){
        time.push(getLocalTime_LL(a));
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
                dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
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

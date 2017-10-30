/*
* @Author: Marte
* @Date:   2017-10-26 11:34:30
* @Last Modified by:   Marte
* @Last Modified time: 2017-10-26 11:35:50
*/

console.log('===微信行为评估js===')

//影响力
var influe_url='/qq_xnr_assessment/influence_qq/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',influe_url,influe);
function influe(data) {
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
var penetration_url='/qq_xnr_assessment/penetration_qq/?xnr_user_no='+ID_Num;
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
var safe_url='/qq_xnr_assessment/safe_qq/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',safe_url,safe);
function safe(data) {
    console.log(data);
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

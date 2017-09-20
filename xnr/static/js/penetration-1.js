var scoreUrl='/weibo_xnr_assessment/penetration_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
var defaultUrl='/weibo_xnr_assessment/penetration_total/?xnr_user_no='+ID_Num;
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
    //total_num、day_num、growth_rate
    console.log(data)
    if (isEmptyObject(data)){
        $('#penContent').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var time=[],fans_group=[];
        for (var i in data['fans_group']){
            fans_group.push(data['fans_group'][i]);
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
                data:['关注群体敏感度','粉丝群体敏感度','发布信息敏感度','社交反馈敏感度','预警上报敏感度'],
                width: '600',
                left:'center'
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
                    formatter: '{value}'
                }
            },
            series: [
                {
                    name:'关注群体敏感度',
                    type:'line',
                    data:follow_group,
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
                    name:'粉丝群体敏感度',
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
}


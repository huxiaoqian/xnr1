var scoreUrl='/weibo_xnr_assessment/influence_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
$('#container .quota .quota-opt .demo-label input').on('click',function () {
    var a=$(this).val();
    if (a=='all'){
        $('#quota-1').show();
        $('#quota-2').hide();
    }else {
        $('#quota-1').hide();
        $('#quota-2').show();
    }
})
var influe_url='/weibo_xnr_assessment/influence_total/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',influe_url,influe);
//总数量
function publicData(data) {
    var a=[];
    for (var b in data){
        a.push(data[b])
    }
    return a;
}
var time=[],growLEG=[],
    growthatData=[],growthfansData=[],growthcommentData=[],
    growthlikeData=[], growthprivateData=[],growthretweetData=[];
function influe(data) {
    //total_num、day_num、growth_rate
    //粉丝数   被转发   被评论   被点赞   被@  被私信
    console.log(data)
    if (isEmptyObject(data)){
        $('#quota-1').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var legend=[],atData=[],fansData=[],commentData=[],likeData=[],privateData=[],retweetData=[],
            totalAt=[],totalFans=[],totalComment=[],totallike=[],totalPrivate=[],totalRetweet=[];
        for (var t in data['day_num']['at']){time.push(getLocalTime(t))}
        for (var i in data['day_num']){
            if (i=='at'){legend.push('被@');atData=publicData(data['day_num'][i]);}
            else if (i=='comment'){legend.push('被评论');commentData=publicData(data['day_num'][i])}
            else if (i=='fans'){legend.push('粉丝');fansData=publicData(data['day_num'][i])}
            else if (i=='like'){legend.push('被点赞');likeData=publicData(data['day_num'][i])}
            else if (i=='private'){legend.push('被私信');privateData=publicData(data['day_num'][i])}
            else if (i=='retweet'){legend.push('被转发');retweetData=publicData(data['day_num'][i])}
        }
        for (var m in data['total_trend']){
            if (m=='at'){legend.push('被@总数');totalAt=publicData(data['total_trend'][m])}
            else if (m=='comment'){legend.push('被评论总数');totalComment=publicData(data['total_trend'][m])}
            else if (m=='fans'){legend.push('粉丝总数');totalFans=publicData(data['total_trend'][m])}
            else if (m=='like'){legend.push('被点赞总数');totallike=publicData(data['total_trend'][m])}
            else if (m=='private'){legend.push('被私信总数');totalPrivate=publicData(data['total_trend'][m])}
            else if (m=='retweet'){legend.push('被转发总数');totalRetweet=publicData(data['total_trend'][m])}
        }
        for (var h in data['growth_rate']){
            if (h=='at'){growLEG.push('被@增长率');growthatData=publicData(data['growth_rate'][h])}
            else if (h=='comment'){growLEG.push('被评论增长率');growthcommentData=publicData(data['growth_rate'][h])}
            else if (h=='fans'){growLEG.push('粉丝增长率');growthfansData=publicData(data['growth_rate'][h])}
            else if (h=='like'){growLEG.push('被点赞增长率');growthlikeData=publicData(data['growth_rate'][h])}
            else if (h=='private'){growLEG.push('被私信增长率');growthprivateData=publicData(data['growth_rate'][h])}
            else if (h=='retweet'){growLEG.push('被转发增长率');growthretweetData=publicData(data['growth_rate'][h])}
        };

        var myChart = echarts.init(document.getElementById('quota-1'),'dark');
        var option = {
            backgroundColor:'transparent',
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    crossStyle: {
                        color: '#999'
                    }
                }
            },
            toolbox: {
                feature: {
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            legend: {
                data:legend,
                width: '500',
                left:'center'
            },
            xAxis: [
                {
                    type: 'category',
                    data: time,
                    axisPointer: {
                        type: 'shadow'
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '数量',
                    min: 0,
                    max: 250,
                    interval: 50,
                    axisLabel: {
                        formatter: '{value} 人'
                    }
                },
                {
                    type: 'value',
                    name: '增加数',
                    min: 0,
                    max: 250,
                    interval: 50,
                    axisLabel: {
                        formatter: '{value} 人'
                    }
                },
            ],
            series: [
                {
                    name:'粉丝',
                    type:'line',
                    yAxisIndex: 1,
                    data:fansData
                },
                {
                    name:'被转发',
                    type:'line',
                    yAxisIndex: 1,
                    data:retweetData
                },
                {
                    name:'被评论',
                    type:'line',
                    yAxisIndex: 1,
                    data:commentData
                },
                {
                    name:'被点赞',
                    type:'line',
                    yAxisIndex: 1,
                    data:likeData
                },
                {
                    name:'被@',
                    type:'line',
                    yAxisIndex: 1,
                    data:atData
                },
                {
                    name:'被私信',
                    type:'line',
                    yAxisIndex: 1,
                    data:privateData
                },
                {
                    name:'粉丝增加数',
                    type:'bar',
                    data:totalFans
                },
                {
                    name:'被转发总数',
                    type:'bar',
                    data:totalRetweet
                },
                {
                    name:'被评论总数',
                    type:'bar',
                    data:totalComment
                },
                {
                    name:'被点赞总数',
                    type:'bar',
                    data:totallike
                },
                {
                    name:'被@总数',
                    type:'bar',
                    data:totalAt
                },
                {
                    name:'被私信总数',
                    type:'bar',
                    data:totalPrivate
                },
            ]
        };
        myChart.setOption(option);
        increase();
    }

}
//增长率
function increase() {
    var myChart = echarts.init(document.getElementById('quota-2'),'dark');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '增长率',
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:growLEG,
            width: '500',
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
                formatter: '{value} %'
            }
        },
        series: [
            {
                name:'被@增长率',
                type:'line',
                // smooth:true,
                data:growthatData,
                // itemStyle:{normal:{areaStyle:{type:'default'}}},
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
                name:'粉丝增长率',
                type:'line',
                // smooth:true,
                data:growthfansData,
                // itemStyle:{normal:{areaStyle:{type:'default'}}},
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
                name:'被评论增长率',
                type:'line',
                // smooth:true,
                data:growthcommentData,
                // itemStyle:{normal:{areaStyle:{type:'default'}}},
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
                name:'被转发增长率',
                type:'line',
                // smooth:true,
                data:growthretweetData,
                // itemStyle:{normal:{areaStyle:{type:'default'}}},
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
                name:'被私信增长率',
                type:'line',
                // smooth:true,
                data:growthprivateData,
                // itemStyle:{normal:{areaStyle:{type:'default'}}},
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
                name:'被点赞增长率',
                type:'line',
                // smooth:true,
                data:growthlikeData,
                // itemStyle:{normal:{areaStyle:{type:'default'}}},
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


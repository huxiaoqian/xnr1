var end=Date.parse(new Date())/1000;
var influe_7day_url='/weibo_xnr_manage/lookup_xnr_assess_info/?xnr_user_no='+ID_Num+
    '&start_time='+getDaysBefore('7')+'&end_time='+end+'&assess_type=influence';
public_ajax.call_request('get',influe_7day_url,influe_7day);
function influe_7day(data) {
    console.log(data);
    var nearTime=[],nearData=[];
    $.each(data,function (index,item) {
        nearTime.push(item['date_time'][0]);
        nearData.push(item['influence'][0]);
    })
    var myChart = echarts.init(document.getElementById('near_7_day'),'dark');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '影响力一周变化趋势图',
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
                name:'影响力分值',
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
};

var scoreUrl='/weibo_xnr_assessment/influence_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
$('#container .quota .quota-opt .demo-label input').on('click',function () {
    var a=$(this).val();
    if (a=='todayValue'){
        $('#quota-1').show();
        $('#quota-2').hide();
        $('#quota-3').hide();
    }else if (a=='totalValue') {
        $('#quota-1').hide();
        $('#quota-2').hide();
        $('#quota-3').show();
    }else {
        $('#quota-1').hide();
        $('#quota-2').show();
        $('#quota-3').hide();
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
    growthlikeData=[], growthprivateData=[],growthretweetData=[],
    legend2=[],totalAt2=[],totalFans2=[],totalComment2=[],totallike2=[],totalPrivate2=[],totalRetweet2=[];
function influe(data) {
    //total_num、day_num、growth_rate
    //粉丝数   被转发   被评论   被点赞   被@  被私信
    console.log(data)
    if (isEmptyObject(data)){
        $('#quota-1').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var legend=[],atData=[],fansData=[],commentData=[],likeData=[],privateData=[],retweetData=[];
        for (var t in data['day_num']['at']){time.push(getLocalTime(t))}
        for (var i in data['day_num']){
            if (i=='at'){legend.push('被@');atData=publicData(data['day_num'][i]);}
            else if (i=='comment'){legend.push('被评论');commentData=publicData(data['day_num'][i])}
            else if (i=='fans'){legend.push('粉丝');fansData=publicData(data['day_num'][i])}
            else if (i=='like'){legend.push('被点赞');likeData=publicData(data['day_num'][i])}
            else if (i=='private'){legend.push('被私信');privateData=publicData(data['day_num'][i])}
            else if (i=='retweet'){legend.push('被转发');retweetData=publicData(data['day_num'][i])}
        }
        var myChart = echarts.init(document.getElementById('quota-1'),'dark');
        var option = {
            backgroundColor:'transparent',
            title : {
                text: '',
                subtext: ''
            },
            tooltip : {
                trigger: 'axis'
            },
            legend: {
                data:legend
            },
            toolbox: {
                show : true,
                feature : {
                    dataView : {show: true, readOnly: false},
                    magicType : {show: true, type: ['line', 'bar']},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            xAxis : [
                {
                    type : 'category',
                    data : time
                }
            ],
            yAxis : [
                {
                    type : 'value'
                }
            ],
            series : [
                {
                    name:'粉丝',
                    type:'bar',
                    data:fansData,
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
                },
                {
                    name:'被转发',
                    type:'bar',
                    data:retweetData,
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
                },
                {
                    name:'被评论',
                    type:'bar',
                    data:commentData,
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
                },
                {
                    name:'被点赞',
                    type:'bar',
                    data:likeData,
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
                },
                {
                    name:'被@',
                    type:'bar',
                    data:atData,
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
                },
                {
                    name:'被私信',
                    type:'bar',
                    data:privateData,
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
                },
            ]
        };
        myChart.setOption(option);
        for (var m in data['total_trend']){
            if (m=='at'){legend2.push('被@总数');totalAt2=publicData(data['total_trend'][m])}
            else if (m=='comment'){legend2.push('被评论总数');totalComment2=publicData(data['total_trend'][m])}
            else if (m=='fans'){legend2.push('粉丝总数');totalFans2=publicData(data['total_trend'][m])}
            else if (m=='like'){legend2.push('被点赞总数');totallike2=publicData(data['total_trend'][m])}
            else if (m=='private'){legend2.push('被私信总数');totalPrivate2=publicData(data['total_trend'][m])}
            else if (m=='retweet'){legend2.push('被转发总数');totalRetweet2=publicData(data['total_trend'][m])}
        }
        for (var h in data['growth_rate']){
            if (h=='at'){growLEG.push('被@增长率');growthatData=publicData(data['growth_rate'][h])}
            else if (h=='comment'){growLEG.push('被评论增长率');growthcommentData=publicData(data['growth_rate'][h])}
            else if (h=='fans'){growLEG.push('粉丝增长率');growthfansData=publicData(data['growth_rate'][h])}
            else if (h=='like'){growLEG.push('被点赞增长率');growthlikeData=publicData(data['growth_rate'][h])}
            else if (h=='private'){growLEG.push('被私信增长率');growthprivateData=publicData(data['growth_rate'][h])}
            else if (h=='retweet'){growLEG.push('被转发增长率');growthretweetData=publicData(data['growth_rate'][h])}
        };
        total();
        increase();
    }

}
//累计值
function total() {
    var myChart = echarts.init(document.getElementById('quota-3'),'dark');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '',
            subtext: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:legend2,
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
                formatter: '{value} 人'
            }
        },
        series: [
            {
                name:'粉丝总数',
                type:'line',
                data:totalFans2,
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
                name:'被转发总数',
                type:'line',
                data:totalRetweet2,
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
                name:'被评论总数',
                type:'line',
                data:totalComment2,
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
                name:'被点赞总数',
                type:'line',
                data:totallike2,
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
                name:'被@总数',
                type:'line',
                data:totalAt2,
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
                name:'被私信总数',
                type:'line',
                data:totalPrivate2,
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
                formatter: '{value}'
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


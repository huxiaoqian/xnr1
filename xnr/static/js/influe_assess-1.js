var scoreUrl='/weibo_xnr_assessment/influence_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
$('#container .type_page #myTabs li').on('click',function () {
    var mid=$(this).attr('midurl');
    var influe_url='/weibo_xnr_assessment/'+mid+'/?xnr_user_no='+ID_Num;
    public_ajax.call_request('get',influe_url,influe);
});
$('#container .influence .fans-1 .demo-label input').on('click',function () {
    var a=$(this).val();
    if (a=='all'){
        $('#fans-2').show();
        $('#fans-3').hide();
    }else {
        $('#fans-2').hide();
        $('#fans-3').show();
    }
})
var influe_1_url='/weibo_xnr_assessment/influ_fans_num/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',influe_1_url,influe);
//总数量
var time=[],growth=[];
function influe(data) {
    //total_num、day_num、growth_rate
    console.log(data)
    if (isEmptyObject(data)){
        $('#fans-2').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var dayData=[],total=[];
        for (var i in data['day_num']){
            dayData.push(data['day_num'][i]);
            time.push(getLocalTime(i));
        };
        for (var j in data['total_num']){total.push(data['total_num'][j])};
        for (var h in data['growth_rate']){growth.push(data['growth_rate'][h])};
        var myChart = echarts.init(document.getElementById('fans-2'),'dark');
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
                data:['粉丝数','粉丝增加总数']
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
                    name: '总数',
                    min: 0,
                    max: 250,
                    interval: 50,
                    axisLabel: {
                        formatter: '{value} 人'
                    }
                },
                {
                    type: 'value',
                    name: '增长数',
                    min: 0,
                    max: 25,
                    interval: 5,
                    axisLabel: {
                        formatter: '{value} 人'
                    }
                }
            ],
            series: [
                {
                    name:'粉丝数',
                    type:'line',
                    yAxisIndex: 1,
                    data:total
                },
                {
                    name:'粉丝增加总数',
                    type:'bar',
                    data:dayData
                },
            ]
        };
        myChart.setOption(option);
        increase();
    }

}
//增长率
function increase() {
    var myChart = echarts.init(document.getElementById('fans-3'),'dark');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '增长率',
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['增长率']
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
                name:'增长率',
                type:'line',
                // smooth:true,
                data:growth,
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


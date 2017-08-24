var scoreUrl='/weibo_xnr_assessment/influence_mark/?xnr_user_no='+nowUser;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
$('#container .type_page #myTabs li').on('click',function () {
    var mid=$(this).attr('midurl');
    var influe_url='/weibo_xnr_assessment/'+mid+'/?xnr_user_no='+nowUser;
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
var influe_1_url='/weibo_xnr_assessment/influ_fans_num/?xnr_user_no='+nowUser;
public_ajax.call_request('get',influe_1_url,influe);


//总数量
function influe(data) {
    //total_num、day_num、growth_rate
    if (!isEmptyObject(data)){
        $('#fans-2').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
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
                data:['粉丝数','粉丝增加总数','增长率']
            },
            xAxis: [
                {
                    type: 'category',
                    data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
                    axisPointer: {
                        type: 'shadow'
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '水量',
                    min: 0,
                    max: 250,
                    interval: 50,
                    axisLabel: {
                        formatter: '{value} ml'
                    }
                },
                {
                    type: 'value',
                    name: '温度',
                    min: 0,
                    max: 25,
                    interval: 5,
                    axisLabel: {
                        formatter: '{value} °C'
                    }
                }
            ],
            series: [
                {
                    name:'粉丝数',
                    type:'bar',
                    data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
                },
                {
                    name:'粉丝增加总数',
                    type:'bar',
                    data:[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
                },
                {
                    name:'增长率',
                    type:'line',
                    yAxisIndex: 1,
                    data:[2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2]
                }
            ]
        };
        myChart.setOption(option);
        increase(data);
    }

}
//增长率
function increase(data) {
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
            data: ['周一','周二','周三','周四','周五','周六','周日']
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} °C'
            }
        },
        series: [
            {
                name:'增长率',
                type:'line',
                // smooth:true,
                data:[11, 11, 15, 13, 12, 13, 10],
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


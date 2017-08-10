// public_ajax.call_request('get',infoWeibo_url,infoWeibo);
// public_ajax.call_request('get',speechWeibo_url,speechWeibo);

//折线图
var myChart = echarts.init(document.getElementById(''));
// 指定图表的配置项和数据
var option = {
    title: {
        text: '未来一周气温变化',
        textStyle: {color: '#fff',},
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data:['最高气温','最低气温'],
        textStyle: {color: '#fff',},
    },
    toolbox: {
        show: true,
        feature: {
            dataZoom: {
                yAxisIndex: 'none'
            },
            magicType: {type: ['line', 'bar']},
            restore: {},
            saveAsImage: {}
        },
        iconStyle:{
            normal:{color:'#fff',borderColor:'#fff'},
        }
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        axisLine:{lineStyle: {color:'#fff'}},
        data: ['周一','周二','周三','周四','周五','周六','周日']
    },
    yAxis: {
        type: 'value',
        axisLine:{lineStyle: {color:'#fff'}},
        axisLabel: {
            formatter: '{value} °C'
        }
    },
    series: [
        {
            name:'最高气温',
            type:'line',
            smooth:true,
            data:[11, 11, 15, 13, 12, 13, 10],
            itemStyle:{normal:{areaStyle:{type:'default'}}},
            areaStyle: {normal:{color:'red',opacity:'0.5'}},
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
            name:'最低气温',
            type:'line',
            data:[1, -2, 2, 5, 3, 2, 0],
            markPoint: {
                data: [
                    {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'},
                    [{
                        symbol: 'none',
                        x: '90%',
                        yAxis: 'max'
                    }, {
                        symbol: 'circle',
                        label: {
                            normal: {
                                position: 'start',
                                formatter: '最大值'
                            }
                        },
                        type: 'max',
                        name: '最高点'
                    }]
                ]
            }
        }
    ]
};
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);

var scoreUrl='/weibo_xnr_assessment/penetration_mark/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',scoreUrl,score);
function score(data) {
    $('.title .tit-2 .score').text(data);
}
var titleName='关注群体敏感度';
$('#container .type_page #myTabs li').on('click',function () {
    var mid=$(this).attr('midurl');
    titleName=$(this).find('a').text().toString().trim();
    if (mid=='pene_feedback_sensitive'){$('.social-1-opt').show()}else {$('.social-1-opt').hide()};
    var penetration_url='/weibo_xnr_assessment/'+mid+'/?xnr_user_no='+ID_Num;
    public_ajax.call_request('get',penetration_url,penetration);
});
var defaultUrl='/weibo_xnr_assessment/pene_follow_group_sensitive/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',defaultUrl,penetration);
//=====
$('.social-1-opt label.soc input').on('click',function() {
    var flag=$(this).val();
    var social_url='/weibo_xnr_assessment/pene_feedback_sensitive/?xnr_user_no='+ID_Num+'&sort_item='+flag;
    public_ajax.call_request('get',social_url,penetration);
});
//画图
function penetration(data) {
    //total_num、day_num、growth_rate
    if (isEmptyObject(data['sensitive_info'])){
        $('#penContent').text('暂无数据').css({textAlign:'center',lineHeight:'400px',fontSize:'22px'});
    }else {
        var time=[],totData=[];
        for (var i in data['sensitive_info']){
            totData.push(data['sensitive_info'][i]);
            time.push(getLocalTime(i));
        };
        var myChart = echarts.init(document.getElementById('penContent'),'dark');
        var option = {
            backgroundColor:'transparent',
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:[titleName]
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
                    name:titleName,
                    type:'line',
                    data:totData,
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


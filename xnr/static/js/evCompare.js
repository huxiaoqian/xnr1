//虚拟人列表
var xnrList_url="/weibo_xnr_create/show_weibo_xnr/?submitter="+admin;
public_ajax.call_request('get',xnrList_url,xnrList);
function xnrList(data) {
    var str='';
    for (var k in data){
        var name=''
        if (data[k]==''||data[k]=='unknown'){
            name='无昵称';
        }
        str+=
            '<label class="demo-label" title="'+data[k]+'">'+
            '   <input class="demo-radio" type="checkbox" name="com1" onclick="joinID(\''+k+'\')" value='+k+'>'+
            '   <span class="demo-checkbox demo-radioInput"></span> '+data[k]+'（'+k+'）'+
            '</label>';
    }
    $('.compareContent .com-1-choose').html(str);
};
//========
var end_time=yesterday();
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
        var startTime;
        if (_val==0){
            startTime=todayTimetamp();
        }else {
            startTime=getDaysBefore(_val);
        };
        var compareData_url='';
        // public_ajax.call_request('get',compareData_url,compareData);
    }
});
$('.sureTime').on('click',function () {
    var s=$('#start_1').val();
    var d=$('#end_1').val();
    if (s==''||d==''){
        $('#successfail p').text('时间不能为空。');
        $('#successfail').modal('show');
    }else {
        var start =(Date.parse(new Date(s))/1000);
        var end = (Date.parse(new Date(d))/1000);
        var compareData_url='';
        // public_ajax.call_request('get',compareData_url,compareData);
    }
});
function compareData() {
    var myChart = echarts.init(document.getElementById('compare'),'chalk');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: '',
            left: ''
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data:['WXNR0044-影响力分值','WXNR0004-影响力分值','WXNR0044-渗透力分值','WXNR0004-渗透力分值']
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                magicType: {type: ['line', 'bar']},
            }
        },
        xAxis:  {
            type: 'category',
            boundaryGap: false,
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        },
        series : [
            {
                name:'WXNR0044-影响力分值',
                type:'line',
                smooth: true,areaStyle: {},
                data:[11,8,5,7,11,6,17],
            },
            {
                name:'WXNR0004-影响力分值',
                type:'line',smooth: true,areaStyle: {},
                data:[9,4,17,8,7,21,15],
            },
            {
                name:'WXNR0044-渗透力分值',
                type:'line',smooth: true,areaStyle: {},
                data:[12,8,15,7,11,6,14,17],
            },
            {
                name:'WXNR0004-渗透力分值',
                type:'line',smooth: true,areaStyle: {},
                data:[22,6,11,9,11,16,11],
            },
        ]
    };
    myChart.setOption(option);
};
compareData();
//=====
var xnr_id=[];
function joinID(_id) {
    xnr_id.push(_id);
    if(xnr_id.length>3){

    }
    console.log(xnr_id)
}
$('.sureCompare').on('click',function () {
    $('.compare .vs').html(xnr_id.join('&nbsp;&nbsp;&nbsp;&nbsp;'));
});
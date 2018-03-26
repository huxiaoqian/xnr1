//虚拟人列表
var thisID=localStorage.getItem('user');
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
            '   <input class="demo-radio" type="checkbox" name="com1" value='+k+'>'+
            '   <span class="demo-checkbox demo-radioInput"></span> '+data[k]+'（'+k+'）'+
            '</label>';
    }
    $('.compareContent .com-1-choose').html(str);
    $('.compareContent .com-1-choose input[value='+thisID+']').attr('checked','true');
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
        $('#errorInfor p').text('时间不能为空。');
        $('#errorInfor').modal('show');
    }else {
        var start =(Date.parse(new Date(s))/1000);
        var end = (Date.parse(new Date(d))/1000);
        var compareData_url='';
        // public_ajax.call_request('get',compareData_url,compareData);
    }
});

//===============================================
function jugeXnr() {
    var xnr_id=[];
    $(".compareContent .com-1-choose input:checkbox:checked").each(function (index,item) {
        xnr_id.push($(this).val());
    });
    return xnr_id;
}
$('.sureCompare').on('click',function () {
    var len=jugeXnr().length;
    if(!(len<6&&len>1)){
        $('#errorInfor p').text('请检查您选择的虚拟人（请保证最少2个，最多5个）');
        $('#errorInfor').modal('show');
        return false;
    }else {
        var xnrList=jugeXnr();
        $('.compare .vs').html(xnrList.join('&nbsp;&nbsp;&nbsp;'));
    };
});
//=============对比内容========
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
// 影响力评估
tableAry('table-1',[{a:2,b:3}],true,false,false);
// 渗透力评估
tableAry('table-2',[{a:2,b:3}],false,true,false);
// 安全性
tableAry('table-3',[{a:2,b:3}],false,false,true);
//表格
function tableAry(_id,data,FT1,FT2,FT3) {
    $('#'+_id).bootstrapTable('load', data);
    $('#'+_id).bootstrapTable({
        data:data,
        search: false,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [15,20,25],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: false,//回车搜索
        showRefresh: false,//刷新按钮
        showColumns: false,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:false,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            {
                title: "虚拟人",//标题
                field: "xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.xnr_user_no==''||row.xnr_user_no=='null'||row.xnr_user_no=='unknown'){
                        return '未知';
                    }else {
                        return row.xnr_user_no;
                    };
                }
            },
            //-----影响力
            {
                title: "被评论量",//标题
                field: "a",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.a==''||row.a=='null'||row.a=='unknown'){
                        return 0;
                    }else {
                        return row.a;
                    };
                }
            },
            {
                title: "被点赞",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {

                }
            },
            {
                title: "被私信",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {

                }
            },
            {
                title: "被@数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
            },
            {
                title: "被转发",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
            },
            //-----渗透力
            {
                title: "关注群体敏感度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
            },
            {
                title: "粉丝群体敏感度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
            },
            {
                title: "发布信息敏感度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
            },
            {
                title: "社交反馈敏感度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
            },
            {
                title: "预警上报敏感度",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
            },
            //------安全性
            {
                title: "发帖量",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
            },
        ],
    });
};
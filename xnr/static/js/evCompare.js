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
var dim;
$('.sureCompare').on('click',function () {
    var len=jugeXnr().length;
    if(!(len<6&&len>1)){
        $('#errorInfor p').text('请检查您选择的虚拟人（请保证最少2个，最多5个）');
        $('#errorInfor').modal('show');
        return false;
    }else {
        dim=$('.com-2-choose input:checked').val();
        $('.chartContent').show();
        var TIME=$('.choosetime input:checked').val();
        chooseTime(TIME);
    };
});
//-===时间选择=========
function chooseTime(TIME) {
    var xnrList=jugeXnr();
    $('.compare .vs').html(xnrList.join('&nbsp;&nbsp;&nbsp;'));
    var mid='',last='';
    if (TIME!='mize'){
        if (TIME==0){mid='_today'}else {
            last='&start_time='+getDaysBefore(TIME)+'&end_time='+end_time;
        }
    }else {
        var s=$('#start_1').val();
        var d=$('#end_1').val();
        if (s==''||d==''){
            $('#successfail p').text('时间不能为空。');
            $('#successfail').modal('show');
            return false;
        }else {
            last='&start_time='+(Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        }
    };
    if(dim=='influence'){
        $('.table-1').show();$('.table-2').hide();$('.table-3').hide();_id='table-1';
    }else if (dim=='penetration'){
        $('.table-1').hide();$('.table-2').show();$('.table-3').hide();_id='table-2';
    }else if (dim=='safe'){
        $('.table-1').hide();$('.table-2').hide();$('.table-3').show();_id='table-3';
    }
    var compareData_url='/weibo_xnr_assessment/compare_assessment'+mid+'/?xnr_user_no_list='+xnrList.join(',')+
        '&dim='+dim+last;
    public_ajax.call_request('get',compareData_url,compareData);
}
$('.choosetime .demo-label input').on('click',function () {
    $('.chartContent').hide();
    $('.load').show();
    var _val=$(this).val();
    if (_val=='mize'){
        $('#start_1').show();
        $('#end_1').show();
        $('.sureTime').show();
    }else {
        $('#start_1').hide();
        $('#end_1').hide();
        $('.sureTime').hide();
        chooseTime(_val);
    }
});
//=============对比内容========
function compareData(data) {
    var trendData=data['trend'];
    var legendData=Object.keys(trendData);
    var time=[],sriesData=[];
    Object.keys(trendData[legendData[0]]).forEach(function(t,s){time.push(getLocalTime(t))});
    $.each(legendData,function (index,item) {
        sriesData.push(
            {
                name:item,
                type:'line',
                smooth: true,areaStyle: {},
                data:Object.values(trendData[item]),
            }
        )
    })
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
            data:legendData
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
            data: time
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} '
            }
        },
        series : sriesData
    };
    myChart.setOption(option);
    if(dim=='influence'){
        FT1=true,FT2=false,FT3=false;
    }else if (dim=='penetration'){
        FT1=false,FT2=true,FT3=false;
    }else if (dim=='safe'){
        FT1=false,FT2=false,FT3=true;
    }
    tableAry(data['trend']);
};
// 影响力评估
// tableAry('table-1',[{a:2,b:3}],true,false,false);
// 渗透力评估
// tableAry('table-2',[{a:2,b:3}],false,true,false);
// 安全性
// tableAry('table-3',[{a:2,b:3}],false,false,true);
//表格
var _id='',FT1,FT2,FT3;
function tableAry(data) {
    console.log(data);
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
                field: "comment_total_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.comment_total_num=='null'||row.comment_total_num=='unknown'){
                        return 0;
                    }else {
                        return row.comment_total_num;
                    };
                }
            },
            {
                title: "被点赞",//标题
                field: "like_total_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.like_total_num=='null'||row.like_total_num=='unknown'){
                        return 0;
                    }else {
                        return row.like_total_num;
                    };
                }
            },
            {
                title: "被私信",//标题
                field: "private_total_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.private_total_num=='null'||row.private_total_num=='unknown'){
                        return 0;
                    }else {
                        return row.private_total_num;
                    };
                }
            },
            {
                title: "被@数",//标题
                field: "at_total_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.at_total_num=='null'||row.at_total_num=='unknown'){
                        return 0;
                    }else {
                        return row.at_total_num;
                    };
                }
            },
            {
                title: "被转发",//标题
                field: "retweet_total_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT1,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.retweet_total_num=='null'||row.retweet_total_num=='unknown'){
                        return 0;
                    }else {
                        return row.retweet_total_num;
                    };
                }
            },
            //-----渗透力
            {
                title: "关注群体敏感度",//标题
                field: "follow_group_sensitive_info",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.follow_group_sensitive_info=='null'||row.follow_group_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.follow_group_sensitive_info;
                    };
                }
            },
            {
                title: "粉丝群体敏感度",//标题
                field: "fans_group_sensitive_info",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.fans_group_sensitive_info=='null'||row.fans_group_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.fans_group_sensitive_info;
                    };
                }
            },
            {
                title: "发布信息敏感度",//标题
                field: "self_info_sensitive_info",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.self_info_sensitive_info=='null'||row.self_info_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.self_info_sensitive_info;
                    };
                }
            },
            {
                title: "社交反馈敏感度",//标题
                field: "feedback_total_sensitive_info",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.feedback_total_sensitive_info=='null'||row.feedback_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.feedback_total_sensitive_info;
                    };
                }
            },
            {
                title: "预警上报敏感度",//标题
                field: "warning_report_total_sensitive_info",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT2,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.warning_report_total_sensitive_info=='null'||row.warning_report_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.warning_report_total_sensitive_info;
                    };
                }
            },
            //------安全性
            {
                title: "总发帖量",//标题
                field: "total_post_sum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.total_post_sum=='null'||row.total_post_sum=='unknown'){
                        return 0;
                    }else {
                        return row.total_post_sum;
                    };
                }
            },
            {
                title: "日常发帖",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.warning_report_total_sensitive_info=='null'||row.warning_report_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.warning_report_total_sensitive_info;
                    };
                }
            },
            {
                title: "热点跟随",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.warning_report_total_sensitive_info=='null'||row.warning_report_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.warning_report_total_sensitive_info;
                    };
                }
            },
            {
                title: "业务发帖",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.warning_report_total_sensitive_info=='null'||row.warning_report_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.warning_report_total_sensitive_info;
                    };
                }
            },
            {
                title: "跟随转发",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.warning_report_total_sensitive_info=='null'||row.warning_report_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.warning_report_total_sensitive_info;
                    };
                }
            },
            {
                title: "其他",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:FT3,//控制显示隐藏
                formatter: function (value, row, index) {
                    if (row.warning_report_total_sensitive_info=='null'||row.warning_report_total_sensitive_info=='unknown'){
                        return 0;
                    }else {
                        return row.warning_report_total_sensitive_info;
                    };
                }
            },
        ],
    });
    $('.chartContent').show();
    $('.load').hide();
};
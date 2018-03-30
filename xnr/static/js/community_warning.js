// 跟踪社区列表
var track_community_data = [
    {
        a:'1',
        b:'西安直播',
        c:'33',
        d:'86',
        e:'24',
        f:'7',
        g:'4361',
        h:'58',
        i:'21',
        g:'5',
        k:'965',
    },
    {
        a:'2',
        b:'民运人士',
        c:'643',
        d:'457',
        e:'8865',
        f:'342',
        g:'25',
        h:'886',
        i:'21',
        g:'34',
        k:'967',
    },
]

function trackCommunity(data){
    $('#track-community').bootstrapTable('load', data);
    $('#track-community').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize:10,//单页记录数
            pageList: [15,20,25],//分页步进值
            sidePagination: "client",//服务端分页
            searchAlign: "left",
            searchOnEnterKey: true,//回车搜索
            showRefresh: false,//刷新按钮
            showColumns: false,//列选择按钮
            buttonsAlign: "right",//按钮对齐方式
            locale: "zh-CN",//中文支持
            detailView: false,
            showToggle:false,
            sortName:'bci',
            sortOrder:"desc",
            columns: [
                /*
                {
                    title: "编号",//标题
                    field: "a",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.a == '' || row.a == 'null' || row.a == 'unknown'||!row.a) {
                            return '未知';
                        } else {
                            return row.a;
                        };
                    }
                },
                 */
                {
                    title: "社区名称",//标题
                    field: "b",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.b == '' || row.b == 'null' || row.b == 'unknown'||!row.b) {
                            return '未知';
                        } else {
                            var str = '<div class="community-name-box"><span class="community-name">'+ row.b +'</span></div>'
                            // return row.b;
                            return str;
                        };
                    }
                },
                {
                    title: "人数",//标题
                    field: "c",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.c == '' || row.c == 'null' || row.c == 'unknown'||!row.c||row.c.length==0) {
                            return '未知';
                        } else {
                            return row.c;
                        };
                    }
                },
                /*
                {
                    title: "紧密度",//标题
                    field: "d",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.d == '' || row.d == 'null' || row.d == 'unknown'||!row.d) {
                            return '未知';
                        } else {
                            return row.d;
                        };
                    }
                },
                 */
                {
                    title: "平均聚集系数",//标题
                    field: "e",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.e==''||row.e=='null'||row.e=='unknown'||!row.e){
                            return '未知';
                        }else {
                            return row.e;
                        }
                    }
                },
                {
                    title: "最大影响力",//标题
                    field: "f",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.f==''||row.f=='null'||row.f=='unknown'||!row.f){
                            return '未知';
                        }else {
                            return row.f;
                        }
                    }
                },

                {
                    title: "平均影响力",//标题
                    field: "g",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.g==''||row.g=='null'||row.g=='unknown'||!row.g){
                            return '未知';
                        }else {
                            return row.g;
                        }
                    }
                },
                {
                    title: "最大敏感度",//标题
                    field: "h",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.h==''||row.h=='null'||row.h=='unknown'||!row.h){
                            return '未知';
                        }else {
                            return row.h;
                        }
                    }
                },
                {
                    title: "平均敏感度",//标题
                    field: "i",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.i==''||row.i=='null'||row.i=='unknown'||!row.i){
                            return '未知';
                        }else {
                            return row.i;
                        }
                    }
                },
                {
                    title: "预警级别",//标题
                    field: "g",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.g==''||row.g=='null'||row.g=='unknown'||!row.g){
                            return '未知';
                        }else {
                            return row.g;
                        }
                    }
                },
                {
                    title: "跟踪详情",//标题
                    field: "k",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;color:white;margin-right:15px;" onclick="jumpFrame(\''+row.entity_name+'\',event)" title="社区详情"><i class="icon icon-file-alt"></i></span>'+
                            '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.entity_name+'\',1,event)" title="预警详情"><i class="icon icon-warning-sign"></i></span>';
                    }
                },
            ],
    });
    $('#track-community p').slideUp(30);

    // 点击行
    $('#track-community').on('click-row.bs.table', function (row,field) {
        // 核心人物列表
        $('#person-list').show();
        show_influ_users('person-list',person_list_data)
        // 关键词
        $('#keyword').show();
        basic_1();
        // 敏感度和影响力分布
        $('#influence').show().siblings('#person-list');
        influence_lef();
        influence_rig();
    });
}
trackCommunity(track_community_data);

// 跳转社区详情页
function jumpFrame(name,e){
    // 阻止默认事件
    e.stopPropagation();
    var html = '/monitor/communityDetails';
    window.location.href = html;
}
// 跳转预警详情页
function jumpFrame_1(name, flag, e){
    // 阻止默认事件
    e.stopPropagation();
    var html = '/monitor/communityWaringdetails?flag='+flag;
    window.location.href = html;
}

// 核心人物列表
function show_influ_users(div_name,data){
    $('#' + div_name).empty();
    var html = '';
    if(data.length!=0){
    html += '<table class="table table-striped table-hover" style="font-size:10px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">天数</th></tr>';
    for (var i = 0; i < data.length; i++) {
       html += '<tr><th style="text-align:center">' + data[i].id + '</th><th style="text-align:center">' + data[i].name + '</th><th style="text-align:center">' + data[i].day + '</th></tr>';
    };
    html += '</table>';
    }else{
        html += '暂无数据';
    }
    $('#'+div_name).append(html);
}
var person_list_data = [
    {id:1,name:'羊城晚报',day:20},
    {id:1,name:'羊城晚报',day:20},
    {id:1,name:'羊城晚报',day:20},
    {id:1,name:'羊城晚报',day:20},
    {id:1,name:'羊城晚报',day:20},
]
show_influ_users('person-list',person_list_data)
function basic_1(){
    var myChart = echarts.init(document.getElementById('keyword'),'chalk');
    var option = {
        title: {
            show:false,
            text: '微话题关键词云',
            textStyle:{
                color:'#fff'
            }
        },
        tooltip: {
            show: true
        },
        series: [{
            name: '微话题',
            type: 'wordCloud',
            size: ['80%', '80%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            textStyle : {
                normal : {
                    fontFamily:'sans-serif',
                    color : function() {
                        return 'rgb('
                            + [ Math.round(Math.random() * 160),
                                Math.round(Math.random() * 160),
                                Math.round(Math.random() * 160) ]
                                .join(',') + ')';
                    }
                },
                emphasis : {
                    shadowBlur : 5,  //阴影距离
                    shadowColor : '#333'  //阴影颜色
                }
            },
            data:
                [{name: "Lord", value: 1133}, {name: "Wrong", value: 1033}, {name: "Similar", value: 1033},
                    {name: "Disappointingly", value: 1033}, {name: "Humorless", value: 1033},
                    {name: "insulting", value: 1033}, {name: "Flat", value: 1033},
                    {name: "apparently", value: 1033}, {name: "mindless", value: 1033}, {name: "convenient", value: 1033}, {name: "stale", value: 1033}, {name: "disaster", value: 1033}, {name: "routine", value: 1033}, {name: "missed", value: 1033}, {name: "mediocre", value: 1033}, {name: "shaky", value: 1033}, {name: "amateurish", value: 1033}, {name: "trite", value: 1033}, {name: "horrible", value: 1033}, {name: "pandering", value: 1033}, {name: "hollow", value: 1033}, {name: "kept", value: 1033}, {name: "stupid", value: 1033}, {name: "scattered", value: 1033}, {name: "doldrums", value: 1033}]
        }]
    };
    myChart.setOption(option);
}


// 新发现社区列表
var new_track_community_data = [
    {
        a:'1',
        b:'西安直播',
        c:'33',
        d:'86',
        e:'24',
        f:'7',
        g:'4361',
        h:'58',
        i:'21',
        g:'5',
        k:'965',
    },
    {
        a:'2',
        b:'民运人士',
        c:'643',
        d:'457',
        e:'8865',
        f:'342',
        g:'25',
        h:'886',
        i:'21',
        g:'34',
        k:'967',
    },
]

function newtrackCommunity(data){
    $('#new-track-community').bootstrapTable('load', data);
    $('#new-track-community').bootstrapTable({
            data:data,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize:10,//单页记录数
            pageList: [15,20,25],//分页步进值
            sidePagination: "client",//服务端分页
            searchAlign: "left",
            searchOnEnterKey: true,//回车搜索
            showRefresh: false,//刷新按钮
            showColumns: false,//列选择按钮
            buttonsAlign: "right",//按钮对齐方式
            locale: "zh-CN",//中文支持
            detailView: false,
            showToggle:false,
            sortName:'bci',
            sortOrder:"desc",
            columns: [
                /*
                {
                    title: "编号",//标题
                    field: "a",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.a == '' || row.a == 'null' || row.a == 'unknown'||!row.a) {
                            return '未知';
                        } else {
                            return row.a;
                        };
                    }
                },
                 */
                {
                    title: "社区名称",//标题
                    field: "b",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.b == '' || row.b == 'null' || row.b == 'unknown'||!row.b) {
                            return '未知';
                        } else {
                            return row.b;
                        };
                    }
                },
                {
                    title: "人数",//标题
                    field: "c",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.c == '' || row.c == 'null' || row.c == 'unknown'||!row.c||row.c.length==0) {
                            return '未知';
                        } else {
                            return row.c;
                        };
                    }
                },
                /*
                {
                    title: "紧密度",//标题
                    field: "d",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.d == '' || row.d == 'null' || row.d == 'unknown'||!row.d) {
                            return '未知';
                        } else {
                            return row.d;
                        };
                    }
                },
                 */
                {
                    title: "平均聚集系数",//标题
                    field: "e",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.e==''||row.e=='null'||row.e=='unknown'||!row.e){
                            return '未知';
                        }else {
                            return row.e;
                        }
                    }
                },
                {
                    title: "预警原因",//标题
                    field: "d",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.d == '' || row.d == 'null' || row.d == 'unknown'||!row.d) {
                            return '未知';
                        } else {
                            return row.d;
                        };
                    }
                },

                {
                    title: "最大影响力",//标题
                    field: "f",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.f==''||row.f=='null'||row.f=='unknown'||!row.f){
                            return '未知';
                        }else {
                            return row.f;
                        }
                    }
                },

                {
                    title: "平均影响力",//标题
                    field: "g",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.g==''||row.g=='null'||row.g=='unknown'||!row.g){
                            return '未知';
                        }else {
                            return row.g;
                        }
                    }
                },
                {
                    title: "最大敏感度",//标题
                    field: "h",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.h==''||row.h=='null'||row.h=='unknown'||!row.h){
                            return '未知';
                        }else {
                            return row.h;
                        }
                    }
                },
                {
                    title: "平均敏感度",//标题
                    field: "i",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.i==''||row.i=='null'||row.i=='unknown'||!row.i){
                            return '未知';
                        }else {
                            return row.i;
                        }
                    }
                },
                {
                    title: "综合评分",//标题
                    field: "g",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row.g==''||row.g=='null'||row.g=='unknown'||!row.g){
                            return '未知';
                        }else {
                            return row.g;
                        }
                    }
                },
                {
                    title: "社区详情",//标题
                    field: "k",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<span style="cursor:pointer;color:white;margin-right:15px;" onclick="jumpFrame(\''+row.entity_name+'\',event)" title="社区详情"><i class="icon icon-file-alt"></i></span>'+
                            '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.entity_name+'\',0,event)" title="预警详情"><i class="icon icon-warning-sign"></i></span>';
                    }
                },
            ],
    });
    $('#new-track-community p').slideUp(30);
}

newtrackCommunity(new_track_community_data)
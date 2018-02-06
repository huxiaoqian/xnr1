// 人数变化图
    function peopleNum(){
        var myChart = echarts.init(document.getElementById('people-num'),'dark');
        var option = {
            backgroundColor:'transparent',
            title: {
                text: '人数变化图',
                // subtext: '纯属虚构'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['最高人数','最低人数']
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
                    // formatter: '{value} °C'
                    formatter: '{value}'
                }
            },
            grid:{
                // height:'80%',
                y:'15%'
            },
            series: [
                {
                    name:'最高人数',
                    type:'line',
                    data:[11, 11, 15, 13, 12, 13, 10],
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
                    name:'最低人数',
                    type:'line',
                    data:[1, -2, 2, 5, 3, 2, 0],
                    markPoint: {
                        data: [
                            {name: '预警点', value: 2, xAxis: 2, yAxis: 2}
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
        myChart.setOption(option)
    }
    peopleNum();

// 平均敏感度变化折线图
    function sensitivity(){
        var myChart = echarts.init(document.getElementById('sensitivity'),'dark');
        var option = {
            backgroundColor:'transparent',
            title: {
                text: '平均敏感度变化折线图',
                // subtext: '纯属虚构'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['最高人数','最低人数']
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
            grid:{
                y:'15%'
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: ['周一','周二','周三','周四','周五','周六','周日']
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                    formatter: '{value}'
                }
            },
            series: [
                {
                    name:'最高人数',
                    type:'line',
                    data:[11, 11, 15, 13, 12, 13, 10],
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
                    name:'最低人数',
                    type:'line',
                    data:[1, -2, 2, 5, 3, 2, 0],
                    markPoint: {
                        data: [
                            {name: '预警点', value: 2, xAxis: 2, yAxis: 2}
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
        myChart.setOption(option)
    }
    sensitivity()

// 平均影响力变化折线图
    function influence(){
        var myChart = echarts.init(document.getElementById('influence'),'dark');
        var option = {
            backgroundColor:'transparent',
            title: {
                text: '平均影响力变化折线图',
                // subtext: '纯属虚构'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['最高人数','最低人数']
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
            grid:{
                y:'15%'
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: ['周一','周二','周三','周四','周五','周六','周日']
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                    formatter: '{value}'
                }
            },
            series: [
                {
                    name:'最高人数',
                    type:'line',
                    data:[11, 11, 15, 13, 12, 13, 10],
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
                    name:'最低人数',
                    type:'line',
                    data:[1, -2, 2, 5, 3, 2, 0],
                    markPoint: {
                        data: [
                            {name: '预警点', value: 2, xAxis: 2, yAxis: 2}
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
        myChart.setOption(option)
    }
    influence()

// 聚集系数变化折线图
    function convergence(){
        var myChart = echarts.init(document.getElementById('convergence'),'dark');
        var option = {
            backgroundColor:'transparent',
            title: {
                text: '聚集系数变化折线图',
                // subtext: '纯属虚构'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:['最高人数','最低人数']
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
            grid:{
                y:'15%'
            },
            xAxis:  {
                type: 'category',
                boundaryGap: false,
                data: ['周一','周二','周三','周四','周五','周六','周日']
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    // formatter: '{value} °C'
                    formatter: '{value}'
                }
            },
            series: [
                {
                    name:'最高人数',
                    type:'line',
                    data:[11, 11, 15, 13, 12, 13, 10],
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
                    name:'最低人数',
                    type:'line',
                    data:[1, -2, 2, 5, 3, 2, 0],
                    markPoint: {
                        data: [
                            {name: '预警点', value: 2, xAxis: 2, yAxis: 2}
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
        myChart.setOption(option)
    }
    convergence()

// tab栏
// 社区详情----
    // 成员变换信息 member-change-1

    var memberChange_data = [
            {
                a:'1',
                b:'1',
                c:'1',
                d:'1',
                e:'1',
                f:'1',
                g:'1',
                h:'1',
                i:'1',
                g:'1',
                k:'1',
            },
            {
                a:'2',
                b:'2',
                c:'2',
                d:'2',
                e:'2',
                f:'2',
                g:'2',
                h:'2',
                i:'2',
                g:'2',
                k:'2',
            },
        ]

    function memberChange_1(data){
        $('#member-change-1').bootstrapTable('load', data);
        $('#member-change-1').bootstrapTable({
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
                    {
                        title: "社区名称",//标题
                        field: "b",//键名
                        sortable: false,//是否可排序
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
                            // return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_2(\''+row.entity_name+'\',\''+row.entity_type+'\',\''+row.id+'\',\''+row.illegal_type+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame(\''+row.entity_name+'\',\''+row.entity_type+'\',\''+row.id+'\',\''+row.illegal_type+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }
                    },
                    {
                        title: "操作",//标题
                        field: "select",
                        checkbox: true,
                        align: "center",//水平
                        valign: "middle"//垂直
                    },
                    /*
                    {
                        title: "登录状态",//标题
                        field: "login_status",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            if (row.login_status == 'logout'){return '离线'}else{return '在线'}
                        },
                    },
                    {
                        title: '操作',//标题
                        field: "",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            var ld;
                            if (row.login_status=='logout'){ld = '登录'}else{ld = '在线中'}
                            var str = '<a onclick="loginIN(this,\''+row.wxbot_id+'\',\''+row.wx_id+'\',\''+row.login_status+'\')" in_out="out" style="cursor: pointer;color:white;" title="'+ld+'"><i class="icon icon-key"></i></a>';
                            str +='<a onclick="enterIn(\''+row.wxbot_id+'\',\''+row.login_status+'\')" style="cursor: pointer;color:white;display: inline-block;margin:0 10px;"  title="进入"><i class="icon icon-link"></i></a>';
                            str +='<a onclick="deletePerson(\''+row.wxbot_id+'\')" style="cursor: pointer;color:white;margin-right:10px;"  title="删除"><i class="icon icon-trash"></i></a>';
                            str +='<a onclick="logoutPerson(\''+row.wxbot_id+'\',\''+row.login_status+'\')" style="cursor: pointer;color:white;"  title="退出登录"><i class="icon icon-signout"></i></a>';
                            str +='<a onclick="loadallGroups(\''+row.wxbot_id+'\',\''+row.login_status+'\')" style="cursor: pointer;color:white;margin-left:10px;"  title="设置群组"><i class="icon icon-cogs"></i></a>';
                            return str;
                        },
                    },
                     */
                ],
        });
        $('#member-change-1 p').slideUp(30);
    }

    memberChange_1(memberChange_data)

    function memberChange_2(data){
        $('#member-change-2').bootstrapTable('load', data);
        $('#member-change-2').bootstrapTable({
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
                            // return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_2(\''+row.entity_name+'\',\''+row.entity_type+'\',\''+row.id+'\',\''+row.illegal_type+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame(\''+row.entity_name+'\',\''+row.entity_type+'\',\''+row.id+'\',\''+row.illegal_type+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }
                    },
                    {
                        title: "操作",//标题
                        field: "select",
                        checkbox: true,
                        align: "center",//水平
                        valign: "middle"//垂直
                    },
                ],
        });
        $('#member-change-2 p').slideUp(30);
    }
    memberChange_2(memberChange_data)

    function memberChange_3(data){
        $('#member-change-3').bootstrapTable('load', data);
        $('#member-change-3').bootstrapTable({
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
                            // return '<span style="cursor:pointer;color:white;" onclick="jumpFrame_2(\''+row.entity_name+'\',\''+row.entity_type+'\',\''+row.id+'\',\''+row.illegal_type+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                            return '<span style="cursor:pointer;color:white;" onclick="jumpFrame(\''+row.entity_name+'\',\''+row.entity_type+'\',\''+row.id+'\',\''+row.illegal_type+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>';
                        }
                    },
                    {
                        title: "操作",//标题
                        field: "select",
                        checkbox: true,
                        align: "center",//水平
                        valign: "middle"//垂直
                    },
                ],
        });
        $('#member-change-3 p').slideUp(30);
    }
    memberChange_3(memberChange_data)

// 基本特征
    function createRandomItemStyle() {
        return {
            normal: {
                color: 'rgb(' + [
                    Math.round(Math.random() * 160),
                    Math.round(Math.random() * 160),
                    Math.round(Math.random() * 160)
                ].join(',') + ')'
            }
        };
    }
    function basic_1(){
        // 路径配置
        require.config({
            paths: {
                echarts: '../../static/js/echarts-2/build/dist',
            }
        });
        // 使用
        require(
            [
                'echarts',
                'echarts/chart/wordCloud'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('basic-1'),'dark');
                var option = {
                    // backgroundColor:'rgba(9, 36, 49, 0.65)',
                    title: {
                        text: '微话题关键词云',
                        textStyle:{
                            color:'#fff'
                        }
                    },
                    tooltip: {
                        show: false
                    },
                    toolbox:{
                        show:true,
                        feature:{
                            saveAsImage:{
                                show:false
                            }
                        },
                        color:'#fff',
                        effectiveColor:'#2a556f'
                    },
                    series: [
                        {
                            name: '微话题',
                            type: 'wordCloud',
                            size: ['80%', '80%'],
                            textRotation : [0, 45, 90, -45],
                            textPadding: 0,
                            autoSize: {
                                enable: true,
                                minSize: 14
                            },
                            data: [
                                {
                                    name: "我要金蛋",
                                    value: 10000,
                                    itemStyle: {
                                        normal: {
                                            color: 'black'
                                        }
                                    }
                                },
                                {
                                    name: "屹农金服",
                                    value: 6181,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "理财去",
                                    value: 4386,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "J联投银帮",
                                    value: 4055,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Charter Communications",
                                    value: 2467,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Chick Fil A",
                                    value: 2244,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Planet Fitness",
                                    value: 1898,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Pitch Perfect",
                                    value: 1484,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Express",
                                    value: 1112,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Home",
                                    value: 965,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Johnny Depp",
                                    value: 847,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Lena Dunham",
                                    value: 582,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Lewis Hamilton",
                                    value: 555,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "KXAN",
                                    value: 550,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Mary Ellen Mark",
                                    value: 462,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Farrah Abraham",
                                    value: 366,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Rita Ora",
                                    value: 360,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Serena Williams",
                                    value: 282,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "NCAA baseball tournament",
                                    value: 273,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Point Break",
                                    value: 265,
                                    itemStyle: createRandomItemStyle()
                                }
                            ]
                        }
                    ]
                };
                 // 为echarts对象加载数据
                myChart.setOption(option);
            }
        );
    }
    basic_1()

    function basic_2(){
        // 路径配置
        require.config({
            paths: {
                echarts: '../../static/js/echarts-2/build/dist',
            }
        });
        // 使用
        require(
            [
                'echarts',
                'echarts/chart/wordCloud'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('basic-2'),'dark');
                var option = {
                    // backgroundColor:'rgba(9, 36, 49, 0.65)',
                    title: {
                        text: '敏感词关键词云',
                        textStyle:{
                            color:'#fff'
                        }
                    },
                    tooltip: {
                        show: false
                    },
                    toolbox:{
                        show:true,
                        feature:{
                            saveAsImage:{
                                show:false
                            }
                        },
                        color:'#fff',
                        effectiveColor:'#2a556f'
                    },
                    series: [
                        {
                            name: '敏感词',
                            type: 'wordCloud',
                            size: ['80%', '80%'],
                            textRotation : [0, 45, 90, -45],
                            textPadding: 0,
                            autoSize: {
                                enable: true,
                                minSize: 14
                            },
                            data: [
                                {
                                    name: "我要金蛋",
                                    value: 10000,
                                    itemStyle: {
                                        normal: {
                                            color: 'black'
                                        }
                                    }
                                },
                                {
                                    name: "屹农金服",
                                    value: 6181,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "理财去",
                                    value: 4386,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "J联投银帮",
                                    value: 4055,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Charter Communications",
                                    value: 2467,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Chick Fil A",
                                    value: 2244,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Planet Fitness",
                                    value: 1898,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Pitch Perfect",
                                    value: 1484,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Express",
                                    value: 1112,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Home",
                                    value: 965,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Johnny Depp",
                                    value: 847,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Lena Dunham",
                                    value: 582,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Lewis Hamilton",
                                    value: 555,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "KXAN",
                                    value: 550,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Mary Ellen Mark",
                                    value: 462,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Farrah Abraham",
                                    value: 366,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Rita Ora",
                                    value: 360,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Serena Williams",
                                    value: 282,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "NCAA baseball tournament",
                                    value: 273,
                                    itemStyle: createRandomItemStyle()
                                },
                                {
                                    name: "Point Break",
                                    value: 265,
                                    itemStyle: createRandomItemStyle()
                                }
                            ]
                        }
                    ]
                };
                 // 为echarts对象加载数据
                myChart.setOption(option);
            }
        );
    }
    basic_2()

    // 典型帖子
    // var weiboUrl='/weibo_xnr_warming_new/show_speech_warming/?xnr_user_no='+ID_Num+'&show_type=0&start_time='+todayTimetamp()+'&end_time='+time2;
    var weiboUrl='/weibo_xnr_warming_new/show_speech_warming/?xnr_user_no=WXNR0044&show_type=0&start_time=1516896000&end_time=1517572495';
    public_ajax.call_request('get',weiboUrl,basic_3);
    function basic_3(data){
        $('#basic-3-content').bootstrapTable('load', data);
        $('#basic-3-content').bootstrapTable({
                data:data,
                search: true,//是否搜索
                pagination: true,//是否分页
                pageSize:5,//单页记录数
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
                    {
                        title: "",//标题
                        field: "",//键名
                        sortable: true,//是否可排序
                        order: "desc",//默认排序方式
                        align: "center",//水平
                        valign: "middle",//垂直
                        formatter: function (value, row, index) {
                            var item=row;
                            var name,text,text2,time,all='',img;
                            if (item.nick_name==''||item.nick_name=='null'||item.nick_name=='unknown'||!item.nick_name){
                                name=item.uid;
                            }else {
                                name=item.nick_name;
                            };
                            if (item.photo_url==''||item.photo_url=='null'||item.photo_url=='unknown'||!item.photo_url){
                                img='/static/images/unknown.png';
                            }else {
                                img=item.photo_url;
                            };
                            if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text){
                                text='暂无内容';
                            }else {
                                if (item.sensitive_words_string||!isEmptyObject(item.sensitive_words_string)){
                                    var s=item.text;
                                    var keywords=item.sensitive_words_string.split('&');
                                    for (var f=0;f<keywords.length;f++){
                                        s=s.toString().replace(new RegExp(keywords[f],'g'),'<b style="color:#ef3e3e;">'+keywords[f]+'</b>');
                                    }
                                    text=s;

                                    var rrr=item.text;
                                    if (rrr.length>=160){
                                        rrr=rrr.substring(0,160)+'...';
                                        all='inline-block';
                                    }else {
                                        rrr=item.text;
                                        all='none';
                                    }
                                    for (var f of keywords){
                                        rrr=rrr.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                                    }
                                    text2=rrr;
                                }else {
                                    text=item.text;
                                    if (text.length>=160){
                                        text2=text.substring(0,160)+'...';
                                        all='inline-block';
                                    }else {
                                        text2=text;
                                        all='none';
                                    }
                                };
                            };
                            if (item.timestamp==''||item.timestamp=='null'||item.timestamp=='unknown'||!item.timestamp){
                                time='未知';
                            }else {
                                time=getLocalTime(item.timestamp);
                            };
                            var rel_str=
                                '<div class="everySpeak everyUser" style="margin:0 auto;width: 100%;text-align: left;">'+
                                '        <div class="speak_center">'+
                                '            <div class="center_rel">'+
                                '                <img src="'+img+'" alt="" class="center_icon">'+
                                '                <a class="center_1 centerNAME" style="color:#f98077;">'+name+'</a>'+
                                '                <a class="mid" style="display: none;">'+item.mid+'</a>'+
                                '                <a class="uid" style="display: none;">'+item.uid+'</a>'+
                                '                <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                '                <a class="_id" style="display: none;">'+item._id+'</a>'+
                                '                <span class="time" style="font-weight: 900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                                '                <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                                '                <p class="allall1" style="display:none;">'+text+'</p>'+
                                '                <p class="allall2" style="display:none;">'+text2+'</p>'+
                                '                <span class="center_2">'+text2+
                                '                </span>'+
                                '                <div class="center_3">'+
                                '                    <span class="cen3-1" onclick="retweet(this,\'预警\')"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                                '                    <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                                '                    <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                                '                    <span class="cen3-5" onclick="joinPolice(this,\'言论\')"><i class="icon icon-plus-sign"></i>&nbsp;&nbsp;加入预警库</span>'+
                                '                    <span class="cen3-9" onclick="robot(this)"><i class="icon icon-github-alt"></i>&nbsp;&nbsp;机器人回复</span>'+
                                '                    <span class="cen3-6" onclick="oneUP(this,\'言论\')"><i class="icon icon-upload-alt"></i>&nbsp;&nbsp;上报</span>'+
                                '                </div>'+
                                '               <div class="forwardingDown" style="width: 100%;display: none;">'+
                                '                   <input type="text" class="forwardingIput" placeholder="转发内容"/>'+
                                '                   <span class="sureFor" onclick="forwardingBtn()">转发</span>'+
                                '               </div>'+
                                '               <div class="commentDown" style="width: 100%;display: none;">'+
                                '                   <input type="text" class="comtnt" placeholder="评论内容"/>'+
                                '                   <span class="sureCom" onclick="comMent(this,\'预警\')">评论</span>'+
                                '               </div>'+
                                '            </div>'+
                                '        </div>';
                            return rel_str;
                        }
                    }

                ],
        });
        $('#basic-3-content p').slideUp(30);
    }
    // basic_3()

// 社交特征
    function social(){
        // 路径配置
        require.config({
            paths: {
                echarts: '../../static/js/echarts-2/build/dist',
            }
        });
        // 使用
        require(
            [
                'echarts',
                'echarts/chart/force'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('social-content'),'dark');
                var option = {
                    title : {
                        text: '人物关系：乔布斯',
                        subtext: '数据来自人立方',
                        x:'right',
                        y:'bottom'
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: '{a} : {b}'
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            restore : {show: true},
                            magicType: {show: true, type: ['force', 'chord']},
                            saveAsImage : {show: true}
                        }
                    },
                    legend: {
                        x: 'left',
                        data:['家人','朋友']
                    },
                    series : [
                        {
                            type:'force',
                            name : "人物关系",
                            ribbonType: false,
                            categories : [
                                {
                                    name: '人物'
                                },
                                {
                                    name: '家人'
                                },
                                {
                                    name:'朋友'
                                }
                            ],
                            itemStyle: {
                                normal: {
                                    label: {
                                        show: true,
                                        textStyle: {
                                            color: '#333'
                                        }
                                    },
                                    nodeStyle : {
                                        brushType : 'both',
                                        borderColor : 'rgba(255,215,0,0.4)',
                                        borderWidth : 1
                                    },
                                    linkStyle: {
                                        type: 'curve'
                                    }
                                },
                                emphasis: {
                                    label: {
                                        show: false
                                        // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                                    },
                                    nodeStyle : {
                                        //r: 30
                                    },
                                    linkStyle : {}
                                }
                            },
                            useWorker: false,
                            minRadius : 15,
                            maxRadius : 25,
                            gravity: 1.1,
                            scaling: 1.1,
                            roam: 'move',
                            nodes:[
                                {category:0, name: '乔布斯', value : 10, label: '乔布斯\n（主要）'},
                                {category:1, name: '丽萨-乔布斯',value : 2},
                                {category:1, name: '保罗-乔布斯',value : 3},
                                {category:1, name: '克拉拉-乔布斯',value : 3},
                                {category:1, name: '劳伦-鲍威尔',value : 7},
                                {category:2, name: '史蒂夫-沃兹尼艾克',value : 5},
                                {category:2, name: '奥巴马',value : 8},
                                {category:2, name: '比尔-盖茨',value : 9},
                                {category:2, name: '乔纳森-艾夫',value : 4},
                                {category:2, name: '蒂姆-库克',value : 4},
                                {category:2, name: '龙-韦恩',value : 1},
                            ],
                            links : [
                                {source : '丽萨-乔布斯', target : '乔布斯', weight : 1, name: '女儿'},
                                {source : '保罗-乔布斯', target : '乔布斯', weight : 2, name: '父亲'},
                                {source : '克拉拉-乔布斯', target : '乔布斯', weight : 1, name: '母亲'},
                                {source : '劳伦-鲍威尔', target : '乔布斯', weight : 2},
                                {source : '史蒂夫-沃兹尼艾克', target : '乔布斯', weight : 3, name: '合伙人'},
                                {source : '奥巴马', target : '乔布斯', weight : 1},
                                {source : '比尔-盖茨', target : '乔布斯', weight : 6, name: '竞争对手'},
                                {source : '乔纳森-艾夫', target : '乔布斯', weight : 1, name: '爱将'},
                                {source : '蒂姆-库克', target : '乔布斯', weight : 1},
                                {source : '龙-韦恩', target : '乔布斯', weight : 1},
                                {source : '克拉拉-乔布斯', target : '保罗-乔布斯', weight : 1},
                                {source : '奥巴马', target : '保罗-乔布斯', weight : 1},
                                {source : '奥巴马', target : '克拉拉-乔布斯', weight : 1},
                                {source : '奥巴马', target : '劳伦-鲍威尔', weight : 1},
                                {source : '奥巴马', target : '史蒂夫-沃兹尼艾克', weight : 1},
                                {source : '比尔-盖茨', target : '奥巴马', weight : 6},
                                {source : '比尔-盖茨', target : '克拉拉-乔布斯', weight : 1},
                                {source : '蒂姆-库克', target : '奥巴马', weight : 1}
                            ]
                        }
                    ]
                };
                 // 为echarts对象加载数据
                myChart.setOption(option);
            }
        );
    }
    social()


//----关键词云
// public_ajax.call_request('get',word_url,wordCloud);
require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
function wordCloud(data) {
    var data=eval(data);
    var wordSeries=[];
    $.each(data,function (index,item) {
        wordSeries.push(
            {
                name: item[0],
                value: item[1].toFixed(2) *100,
                itemStyle: createRandomItemStyle()
            }
        )
    });
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],
        //关键词
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('content-1-word'));
            option = {
                title: {
                    text: '',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    type: 'wordCloud',
                    size: ['80%', '80%'],
                    textRotation : [0, 0, 0, 0],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data: wordSeries
                }]
            };

            myChart.setOption(option);
            var ecConfig = require('echarts/config');
            myChart.on(ecConfig.EVENT.HOVER, function (param){
                var selected = param.name;
            });
        }
    );
}
//表格
function userlist(persondata) {
    var person=window.JSON?JSON.parse(persondata):eval("("+persondata+")");
    var person_all=[];
    $.each(person,function (index,item) {
        person_all.push({
            'name':item[1],
            'include':item[2],
            'time':item[5],
            'keywords':item[3],
            'label':item[4],
        })
    });
    $('.userList #userList').bootstrapTable('load', person_all);
    $('.userList #userList').bootstrapTable({
        data:person_all,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 10,//单页记录数
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
                title: "用户ID",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[1];
                // }
            },
            {
                title: "昵称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[2];
                // }
            },
            {
                title: "注册地",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[5];
                // },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "影响力",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "网民详情",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a style="cursor: pointer;" onclick="">网民详情</a>'
                },
            },
            {
                title: "添加关注",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='查看') {
                window.open();
            }else if ($element[0].innerText=='') {
                window.open();
            }
        }
    });
},
//-------------------颜色----------------------
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
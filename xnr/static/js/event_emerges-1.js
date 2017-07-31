// public_ajax.call_request('get',word_url,mainJoin);
function mainJoin(data) {
    var influence=window.JSON?JSON.parse(data):eval("("+data+")");
    $.each(data,function (index,item) {
        theme_all.push({
            'name':item[1],
            'include':item[2],
            'time':item[5],
            'keywords':item[3],
            'label':item[4],
        })
    });
    $('#mainEvent').bootstrapTable('load', influence);
    $('#mainEvent').bootstrapTable({
        data:influence,
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
                title: "编号",//标题
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
                title: "用户UID",//标题
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
                title: "用户昵称",//标题
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
                title: "关注数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
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
                title: '操作',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a style="cursor: pointer;" onclick="" data-toggle="modal" data-target="#details">查看详情</a>';

                },
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
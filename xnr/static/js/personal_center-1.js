function auto() {
    //var has_url = '';
    //var notHao_url = '';
    //public_ajax.call_request('GET',has_url,has_table);
    // public_ajax.call_request('GET',notHao_url,not_yet);
}
auto();
function has_table(has_data) {
    // var person=window.JSON?JSON.parse(has_data):eval("("+has_data+")");
    var person=eval(has_data)
    console.log(person)
    $.each(data,function (index,item) {
        theme_all.push({
            'name':item[1],
            'include':item[2],
            'time':item[5],
            'keywords':item[3],
            'label':item[4],
        })
    });
    $('.has_list #haslist').bootstrapTable('load', person);
    $('.has_list #haslist').bootstrapTable({
        data:person,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 10,//单页记录数
        pageList: [15,25,35],//分页步进值
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
                title: "创建时间",//标题
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
                title: "渗透领域",//标题
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
                title: "角色定位",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "活跃时间",//标题
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
                title: "历史发帖量",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "历史评论数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "今日发帖量",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "今日提醒",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a style="cursor: pointer;">查看</a>';
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
                    return '<a style="cursor: pointer;" onclick="">进入</a>'+
                        '<a style="cursor: pointer;" onclick="">修改</a>'+
                        '<a style="cursor: pointer;" onclick="">删除</a>';
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
};
function not_yet(no_data) {
    let undone_person=window.JSON?JSON.parse(no_data):eval("("+no_data+")");
    $.each(data,function (index,item) {
        theme_all.push({
            'name':item[1],
            'include':item[2],
            'time':item[5],
            'keywords':item[3],
            'label':item[4],
        })
    });
    $('.undone_list #undonelist').bootstrapTable('load', undone_person);
    $('.undone_list #undonelist').bootstrapTable({
        data:undone_person,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 10,//单页记录数
        pageList: [15,25,35],//分页步进值
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
                title: "创建时间",//标题
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
                title: "渗透领域",//标题
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
                title: "角色定位",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "活跃时间",//标题
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
                    return '<a style="cursor: pointer;" onclick="">继续</a>'+
                        '<a style="cursor: pointer;" onclick="">删除</a>';
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {

        }
    });
};
function success_fail(data) {
    var flag=eval(data),word;
    if (flag==1){
        word='删除成功。';
    }else {
        word='删除失败。';
    }
    $('#succee_fail #words').text(word);
    $('#succee_fail').modal('show');
}





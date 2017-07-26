var public_ajax= {
    call_request:function(ajax_method,url,callback) {
        $.ajax({
            type:ajax_method,
            url:url,
            async:true,
            //timeout:300,
            //data:{"name":"xm"},//传参数
            dataType:"json",
            success:callback,
            error:function (xhr,textStatus,errorThrown) {
                //请求失败执行的函数
                console.log("请求失败",textStatus,errorThrown)
            },
            global:false//是否触发全局请求,需要触发就是true,不需要false
        });
    },
    influe:function (has_data) {
        var influence=window.JSON?JSON.parse(has_data):eval("("+has_data+")");
        $.each(data,function (index,item) {
            theme_all.push({
                'name':item[1],
                'include':item[2],
                'time':item[5],
                'keywords':item[3],
                'label':item[4],
            })
        });
        $('#influence').bootstrapTable('load', influence);
        $('#influence').bootstrapTable({
            data:influence,
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
                    title: "用户ID",//标题
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
                        return '<a style="cursor: pointer;" onclick="" data-toggle="modal" data-target="#details">查看详情</a>'+
                                '<a style="cursor: pointer;" onclick="">直接关注</a>';

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
    sensitive:function (no_data) {
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
                if ($element[0].innerText=='查看') {
                    window.open();
                }else if ($element[0].innerText=='') {
                    window.open();
                }
            }
        });
    },
};
function auto() {
    var ajax_method='GET';
    var url_1 = '';
    var url_2 = '';
    var url_3 = '';
    public_ajax.call_request(ajax_method,url_1,public_ajax.influe);
    public_ajax.call_request(ajax_method,url_2,public_ajax.sensitive);
    public_ajax.call_request(ajax_method,url_3,public_ajax.friends);
}
// auto();




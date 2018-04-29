var userList_Url='/system_manage/show_all_users_account/';
public_ajax.call_request('get',userList_Url,userList);
function userList(data) {
    $('#userlist').bootstrapTable('load', data);
    $('#userlist').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
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
                title: "用户名",//标题
                field: "user_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "已完成微博虚拟人",//标题
                field: "complete_xnr_weibo",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.complete_xnr_weibo==''||row.complete_xnr_weibo=='null'||
                        row.complete_xnr_weibo=='unknown'||row.complete_xnr_weibo.length==0||!row.complete_xnr_weibo){
                        return '无';
                    }else {
                        return row.complete_xnr_weibo.join('<br/>');
                    };
                }
            },
            {
                title: "已完成QQ虚拟人",//标题
                field: "complete_xnr_qq",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.complete_xnr_qq==''||row.complete_xnr_qq=='null'||
                        row.complete_xnr_qq=='unknown'||row.complete_xnr_qq.length==0||!row.complete_xnr_qq){
                        return '无';
                    }else {
                        return row.complete_xnr_qq.join('<br/>');
                    };
                }
            },
            {
                title: "已完成微信虚拟人",//标题
                field: "complete_xnr_weixin",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.complete_xnr_weixin==''||row.complete_xnr_weixin=='null'||
                        row.complete_xnr_weixin=='unknown'||row.complete_xnr_weixin.length==0||!row.complete_xnr_weixin){
                        return '无';
                    }else {
                        return row.complete_xnr_weixin.join('<br/>');
                    };
                }
            },
            {
                title: "已完成facebook虚拟人",//标题
                field: "complete_xnr_facebook",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.complete_xnr_facebook==''||row.complete_xnr_facebook=='null'||
                        row.complete_xnr_facebook=='unknown'||row.complete_xnr_facebook.length==0||
                        !row.complete_xnr_facebook){
                        return '无';
                    }else {
                        return row.complete_xnr_facebook.join('<br/>');
                    };
                }
            },
            {
                title: "已完成twitter虚拟人",//标题
                field: "complete_xnr_twitter",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.complete_xnr_twitter==''||row.complete_xnr_twitter=='null'||
                        row.complete_xnr_twitter=='unknown'||row.complete_xnr_twitter.length==0||
                        !row.complete_xnr_twitter){
                        return '无';
                    }else {
                        return row.complete_xnr_twitter.join('<br/>');
                    };
                }
            },
            {
                title: "未完成微博虚拟人",//标题
                field: "uncomplete_xnr_weibo",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uncomplete_xnr_weibo==''||row.uncomplete_xnr_weibo=='null'||
                        row.uncomplete_xnr_weibo=='unknown'||row.uncomplete_xnr_weibo.length==0||!row.uncomplete_xnr_weibo){
                        return '无';
                    }else {
                        return row.uncomplete_xnr_weibo.join('<br/>');
                    };
                }
            },
            {
                title: "未完成QQ虚拟人",//标题
                field: "uncomplete_xnr_qq",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uncomplete_xnr_qq==''||row.uncomplete_xnr_qq=='null'||
                        row.uncomplete_xnr_qq=='unknown'||row.uncomplete_xnr_qq.length==0||!row.uncomplete_xnr_qq){
                        return '无';
                    }else {
                        return row.uncomplete_xnr_qq.join('<br/>');
                    };
                }
            },
            {
                title: "未完成微信虚拟人",//标题
                field: "uncomplete_xnr_weixin",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uncomplete_xnr_weixin==''||row.uncomplete_xnr_weixin=='null'||
                        row.uncomplete_xnr_weixin=='unknown'||row.uncomplete_xnr_weixin.length==0||!row.uncomplete_xnr_weixin){
                        return '无';
                    }else {
                        return row.uncomplete_xnr_weixin.join('<br/>');
                    };
                }
            },
            {
                title: "未完成facebook虚拟人",//标题
                field: "uncomplete_xnr_facebook",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uncomplete_xnr_facebook==''||row.uncomplete_xnr_facebook=='null'||
                        row.uncomplete_xnr_facebook=='unknown'||row.uncomplete_xnr_facebook.length==0||
                        !row.uncomplete_xnr_facebook){
                        return '无';
                    }else {
                        return row.uncomplete_xnr_facebook.join('<br/>');
                    };
                }
            },
            {
                title: "未完成twitter虚拟人",//标题
                field: "uncomplete_xnr_twitter",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uncomplete_xnr_twitter==''||row.uncomplete_xnr_twitter=='null'||
                        row.uncomplete_xnr_twitter=='unknown'||row.uncomplete_xnr_twitter.length==0||
                        !row.uncomplete_xnr_twitter){
                        return '无';
                    }else {
                        return row.uncomplete_xnr_twitter.join('<br/>');
                    };
                }
            },
        ],
    });
}


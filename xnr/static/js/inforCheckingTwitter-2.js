// =====关注列表====
$('.focusSEN .demo-label input').on('click',function () {
    var orderType=$(this).val();
    var ClickFocusOn_url='/weibo_xnr_manage/wxnr_list_concerns/?user_id='+ID_Num+'&order_type='+orderType;
    public_ajax.call_request('get',ClickFocusOn_url,focusOn);
})
var focusOn_url='/weibo_xnr_manage/wxnr_list_concerns/?user_id='+ID_Num+'&order_type=influence';
public_ajax.call_request('get',focusOn_url,focusOn);
function focusOn(data) {
    $('#focus p').show();
    $('#focus').bootstrapTable('load', data);
    $('#focus').bootstrapTable({
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
                title: "头像",//标题
                field: "photo_url",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        return '<img style="width: 30px;height: 30px;" src="/static/images/unknown.png">';
                    }else {
                        return '<img style="width: 30px;height: 30px;" src="'+row.photo_url+'">';
                    };
                }
            },
            {
                title: "用户昵称",//标题
                field: "nick_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        return row.uid;
                    }else {
                        return row.nick_name;
                    };
                }
            },
            {
                title: "性别",//标题
                field: "sex",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.sex==''||row.sex=='null'||row.sex=='unknown'){
                        return '未知';
                    }else {
                        if (row.sex=='male'){return '男';}else if (row.sex=='female'){return '女'}else {return '未知'}
                    };
                }
            },
            {
                title: "关注来源",//标题
                field: "follow_source",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.follow_source==''||row.follow_source=='null'||row.follow_source=='unknown'||!row.follow_source){
                        return '未知';
                    }else {
                        return row.follow_source;
                    };
                }
            },
            {
                title: "话题领域",//标题
                field: "topic_string",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.topic_string==''||row.topic_string=='null'||row.topic_string=='unknown'||!row.topic_string){
                        return '未知';
                    }else {
                        return row.topic_string.replace(/&/g,',');
                    };
                }
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.influence==''||row.influence=='null'||row.influence=='unknown'){
                        return 0;
                    }else {
                        return row.influence;
                    };
                }
            },
            {
                title: "敏感度",//标题
                field: "sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "关注状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var ID=row.uid;
                    return '<span style="cursor: pointer;" onclick="focus_ornot(\''+ID+'\',\'cancel_follow_user\')" title="取消关注"><i class="icon icon-heart"></i></span>';
                    //'<span style="cursor: pointer;" onclick="lookDetails(\''+ID+'\')" title="查看详情"><i class="icon icon-link"></i></span>&nbsp;&nbsp;'+
                    //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="修改"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;'+
                    //'<span style="cursor: pointer;" onclick="focus_ornot(\''+ID+'\',\'cancel_follow_user\')" title="取消关注"><i class="icon icon-heart-empty"></i></span>';
                }
            },
        ],
    });
    $('#focus p').slideUp(700);
}
//=====粉丝列表====
$('.fansSEN .demo-label input').on('click',function () {
    var orderType=$(this).val();
    var clikcFans_url='/weibo_xnr_manage/wxnr_list_fans/?user_id='+ID_Num+'&order_type='+orderType;
    public_ajax.call_request('get',clikcFans_url,fans);
})
var fans_url='/weibo_xnr_manage/wxnr_list_fans/?user_id='+ID_Num+'&order_type=influence';
public_ajax.call_request('get',fans_url,fans);
function fans(data) {
    $('#fans p').show();
    $('#fans').bootstrapTable('load', data);
    $('#fans').bootstrapTable({
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
                title: "头像",//标题
                field: "photo_url",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        return '<img style="width: 30px;height: 30px;" src="/static/images/unknown.png">';
                    }else {
                        return '<img style="width: 30px;height: 30px;" src="'+row.photo_url+'">';
                    };
                }
            },
            {
                title: "UID",//标题
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "用户昵称",//标题
                field: "nick_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        return row.uid;
                    }else {
                        return row.nick_name;
                    };
                }
            },
            {
                title: "性别",//标题
                field: "sex",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.sex==''||row.sex=='null'||row.sex=='unknown'){
                        return '未知';
                    }else {
                        if (row.sex=='male'){return '男';}else if (row.sex=='female'){return '女'}else {return '未知'}
                    };
                }
            },
            {
                title: "粉丝来源",//标题
                field: "fan_source",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.fan_source==''||row.fan_source=='null'||row.fan_source=='unknown'||!row.fan_source){
                        return '未知';
                    }else {
                        return row.fan_source;
                    };
                }
            },
            {
                title: "所在地",//标题
                field: "user_location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.user_location==''||row.user_location=='null'||row.user_location=='unknown'){
                        return '未知';
                    }else {
                        return row.user_location;
                    };
                }
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.influence==''||row.influence=='null'||row.influence=='unknown'||!row.influence){
                        return 0;
                    }else {
                        return row.influence;
                    };
                }
            },
            {
                title: "敏感度",//标题
                field: "sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "关注状态",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var ID=row.id;
                    return '<span style="cursor: pointer;" onclick="focus_ornot(\''+ID+'\',\'attach_fans_follow\')" title="直接关注"><i class="icon icon-heart-empty"></i></span>';
                    //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="查看详情"><i class="icon icon-link"></i></span>&nbsp;&nbsp;'+
                    //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="修改"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;'+
                    //'<span style="cursor: pointer;" onclick="revoked(\''+ID+'\',\'attach_fans_follow\')" title="直接关注"><i class="icon icon-heart"></i></span>';
                }
            },
        ],
    });
    $('#fans p').slideUp(700);
}
function focus_ornot(_id,mid) {
    var focusNOT_url='/weibo_xnr_manage/'+mid+'/?xnr_user_no='+ID_Num+'&uid='+_id;
    public_ajax.call_request('get',focusNOT_url,succeedFail);
}
function succeedFail(data) {
    var t ='操作成功';
    if (!data){t='操作失败'}else {
        setTimeout(function () {
            public_ajax.call_request('get',focusOn_url,focusOn);
            public_ajax.call_request('get',fans_url,fans);
        },700);
    };
    $('#pormpt p').text(t);
    $('#pormpt').modal('show');
}
var start_time='1500108142';
var end_time='1500108142';
//=====历史统计====定时任务列表====历史消息===时间段选择===
$('.choosetime .demo-label input').on('click',function () {
    var _val=$(this).val();
    var sh=$(this).attr('shhi');
    var mid=$(this).parents('.choosetime').attr('midurl');
    if (_val=='mize'&&sh!=0){
        $(this).parents('.choosetime').find('#start_'+sh).show();
        $(this).parents('.choosetime').find('#end_'+sh).show();
        $(this).parents('.choosetime').find('#sure-'+sh).css({display:'inline-block'});
    }else {
        $(this).parents('.choosetime').find('#start_'+sh).hide();
        $(this).parents('.choosetime').find('#end_'+sh).hide();
        $(this).parents('.choosetime').find('#sure-'+sh).hide();
    }
});
$('.sureTime').on('click',function () {
    var t=$(this).attr('shhi');
    var s=$(this).parents('.choosetime').find('#start_'+t).val();
    var e=$(this).parents('.choosetime').find('#end'+t).val();
    if (s==''||e==''){
        $('#successfail p').text('时间不能为空。');
        $('#successfail').modal('show');
    }else {
        var mid=$(this).parents('.choosetime').attr('midurl');
    }
});
$(".customizeTime").keydown(function(e) {
    if (e.keyCode == 13) {
        var _val=$(this).val();
        var reg = new RegExp("^[0-9]*$");
        if (reg.test(_val)){

        }else {
            $('#successfail p').text('只能输入数字。');
            $('#successfail').modal('show');
        }

    }
});
//历史统计
var historyTotal_url='/weibo_xnr_manage/show_history_count/?xnr_user_no='+ID_Num+'&type=today&start_time=0&end_time=1505044800'
public_ajax.call_request('get',historyTotal_url,historyTotal);
function historyTotal(data) {
    console.log(data)
}
//定时发送任务列表
var timingTask_url='/weibo_xnr_manage/show_timing_tasks/?xnr_user_no='+ID_Num+'&start_time=1500108142&end_time=1500108142';
public_ajax.call_request('get',timingTask_url,timingTask);
var TYPE={
    'origin':'原创','retweet':'转发','comment':'评论'
}
function timingTask(data) {
    console.log(data)
    $('#time').bootstrapTable('load', data);
    $('#time').bootstrapTable({
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
                title: "编号",//标题
                field: "user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "任务来源",//标题
                field: "task_source",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.task_source==''||row.task_source=='null'||row.task_source=='unknown'){
                        return '未知';
                    }else {
                        return row.task_source;
                    };
                }
            },
            {
                title: "操作类型",//标题
                field: "operate_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.operate_type==''||row.operate_type=='null'||row.operate_type=='unknown'){
                        return '未知';
                    }else {
                        return TYPE[row.operate_type];
                    };
                }
            },
            {
                title: "提交时间",//标题
                field: "create_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'){
                        return '未知';
                    }else {
                        return getLocalTime(row.create_time);
                    };
                }
            },
            {
                title: "定时发送时间",//标题
                field: "post_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.post_time==''||row.post_time=='null'||row.post_time=='unknown'||!row.post_time){
                        return '未知';
                    }else {
                        return getLocalTime(row.post_time);
                    };
                }
            },
            {
                title: "备注",//标题
                field: "remark",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.remark==''||row.remark=='null'||row.remark=='unknown'){
                        return '无备注';
                    }else {
                        return row.remark;
                    };
                }
            },
            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var ID=row.id;
                    return '<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="查看详情"><i class="icon icon-link"></i></span>&nbsp;&nbsp;'+
                    //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="修改"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;'+
                    '<span style="cursor: pointer;" onclick="revoked(\''+ID+'\')" title="撤销"><i class="icon icon-reply"></i></span>';
                }
            },
        ],
    });
}

//操作
//=====查看====
function lookRevise(_id) {
    var saw_url='/weibo_xnr_manage/wxnr_timing_tasks_lookup/?task_id='+_id;
    public_ajax.call_request('get',saw_url,saw);
}
function saw(data) {
    var t1='无内容',t2='无备注',m='未知';
    if (data.post_time!=''||data.post_time!='null'||data.post_time!='unknown'||!data.post_time){
        m= getLocalTime(data.post_time);
    }
    if (data.text!=''||data.text!='null'||data.text!='unknown'||!data.text){
        t1= data.text;
    }
    if (data.remark!=''||data.remark!='null'||data.remark!='unknown'||!data.remark){
        t2= data.remark;
    }
    $("#details .taskid").text(data.id);
    $("#details .create_time").text(data.create_time);
    $("#details .details-1 input[type='radio'][value='"+data.task_source+"']").attr("checked",true);
    $("#details .details-2 input[type='radio'][value='"+data.operate_type+"']").attr("checked",true);
    $("#details .details-3 #_timing").attr("placeholder",m);
    $("#details .details-4 #words").val(t1);
    $("#details .details-5 #remarks").val(t2);
    $('#details').modal('show');
}
//修改内容参数
function sureModify() {
    var id=$("#details .taskid").text();
    var creat_time=$("#details .create_time").text();
    var task_source=$('#details .details-1 input:radio[name="dett"]:checked').val();
    var operate_type=$('#details .details-2 input:radio[name="opert"]:checked').val();
    var post_time=$("#details .details-3 #_timing").val(),mi='';
    var text=$("#details .details-4 #words").val();
    var remark=$("#details .details-5 #remarks").val();
    if (post_time){
        mi=Date.parse(new Date(post_time))/1000;
    }else {
        post_time=$("#details .details-3 #_timing").attr('placeholder');
        mi=Date.parse(new Date(post_time))/1000;
    }
    var againSave_url='/weibo_xnr_manage/wxnr_timing_tasks_change/?task_id='+id+'&task_source='+task_source+
        '&operate_type='+operate_type+'&create_time='+creat_time+'&post_time='+mi+'&text='+text+'&remark='+remark;
    public_ajax.call_request('get',againSave_url,successFail);
}
//撤销
function revoked(_id) {
    var delTask_url='/weibo_xnr_manage/wxnr_timing_tasks_revoked/?task_id='+_id;
    public_ajax.call_request('get',delTask_url,successFail);
}
//=========
function successfail(data) {
    var t ='操作成功';
    if (!data){t='操作失败'}else {
        setTimeout(function () {
            public_ajax.call_request('get',timingTask_url,timingTask);
        },700);
    };
    $('#successfail p').text(t);
    $('#successfail').modal('show');
}
//------历史消息type分页-------
var typeDown='';
$('#container .rightWindow .news #myTabs li').on('click',function () {
    htp=[];
    var middle=$(this).attr('midurl').split('&');
    typeDown=middle[0];
    var liNews_url='/weibo_xnr_manage/'+middle[0]+'/?xnr_user_no='+ID_Num+'&task_source='+middle[1]+
        '&start_time='+start_time+'&end_time='+end_time;
    public_ajax.call_request('get',liNews_url,historyNews);
})

//------历史消息type分页下的按钮选择-----
var htp=[];
$('#container .rightWindow .oli #content input').on('click',function () {
    var flag=$(this).parents('.tab-pane').attr('id');
    $("#"+flag+" input:checkbox:checked").each(function (index,item) {
        htp.push($(this).val());
    });
    var content_type=htp.join(',');
    var againHistoryNews_url='/weibo_xnr_manage/'+typeDown+'/?xnr_user_no='+ID_Num+'&content_type='+content_type+
        '&start_time='+start_time+'&end_time='+end_time;
    public_ajax.call_request('get',againHistoryNews_url,historyNews);
})
var historyNews_url='/weibo_xnr_manage/show_history_posting/?xnr_user_no='+ID_Num+'&task_source=daily_post,hot_post'+
    '&start_time='+start_time+'&end_time='+end_time;
public_ajax.call_request('get',historyNews_url,historyNews);
function historyNews(data) {
    console.log(data)
}
//===========
// =====关注列表====
$('.focusSEN .demo-label input').on('click',function () {
    var orderType=$(this).val();
    var ClickFocusOn_url='/weibo_xnr_manage/wxnr_list_concerns/?user_id='+ID_Num+'&order_type='+orderType;
    public_ajax.call_request('get',ClickFocusOn_url,focusOn);
})
var focusOn_url='/weibo_xnr_manage/wxnr_list_concerns/?user_id='+ID_Num+'&order_type=influence';
public_ajax.call_request('get',focusOn_url,focusOn);
function focusOn(data) {
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
                        if (row.sex==1){return '男'}else if (row.sex==2){return '女'}else{return '未知'}
                    };
                }
            },
            {
                title: "年龄",//标题
                field: "age",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.age==''||row.age=='null'||row.age=='unknown'||!row.age){
                        return '未知';
                    }else {
                        return row.age;
                    };
                }
            },
            {
                title: "注册时间",//标题
                field: "post_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.post_time==''||row.post_time=='null'||row.post_time=='unknown'||!row.post_time){
                        return '未知';
                    }else {
                        return getLocalTime(row.post_time);
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
                    return '<span style="cursor: pointer;" onclick="focus_ornot(\''+ID+'\',\'cancel_follow_user\')" title="取消关注"><i class="icon icon-heart-empty"></i></span>';
                        //'<span style="cursor: pointer;" onclick="lookDetails(\''+ID+'\')" title="查看详情"><i class="icon icon-link"></i></span>&nbsp;&nbsp;'+
                        //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="修改"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;'+
                        //'<span style="cursor: pointer;" onclick="focus_ornot(\''+ID+'\',\'cancel_follow_user\')" title="取消关注"><i class="icon icon-heart-empty"></i></span>';
                }
            },
        ],
    });
}
//=====粉丝列表====
$('.fansSEN .demo-label input').on('click',function () {
    var orderType=$(this).val();
    var clikcFans_url='/weibo_xnr_manage/wxnr_list_fans/?user_id='+ID_Num+'&order_type=influence';
    public_ajax.call_request('get',clikcFans_url,fans);
})
var fans_url='/weibo_xnr_manage/wxnr_list_fans/?user_id='+ID_Num+'&order_type=influence';
public_ajax.call_request('get',fans_url,fans);
function fans(data) {
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
                title: "编号",//标题
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
                        if (row.sex==1){return '男';}else if (row.sex==2){return '女'}else {return '未知'}
                    };
                }
            },
            {
                title: "年龄",//标题
                field: "create_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'){
                        return '未知';
                    }else {
                        return getLocalTime(row.create_time);
                    };
                }
            },
            {
                title: "注册时间",//标题
                field: "create_at",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_at==''||row.create_at=='null'||row.create_at=='unknown'||!row.create_at){
                        return '未知';
                    }else {
                        return getLocalTime(row.create_at);
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
                    var ID=row.id;
                    return '<span style="cursor: pointer;" onclick="revoked(\''+ID+'\',\'attach_fans_follow\')" title="直接关注"><i class="icon icon-heart"></i></span>';
                    //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="查看详情"><i class="icon icon-link"></i></span>&nbsp;&nbsp;'+
                        //'<span style="cursor: pointer;" onclick="lookRevise(\''+ID+'\')" title="修改"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;'+
                        //'<span style="cursor: pointer;" onclick="revoked(\''+ID+'\',\'attach_fans_follow\')" title="直接关注"><i class="icon icon-heart"></i></span>';
                }
            },
        ],
    });
}
//======查看详情===关注与否====

// function lookDetails(_id) {
//     var details_url='/weibo_xnr_manage/lookup_detail_weibouser/?uid='+_id;
//     public_ajax.call_request('get',details_url,detailsOK);
// }
// function detailsOK(data) {
//     console.log(data)
// }

function focus_ornot(_id,mid) {
    var focusNOT_url='/weibo_xnr_manage/'+mid+'/?xnr_user_no='+ID_Num+'&uid='+_id;
    public_ajax.call_request('get',focusNOT_url,focusOrNot);
}
//=========
function succeedFail(data) {
    var t ='操作成功';
    if (!data){t='操作失败'}else {
        setTimeout(function () {
            public_ajax.call_request('get',focusOn_url,focusOn);
            public_ajax.call_request('get',fans_url,fans);
        },700);
    };
    $('#focusOrNot p').text(t);
    $('#focusOrNot').modal('show');
}

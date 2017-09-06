var timingTask_url='/weibo_xnr_manage/wxnr_timing_tasks/?user_id='+ID_Num;
public_ajax.call_request('get',timingTask_url,timingTask);
var TYPE={
    'origin':'原创','retweet':'转发','comment':'评论'
}
function timingTask(data) {
    console.log(data);
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

//========历史消息====
var historyNews_url='/weibo_xnr_manage/show_history_posting/?xnr_user_no='+ID_Num+'&task_source=daily_post,business_post';
public_ajax.call_request('get',historyNews_url,historyNews);
function historyNews(data) {

}
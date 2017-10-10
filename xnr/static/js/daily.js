var dailyLOG_Url='/system_manage/show_log_list/';
public_ajax.call_request('get',dailyLOG_Url,dailyLOG);
function dailyLOG(data) {
    console.log(data)
    $('#loglist').bootstrapTable('load', data);
    $('#loglist').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 8,//单页记录数
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
                field: "user_id",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "用户名",//标题
                field: "user_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.user_name==''||row.user_name=='null'||row.user_name=='unknown'){
                        return row.user_id;
                    }else {
                        return row.user_name;
                    };
                }
            },
            {
                title: "登陆时间",//标题
                field: "login_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.login_time==''||row.login_time=='null'||row.login_time=='unknown'||row.login_time.length==0){
                        return '未知';
                    }else {
                        var y=[];
                        for(var j of row.login_time){
                            y.push(getLocalTime(j))
                        }
                        return y.join('<br/>');
                    };
                }
            },
            {
                title: "登录IP",//标题
                field: "login_ip",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.login_ip==''||row.login_ip=='null'||row.login_ip=='unknown'){
                        return '未知';
                    }else {
                        return row.login_ip.join('<br/>');
                    };
                }
            },
            {
                title: "操作时间",//标题
                field: "operate_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.operate_time==''||row.operate_time=='null'||row.operate_time=='unknown'){
                        return '无内容';
                    }else {
                        return getLocalTime(row.operate_time);
                    };
                }
            },
            {
                title: "操作内容",//标题
                field: "operate_content",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.operate_content==''||row.operate_content=='null'||row.operate_content=='unknown'){
                        return '无内容';
                    }else {
                        return row.operate_content.join('<br/>');
                    };
                }
            },
            {
                title: "删除",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor:pointer;color:white;" onclick="deleteLog(\''+row.log_id+'\')"><i class="icon icon-trash"></i></span>';
                }
            },
        ],
    });
}
// 添加
function AddLogSure() {
    var user_id=$('#addLogModal .user_id').val(),user_name=$('#addLogModal .user_name').val(),
        login_time=$('#addLogModal .login_time').val(),login_ip=$('#addLogModal .login_ip').val(),
        operate_time=$('#addLogModal .operate_time').val(),operate_content=$('#addLogModal .operate_content').val();
    if (user_id||user_name||login_time||login_ip||operate_time||operate_content){
        var addLog_url='/system_manage/create_log_list/?user_id='+user_id+'&user_name='+user_name+
            '&login_time='+(Date.parse(new Date(login_time))/1000)+'&login_ip='+login_ip+
            '&operate_time='+(Date.parse(new Date(operate_time))/1000)+'&operate_content='+operate_content;
        public_ajax.call_request('get',addLog_url,successFail);
    }else {
        $('#pormpt p').text('请检查您输入的内容，不能为空。');
        $('#pormpt').modal('show');
    }
}
//删除
var login_id='';
function deleteLog(_id) {
    $('#delAgain').modal('show');
    login_id=_id;
}
function sureDelLog() {
    var delLOG_Url='/system_manage/delete_log_list/?log_id='+login_id;
    public_ajax.call_request('get',delLOG_Url,successFail);
}
function successFail(data) {
    console.log(data)
    var f='';
    if (data[0]||data||data[0][0]){
        f='操作成功';
        setTimeout(function () {
            public_ajax.call_request('get',dailyLOG_Url,dailyLOG);
        },700);
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
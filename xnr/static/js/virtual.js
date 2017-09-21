var virtual_url='/system_manage/show_users_account/';
public_ajax.call_request('get',virtual_url,virtual);
function virtual(data) {
    console.log(data);
    $('#virtualtable').bootstrapTable('load', data);
    $('#virtualtable').bootstrapTable({
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
                title: "虚拟人管理",//标题
                field: "my_xnrs",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.my_xnrs==''||row.my_xnrs=='null'||row.my_xnrs=='unknown'||row.my_xnrs.length==0){
                        return '无任何虚拟人';
                    }else {
                        return row.my_xnrs.join('，');
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
                    return '<span style="cursor:pointer;color:white;" onclick="addVirModify(\''+row.user_id+'\',\''+row.user_name+'\',\''+row.my_xnrs+'\')" title="编辑"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<span style="cursor:pointer;color:white;" onclick="deleteVir(\''+row.user_id+'\',\''+row.my_xnrs+'\')" title="删除"><i class="icon icon-trash"></i></span>';
                }
            },
        ],
    });
};
//添加新的账户
function addAccountSure() {
    var user_id=$('#addAccountModal .user_id').val();
    var user_name=$('#addAccountModal .user_name').val();
    var my_xnrs=$('#addAccountModal .my_xnrs').val().toString().replace(/，/g,',');
    if (user_id||user_name||my_xnrs){
        var addAccount_url='/system_manage/create_user_account/?user_id='+user_id+'&user_name='+user_name+'&my_xnrs='+my_xnrs;
        public_ajax.call_request('get',addAccount_url,successFail);
    }else {
        $('#pormpt p').text('请检查虚拟人账号的信息，不能为空。');
        $('#pormpt').modal('show');
    }
};

//编辑虚拟人
var nowNewXnr;
function addVirModify(userID,userName,myXnrs) {
    nowNewXnr=userID;
    $('#modifyAccount .userID').val(userID);
    $('#modifyAccount .userName').val(userName);
    var xnrlist=myXnrs.split(','),str='';
    for (var i of xnrlist){
        str+=
            '<p class="everyXnr"><span>'+i+'</span>&nbsp;&nbsp;&nbsp;&nbsp;' +
            '<b class="icon icon-trash" title="删除此虚拟人" style="cursor:pointer;" onclick="delXnr(this)"></b></p>'
    }
    $('#modifyAccount .nowXnr').html(str);
    $('#modifyAccount').modal('show');
}
function modifyAccountSure() {
    var user_id=$('#modifyAccount .userID').val();
    var user_name=$('#modifyAccount .userName').val();
    if (user_id||user_name){
        var xnr_span=$('#modifyAccount .nowXnr').find('span');
        var xnrSpans=[];
        for (var a in xnr_span){xnrSpans.push($(a).text())};
        var my_xnrs=$('#modifyAccount .my_xnrs').val().toString().replace(/，/g,',');
        var modify_url='/system_manage/change_user_account/?user_id='+user_id+'&user_name='+user_name+
            '&my_xnrs='+xnrSpans.join(',');
        public_ajax.call_request('get',modify_url,successFail);
    }else {
        $('#pormpt p').text('账号ID和用户名不能为空。');
        $('#pormpt').modal('show');
    }
}
//删除账户
var del_id='',del_account='';
function deleteVir(_id,account) {
    del_id=_id,del_account=account;
    $('#delPrompt').modal('show');
}
function delVirSure() {
    var delVir_url='/system_manage/delete_user_xnraccount/?account_id='+del_id+'&xnr_accountid='+del_account;
    public_ajax.call_request('get',delVir_url,successFail);
}

//删除指定的虚拟人
function delXnr(_this) {
    var xnrNum=$(_this).prev().text();
    var delXne_url='/system_manage/delete_user_xnraccount/?account_id='+nowNewXnr+'&xnr_accountid='+xnrNum;
    public_ajax.call_request('get',delXne_url,successFail);
}
//为指定账户下添加虚拟人
var addXnrGone=0;
function addVirSure() {
    var accountid=$('#modifyAccount .modAct .newXnrList').val().toString().replace(/，/g,',');
    if (accountid){
        addXnrGone=1;
        var new_vir_url='/system_manage/add_user_xnraccount/?account_id='+nowNewXnr+'&xnr_accountid='+accountid;
        public_ajax.call_request('get',new_vir_url,successFail);
    }else {
        $('#pormpt p').text('虚拟人账号不能为空。');
        $('#pormpt').modal('show');
    }
}

//=====
function successFail(data) {
    console.log(data)
    var f='';
    if (data[0]||data||data[0][0]){
        f='操作成功';
        if (addXnrGone==1){
            var accountids=$('#modifyAccount .modAct .newXnrList').val().toString().replace(/，/g,',').split(','),str='';
            for (var i of accountids){
                str+=
                    '<p class="everyXnr"><span>'+i+'</span>&nbsp;&nbsp;&nbsp;&nbsp;' +
                    '<b class="icon icon-trash" title="删除此虚拟人" style="cursor:pointer;" onclick="delXnr(this)"></b></p>'
            }
            $('#modifyAccount .nowXnr').append(str);
            addXnrGone=0;
        }
    }else {f='操作失败'}
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}


//给指定账户添加新的虚拟人
// var current_id='';
// function addVir(_id) {
//     current_id=_id;
//     $('#addVir').modal('show');
// }
// function addVirSure() {
//     var accountid=$('#addVir .addVirContent .vir').val().toString().replace(/，/g,',');
//     if (accountid){
//         var new_vir_url='/system_manage/add_user_xnraccount/?account_id='+_id+'&xnr_accountid='+accountid;
//         public_ajax.call_request('get',new_vir_url,successFail);
//     }else {
//         $('#pormpt p').text('虚拟人账号不能为空。');
//         $('#pormpt').modal('show');
//     }
// }
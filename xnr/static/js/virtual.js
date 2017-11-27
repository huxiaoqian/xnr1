var virtual_url='/system_manage/show_users_account/?main_user='+admin;
public_ajax.call_request('get',virtual_url,virtual);
function virtual(data) {
    $('#virtualtable').bootstrapTable('load', data);
    $('#virtualtable').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
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
            // {
            //     title: "用户ID",//标题
            //     field: "user_id",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            // },
            {
                title: "平台名称",//标题
                field: "platform_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.platform_name==''||row.platform_name=='null'||row.platform_name=='unknown'||!row.platform_name){
                        return '未知';
                    }else {
                        return row.platform_name;
                    };
                }
            },
            {
                title: "已完成虚拟人",//标题
                field: "complete_xnr_list",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.complete_xnr_list==''||row.complete_xnr_list=='null'||!row.complete_xnr_list
                        ||row.complete_xnr_list=='unknown'||row.complete_xnr_list.length==0){
                        return '无任何虚拟人';
                    }else {
                        return row.complete_xnr_list.join('，');
                    };
                }
            },
            {
                title: "未完成虚拟人",//标题
                field: "uncomplete_xnr_list",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uncomplete_xnr_list==''||row.uncomplete_xnr_list=='null'||!row.uncomplete_xnr_list
                        ||row.uncomplete_xnr_list=='unknown'||row.uncomplete_xnr_list.length==0){
                        return '无任何虚拟人';
                    }else {
                        return row.uncomplete_xnr_list.join('，');
                    };
                }
            },
            // {
            //     title: "操作",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return '<span style="cursor:pointer;color:white;" onclick="addVirModify(\''+row.user_id+'\',\''+row.user_name+'\',\''+row.my_xnrs+'\')" title="编辑"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
            //             '<span style="cursor:pointer;color:white;" onclick="deleteVir(\''+row.user_id+'\',\''+row.my_xnrs+'\')" title="删除"><i class="icon icon-trash"></i></span>';
            //     }
            // },
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
var del_id='',del_account='',delCnrGone=0;
function deleteVir(_id,account) {
    del_id=_id,del_account=account;
    $('#delPrompt').modal('show');
}
function delVirSure() {
    var delVir_url='/system_manage/delete_user_xnraccount/?account_id='+del_id
    public_ajax.call_request('get',delVir_url,successFail);
}
//删除指定的虚拟人
var thisXnr;
function delXnr(_this) {
    thisXnr=_this;
    var xnrNum=$(_this).prev().text();delCnrGone=1;
    var delXne_url='/system_manage/delete_user_xnraccount/?account_id='+nowNewXnr+'&xnr_accountid='+xnrNum;
    public_ajax.call_request('get',delXne_url,successFail);
}
function delThis() {
    $(thisXnr).parent().remove();
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
        if (delCnrGone==1){
            delThis();
            delCnrGone=0;
        }
        setTimeout(function () {
            public_ajax.call_request('get',virtual_url,virtual);
        },700);
    }else {f='操作失败'}
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}


//虚拟人通道管理
var xnr_road_url='/system_manage/show_xnr_map_relationship/?main_user='+admin;
public_ajax.call_request('get',xnr_road_url,xnr_road);
function xnr_road(data) {
    $('#virtualtable_2').bootstrapTable('load', data);
    $('#virtualtable_2').bootstrapTable({
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
                title: "微博虚拟人",//标题
                field: "weibo_xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.weibo_xnr_user_no==''||row.weibo_xnr_user_no=='null'||row.weibo_xnr_user_no=='unknown'||!row.weibo_xnr_user_no){
                        return '未知';
                    }else {
                        var name=row.weibo_xnr_name;
                        if (!name){name=row.weibo_xnr_user_no}
                        var Nm=name+'（'+row.weibo_xnr_user_no+'）\n';
                        return Nm;
                    };
                }
            },
            {
                title: "QQ虚拟人",//标题
                field: "qq_xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.qq_xnr_user_no==''||row.qq_xnr_user_no=='null'||!row.qq_xnr_user_no||row.qq_xnr_user_no=='unknown'){
                        return '无任何虚拟人';
                    }else {
                        var name=row.qq_xnr_name;
                        if (!name){name=row.qq_xnr_user_no}
                        var Nm=name+'（'+row.qq_xnr_user_no+'）\n';
                        return Nm;
                    };
                }
            },
            {
                title: "微信虚拟人",//标题
                field: "weixin_xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.weixin_xnr_user_no==''||row.weixin_xnr_user_no=='null'||!row.weixin_xnr_user_no||row.weixin_xnr_user_no=='unknown'){
                        return '无任何虚拟人';
                    }else {
                        var name=row.weixin_xnr_name;
                        if (!name){name=row.weixin_xnr_user_no}
                        var Nm=name+'（'+row.weixin_xnr_user_no+'）\n';
                        return Nm;
                    };
                }
            },
            {
                title: "faceBook虚拟人",//标题
                field: "facebook_xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.facebook_xnr_user_no==''||row.facebook_xnr_user_no=='null'||!row.facebook_xnr_user_no||row.facebook_xnr_user_no=='unknown'){
                        return '无任何虚拟人';
                    }else {
                        var name=row.facebook_xnr_name;
                        if (!name){name=row.facebook_xnr_user_no}
                        var Nm=name+'（'+row.facebook_xnr_user_no+'）\n';
                        return Nm;
                    };
                }
            },
            {
                title: "twitter虚拟人",//标题
                field: "twitter_xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.twitter_xnr_user_no==''||row.twitter_xnr_user_no=='null'||!row.twitter_xnr_user_no||row.twitter_xnr_user_no=='unknown'){
                        return '无任何虚拟人';
                    }else {
                        var name=row.twitter_xnr_name;
                        if (!name){name=row.twitter_xnr_user_no}
                        var Nm='<span>'+name+'<br/>（'+row.twitter_xnr_user_no+'）</span>';
                        return Nm;
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
                    return '<span style="cursor:pointer;color:white;" onclick="addRoad(\'2\')" title="编辑"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<span style="cursor:pointer;color:white;" onclick="deleteRoadXnrInfo(\''+row.id+'\')" title="删除"><i class="icon icon-trash"></i></span>';
                }
            },
        ],
    });
}
//添加通道
var add_or_mondify;
function addRoad(num) {
    add_or_mondify=num;
    var add_road_url='/system_manage/control_add_xnr_map_relationship/?main_user='+admin;
    public_ajax.call_request('get',add_road_url,roadXnrModify);
}
// 编辑和添加通道
function roadXnrModify(data) {
    listIDname=[];
    var weibo=everyRoad(data['weibo_xnr_list'],'weibo');
    var qq=everyRoad(data['qq_xnr_list'],'qq');
    var weixin=everyRoad(data['weixin_xnr_list'],'weixin');
    var faceBook=everyRoad(data['facebook_xnr_list'],'faceBook');
    var twitter=everyRoad(data['twitter_xnr_list'],'twitter');
    $('#modifyAndAddRoad .weibolist').html(weibo);
    $('#modifyAndAddRoad .QQlist').html(qq);
    $('#modifyAndAddRoad .wxlist').html(weixin);
    $('#modifyAndAddRoad .fblist').html(faceBook);
    $('#modifyAndAddRoad .twlist').html(twitter);
    $('#modifyAndAddRoad h4.tit').text('添加通道');
    $('#modifyAndAddRoad').modal('show');
}
function everyRoad(roadArray,key) {
    var str='';
    if (roadArray.length==0){
        str='<b style="display:inline-block;width: 100%;text-align: center;">暂无虚拟人</b>';
    }else {
        $.each(roadArray,function (index,item) {
            var a=item.xnr_name;
            if(!a){a=item.xnr_user_no};
            str+=
                '<label class="demo-label" title="'+a+'">' +
                '   <input class="demo-radio" type="radio" name="'+key+'" valueID="'+item.xnr_user_no+'" valueName="'+a+'">' +
                '   <span class="demo-checkbox demo-radioInput"></span> '+a+
                '</label>';
        })
    }
    return str;
}
//确定添加
var listIDname=[];
function sureAddModify() {
    var weiboID=$('#modifyAndAddRoad input:radio[name="weibo"]:checked').attr('valueID')||'';listIDname.push(weiboID);
    var weiboName=$('#modifyAndAddRoad input:radio[name="weibo"]:checked').attr('valueName')||'';
    var qqID=$('#modifyAndAddRoad input:radio[name="qq"]:checked').attr('valueID')||'';listIDname.push(qqID);
    var qqName=$('#modifyAndAddRoad input:radio[name="qq"]:checked').attr('valueName')||'';
    var weixinID=$('#modifyAndAddRoad input:radio[name="weixin"]:checked').attr('valueID')||'';listIDname.push(weixinID);
    var weixinName=$('#modifyAndAddRoad input:radio[name="weixin"]:checked').attr('valueName')||'';
    var faceBookID=$('#modifyAndAddRoad input:radio[name="faceBook"]:checked').attr('valueID')||'';listIDname.push(faceBookID);
    var faceBookName=$('#modifyAndAddRoad input:radio[name="faceBook"]:checked').attr('valueName')||'';
    var twitterID=$('#modifyAndAddRoad input:radio[name="twitter"]:checked').attr('valueID')||'';listIDname.push(twitterID);
    var twitterName=$('#modifyAndAddRoad input:radio[name="twitter"]:checked').attr('valueName')||'';
    if (listIDname.length<2){
        $('#pormpt p').text('请选择虚拟人,最少2个。');
        $('#pormpt').modal('show');
    }else {
        var mid='';
        if (add_or_mondify=='1'){
            mid='add_xnr_map_relationship';
        }else {
            mid='update_xnr_map_relationship';
        }
        var addModify_url='/system_manage/'+mid+'/?main_user='+admin+'&weibo_xnr_user_no='+weiboID+
            '&weibo_xnr_name='+weiboName+'&qq_xnr_user_no='+qqID+'&qq_xnr_name='+qqName+'&weixin_xnr_user_no='+weixinID+
            '&weixin_xnr_name='+weixinName+'&facebook_xnr_user_no='+faceBookID+'&facebook_xnr_name='+faceBookName+
            '&twitter_xnr_user_no='+twitterID+'&twitter_xnr_name='+twitterName;
        public_ajax.call_request('get',addModify_url,sufa);
    }

}
//system_manage/change_xnr_platform/?origin_platform=weibo&origin_xnr_user_no=WXNR0001&new_platform=qq

function checkUndefined(f) {
    if (f){listIDname.push(f)};
}
//删除通道
var map_id;
function deleteRoadXnrInfo(mapID) {
    map_id=mapID;
    $('#delroad').modal('show');
}
function deleteRoadXnr() {
    var del_url='/system_manage/delete_xnr_map_relationship/?xnr_map_id='+map_id;
    public_ajax.call_request('get',del_url,sufa);
}
function sufa(data) {
    var f='';
    if (data){
        f='操作成功';
        setTimeout(function () {
            public_ajax.call_request('get',xnr_road_url,xnr_road);
        },1000)
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');

}


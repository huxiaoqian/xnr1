function has_table_QQ(has_data_QQ) {
    var sourcePER=eval(has_data_QQ);
    $('.has_list_QQ #haslistQQ').bootstrapTable('load', sourcePER);
    $('.has_list_QQ #haslistQQ').bootstrapTable({
        data:sourcePER,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize:10,//单页记录数
        pageList: [15,20,25],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: true,//回车搜索
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
                field: "xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.xnr_user_no == '' || row.xnr_user_no == 'null' || row.xnr_user_no == 'unknown'||!row.xnr_user_no) {
                        return '未知';
                    } else {
                        return row.xnr_user_no;
                    };
                }
            },
            {
                title: "QQ号码",//标题
                field: "qq_number",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.qq_number == '' || row.qq_number == 'null' || row.qq_number == 'unknown'||!row.qq_number) {
                        return '未知';
                    } else {
                        return row.qq_number;
                    };
                }
            },
            {
                title: "QQ群",//标题
                field: "qq_groups",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.qq_groups == '' || row.qq_groups == 'null' || row.qq_groups == 'unknown'||!row.qq_groups||row.qq_groups.length==0) {
                        return '未知';
                    } else {
                        // return row.qq_groups.join('\n');
                        return row.qq_groups.join('<br/>');
                    };
                }
            },
            {
                title: "QQ群数量",//标题
                field: "qq_group_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.qq_group_num == '' || row.qq_group_num == 'null' || row.qq_group_num == 'unknown'||!row.qq_group_num) {
                        return '未知';
                    } else {
                        return row.qq_group_num;
                    };
                }
            },
            {
                title: "昵称",//标题
                field: "nickname",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.nickname==''||row.nickname=='null'||row.nickname=='unknown'||!row.nickname){
                        return '未知';
                    }else {
                        return row.nickname;
                    }
                }
            },
            {
                title: "创建时间",//标题
                field: "create_ts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_ts==''||row.create_ts=='null'||row.create_ts=='unknown'||!row.create_ts){
                        return '未知';
                    }else {
                        return getLocalTime(row.create_ts);
                    }
                }
            },
            {
                title: "今日发言量",//标题
                field: "daily_post_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     if (row.daily_post_num==''||row.daily_post_num=='null'||row.daily_post_num=='unknown'){
                //         return '未知';
                //     }else {
                //         return row.daily_post_num;
                //     }
                // },
            },
            {
                title: "历史发言量",//标题
                field: "total_post_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     if (row.total_post_num==''||row.total_post_num=='null'||row.total_post_num=='unknown'){
                //         return '未知';
                //     }else {
                //         return row.total_post_num;
                //     }
                // },
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
                    }
                },
            },
            {
                title: "登录状态",//标题
                field: "login_status",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.login_status){return '在线'}else{return '离线'}
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
                    var group_info=JSON.parse(row.group_info);
                    var qq_groups=[];
                    for (var t in group_info){
                        var len=group_info[t]['group_name'];
                        qq_groups.push(len[len.length-1]+'('+t+')');
                    }
                    var ld;
                    if (row.login_status){ld = '在线中'}else{ld = '登录'}
                    return '<a style="cursor: pointer;color:white;" onclick="nowGroup(\''+qq_groups.join('，')+'\',\''+row.xnr_user_no+'\',\''+row.qq_number+'\')" title="编辑"><i class="icon icon-edit"></i></a>&nbsp;&nbsp;'+
                        '<a in_out="out" style="cursor: pointer;color:white;" onclick="loginIN(this,\''+row.qq_number+'\',\''+qq_groups.join('，')+'\',\''+row.nickname+'\',\''+row.xnr_user_no+'\')" title="'+ld+'"><i class="icon icon-key"></i></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color:white;display: inline-block;" onclick="enterIn(\''+row.xnr_user_no+'\',\''+row.qq_number+'\',\''+row.login_status+'\',this)" title="进入"><i class="icon icon-link"></i></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color:white;" onclick="deletePerson(\''+row.xnr_user_no+'\')" title="删除"><i class="icon icon-trash"></i></a>';
                },
            },
        ],
    });
    $('.has_list_QQ #haslistQQ p').hide();
}
var url_QQ = '/qq_xnr_manage/show_qq_xnr/';
public_ajax.call_request('GET',url_QQ,has_table_QQ);
//编辑群
var xnrThis,qqNumThis;
function nowGroup(groupName,id,qqNum) {
    xnrThis=id,qqNumThis=qqNum;
    var groupList=groupName.split('，');
    var str='';
    $.each(groupList,function (index,item) {
        str+='<span style="display: inline-block;padding: 3px 6px;background: #176595;margin:10px 10px 0 0;"><b>'+item+
            '</b>&nbsp;<i class="icon icon-remove" onclick="delThisGroup(this)" style="cursor: pointer;" title="删除"></i></span>'
    });
    $('#modGroup .nowGroup').html(str);
    $('#modGroup').modal('show');
}
var hideThis;
function delThisGroup(_this) {
    hideThis=_this;
    $('#delThisGroupInfor').modal('show');
}
function Iamdel() {
    var num=$(hideThis).prev().text().toString().split(/[()]/)[1];
    var del_url='/qq_xnr_manage/delete_group/?xnr_user_no='+xnrThis+'&group_numbers='+num;
    public_ajax.call_request('get',del_url,delGroupBack);
}
function delGroupBack(data) {
    var f='删除失败。';
    if(data[0]){
        f='删除成功。';$(hideThis).parent().remove();
        setTimeout(function () {
            public_ajax.call_request('GET',url_QQ,has_table_QQ);
        },1500);
    }else {
        f+=data[1]+'。';
    }
    $('#succee_fail #words').text(f);
    $('#succee_fail').modal('show');
}
var TTqgp,TTqgpName,TTqgpBEIZHU;
function sureModGroup() {
    TTqgp=$('#modGroup .QQgroup').val().toString().replace(/,/g,'，');
    TTqgpName=$('#modGroup .QQgroupName').val().toString().replace(/,/g,'，');
    TTqgpBEIZHU=$('#modGroup .QQgroupbeizhu').val().toString().replace(/,/g,'，');
    var qqAdd_url='/qq_xnr_manage/add_qq_xnr/?qq_number='+qqNumThis+'&group_numbers='+TTqgp+'&group_names='
        +TTqgpName+'&mark_names='+TTqgpBEIZHU;
    public_ajax.call_request('get',qqAdd_url,addOR);
}
//登陆一个QQ虚拟人
var $this_QQ,$this_QQ_id;
function loginIN(_this,id,qgp,qname,qpower) {
    $this_QQ=_this;
    $this_QQ_id=id;xnrThis=qpower;
    var login_1_url='/qq_xnr_manage/click_login/?xnr_user_no='+qpower;
    public_ajax.call_request('get',login_1_url,login_1);
}
function login_1(data) {
    if (data){
        var login_2_url='/qq_xnr_manage/login_status/?xnr_user_no='+xnrThis;
        $.ajax({
            type:'GET',
            url:login_2_url,
            async:true,
            dataType:"json",
            success:function (data) {
                if (data){
                    $('#succee_fail #words').text('您的QQ号码已经自动登录。');
                    $('#succee_fail').modal('show');
                }else {
                    var login_url='/qq_xnr_manage/get_qr_code/?qq_number='+$this_QQ_id;
                    public_ajax.call_request('get',login_url,login_QR_code);
                }
            },
            //cache:false,//不会从浏览器缓存中加载请求信息
        });
    }else {
        $('#succee_fail #words').text('您的QQ号码出现问题，请稍后再登陆。');
        $('#succee_fail').modal('show');
    }
}
function login_QR_code(data) {
    if (data){
        if (data=='login'){
            $('#succee_fail #words').text('该QQ已经自动登录。');
            $('#succee_fail').modal('show');
            setTimeout(function () {
                public_ajax.call_request('GET','/qq_xnr_manage/show_qq_xnr/',has_table_QQ);
            },1500);
        }else if(data=='try later'){
            $('#succee_fail #words').text('系统繁忙，稍后再试。');
            $('#succee_fail').modal('show');
            return false;
        }else {
            var kl=data.toString();
            if (kl.substring(kl.length-3)!='png'){
                $('#succee_fail #words').text('您的QQ号码已经在线。');
                $('#succee_fail').modal('show');
            }else {
                var _src='/static/images/QQ/'+data;
                $('#QR_code #QQ_picture .imageqq').attr('src',_src);
                $('#QR_code').modal('show');
            }
        };
        if (document.getElementsByClassName('imageqq')[0].complete){
            var inout=$($this_QQ).attr('in_out');
            if (inout=='out'){
                $($this_QQ).attr('title','在线中').parent().prev().text('在线');
                $($this_QQ).attr('in_out','in');
            }else {
                $($this_QQ).attr('title','登录').parent().prev().text('离线');
                $($this_QQ).attr('in_out','out');
            }
        }
    }else {
        $('#succee_fail #words').text('登陆失败，请稍后重试。');
        $('#succee_fail').modal('show');
    }
}
$('#QR_code').one('hidden.bs.modal', function (e) {
    $('#modGroup .QQgroup').val('');
    $('#modGroup .QQgroupName').val('');
    $('#modGroup .QQgroupbeizhu').val('');
    setTimeout(function () {
        public_ajax.call_request('GET','/qq_xnr_manage/show_qq_xnr/',has_table_QQ);
    },1500);
})
//删除一个虚拟人
var thisDelNum='';
function deletePerson(num) {
    thisDelNum=num;
    $('#delQQxnr').modal('show');
}
function sureDel(QQnumber) {
    var del_url='/qq_xnr_manage/delete_qq_xnr/?qq_number='+thisDelNum;
    public_ajax.call_request('get',del_url,success_fail);
}
function success_fail(data) {
    var flag=eval(data),word;
    if (flag==1){
        word='删除成功。';
        setTimeout(function () {
            public_ajax.call_request('GET',url_QQ,has_table_QQ);
        },800)
    }else {
        word='删除失败。';
    }
    $('#succee_fail #words').text(word);
    $('#succee_fail').modal('show');
}

//进入虚拟人的具体操作
function enterIn(QQ_id,QQ_num,status,_this) {
    var d=$(_this).parent().prev().text();
    if (d=='在线'){
        window.open('/control/postingQQ/?QQ_id='+QQ_id+'&QQ_num='+QQ_num);
    }else {
        $('#succee_fail #words').text('请先登录在进行其他操作。');
        $('#succee_fail').modal('show');
    }
}

//添加虚拟人
var k=1;
$('.hasAddQQ').on('click',function () {
    if (k==1){
        $('.addQQperson').slideDown(30,function(){
            k=0;
            // 滚动到底部
            $('html, body, #containe').animate({scrollTop: $(document).height()},'slow');
        });
    }else {
        $('.addQQperson').slideUp(20);
        k=1;
    }
})
$('.optClear').on('click',function () {
    $('.QQoptions .QQnumber').val('');
    $('.QQoptions .QQgroup').val('');
    $('.QQoptions .QQname').val('');
    $('.QQoptions .QQtime').val('');
    $('.QQoptions .QQpower').val('');
});
$('.optSureadd').on('click',function () {
    var qnum=$('.QQoptions .QQnumber').val();
    var qgp=$('.QQoptions .QQgroup').val().toString().replace(/,/g,'，');
    var qgpName=$('.QQoptions .QQgroupName').val().toString().replace(/,/g,'，');
    var qgpBEIZHU=$('.QQoptions .QQgroupbeizhu').val().toString().replace(/,/g,'，');
    var qname=$('.QQoptions .QQname').val();
    var qpower=$('.QQoptions .QQpower').val();
    var qremark=$('.QQoptions .QQxnrBEIZHU').val();
    if (!(qnum||qgp||qname||qpower)){
        $('#succee_fail #words').text('请检查您填写的内容。（不能为空）');
        $('#succee_fail').modal('show');
    }else {
        var qqAdd_url='/qq_xnr_manage/add_qq_xnr/?qq_number='+qnum+'&group_numbers='+qgp+'&group_names='+qgpName+
            '&mark_names='+qgpBEIZHU+'&qq_nickname='+qname+'&remark='+qremark+'&access_id='+qpower+'&submitter='+admin;
        public_ajax.call_request('get',qqAdd_url,addOR);
    }
});
function addOR(data) {
    var Iadd='添加失败。';
    if (data[0]){
        Iadd='添加成功。';
        if (data[1].length!=0){Iadd+='<br/>重复添加的QQ群：'+data[1].join('，')}
        var a=TTqgp.split('，'),b=TTqgpName.split('，');
        $('#modGroup .QQgroup').val('');
        $('#modGroup .QQgroupName').val('');
        $('#modGroup .QQgroupbeizhu').val('');
        $.each(a,function (index,item) {
            $('#modGroup .nowGroup').append('<span style="display: inline-block;padding: 3px 6px;background: #176595;margin:10px 10px 0 0;"><b>'+b[index]+'('+item+')'+
                '</b>&nbsp;<i class="icon icon-remove" onclick="delThisGroup(this)" style="cursor: pointer;" title="删除"></i></span>');
        });
        setTimeout(function () {
            public_ajax.call_request('GET',url_QQ,has_table_QQ);
        },1500);
    }else {
        Iadd+=data[1];
    }
    $('#succee_fail #words').text(Iadd);
    $('#succee_fail').modal('show');
}




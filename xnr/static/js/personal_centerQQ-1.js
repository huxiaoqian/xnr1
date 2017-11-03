function has_table_QQ(has_data_QQ) {
    let sourcePER=eval(has_data_QQ);
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
                    var ld;
                    if (row.login_status){ld = '在线中'}else{ld = '登录'}
                    return '<a in_out="out" style="cursor: pointer;color:white;" onclick="loginIN(this,\''+row.qq_number+'\',\''+row.qq_groups.join('，')+'\',\''+row.nickname+'\',\''+row.access_id+'\')" title="'+ld+'"><i class="icon icon-key"></i></a>'+
                        '<a style="cursor: pointer;color:white;display: inline-block;margin:0 10px;" onclick="enterIn(\''+row.xnr_user_no+'\',\''+row.qq_number+'\',\''+row.login_status+'\')" title="进入"><i class="icon icon-link"></i></a>'+
                        '<a style="cursor: pointer;color:white;" onclick="deletePerson(\''+row.qq_number+'\')" title="删除"><i class="icon icon-trash"></i></a>';
                },
            },
        ],
    });
    $('.has_list_QQ #haslistQQ p').hide();
}
var url_QQ = '/qq_xnr_manage/show_qq_xnr/';
public_ajax.call_request('GET',url_QQ,has_table_QQ);

//登陆一个QQ虚拟人
var $this_QQ,$this_QQ_id;
function loginIN(_this,id,qgp,qname,qpower) {
    $this_QQ=_this;
    $this_QQ_id=id;
    var login_1_url='/qq_xnr_manage/add_qq_xnr/?qq_number='+id+'&qq_groups='+qgp+
        '&qq_nickname='+qname+'&access_id='+qpower;
    public_ajax.call_request('get',login_1_url,login_1);
}
function login_1(data) {
    if (data){
        var login_url='/qq_xnr_manage/get_qr_code/?qq_number='+$this_QQ_id;
        public_ajax.call_request('get',login_url,login_QR_code);
    }else {
        $('#succee_fail #words').text('您的QQ号码出现问题，请稍后再登陆。');
        $('#succee_fail').modal('show');
    }
}
function login_QR_code(data) {
    if (data){
        var kl=data.toString();
        if (kl.substring(kl.length-3)!='png'){
            $('#succee_fail #words').text('您的QQ号码已经在线。');
            $('#succee_fail').modal('show');
        }else {
            if(data=='try later'){
                $('#succee_fail #words').text('系统繁忙，稍后再试。');
                $('#succee_fail').modal('show');
            }else {
                var _src='/static/images/QQ/'+data;
                $('#QR_code #QQ_picture .imageqq').attr('src',_src);
                $('#QR_code').modal('show');
                // LL_11-3 模态框显示之后一直获取所有虚拟人数据,判断登录状态以关闭模态框
                var timer1 = setInterval(function(){
                    public_ajax.call_request('GET','/qq_xnr_manage/show_qq_xnr/',getXnr);
                    function getXnr(data){
                        // console.log(data)
                        for(var i=0;i<data.length;i++){
                            if(data[i].qq_number == $this_QQ_id){
                                // 获取当前虚拟人的wxbot_id
                                console.log(data[i].login_status)
                                // 查询此wxbot_id的登录状态  listening时关闭二维码框
                                if(data[i].login_status == true){
                                    $('#QR_code').modal('hide');
                                    window.clearInterval(timer1)
                                }
                            }
                        }
                    }
                }, 500)
                // LL_11-3 模态框关闭之后重新画表
                $('#QR_code').on('hidden.bs.modal', function (e) {
                    // 停止请求
                    window.clearInterval(timer1)
                    public_ajax.call_request('GET','/qq_xnr_manage/show_qq_xnr/',has_table_QQ);
                })
            }
        }
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

//删除一个虚拟人
function deletePerson(QQnumber) {
    var del_url='/qq_xnr_manage/delete_qq_xnr/?qq_number='+QQnumber;
    public_ajax.call_request('get',del_url,success_fail);
}
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

//进入虚拟人的具体操作
function enterIn(QQ_id,QQ_num,status) {
    if (status=='true'){
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
        $('.addQQperson').slideDown(30);
        k=0;
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
    var qname=$('.QQoptions .QQname').val();
    var qpower=$('.QQoptions .QQpower').val();
    if (!(qnum||qgp||qname||qpower)){
        $('#succee_fail #words').text('请检查您填写的内容。（不能为空）');
        $('#succee_fail').modal('show');
    }else {
        var qqAdd_url='/qq_xnr_manage/add_qq_xnr/?qq_number='+qnum+'&qq_groups='+qgp+
            '&qq_nickname='+qname+'&access_id='+qpower;
        public_ajax.call_request('get',qqAdd_url,addOR);
    }
});
function addOR(data) {
    var Iadd='添加失败。';
    if (data){
        Iadd='添加成功。';
    }
    $('#succee_fail #words').text(Iadd);
    $('#succee_fail').modal('show');
}




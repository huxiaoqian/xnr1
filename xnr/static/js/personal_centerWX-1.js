//登录用户名
var admin='admin@qq.com';

// 表格生成
function has_table_WX(has_data_QQ) {
    let sourcePER=eval(has_data_QQ);
    // console.log(sourcePER)
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
                field: "wxbot_id",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.wxbot_id == '' || row.wxbot_id == 'null' || row.wxbot_id == 'unknown'||!row.wxbot_id) {
                        return '未知';
                    } else {
                        return row.wxbot_id;
                    };
                }
            },
            // {
            //     title: "微信号码",//标题
            //     field: "qq_number",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.qq_number == '' || row.qq_number == 'null' || row.qq_number == 'unknown'||!row.qq_number) {
            //             return '未知';
            //         } else {
            //             return row.qq_number;
            //         };
            //     }
            // },
            {
                title: "微信群",//标题
                field: "wx_groups_nickname",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "left",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.wx_groups_nickname == '' || row.wx_groups_nickname == 'null' || row.wx_groups_nickname == 'unknown'||!row.wx_groups_nickname||row.wx_groups_nickname.length==0) {
                        return '未知';
                    } else {
                        return row.wx_groups_nickname.join('<br/>');
                    };
                }
            },
            {
                title: "微信群数量",//标题
                field: "wx_groups_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.wx_groups_num == '' || row.wx_groups_num == 'null' || row.wx_groups_num == 'unknown'||!row.wx_groups_num) {
                        return '未知';
                    } else {
                        return row.wx_groups_num;
                    };
                }
            },
            {
                title: "昵称",//标题
                field: "wx_id",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.wx_id==''||row.wx_id=='null'||row.wx_id=='unknown'||!row.wx_id){
                        return '未知';
                    }else {
                        return row.wx_id;
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
            // {
            //     title: "今日发言量",//标题
            //     field: "daily_post_num",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     // formatter: function (value, row, index) {
            //     //     if (row.daily_post_num==''||row.daily_post_num=='null'||row.daily_post_num=='unknown'){
            //     //         return '未知';
            //     //     }else {
            //     //         return row.daily_post_num;
            //     //     }
            //     // },
            // },
            // {
            //     title: "历史发言量",//标题
            //     field: "total_post_num",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     // formatter: function (value, row, index) {
            //     //     if (row.total_post_num==''||row.total_post_num=='null'||row.total_post_num=='unknown'){
            //     //         return '未知';
            //     //     }else {
            //     //         return row.total_post_num;
            //     //     }
            //     // },
            // },
            // {
            //     title: "备注",//标题
            //     field: "remark",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.remark==''||row.remark=='null'||row.remark=='unknown'){
            //             return '无备注';
            //         }else {
            //             return row.remark;
            //         }
            //     },
            // },
            {
                title: "登录状态",//标题
                field: "login_status",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.login_status == 'logout'){return '离线'}else{return '在线'}
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
                    if (row.login_status=='logout'){ld = '登录'}else{ld = '在线中'}
                    var str = '<a onclick="loginIN(this,\''+row.wxbot_id+'\',\''+row.wx_id+'\')" in_out="out" style="cursor: pointer;color:white;" title="'+ld+'"><i class="icon icon-key"></i></a>';
                    str +='<a onclick="enterIn(\''+row.wxbot_id+'\')" style="cursor: pointer;color:white;display: inline-block;margin:0 10px;"  title="进入"><i class="icon icon-link"></i></a>';
                    str +='<a onclick="deletePerson(\''+row.wxbot_id+'\')" style="cursor: pointer;color:white;margin-right:10px;"  title="删除"><i class="icon icon-trash"></i></a>';
                    str +='<a onclick="logoutPerson(\''+row.wxbot_id+'\')" style="cursor: pointer;color:white;"  title="退出登录"><i class="icon icon-signout"></i></a>';
                    str +='<a onclick="loadallGroups(\''+row.wxbot_id+'\')" style="cursor: pointer;color:white;margin-left:10px;"  title="设置群组"><i class="icon icon-cogs"></i></a>';
                    return str;
                },
            },
        ],
    });
    $('.has_list_QQ #haslistQQ p').hide();
}
var url_WX = '/wx_xnr_manage/show/';
// =========展示所有虚拟人=========
public_ajax.call_request('GET',url_WX,has_table_WX);

//=========登录一个微信虚拟人=========
var $this_WX,$this_WXbot_id,$this_wx_id;
function loginIN(_this, wxbot_id, wx_id) {
    $this_WX=_this;
    $this_WXbot_id=wxbot_id;
    $this_wx_id = wx_id;
    var login_1_url='/wx_xnr_manage/login/?wxbot_id='+wxbot_id;
    // console.log(login_1_url)
    public_ajax.call_request('get',login_1_url,login_QR_code);
}
// function login_1(data) {
//     console.log(data)
//     if (data){
//         var login_url='/qq_xnr_manage/get_qr_code/?qq_number='+$this_QQ_id;
//         // http://219.224.134.213:9088/wx_xnr_manage/create/?wx_id=lvlei&submitter=asdafdssaf
//         // var login_url='/wx_xnr_manage/create/?wx_id=lvlei&submitter=asdafdssaf';
//         // console.log(login_url)
//         public_ajax.call_request('get',login_url,login_QR_code);
//     }else {
//         $('#succee_fail #words').text('您的QQ号码出现问题，请稍后再登陆。');
//         $('#succee_fail').modal('show');
//     }
// }
function login_QR_code(data) {
    // console.log(data)
    if (data){
        var kl=data.toString();
        if (kl.substring(kl.length-3)!='png'){
            $('#succee_fail #words').text('您的微信号码已经在线。');
            $('#succee_fail').modal('show');
        }else {
            // var _src='/static/images/QQ/'+data;
            var start = data.indexOf('/static');
            // 显示二维码
            // $('#QR_code #QQ_picture .imagewx').attr('src',_src);
            $('#QR_code').modal('show');
            $('#QR_code #L-points').empty().append('<center>请使用'+$this_wx_id+'微信扫码登录</center>')
            $('#QR_code #QQ_picture .imagewx').attr('src',data.slice(start));
            // 模态框显示之后一直获取所有虚拟人数据
            var timer1 = setInterval(function(){
                public_ajax.call_request('GET','/wx_xnr_manage/show/',getXnr);
                function getXnr(data){
                    // console.log(data)
                    for(var i=0;i<data.length;i++){
                        if(data[i].wxbot_id == $this_WXbot_id){
                            // 获取当前虚拟人的wxbot_id
                            console.log(data[i].login_status)
                            // 查询此wxbot_id的登录状态  listening时关闭二维码框
                            if(data[i].login_status == "listening"){
                                $('#QR_code').modal('hide');

                                window.clearInterval(timer1)
                            }
                        }
                    }
                }
            }, 500)

            $('#QR_code').on('hidden.bs.modal', function (e) {
                // window.location.reload();
                // 模态框关闭之后重新画表
                public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
                // 判断登录状态
                var checkstatus_url='/wx_xnr_manage/checkstatus/?wxbot_id='+$this_WXbot_id;
                public_ajax.call_request('get',checkstatus_url,checkStatus);
                function checkStatus(data){
                    // console.log(data)
                    if(data!='logout'){
                            $($this_WX).attr('title','在线中').parent().prev().text('在线');
                            $($this_WX).attr('in_out','in');
                    }else {
                            $($this_WX).attr('title','登录').parent().prev().text('离线');
                            $($this_WX).attr('in_out','out');
                    }
                }
            })
        }
    }else {
        $('#succee_fail #words').text('登陆失败，请稍后重试。');
        $('#succee_fail').modal('show');
    }
}

// =========退出登录=========
function logoutPerson(wxbot_id) {
    var _wxbot_id = wxbot_id;
    // 判断登录状态
    var checkstatus_url='/wx_xnr_manage/checkstatus/?wxbot_id='+wxbot_id;
    public_ajax.call_request('get',checkstatus_url,LL_checkStatus);
    function LL_checkStatus(data){
        if(data=='listening'){
            //弹出退出确认框
            $('#L-delete #L-title').text('确认退出登录吗？');
            $('#L-delete').modal('show');
            $('#L-del-sure').on('click',function(){
                var out_url='/wx_xnr_manage/logout/?wxbot_id='+_wxbot_id;
                public_ajax.call_request('get',out_url,logout_success_fail);
            })
        }else{
            $('#succee_fail #words').text('请先登录再进行其他操作！');
            $('#succee_fail').modal('show');
            $('#succee_fail').on('hidden.bs.modal', function (e) {
                // 模态框关闭之后重新画表
                public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
            })
        }
    }
}
function logout_success_fail(data) {
    // console.log(data)
    var flag=eval(data),word;
    if (flag==1){
        word='退出登录成功。';
    }else {
        word='退出登录失败。';
    }
    $('#succee_fail #words').text(word);
    $('#succee_fail').modal('show');

    $('#succee_fail').on('hidden.bs.modal', function (e) {
        // window.location.reload();
        // 模态框关闭之后重新画表
        public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
    })
}

//=========删除一个虚拟人=========
function deletePerson(wxbot_id) {
    var _wxbot_id = wxbot_id;
    //弹出删除确认框
    $('#L-delete').modal('show');
    $('#L-del-sure').on('click',function(){
        var del_url='/wx_xnr_manage/delete/?wxbot_id='+_wxbot_id;
        public_ajax.call_request('get',del_url,success_fail);
    })
    $('#L-delete').on('hidden.bs.modal', function (e) {
        // 模态框关闭之后重新画表
        public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
    })
}
function success_fail(data) {
    // console.log(data)
    var flag=eval(data),word;
    if (flag==1){
        word='删除成功。';
    }else {
        word='删除失败。';
    }
    $('#succee_fail #words').text(word);
    $('#succee_fail').modal('show');
    $('#succee_fail').on('hidden.bs.modal', function (e) {
        // 模态框关闭之后重新画表
        public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
    })
}

//=========进入虚拟人的具体操作=========
function enterIn(WXbot_id) {
    // 判断登录状态
    var checkstatus_url='/wx_xnr_manage/checkstatus/?wxbot_id='+WXbot_id;
    public_ajax.call_request('get',checkstatus_url,LL_checkStatus);

    var _WXbot_id = WXbot_id;
    function LL_checkStatus(data){
        if(data=='listening'){
            // 进入虚拟人
            window.open('/control/postingWX/?WXbot_id='+_WXbot_id);
        }else{
            $('#succee_fail #words').text('请先登录再进行其他操作！');
            $('#succee_fail').modal('show');
            $('#succee_fail').on('hidden.bs.modal', function (e) {
                // 模态框关闭之后重新画表
                public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
            })
        }
    }
}

//===============创建登录虚拟人================
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
// 重填按钮
$('.optClear').on('click',function () {
    $('.QQoptions .wx_id').val('');
    $('.QQoptions .wxRemark').val('');
    $('.QQoptions .email').val('');
    $('.QQoptions .wxPower').val('');
});
// 确定按钮
var new_wx_id;
$('.optSureadd').on('click',function () {
    // var qnum=$('.QQoptions .QQnumber').val();
    var wx_id=$('.QQoptions .wx_id').val();
    new_wx_id = wx_id;
    // var qgp=$('.QQoptions .QQgroup').val().toString().replace(/,/g,'，');
    // var qname=$('.QQoptions .QQname').val();
    // var qpower=$('.QQoptions .QQpower').val();
    var wxPower=$('.QQoptions .wxPower').val();
    var wxremark=$('.QQoptions .wxRemark').val();
    var email=$('.QQoptions .email').val();
    // if (!(qnum||qgp||qname||qpower)){
    if (!(wx_id||wxPower)){
        $('#succee_fail #words').text('请检查您填写的内容。（不能为空）');
        $('#succee_fail').modal('show');
    }else if(wxremark){
        // var qqAdd_url='/qq_xnr_manage/add_qq_xnr/?qq_number='+qnum+'&qq_groups='+qgp+
        //     '&qq_nickname='+qname+'&access_id='+qpower;
        // var wxAdd_url='/wx_xnr_manage/create/?wx_id='+wx_id+'&submitter=asdafdssaf';
        var wxAdd_url='/wx_xnr_manage/create/?wx_id='+wx_id+'&submitter='+admin+'&mail='+email+'&access_id='+wxPower+'&remark='+wxremark;
        // console.log(wxAdd_url)
        public_ajax.call_request('get',wxAdd_url,addOR);
    }else {
        var wxAdd_url='/wx_xnr_manage/create/?wx_id='+wx_id+'&submitter='+admin+'&mail='+email+'&access_id='+wxPower;
        // console.log(wxAdd_url)
        public_ajax.call_request('get',wxAdd_url,addOR);
    }
});
function addOR(data) {
    // ===============10-24=====================
    // 显示二维码
    // console.log(data)
    if(data !='loginedwithcache'){
        // console.log(data.indexOf('/static'))
        var start = data.indexOf('/static');
        // console.log(data.slice(start,data.length))
        // 生成二维码
        // $('#QR_code #QQ_picture .imagewx').attr('src',data.slice(start,data.length));
        $('#QR_code #QQ_picture .imagewx').attr('src',data.slice(start));
        $('#QR_code #L-points').empty().append('<center>请使用'+new_wx_id+'微信扫码登录</center>')
        $('#QR_code').modal('show');
        // 模态框显示之后一直获取所有虚拟人数据
        var L_timer = setInterval(function(){
            public_ajax.call_request('GET','/wx_xnr_manage/show/',getXnr);
            function getXnr(data){
                // console.log(data)
                for(var i=0;i<data.length;i++){
                    if(data[i].wx_id == new_wx_id){
                        // 获取新添加的wx_id的wxbot_id
                        // console.log(data[i].wxbot_id)
                        console.log(data[i].login_status)
                        // 查询此wxbot_id的登录状态  listening时关闭二维码框
                        if(data[i].login_status == "listening"){
                            $('#QR_code').modal('hide');

                            window.clearInterval(L_timer)
                        }
                    }
                }
            }
        }, 1000)

        $('#QR_code').on('hidden.bs.modal', function (e) {
            // 模态框关闭之后重新画表
            public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
        });
    }
}
//=======创建登录虚拟人完成=====================

// ================获取群组===================
var _wxbot_id;
function loadallGroups(wxbot_id){
    _wxbot_id = wxbot_id;

    // 判断登录状态
    var checkstatus_url='/wx_xnr_manage/checkstatus/?wxbot_id='+wxbot_id;
    public_ajax.call_request('get',checkstatus_url,L_checkStatus);

    // var groups_url='/wx_xnr_manage/loadallgroups/?wxbot_id='+wxbot_id;
    // public_ajax.call_request('GET',groups_url,loadallGroups_1);
}
function L_checkStatus (data){
    if(data=='listening'){
        // 获取群组
        var groups_url='/wx_xnr_manage/loadallgroups/?wxbot_id='+_wxbot_id;
        public_ajax.call_request('GET',groups_url,loadallGroups_1);
    }else{
        $('#succee_fail #words').text('请先登录在进行其他操作！');
        $('#succee_fail').modal('show');
        $('#succee_fail').on('hidden.bs.modal', function (e) {
            // 模态框关闭之后重新画表
            public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
        })
    }
}
// ==========展示所有群组=================
function loadallGroups_1(data){
    // console.log(data);
    var str = '';
    for(var i=0;i<data.length;i++){
        str +='<label style="text-align:left;width:30%;" class="demo-label"><input class="demo-radio" type="checkbox" name="L-demo-checkbox" value="'+data[i][0]+'" checked><span class="demo-checkbox demo-radioInput"></span>'+data[i][1]+'</label>';
    }
    $('#setgroups #loadallGroups').empty().append(str)
    $('#setgroups').modal('show');
    // console.log(str)
    // 获取已监听群组（======设为选中--此功能取消，默认选中所有。=========）
    // var loadgroups_url = '/wx_xnr_operate/loadgroups/?wxbot_id='+_wxbot_id;
    // public_ajax.call_request('GET',loadgroups_url,loadGroups);
}
// function loadGroups(data){
//     console.log(data)
//     for(i in data){
//         console.log(i)
//         $('#setgroups #loadallGroups input[value='+i+']').attr('checked',true)
//     }
//     $('#setgroups').modal('show');
//     // 已监听的群组设置checked
//     // $('#setgroups #loadallGroups input[value=""]').attr('checked',true)
// }

// =========设置需要监听的群组=========
$('#L-sure').on('click',function(){
    var id_array=new Array();
    $('input[name="L-demo-checkbox"]:checked').each(function(){
        id_array.push($(this).val());//向数组中添加元素
    });
    var idstr=id_array.join(',');//将数组元素连接起来以构建一个字符串
    // console.log(idstr);
    // console.log(idstr.replace(/\'/g, ""));//去除字符串引号
    var idstr=id_array.join(',').replace(/\'/g, "");

    var setgroups_url='/wx_xnr_manage/setgroups/?wxbot_id='+_wxbot_id+'&group_list='+idstr
    // console.log(setgroups_url)
    public_ajax.call_request('GET',setgroups_url,setGroups);

})
function setGroups(data){
    // console.log(data)
    if(data ==1){
        $('#succee_fail #words').text('设置成功！');
        $('#succee_fail').modal('show');
        $('#succee_fail').on('hidden.bs.modal', function (e) {
            // 设置群组提示模态框关闭之后重新画表
            public_ajax.call_request('GET','/wx_xnr_manage/show/',has_table_WX);
        })
    }
}


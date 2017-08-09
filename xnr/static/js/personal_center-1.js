var public_ajax= {
    call_request:function(ajax_method,url,callback) {
        $.ajax({
            type:ajax_method,
            url:url,
            async:true,
            timeout:300,
            //data:{"name":"xm"},//传参数
            dataType:"json",
            success:callback,
            error:function (xhr,textStatus,errorThrown) {
                //请求失败执行的函数
                console.log("请求失败",textStatus,errorThrown)
            },
            global:false//是否触发全局请求,需要触发就是true,不需要false
        });
    },
    has_table:function (has_data) {
        // var person=window.JSON?JSON.parse(has_data):eval("("+has_data+")");
        var person=eval(has_data)
        console.log(person)
        $.each(data,function (index,item) {
            theme_all.push({
                'name':item[1],
                'include':item[2],
                'time':item[5],
                'keywords':item[3],
                'label':item[4],
            })
        });
        $('.has_list #haslist').bootstrapTable('load', person);
        $('.has_list #haslist').bootstrapTable({
            data:person,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 10,//单页记录数
            pageList: [15,25,35],//分页步进值
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
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     return row[1];
                    // }
                },
                {
                    title: "创建时间",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     return row[2];
                    // }
                },
                {
                    title: "渗透领域",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     return row[5];
                    // },
                },
                {
                    title: "角色定位",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "活跃时间",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "粉丝数",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "历史发帖量",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "历史评论数",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "今日发帖量",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "今日提醒",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '<a style="cursor: pointer;">查看</a>';
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
                        return '<a style="cursor: pointer;" onclick="">进入</a>'+
                            '<a style="cursor: pointer;" onclick="">修改</a>'+
                            '<a style="cursor: pointer;" onclick="">删除</a>';
                    },
                },
            ],
            onClickCell: function (field, value, row, $element) {
                if ($element[0].innerText=='查看') {
                    window.open();
                }else if ($element[0].innerText=='') {
                    window.open();
                }
            }
        });
    },
    not_yet:function (no_data) {
        let undone_person=window.JSON?JSON.parse(no_data):eval("("+no_data+")");
        $.each(data,function (index,item) {
            theme_all.push({
                'name':item[1],
                'include':item[2],
                'time':item[5],
                'keywords':item[3],
                'label':item[4],
            })
        });
        $('.undone_list #undonelist').bootstrapTable('load', undone_person);
        $('.undone_list #undonelist').bootstrapTable({
            data:undone_person,
            search: true,//是否搜索
            pagination: true,//是否分页
            pageSize: 10,//单页记录数
            pageList: [15,25,35],//分页步进值
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
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     return row[1];
                    // }
                },
                {
                    title: "创建时间",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     return row[2];
                    // }
                },
                {
                    title: "渗透领域",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    // formatter: function (value, row, index) {
                    //     return row[5];
                    // },
                },
                {
                    title: "角色定位",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

                    },
                },
                {
                    title: "活跃时间",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {

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
                        return '<a style="cursor: pointer;" onclick="">继续</a>'+
                            '<a style="cursor: pointer;" onclick="">删除</a>';
                    },
                },
            ],
            onClickCell: function (field, value, row, $element) {

            }
        });
    },
    has_table_QQ:function (has_data_QQ) {
        let QQperson=eval(has_data_QQ);
        console.log(QQperson)
        let sourcePER=QQperson.hits.hits;
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
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return index+1;
                    }
                },
                {
                    title: "昵称",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row._source.nickname==''||row._source.nickname=='null'||row._source.nickname=='unbknown'){
                            return '未知';
                        }else {
                            return row._source.nickname;
                        }
                    }
                },
                {
                    title: "创建时间",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row._source.create_ts==''||row._source.create_ts=='null'||row._source.create_ts=='unbknown'){
                            return '未知';
                        }else {
                            return getLocalTime(row._source.create_ts);
                        }
                    }
                },
                {
                    title: "活跃时间",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        if (row._source.active_time==''||row._source.active_time=='null'||row._source.active_time=='unbknown'){
                            return '未知';
                        }else {
                            return row._source.active_time;
                        }
                    },
                },
                {
                    title: "历史发言数",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        // if (row._source.active_time==''||row._source.active_time=='null'||row._source.active_time=='unbknown'){
                        //     return '未知';
                        // }else {
                        //     return row._source.active_time;
                        // }
                    },
                },
                {
                    title: "今日发言量",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        // if (row._source.active_time==''||row._source.active_time=='null'||row._source.active_time=='unbknown'){
                        //     return '未知';
                        // }else {
                        //     return row._source.active_time;
                        // }
                    },
                },
                {
                    title: "登录状态",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        return '离线';
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
                        return '<a style="cursor: pointer;color:white;" onclick="loginIN(this)" title="登录"><i class="icon icon-key"></i></a>'+
                            '<a style="cursor: pointer;color:white;display: inline-block;margin:0 10px;" onclick="enterIn(\''+row._id+'\')" title="进入"><i class="icon icon-link"></i></a>'+
                            '<a style="cursor: pointer;color:white;" onclick="deletePerson(\''+row._id+'\')" title="删除"><i class="icon icon-trash"></i></a>';
                    },
                },
            ],
            onClickCell: function (field, value, row, $element) {

            }
        });
    },
};
var ajax_method='GET';
function auto() {
    //let url_1 = '';
    // let url_2 = '';
    let url_3 = '/qq_xnr_manage/show_qq_xnr/';
    //public_ajax.call_request(ajax_method,url_1,public_ajax.has_table);
    // public_ajax.call_request(ajax_method,url_2,public_ajax.not_yet);
    public_ajax.call_request(ajax_method,url_3,public_ajax.has_table_QQ);
}
auto();

//登陆一个QQ虚拟人
function loginIN(_this) {
    // console.log(QQnumber)
    $(_this).attr('title','在线中').parent().prev().text('在线');
    var trs=$(_this).parents('tr').siblings('tr');
    for(var t=0;t<trs.length;t++){
        $(trs[t]).find('td').eq(6).text('离线');
        $(trs[t]).find('td').eq(7).find('a').eq(0).attr('title','登录');
    }
}
//删除一个虚拟人
function deletePerson(QQnumber) {
    var del_url='/qq_xnr_manage/delete_qq_xnr/?qq_number='+QQnumber;
    public_ajax.call_request(ajax_method,del_url,success_fail);
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
function enterIn(QQ_id) {
    // var if_in=encodeURI($(_this).parent().prev().text());
    window.open('/control/postingQQ/?QQ_id='+QQ_id);
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
});
$('.optSureadd').on('click',function () {
    var qnum=$('.QQoptions .QQnumber').val();
    var qgp=$('.QQoptions .QQgroup').val();
    var qname=$('.QQoptions .QQname').val();
    var qtime=$('.QQoptions .QQtime').val();
    if (!(qnum||qgp||qname||qtime)){
        $('#succee_fail #words').text('请检查您填写的内容。（不能为空）');
        $('#succee_fail').modal('show');
    }else {
        var qqAdd_url='/qq_xnr_manage/add_qq_xnr/?qq_number='+qnum+'&qq_groups='+qgp+'&qq_nickname='+
            qname+'&qq_active_time='+qtime;
        public_ajax.call_request(ajax_method,qqAdd_url,addOR);
    }
});
function addOR(data) {
    var Iadd='';
    if (flag==1){
        Iadd='添加成功。';
    }else {
        Iadd='添加失败。';
    }
    $('#succee_fail #words').text(Iadd);
    $('#succee_fail').modal('show');
}




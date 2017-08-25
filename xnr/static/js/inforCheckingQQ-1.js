var qqnumber='365217204';
//敏感消息
var senNews_url='/qq_xnr_monitor/search_by_xnr_number/?xnr_number='+qqnumber+'&date='+(Number(Date.parse(new Date()))/1000);
public_ajax.call_request('get',senNews_url,senNews);
function senNews(data) {
    var news=data.hits.hits;
    $('#content-1-word').bootstrapTable('load', news);
    $('#content-1-word').bootstrapTable({
        data:news,
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
            {
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    var str=
                        '<div class="everySpeak">'+
                        '   <div class="speak_center">'+
                        '       <div class="center_rel">'+
                        '           <img src="/static/images/post-6.png" class="center_icon">'+
                        '           <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                        '               <b class="name">'+name+'</b> <span>（</span><b class="QQnum">'+row._source.qq_group_number+'</b><span>）</span>' +
                        '               <b class="time" style="display: inline-block;margin-left: 30px;""><i class="icon icon-time"></i>&nbsp;'+getLocalTime(row._source.timestamp)+'</b>  '+
                        '               <span class="joinWord" onclick="joinWord()">加入语料库</span>'+
                        '           </a>'+
                        '           <div class="center_2" style="margin-top: 10px;"><b style="color:blanchedalmond;font-weight: 700;">摘要内容：</b>'+row._source.text+'</div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('.content-1-word .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物qq号码（回车搜索）');
}
//敏感用户
var senUserurl='/qq_xnr_monitor/show_sensitive_users/?xnr_number='+qqnumber;
public_ajax.call_request('get',senUserurl,senUser);
function senUser(data) {
    console.log(data)
    $('#hot-2').bootstrapTable('load', news);
    $('#hot-2').bootstrapTable({
        data:news,
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
            {
                title: "QQ号",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    return name;
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
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    return name;
                }
            },
            {
                title: "好友数量",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    return name;
                }
            },
            {
                title: "敏感发言QQ群",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    return name;
                }
            },
            {
                title: "发言时间",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    return name;
                }
            },
            {
                title: "敏感言论消息",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
                    };
                    return name;
                }
            },
        ],
    });
    $('.hot-2 .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物qq号码（回车搜索）');
}
//选择时间搜索
$('#container .titTime .timeSure').on('click',function () {
    var start=$('.start').val();
    var end=$('.end').val();
    if (start==''||end==''){
        $('#pormpt p').text('请检查时间，不能为空。');
        $('#pormpt').modal('show');
    }else {
        var search_news_url='/qq_xnr_operate/search_by_period/?xnr_number='+qqnumber+'&startdate='+start+'&enddate='+end;
        public_ajax.call_request('get',search_news_url,senNews);
    }
});
//加入语料库
function joinWord(_this) {

}
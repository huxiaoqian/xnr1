function personEarly(personEarly_QQ) {
    var QQperson=eval(personEarly_QQ);
    console.log(QQperson)
    var sourcePER=QQperson.hits.hits;

    $('#historyNews').bootstrapTable('load', sourcePER);
    $('#historyNews').bootstrapTable({
        data:sourcePER,
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
                        '           </a>'+
                        '           <div class="center_2" style="margin-top: 10px;"><b style="color:#ff5722;font-weight: 700;">摘要内容：</b>'+row._source.text+ '</div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('.historyNews .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物qq号码（回车搜索）');
};
var time=Date.parse(new Date());
var QQ_news_url='/qq_xnr_operate/search_by_xnr_number/?xnr_number='+qqNumber+'&date='+Number(time)/1000;
public_ajax.call_request('get',QQ_news_url,personEarly);
//展示QQ群
// var QQgroup_url='/qq_xnr_operate/show_all_groups/';
// public_ajax.call_request('get',QQgroup_url,QQgroup);
// function QQgroup(data) {
//     console.log(data)
// }
// public_ajax.call_request('get','/qq_xnr_manage/get_qr_code/',loginQQ);
// function loginQQ(data) {
//     console.log(data)
//     $('#rr').attr('src',data)
//     $('#myModal-undone').modal('show');
// }

//选择时间搜索
$('#container .post_post .post-2 .titTime .timeSure').on('click',function () {
    var start=$('.start').val();
    var end=$('.end').val();
    if (start==''||end==''){
        $('#timeChecking').modal('show');
    }else {
        var search_news_url='/qq_xnr_operate/search_by_period/?xnr_number='+qqNumber+'&startdate='+start+'&enddate='+end;
        public_ajax.call_request('get',search_news_url,personEarly);
    }
});


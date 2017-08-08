function personEarly(personEarly_QQ) {
    let QQperson=eval(personEarly_QQ);
    console.log(QQperson)
    let sourcePER=QQperson.hits.hits;

    $('#historyNews').bootstrapTable('load', sourcePER);
    $('#historyNews').bootstrapTable({
        data:sourcePER,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 10,//单页记录数
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
                    if (row._source.speaker_nickname==''||row._source.speaker_nickname=='null'||row._source.speaker_nickname=='unknown'){
                        name=row._source.speaker_qq_number;
                    }else {
                        name=row._source.speaker_nickname;
                    };
                    var str=
                        '<div class="everySpeak" style="margin:0;">'+
                        '   <div class="speak_center">'+
                        '       <div class="center_rel">'+
                        '           <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                        '           <a class="center_1" href="###" style="color:#03a9f4;font-weight: 700;">'+
                        '           <b class="name">'+name+'</b> <span>（</span><b class="QQnum">'+row._source.speaker_qq_number+'</b><span>）</span></a>：'+
                        '           <span class="center_2">'+row._source.text+ '</span>'+
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
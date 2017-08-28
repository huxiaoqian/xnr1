function personEarly(personEarly_QQ) {
    var QQperson=eval(personEarly_QQ);
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
function QQgroup(data) {
    console.log(data)
    var str1='',str2='',b=0;
    for(var a in data){
        var n=data[a];
        if (n==''){n=a};
        if (b<=5){
            str1+=
                '<label class="demo-label" title="">'+
                '   <input class="demo-radio" type="checkbox" name="group" value="">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+
                '</label>';
        }else {
            if (b==6){
                str1+= '<a class="more" href="###" data-toggle="modal" data-target="#moreThing"' +
                    'style="color:#b0bdd0;font-size: 10px;border: 1px solid silver;float:right;' +
                    'padding: 2px 6px;margin:10px 0;border-radius: 7px;">更多</a>'
            };
            str2+=
                '<label class="demo-label" title="">'+
                '   <input class="demo-radio" type="checkbox" name="group" value="">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+
                '</label>';

        }
        b++;
    }
    $('#user_recommend .user_example_list').html(str1);
    if (str2){
        $('#moreThing .moreCon ul').html(str2);
    }
}
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
        $('#pormpt p').text('请检查时间，不能为空。');
        $('#pormpt').modal('show');
    }else {
        var search_news_url='/qq_xnr_operate/search_by_period/?xnr_number='+qqNumber+'&startdate='+start+'&enddate='+end;
        public_ajax.call_request('get',search_news_url,personEarly);
    }
});
//发送消息
$('#sure_post').on('click',function () {
    var value=$('#post-2-content').val();
    var group=[];
    $(".user_example_list input:checkbox:checked").each(function(index,item) {
        group.push($(this).val());
    });
    if (value==''||group.length==0){
        $('#pormpt p').text('请检查消息内容，不能为空。');
        $('#pormpt').modal('show');
    }else {
        var post_news_url='/qq_xnr_operate/send_qq_group_message/?text='+value+'&group='+start;
        public_ajax.call_request('get',post_news_url,postYES);
    }
})
//操作返回结果
function postYES(data) {
    var f='';
    if (data){f='操作成功'}else {f='操作失败'};
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}


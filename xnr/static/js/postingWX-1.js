
var time=Date.parse(new Date());

//展示WX群
// ========监听的群组===========
var WXgroup_url='/wx_xnr_operate/loadgroups/?wxbot_id='+wxbot_id;
public_ajax.call_request('get',WXgroup_url,WXgroup);
function WXgroup(data) {
    var str = '',poi=0;
    for (var d in data){
        var ched='';
        if (poi==0){
            ched='checked';
            var WX_news_url='/wx_xnr_operate/searchbygrouppuid/?wxbot_id='+wxbot_id+'&group_puid='+d+'&period=7';
            public_ajax.call_request('get',WX_news_url,personEarly);
        }
        str +=
            '<label class="demo-label" onclick="diff_group_news(this)">'+
            '    <input class="demo-radio" type="radio" name="demo-radio" value="'+d+'" title="'+data[d]+'" '+ched+'>'+
            '    <span class="demo-checkbox demo-radioInput"></span> '+data[d]+
            '</label>';
        poi++;
    }
    // ============此账号所在的群============
    $('.QQgroup .groupName').html(str);

    var str1='',str2='',b=0;
    for(var a in data){
        var n=data[a];
        if (n==''){n=a};
        if (b<=3){
            str1+=
                '<label class="demo-label" title="'+n+'">'+
                '   <input class="demo-radio" type="checkbox" name="group" value="'+a+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+n+
                '</label>';
        }else {
            if (b==4){
                str1+= '<a class="more" href="###" data-toggle="modal" data-target="#moreThing"' +
                    'style="color:#b0bdd0;font-size: 10px;border: 1px solid silver;float:right;' +
                    'padding: 2px 6px;margin:10px 0;border-radius: 7px;">更多</a>'
            };
            str2+=
                '<label class="demo-label" title="'+n+'">'+
                '   <input class="demo-radio" type="checkbox" name="group" value="'+a+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+n+
                '</label>';
        }
        b++;
    }
    // ======消息推送微信群名称=======
    $('#user_recommend .user_example_list').html(str1);
    if (str2){
        $('#moreThing .moreCon ul').html(str2);
    }
}

// =======群消息历史==========
function personEarly(personEarly_QQ) {
    var QQperson=eval(personEarly_QQ);
    // console.log(QQperson)
    // var sourcePER=QQperson.hits.hits;
    var sourcePER=QQperson;
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
                    if (row._source.group_name==''||row._source.group_name=='null'||row._source.group_name=='unknown'){
                        name=row._source.group_id;
                    }else {
                        name=row._source.group_name;
                    };
                    var str=
                        '<div class="everySpeak">'+
                        '   <div class="speak_center">'+
                        '       <div class="center_rel">'+
                        '           <img src="/static/images/post-6.png" class="center_icon">'+
                        '           <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                        '               <b class="name">'+name+
                        '               <b class="time" style="display: inline-block;margin-left: 30px;""><i class="icon icon-time"></i>&nbsp;'+getLocalTime(row._source.timestamp)+'</b>  '+
                        '               <b class="speaker" style="display: inline-block;margin-left: 30px;""><i class="icon icon-bullhorn"></i>&nbsp;发言人：'+row._source.speaker_name+'</b>  '+
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
    $('.historyNews .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物微信号码（回车搜索）');
};

//========选择群========
var _group_puid;
function diff_group_news(_this) {
    var group_puid=$(_this).find('input').val();
    _group_puid = group_puid;
    var chooseGroup_url='/wx_xnr_operate/searchbygrouppuid/?wxbot_id='+wxbot_id+'&group_puid='+group_puid+'&period=7';
    public_ajax.call_request('get',chooseGroup_url,personEarly);
}

//选择时间搜索
// $('#container .post_post .post-2 .titTime .timeSure').on('click',function () {
//     var start=$('.start').val();
//     var end=$('.end').val();
//     var group_puid=$('.groupName input:radio[name="demo-radio"]:checked').val();
//     if (start==''||end==''){
//         $('#pormpt p').text('请检查时间，不能为空。');
//         $('#pormpt').modal('show');
//     }else {
//         var search_news_url = '/wx_xnr_operate/searchbygrouppuid/?wxbot_id='+wxbot_id+'&group_puid='+group_puid+'&startdate='+start+'&enddate='+end;
//         console.log(search_news_url)
//         public_ajax.call_request('get',search_news_url,personEarly);
//     }
// });
//================发送消息更改11-16 7天 30天那种===============
// 时间选项
$('.choosetime .demo-label input').on('click',function () {
    var _val=$(this).val();
    if (_val=='mize'){
        $('#start_1').show();
        $('#end_1').show();
        $('.sureTime').show();
    }else {
        $('#start_1').hide();
        $('#end_1').hide();
        $('.sureTime').hide();
        var urlLast='&period='+_val;
        var group_puid=$('.groupName input:radio[name="demo-radio"]:checked').val();
        var search_news_url = '/wx_xnr_operate/searchbygrouppuid/?wxbot_id='+wxbot_id+'&group_puid='+group_puid+urlLast;
        console.log(search_news_url)
        public_ajax.call_request('get',search_news_url,personEarly);
    }
});
// 确定时间搜索
$('.sureTime').on('click',function () {
    var s=$('#start_1').val();
    var d=$('#end_1').val();
    var group_puid=$('.groupName input:radio[name="demo-radio"]:checked').val();
    if (s==''||d==''){
        $('#pormpt p').text('请检查时间，不能为空。');
        $('#pormpt').modal('show');
    }else {
        var search_news_url = '/wx_xnr_operate/searchbygrouppuid/?wxbot_id='+wxbot_id+'&group_puid='+group_puid+'&startdate='+s+'&enddate='+d;
        console.log(search_news_url)
        public_ajax.call_request('get',search_news_url,personEarly);
    }
});





//================发送消息===============
$('#sure_post').on('click',function () {
    var value=$('#post-2-content').val();
    var group=[];
    $(".user_example_list input:checkbox:checked").each(function(index,item) {
        group.push($(this).val());
    });
    //模态框中的群组
    $("#moreThing input:checkbox:checked").each(function(index,item) {
        group.push($(this).val());
    });
    if (value==''){
        $('#pormpt p').text('请检查消息内容，不能为空。');
        $('#pormpt').modal('show');
    }else if(group.length==0){
        $('#pormpt p').text('请选择要发送的群组。');
        $('#pormpt').modal('show');
    }else {
        var post_news_url='/wx_xnr_operate/sendmsg/?wxbot_id='+wxbot_id+'&group_list='+group.join(',')+'&msg='+value;
        public_ajax.call_request('get',post_news_url,postYES);
    }
})
//操作返回结果
function postYES(data) {
    var f='';
    if (data){f='操作成功'}else {f='操作失败'};
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
    $('#pormpt').on('hidden.bs.modal', function (e) {
        // 模态框关闭之后清空输入框
        $('#post-2-content').val('');
        // 重新请求数据，以显示刚发送的消息
        var _group_puid = $('.groupName input:checked').val()
        var _chooseGroup_url='/wx_xnr_operate/searchbygrouppuid/?wxbot_id='+wxbot_id+'&group_puid='+_group_puid+'&period=7';
        public_ajax.call_request('get',_chooseGroup_url,personEarly);
    })
}


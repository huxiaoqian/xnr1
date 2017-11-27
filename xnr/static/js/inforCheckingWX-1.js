/*
* @Author: Marte
* @Date:   2017-10-26 11:22:02
* @Last Modified by:   Marte
* @Last Modified time: 2017-11-17 10:35:36
*/

console.log('===微信预警监控页面js===')

//===============敏感消息======已完成10-31=========
// var senNews_url='/qq_xnr_monitor/search_by_xnr_number/?xnr_number='+userQQnum+'&date='+(Number(Date.parse(new Date()))/1000);
var senNews_url='/wx_xnr_monitor/search/?wxbot_id='+wxbot_id+'&period=7';//默认请求7天的数据
public_ajax.call_request('get',senNews_url,senNews);
function senNews(data) {
    console.log(data)
    // var news=data.hits.hits;
    var news=data;
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
                    var name,txt;
                    if (row._source.group_name==''||row._source.group_name=='null'||row._source.group_name=='unknown'){
                        name=row._source.group_id;
                    }else {
                        name=row._source.group_name;
                    };
                    if (row._source.text==''||row._source.text=='null'||row._source.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        var keyword=row._source.sensitive_words_string.split('&');
                        var s=row._source.text;
                        for (var f=0;f<keyword.length;f++){
                            s=s.toString().replace(new RegExp(keyword[f],'g'),'<b style="color:#ef3e3e;">'+keyword[f]+'</b>');
                        }
                        txt=s;
                    };
                    var str=
                        '<div class="everySpeak">'+
                        '   <div class="speak_center">'+
                        '       <div class="center_rel" style="text-align: left;">'+
                        '           <img src="/static/images/post-6.png" class="center_icon">'+
                        '           <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                        // '               <b class="name">'+name+'</b> <span>（</span><b class="QQnum">'+row._source.group_id+'</b><span>）</span>' +
                        '               <b class="name">'+name+'</b>' +
                        '               <b class="time" style="display: inline-block;margin-left: 30px;""><i class="icon icon-time"></i>&nbsp;'+getLocalTime(row._source.timestamp)+'</b>  '+
                        '               <span class="joinWord" onclick="joinWord(this)" tp="content" speaker_id='+row._source.speaker_id+' sensitive_value='+row._source.sensitive_value+' sensitive_words_string='+row._source.sensitive_words_string+' text='+row._source.text+' speaker_nickname='+row._source.speaker_nickname+' timestamp='+row._source.timestamp+' group_puid='+row._source.group_puid+'>上报</span>'+
                        '           </a>'+
                        '           <div class="center_2" style="margin-top: 10px;"><b style="color:#ff5722;font-weight: 700;">摘要内容：</b><span>'+txt+'</span></div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('.content-1-word .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物微信ID（回车搜索）');
}

//===============敏感用户===============
// var senUserurl='/qq_xnr_monitor/show_sensitive_users/?xnr_number='+userQQnum;
var senUserurl='/wx_xnr_monitor/show_sensitive_users/?wxbot_id='+wxbot_id+'&period=7';
public_ajax.call_request('get',senUserurl,senUser);
function senUser(data) {
    console.log(data)
    $('#hot-2').bootstrapTable('load', data);
    $('#hot-2').bootstrapTable({
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
            //     title: "QQ号码",//标题
            //     field: "qq_number",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            // },
            {
                title: "昵称",//标题
                field: "nickname",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row.nickname==''||row.nickname=='null'||row.nickname=='unknown'){
                        name='无';
                    }else {
                        name=row.nickname;
                    };
                    return name;
                }
            },
            {
                title: "敏感发言数量",//标题
                field: "count",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "发言时间",//标题
                field: "last_speak_ts",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var time;
                    if (row.last_speak_ts==''||row.last_speak_ts=='null'||row.last_speak_ts=='unknown'){
                        time='未知';
                    }else {
                        time=getLocalTime(row.last_speak_ts);
                    };
                    return time;
                }
            },
            {
                title: "敏感言论群",//标题
                field: "groups_list",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var str='';
                    if (row.groups_list==''||row.groups_list=='null'||row.groups_list=='unknown'||isEmptyObject(row.groups_list)==true){
                        str='无数据';
                    }else {
                        row.groups_list = row.groups_list.split(',')
                        // for(var k in row.groups_list){
                        //     str +=
                        //         '<div class="center_rel">'+
                        //         '   <img src="/static/images/post-6.png" class="center_icon" style="width: 20px;height: 20px;">'+
                        //         '   <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                        //         '       <b class="name">'+row.groups_list[k]+'</b> <span>（</span><b class="QQnum">'+k+'</b><span>）</span>' +
                        //         '   </a>'+
                        //         '</div>';
                        // }
                        for(var i=0;i< row.groups_list.length;i++){
                            str +=
                                // '<div class="center_rel">'+
                                // '   <img src="/static/images/post-6.png" class="center_icon" style="width: 20px;height: 20px;">'+
                                // '   <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                                // '       <b class="name">'+row.groups_list[i]+'</b> <span>（</span><b class="QQnum">'+i+'</b><span>）</span>' +
                                // '   </a>'+
                                // '</div>';
                                '<div class="center_rel">'+
                                '   <img src="/static/images/post-6.png" class="center_icon" style="width: 20px;height: 20px;">'+
                                '   <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                                '       <b class="name">'+row.groups_list[i]+'</b> ' +
                                '   </a>'+
                                '</div>';
                        }
                    };
                    return str;
                }
            },
        ],
        onClickRow: function (row, $element) {
            $('#QQgroup_weibo .QW-1').text(row.qq_number);
            var txt=row.text,str='';
            if (txt.length!=0||txt){
                $.each(txt,function (index,item) {
                    str+=
                        '<div class="center_rel" style="margin-bottom: 10px;">'+
                        '   <img src="/static/images/post-6.png" class="center_icon" style="width: 20px;height: 20px;">'+
                        '   <a class="center_1 qq-2" href="###" style="color:blanchedalmond;font-weight: 700;">'+item[0]+'</a>'+
                        '   <b class="qq-1" style="display: none;">'+item[1]+'</b>'+
                        '   <span class="joinWord" onclick="joinWord(this)" tp="user">上报</span>'+
                        '</div>';
                })
            }else {
                str='<p style="text-align: center;font-size: 18px;color: #fff;font-weight: 900;">暂无任何敏感内容</p>';
            }

            $('#QQgroup_weibo .QW-2').html(str);
            $('#QQgroup_weibo').modal('show');
        }
    });
    $('.hot-2 .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物微信ID（回车搜索）');
}

//===============选择时间搜索===============
// $('#container .titTime .timeSure').on('click',function () {
//     var start=$('.start').val();
//     var end=$('.end').val();
//     if (start==''||end==''){
//         $('#pormpt p').text('请检查时间，不能为空。');
//         $('#pormpt').modal('show');
//     }else {
//         // ===============敏感消息完成=================
//         var search_news_url='/wx_xnr_monitor/search/?wxbot_id='+wxbot_id+'&startdate='+start+'&enddate='+end;
//         console.log(search_news_url)
//         public_ajax.call_request('get',search_news_url,senNews);

//         // ===============敏感用户完成=================
//         // var senUserurl='/qq_xnr_monitor/show_sensitive_users/?xnr_number='+userQQnum+'&startdate='+start+'&enddate='+end;
//         var senUserurl='/wx_xnr_monitor/show_sensitive_users/?wxbot_id='+wxbot_id+'&startdate='+start+'&enddate='+end;
//         public_ajax.call_request('get',senUserurl,senUser);
//     }
// });
//===============时间搜索更改11-16 ===============
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
        var startTime='',midurl_1='search',midurl_2='show_sensitive_users',urlLast='';
        urlLast='&period='+_val;
        // 敏感消息
        var senNews_url='/wx_xnr_monitor/'+midurl_1+'/?wxbot_id='+wxbot_id+urlLast;
        console.log(senNews_url)
        public_ajax.call_request('get',senNews_url,senNews);
        // 敏感用户
        var senUserurl='/wx_xnr_monitor/'+midurl_2+'/?wxbot_id='+wxbot_id+urlLast;
        console.log(senUserurl)
        public_ajax.call_request('get',senUserurl,senUser);
    }
});
// 确定时间搜索
$('.sureTime').on('click',function () {
    var s=$('#start_1').val();
    var d=$('#end_1').val();
    if (s==''||d==''){
        $('#pormpt p').text('请检查时间，不能为空。');
        $('#pormpt').modal('show');
    }else {
        // ===============敏感消息完成=================
        var search_news_url='/wx_xnr_monitor/search/?wxbot_id='+wxbot_id+'&startdate='+s+'&enddate='+d;
        console.log(search_news_url)
        public_ajax.call_request('get',search_news_url,senNews);

        // ===============敏感用户完成=================
        var senUserurl='/wx_xnr_monitor/show_sensitive_users/?wxbot_id='+wxbot_id+'&startdate='+s+'&enddate='+d;
        public_ajax.call_request('get',senUserurl,senUser);
    }
});




//===============上报===============
function joinWord(_this) {
    var qq_1=($(_this).parents('.center_1').find('.QQnum').text())||($(_this).prev().text());//群id
    var qq_2=($(_this).parents('.center_1').next('.center_2').find('span').text())||($(_this).parents('.center_rel').find('qq-2').text());//内容
    var speaker_id = $(_this).attr('speaker_id');
    var sensitive_value = $(_this).attr('sensitive_value');
    var sensitive_words_string = $(_this).attr('sensitive_words_string');
    var text = $(_this).attr('text');
    var speaker_nickname = $(_this).attr('speaker_nickname');
    var timestamp = $(_this).attr('timestamp');
    var group_puid = $(_this).attr('group_puid');

    var reportContent = {'speaker_id':speaker_id, "sensitive_value": sensitive_value,"sensitive_words_string": sensitive_words_string, "text": text,"speaker_nickname": speaker_nickname, "timestamp": timestamp,"group_puid":group_puid };
    reportContent = JSON.stringify(reportContent);

    var reportType=$(_this).attr('tp');//--- content
    // var upload_mange_url='/qq_xnr_monitor/report_warming_content/?report_type='+reportType+'&xnr_user_no='+ID_Num+
    //     '&qq_number='+qq_1+'&report_content='+qq_2;
    var upload_mange_url='/wx_xnr_monitor/report_warning_content/?wxbot_id='+wxbot_id+'&report_type='+reportType+
        '&speaker_id='+speaker_id+'&report_content='+reportContent;
    console.log(upload_mange_url)
    // var uploadData={'report_type':reportType, "xnr_user_no": ID_Num,"qq_number": qq_1, "report_content": qq_2};
    // var uploadData={'report_type':reportType, "wxbot_id": wxbot_id,"speaker_id": qq_1, "report_content": qq_2};
    // uploadData=JSON.stringify(uploadData);
    public_ajax.call_request('get',upload_mange_url,postYES);
    // $.ajax({
    //     type:'get',
    //     // url:'/qq_xnr_monitor/report_warming_content/',
    //     url:'/wx_xnr_monitor/report_warning_content/',
    //     async:true,
    //     dataType:"json",
    //     data:uploadData,
    //     success:postYES,
    //     error:function (xhr,textStatus,errorThrown) {
    //         //请求失败执行的函数
    //         console.log("请求失败",textStatus,errorThrown);
    //         var errorHtml='请求失败！！可能是因为服务器速度太慢或者网络原因导致。';
    //         if (ISclear=='clear'){
    //             errorHtml='登录过期，请清除缓存，重新登录。'
    //             ISclear='againSet';
    //         }
    //         $('#errorInfor p').text(errorHtml);
    //         $('#errorInfor').modal('show');
    //     },
    // });
}

//===============确定加入===============
//===============操作返回结果===============
function postYES(data) {
    console.log(data)
    var f='';
    if (data){f='操作成功'}else {f='操作失败'};
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
//敏感消息
var senNews_url='/qq_xnr_monitor/search_by_xnr_number/?xnr_number='+userQQnum+'&date='+(Number(Date.parse(new Date()))/1000);
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
                    var name,txt;
                    if (row._source.qq_group_nickname==''||row._source.qq_group_nickname=='null'||row._source.qq_group_nickname=='unknown'){
                        name=row._source.qq_group_number;
                    }else {
                        name=row._source.qq_group_nickname;
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
                        '               <b class="name">'+name+'</b> <span>（</span><b class="QQnum">'+row._source.qq_group_number+'</b><span>）</span>' +
                        '               <b class="time" style="display: inline-block;margin-left: 30px;""><i class="icon icon-time"></i>&nbsp;'+getLocalTime(row._source.timestamp)+'</b>  '+
                        '               <span class="joinWord" onclick="joinWord(this)" tp="content">上报</span>'+
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
    $('.content-1-word .search .form-control').attr('placeholder','请输入关键词或人物昵称或人物qq号码（回车搜索）');
}
//敏感用户
var senUserurl='/qq_xnr_monitor/show_sensitive_users/?xnr_number='+userQQnum;
public_ajax.call_request('get',senUserurl,senUser);
function senUser(data) {
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
            {
                title: "QQ号码",//标题
                field: "qq_number",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "昵称",//标题
                field: "qq_nick",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row.qq_nick==''||row.qq_nick=='null'||row.qq_nick=='unknown'){
                        name='无';
                    }else {
                        name=row.qq_nick;
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
                field: "qq_groups",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var str='';
                    if (row.qq_groups==''||row.qq_groups=='null'||row.qq_groups=='unknown'||isEmptyObject(row.qq_groups)==true){
                        str='无数据';
                    }else {
                        for(var k in row.qq_groups){
                            str +=
                                '<div class="center_rel">'+
                                '   <img src="/static/images/post-6.png" class="center_icon" style="width: 20px;height: 20px;">'+
                                '   <a class="center_1" href="###" style="color:blanchedalmond;font-weight: 700;">'+
                                '       <b class="name">'+row.qq_groups[k]+'</b> <span>（</span><b class="QQnum">'+k+'</b><span>）</span>' +
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
                    var keyword=item[2].split('&');
                    var s=item[0];
                    for (var f=0;f<keyword.length;f++){
                        s=s.toString().replace(new RegExp(keyword[f],'g'),'<b style="color:#ef3e3e;">'+keyword[f]+'</b>');
                    }

                    str+=
                        '<div class="center_rel" style="margin-bottom: 10px;">'+
                        '   <img src="/static/images/post-6.png" class="center_icon" style="width: 20px;height: 20px;">'+
                        '   <a class="center_1 qq-2" href="###" style="font-weight: 700;color: white;">'+s+'</a>'+
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
        var search_news_url='/qq_xnr_monitor/search_by_period/?xnr_number='+userQQnum+'&startdate='+start+'&enddate='+end;
        public_ajax.call_request('get',search_news_url,senNews);
        var senUserurl='/qq_xnr_monitor/show_sensitive_users/?xnr_number='+userQQnum+'&startdate='+start+'&enddate='+end;
        public_ajax.call_request('get',senUserurl,senUser);
    }
});
//上报
function joinWord(_this) {
    var qq_1=($(_this).parents('.center_1').find('.QQnum').text())||($(_this).prev().text());
    var qq_2=($(_this).parents('.center_1').next('.center_2').find('span').text())||($(_this).parents('.center_rel').find('qq-2').text());
    var reportType=$(_this).attr('tp');
    var upload_mange_url='/qq_xnr_monitor/report_warming_content/?report_type='+reportType+'&xnr_user_no='+ID_Num+
        '&qq_number='+qq_1+'&report_content='+qq_2;
    var uploadData={'report_type':reportType, "xnr_user_no": ID_Num,"qq_number": qq_1, "report_content": qq_2};
    uploadData=JSON.stringify(uploadData);
    $.ajax({
        type:'get',
        url:'/qq_xnr_monitor/report_warming_content/',
        async:true,
        dataType:"json",
        data:uploadData,
        success:postYES,
        error:function (xhr,textStatus,errorThrown) {
            //请求失败执行的函数
            console.log("请求失败",textStatus,errorThrown);
            var errorHtml='请求失败！！可能是因为服务器速度太慢或者网络原因导致。';
            if (ISclear=='clear'){
                errorHtml='登录过期，请清除缓存，重新登录。'
                ISclear='againSet';
            }
            $('#errorInfor p').text(errorHtml);
            $('#errorInfor').modal('show');
        },
    });
}
//确定加入
//操作返回结果
function postYES(data) {
    var f='';
    if (data){f='操作成功'}else {f='操作失败'};
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
var ID_Num='FXNR0001';
var time2=Date.parse(new Date())/1000;
var weiboUrl='/facebook_xnr_warning/show_personnal_warning/?xnr_user_no='+ID_Num+'&start_time='+todayTimetamp()+'&end_time='+time2;
public_ajax.call_request('get',weiboUrl,weibo);
//时间选择
$('.choosetime .demo-label input').on('click',function () {
    var _val = $(this).val();
    if (_val == 'mize') {
        $(this).parents('.choosetime').find('#start').show();
        $(this).parents('.choosetime').find('#end').show();
        $(this).parents('.choosetime').find('#sure').css({display: 'inline-block'});
    } else {
        $(this).parents('.choosetime').find('#start').hide();
        $(this).parents('.choosetime').find('#end').hide();
        $(this).parents('.choosetime').find('#sure').hide();
        var weiboUrl='/facebook_xnr_warning/show_personnal_warning/?xnr_user_no='+ID_Num+'&start_time='+getDaysBefore(_val)+'&end_time='+time2;
        public_ajax.call_request('get',weiboUrl,weibo);
    }
});
$('#sure').on('click',function () {
    var s=$(this).parents('.choosetime').find('#start').val();
    var d=$(this).parents('.choosetime').find('#end').val();
    if (s==''||d==''){
        $('#pormpt p').text('时间不能为空。');
        $('#pormpt').modal('show');
    }else {
        var weiboUrl='/facebook_xnr_warning/show_personnal_warning/?xnr_user_no='+ID_Num+'&start_time='+
            (Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        public_ajax.call_request('get',weiboUrl,weibo);
    }
});

function weibo(data) {
    $('#weiboContent p').show();
    $('#weiboContent').bootstrapTable('load', data);
    $('#weiboContent').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 1,//单页记录数
        pageList: [3,7,11],//分页步进值
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
                field: "content",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var artical=row.content,str='';
                    if (artical.length==0||!artical){
                        str='暂无微博内容';
                    }else {
                        $.each(artical,function (index,item) {
                            var text,time;
                            if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text){
                                text='暂无内容';
                            }else {
                                if (item.sensitive_words_string||!isEmptyObject(item.sensitive_words_string)){
                                    var s=item.text;
                                    var keywords=item.sensitive_words_string.split('&');
                                    for (var f=0;f<keywords.length;f++){
                                        s=s.toString().replace(new RegExp(keywords[f],'g'),'<b style="color:#ef3e3e;">'+keywords[f]+'</b>');
                                    }
                                    text=s;
                                }else {
                                    text=item.text;
                                };
                            };
                            if (item.timestamp==''||item.timestamp=='null'||item.timestamp=='unknown'||!item.timestamp){
                                time='未知';
                            }else {
                                time=getLocalTime(item.timestamp);
                            };
                            var sye_1='',sye_2='';
                            if (Number(item.sensitive) < 50){
                                sye_1='border-color: transparent transparent #131313';
                                sye_2='color: yellow';
                            }
                            str+=
                                '<div class="center_rel">'+
                                '   <div class="icons" style="'+sye_1+'">'+
                                '       <i class="icon icon-warning-sign weiboFlag" style="'+sye_2+'"></i>'+
                                '   </div>'+
                                '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                                '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                                '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                '   <a class="sensitive" style="display: none;">'+item.sensitive+'</a>'+
                                '   <a class="sensitiveWords" style="display: none;">'+item.sensitive_words_string+'</a>'+
                                '   <span class="center_2">'+text+'</span>'+
                                '   <div class="center_3">'+
                                '       <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                                '       <span class="cen3-2" onclick="retComLike(this)" type="get_weibohistory_retweet"><i class="icon icon-share"></i>&nbsp;&nbsp;转推（<b class="forwarding">'+item.share+'</b>）</span>'+
                                '       <span class="cen3-3" onclick="retComLike(this)" type="get_weibohistory_comment"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                                '       <span class="cen3-4" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;喜欢(<b class="like">'+item.favorite+'</b>)</span>'+
                                '       <span class="cen3-4" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-envelope-alt"></i>&nbsp;&nbsp;私信</span>'+
                                '    </div>'+
                                '    <div class="commentDown" style="width: 100%;display: none;">'+
                                '        <input type="text" class="comtnt" placeholder="评论内容"/>'+
                                '        <span class="sureCom" onclick="comMent(this)">评论</span>'+
                                '    </div>'+
                                '</div>'
                        });
                    }
                    var nameuid;
                    if (row.user_name==''||row.user_name=='null'||row.user_name=='unknown'||!row.user_name){
                        nameuid=row.uid;
                    }else {
                        nameuid=row.user_name;
                    };
                    var rel_str=
                        '<div class="everyUser" style="margin: 0 auto;width: 950px;text-align:left;">'+
                        '        <div class="user_center">'+
                        '            <div style="margin: 10px 0;">'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio" type="checkbox" name="demo-checkbox">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        '                </label>'+
                        '                <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                        '                <a class="center_1" href="###">'+nameuid+'</a>'+
                        '                <a class="mainUID" style="display: none;">'+row.uid+'</a>'+
                        '                <a onclick="oneUP(this)" class="report" style="margin-left: 50px;cursor: pointer;"><i class="icon icon-upload-alt"></i>  上报</a>'+
                        '            </div>'+
                        '           <div>'+str+'</div>'+
                        '        </div>'+
                        '    </div>';
                    return rel_str;

                }
            },
        ],
    });
    $('#weiboContent p').slideUp(300);
};

// 转发===评论===点赞
function retComLike(_this) {
    var mid=$(_this).parents('.center_rel').find('.mid').text();
    var middle=$(_this).attr('type');
    var opreat_url;
    if (middle=='get_weibohistory_like'){
        var uid=$(_this).parents('.center_rel').find('.uid').text();
        var timestamp=$(_this).parents('.center_rel').find('.timestamp').text();
        var text=$(_this).parents('.center_rel').find('.center_2').text();
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&uid='+uid+'&text='+text+
            '&timestamp='+timestamp+'&nick_name='+REL_name;
        public_ajax.call_request('get',opreat_url,postYES);
    }else if (middle=='get_weibohistory_comment'){
        $(_this).parents('.center_rel').find('.commentDown').show();
    }else {
        var txt=$(_this).parents('.center_rel').find('.center_2').text();
        if (txt=='暂无内容'){txt=''};
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&text='+txt;
        public_ajax.call_request('get',opreat_url,postYES);
    }
}
function comMent(_this){
    var txt = $(_this).prev().val();
    var mid = $(_this).parents('.center_rel').find('.mid').text();
    if (txt!=''){
        var post_url='/weibo_xnr_report_manage/get_weibohistory_comment/?text='+txt+'&xnr_user_no='+ID_Num+'&mid='+mid;
        public_ajax.call_request('get',post_url,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}
//一键上报
function oneUP(_this) {
    //[mid,text,timestamp,retweeted,like,comment]
    var len=$(_this).parents('.everyUser').find('.center_rel');
    if (len){
        var mainUID=$(_this).parents('.everyUser').find('.mainUID').text();
        var dataStr='';
        for (var i=0;i<len.length;i++){
            var alldata=[];
            var mid = $(len[i]).find('.mid').text();alldata.push(mid);
            var txt=$(len[i]).find('.center_2').text().toString().replace(/\#/g,'%23').replace(/\&/g,'%26');alldata.push(txt);
            var timestamp = $(len[i]).find('.timestamp').text();alldata.push(timestamp);
            var forwarding = $(len[i]).find('.forwarding').text();alldata.push(forwarding);alldata.push(0);
            var comment = $(len[i]).find('.comment').text();alldata.push(comment);
            var sensitive = $(len[i]).find('.sensitive').text();alldata.push(sensitive);
            var sensitiveWords = $(len[i]).find('.sensitiveWords').text().toString().replace(/\&/g,'%26');alldata.push(sensitiveWords);
            dataStr+=alldata.join(',').toString();
            if (i!=len.length-1){dataStr+='*'}
        }
        var once_url='/weibo_xnr_warming/report_warming_content/?report_type=人物&xnr_user_no='+ID_Num+'&uid='+mainUID+
            '&weibo_info='+dataStr;
        public_ajax.call_request('get',once_url,postYES);
    }else {
        $('#pormpt p').text('微博内容为空，无法上报。');
        $('#pormpt').modal('show');
    }
}
//操作返回结果
function postYES(data) {
    var f='';
    if (data[0]||data){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}

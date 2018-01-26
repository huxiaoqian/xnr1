var operateType='info_warning';
var time2=Date.parse(new Date())/1000;//1480176000
$('#typelist .demo-radio').on('click',function () {
    var _val=$(this).val();
    var time=$('.choosetime input:radio[name="time"]:checked').val();
    var time1=getDaysBefore(time);
    if (time=='mize'){
        var s=$('.choosetime').find('#start').val();
        var d=$('.choosetime').find('#end').val();
        if (s==''||d==''){
            $('#pormpt p').text('时间不能为空。');
            $('#pormpt').modal('show');
            return false;
        }else {
            time1=(Date.parse(new Date(s))/1000);
            time2=(Date.parse(new Date(d))/1000);
        }
    }
    var weiboUrl='/twitter_xnr_warning/show_speech_warning/?xnr_user_no='+ID_Num+'&show_type='+_val+
        '&start_time='+time1+'&end_time='+time2;
    public_ajax.call_request('get',weiboUrl,weibo);
});
//时间选择
$('.choosetime .demo-label input').on('click',function () {
    var _val = $(this).val();
    var valCH=$('#typelist input:radio[name="focus"]:checked').val();
    if (_val == 'mize') {
        $(this).parents('.choosetime').find('#start').show();
        $(this).parents('.choosetime').find('#end').show();
        $(this).parents('.choosetime').find('#sure').css({display: 'inline-block'});
    } else {
        $(this).parents('.choosetime').find('#start').hide();
        $(this).parents('.choosetime').find('#end').hide();
        $(this).parents('.choosetime').find('#sure').hide();
        var weiboUrl='/twitter_xnr_warning/show_speech_warning/?xnr_user_no='+ID_Num+'&show_type='+valCH+
            '&start_time='+getDaysBefore(_val)+'&end_time='+time2;
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
        var weiboUrl='/twitter_xnr_warning/show_speech_warning/?xnr_user_no='+ID_Num+'&start_time='+
            (Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        public_ajax.call_request('get',weiboUrl,weibo);
    }
});

var weiboUrl='/twitter_xnr_warning/show_speech_warning/?xnr_user_no='+ID_Num+'&show_type=0&start_time='+todayTimetamp()+'&end_time='+time2;
public_ajax.call_request('get',weiboUrl,weibo);
function weibo(data) {
    $('#weiboContent p').show();
    $('#weiboContent').bootstrapTable('load', data);
    $('#weiboContent').bootstrapTable({
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var item=row;
                    var name,text,text2,time,all='',img;
                    if (item.nick_name==''||item.nick_name=='null'||item.nick_name=='unknown'||!item.nick_name){
                        name=item.uid;
                    }else {
                        name=item.nick_name;
                    };
                    if (item.photo_url==''||item.photo_url=='null'||item.photo_url=='unknown'||!item.photo_url){
                        img='/static/images/unknown.png';
                    }else {
                        img=item.photo_url;
                    };
                    if (item.user_name==''||item.user_name=='null'||item.user_name=='unknown'||!item.user_name){
                        name=item.uid;
                    }else {
                        name=item.user_name;
                    };
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

                            var rrr=item.text;
                            if (rrr.length>=160){
                                rrr=rrr.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                rrr=item.text;
                                all='none';
                            }
                            for (var f of keywords){
                                rrr=rrr.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                            text2=rrr;
                        }else {
                            text=item.text;
                            if (text.length>=160){
                                text2=text.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                text2=text;
                                all='none';
                            }
                        };
                    };
                    if (item.timestamp==''||item.timestamp=='null'||item.timestamp=='unknown'||!item.timestamp){
                        time='未知';
                    }else {
                        time=getLocalTime(item.timestamp);
                    };
                    var rel_str=
                        '<div class="everySpeak " style="margin: 0 auto;width: 950px;text-align: left;">'+
                        '        <div class="speak_center everyUser">'+
                        '            <div class="center_rel">'+
                        // '                <label class="demo-label">'+
                        // '                    <input class="demo-radio" type="checkbox" name="demo-checkbox">'+
                        // '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        // '                </label>'+
                        '                <img src="'+img+'" alt="" class="center_icon">'+
                        '                <a class="center_1 centerNAME" href="###">'+name+'</a>'+
                        '                <a class="tid" style="display: none;">'+item.tid+'</a>'+
                        '                <a class="uid mainUID" style="display: none;">'+item.uid+'</a>'+
                        '                <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                        '                <a class="_id" style="display: none;">'+item._id+'</a>'+
                        '                <span class="time" style="font-weight: 900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                        '                <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                        '                <p class="allall1" style="display:none;">'+text+'</p>'+
                        '                <p class="allall2" style="display:none;">'+text2+'</p>'+
                        '                <span class="center_2">'+text2+
                        '                </span>'+
                        '                <div class="_translate" style="display: none;"><b style="color: #f98077;">译文：</b><span class="tsWord"></span></div>'+
                        '                <div class="center_3">'+
                        // '                    <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                        '                    <span class="cen3-2" onclick="retComLike(this)" type="retweet_operate"><i class="icon icon-share"></i>&nbsp;&nbsp;转推（<b class="forwarding">'+item.share+'</b>）</span>'+
                        '                    <span class="cen3-3" onclick="retComLike(this)" type="comment_operate"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;回复（<b class="comment">'+item.comment+'</b>）</span>'+
                        '                    <span class="cen3-4" onclick="retComLike(this)" type="like_operate"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;喜欢(<b class="like">'+item.favorite+'</b>)</span>'+
                        '                    <span class="cen3-4" onclick="emailThis(this)"><i class="icon icon-envelope"></i>&nbsp;&nbsp;私信</span>'+
                        '                    <span class="cen3-5" onclick="translateWord(this)"><i class="icon icon-exchange"></i>&nbsp;&nbsp;翻译</span>'+
                        '                    <span class="cen3-5" onclick="joinPolice(this,\'言论\')"><i class="icon icon-plus-sign"></i>&nbsp;&nbsp;加入预警库</span>'+
                        '                    <span class="cen3-9" onclick="robot(this)"><i class="icon icon-github-alt"></i>&nbsp;&nbsp;机器人回复</span>'+
                        '                    <span class="cen3-6" onclick="oneUP(this,\'言论\')"><i class="icon icon-upload-alt"></i>&nbsp;&nbsp;上报</span>'+
                        '                </div>'+
                        '               <div class="commentDown" style="width: 100%;display: none;">'+
                        '                   <input type="text" class="comtnt" placeholder="回复内容"/>'+
                        '                   <span class="sureCom" onclick="comMent(this)">回复</span>'+
                        '               </div>'+
                        '            </div>'+
                        '        </div>';
                    return rel_str;
                }
            },
        ],
    });
    $('#weiboContent p').slideUp(300);
};

// 转发===评论===点赞
function retComLike(_this) {
    var txt = $(_this).parent().prev().text().replace(/\&/g,'%26').replace(/\#/g,'%23');
    var uid=$(_this).parents('.center_rel').find('.uid').text();
    var tid=$(_this).parents('.center_rel').find('.tid').text();
    var middle=$(_this).attr('type');
    var opreat_url;
    if (middle=='retweet_operate'){
        opreat_url='/twitter_xnr_operate/retweet_operate/?tweet_type='+operateType+'&xnr_user_no='+ID_Num+
            '&text='+txt+'&tid='+tid+'&uid='+uid;
        public_ajax.call_request('get',opreat_url,postYES);
    }else if (middle=='comment_operate'){
        $(_this).parents('.center_rel').find('.commentDown').show();
    }else {
        opreat_url='/twitter_xnr_operate/like_operate/?xnr_user_no='+ID_Num+
            '&tid='+tid+'&uid='+uid;
        public_ajax.call_request('get',opreat_url,postYES);
    }
}
function comMent(_this){
    var txt = $(_this).prev().val().replace(/\&/g,'%26').replace(/\#/g,'%23');
    var uid = $(_this).parents('.center_rel').find('.uid').text();
    var tid = $(_this).parents('.center_rel').find('.tid').text();
    if (txt!=''){
        var post_url='/twitter_xnr_operate/comment_operate/?tweet_type='+operateType+'&xnr_user_no='+ID_Num+
            '&text='+txt+'&tid='+tid+'&uid='+uid;
        public_ajax.call_request('get',post_url,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}

//操作返回结果
function postYES(data) {
    var f='操作成功';
    if (!data){f='操作失败'}
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
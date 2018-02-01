var operateType='info_warning';
var time2=Date.parse(new Date())/1000;
var weiboUrl='/twitter_xnr_warning/show_personnal_warning/?xnr_user_no='+ID_Num+'&start_time='+todayTimetamp()+'&end_time='+time2;
public_ajax.call_request('get',weiboUrl,weibo);
//时间选择
$('.choosetime .demo-label input').on('click',function () {
    var _val = $(this).val();
    if (_val == 'mize') {
        $(this).parents('.choosetime').find('#start').show();
        $(this).parents('.choosetime').find('#end').show();
        $(this).parents('.choosetime').find('#sure').css({display: 'inline-block'});
    } else {
        $('#weiboContent p').show();
        $(this).parents('.choosetime').find('#start').hide();
        $(this).parents('.choosetime').find('#end').hide();
        $(this).parents('.choosetime').find('#sure').hide();
        var weiboUrl='/twitter_xnr_warning/show_personnal_warning/?xnr_user_no='+ID_Num+'&start_time='+getDaysBefore(_val)+'&end_time='+time2;
        public_ajax.call_request('get',weiboUrl,weibo);
    }
});
$('#sure').on('click',function () {
    $('#weiboContent p').show();
    var s=$(this).parents('.choosetime').find('#start').val();
    var d=$(this).parents('.choosetime').find('#end').val();
    if (s==''||d==''){
        $('#pormpt p').text('时间不能为空。');
        $('#pormpt').modal('show');
    }else {
        var weiboUrl='/twitter_xnr_warning/show_personnal_warning/?xnr_user_no='+ID_Num+'&start_time='+
            (Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        public_ajax.call_request('get',weiboUrl,weibo);
    }
});

function weibo(data) {   
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
                            var txt,txt2,all='',name,img;
                            if (item.photo_url==''||item.photo_url=='null'||item.photo_url=='unknown'||!item.photo_url){
                                img='/static/images/unknown.png';
                            }else {
                                img=item.photo_url;
                            };
                            if (item.nick_name==''||item.nick_name=='null'||item.nick_name=='unknown'||!item.nick_name){
                                name=item.uid;
                            }else {
                                name=item.nick_name;
                            };
                            if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text){
                                txt='暂无内容';
                            }else {
                                if (item.sensitive_words_string||!isEmptyObject(item.sensitive_words_string)){
                                    var s=item.text;
                                    var keywords=item.sensitive_words_string.split('&');
                                    for (var f=0;f<keywords.length;f++){
                                        s=s.toString().replace(new RegExp(keywords[f],'g'),'<b style="color:#ef3e3e;">'+keywords[f]+'</b>');
                                    }
                                    txt=s;

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
                                    txt2=rrr;
                                }else {
                                    txt=item.text;
                                    if (txt.length>=160){
                                        txt2=txt.substring(0,160)+'...';
                                        all='inline-block';
                                    }else {
                                        txt2=txt;
                                        all='none';
                                    }
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
                                '   <img src="'+img+'" alt="" class="center_icon">'+
                                '   <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>&nbsp;'+
                                '   <a class="tid" style="display: none;">'+item.tid+'</a>'+
                                '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                                '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                '   <span class="time" style="font-weight:900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                                '   <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                                '   <p class="allall1" style="display:none;">'+txt+'</p>'+
                                '   <p class="allall2" style="display:none;">'+txt2+'</p>'+
                                '   <span class="center_2">'+txt2+'</span>'+
                                '   <div class="_translate" style="display: none;"><b style="color: #f98077;">译文：</b><span class="tsWord"></span></div>'+
                                '   <div class="center_3">'+
                                '       <span class="cen3-1" onclick="retweet(this,\''+operateType+'\')"><i class="icon icon-share"></i>&nbsp;&nbsp;转推（<b class="forwarding">'+item.share+'</b>）</span>'+
                                '       <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                                '       <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;喜欢(<b class="like">'+item.favorite+'</b>)</span>'+
                                '       <span class="cen3-4" onclick="emailThis(this)"><i class="icon icon-envelope"></i>&nbsp;&nbsp;私信</span>'+
                                '       <span class="cen3-5" onclick="joinPolice(this,\'人物\')"><i class="icon icon-plus-sign"></i>&nbsp;&nbsp;加入预警库</span>'+
                                '       <span class="cen3-9" onclick="robot(this)"><i class="icon icon-github-alt"></i>&nbsp;&nbsp;机器人回复</span>'+
                                '       <span class="cen3-5" onclick="translateWord(this)"><i class="icon icon-exchange"></i>&nbsp;&nbsp;翻译</span>'+
                                '    </div>'+
                                '    <div class="commentDown" style="width: 100%;display: none;">'+
                                '        <input type="text" class="comtnt" placeholder="评论内容"/>'+
                                '        <span class="sureCom" onclick="comMent(this)">评论</span>'+
                                '    </div>'+
                                '    <div class="emailDown" style="width: 100%;display: none;">'+
                                '        <input type="text" class="infor" placeholder="私信内容"/>'+
                                '        <span class="sureEmail" onclick="letter(this)">发送</span>'+
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
                        '            <div>'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio" type="checkbox" name="demo-checkbox">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        '                </label>'+
                        '                <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                        '                <a class="center_1 centerNAME" href="###">'+nameuid+'</a>'+
                        '                <a class="mainUID" style="display: none;">'+row.uid+'</a>'+
                        '                <a class="_id" style="display: none;">'+row._id+'</a>'+
                        '                <a onclick="oneUP(this,\'人物\')" class="report" style="margin-left: 50px;cursor: pointer;"><i class="icon icon-upload-alt"></i>  上报</a>'+
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
    var txt = $(_this).parents('.center_rel').find('.center_2').text().replace(/\&/g,'%26').replace(/\#/g,'%23');
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
    var f='';
    if (data[0]||data){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}

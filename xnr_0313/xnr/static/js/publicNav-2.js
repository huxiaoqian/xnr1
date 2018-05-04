function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 128+127),
                Math.round(Math.random() * 128+127),
                Math.round(Math.random() * 128+127)
            ].join(',') + ')'
        }
    };
}
function getDaysBefore($time) {
    var a=new Date(new Date(new Date().setDate(new Date().getDate()-Number($time))).setHours(0,0,0,0));
    var b=Date.parse(a)/1000;
    return b;
}
//================
var localTime=new Date();
Y= localTime.getFullYear()+'-';
M=(localTime.getMonth()+1<10?'0'+(localTime.getMonth()+1):localTime.getMonth()+1)+'-';
D=(localTime.getDate()-1<10?'0'+(localTime.getDate()):localTime.getDate());
var $_time=Y+M+D;
//当天零点的时间戳
function todayTimetamp() {
    var start=new Date();
    start.setHours(0);
    start.setMinutes(0);
    start.setSeconds(0);
    start.setMilliseconds(0);
    var todayStartTime=Date.parse(start)/1000;
    return todayStartTime;
}
//昨天时间到23:59
function yesterday() {
    var day = new Date();
    day.setTime(day.getTime()-24*60*60*1000);
    var s1 = day.getFullYear()+ "-" + (day.getMonth()+1) + "-" + day.getDate();
    var s2 = (Date.parse(new Date(new Date(new Date(s1).toLocaleDateString()).getTime()+24*60*60*1000-1)))/1000;
    return s2;
}
//时间戳转时间
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日|上午|下午/g, " ");
}
//去除空格
function delSpace(str){
    var str=str.replace(/<\/?[^>]*>/gim,"");//去掉所有的html标记
    var result=str.replace(/(^\s+)|(\s+$)/g,"");//去掉前后空格
    return  result.replace(/\s/g,"");//去除文章中间空格
}
//判断字符串中某个字符出现的次数
function patch(re,s){ //参数1正则式，参数2字符串
    re=eval("/"+re+"/ig"); //不区分大小写，如须则去掉i,改为 re=eval_r("/"+re+"/g")
    var len = s.match(re).length;
    return len;
}
//判断空对象
function isEmptyObject(e) {
    var t;
    for (t in e)
        return !1;
    return !0
}
//删除数组指定项
Array.prototype.removeByValue = function(val) {
    for(var i=0; i<this.length; i++) {
        if(this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
};
//查看全文
function allWord(_this) {
    var a=$(_this).attr('data-all');
    if (a==0){
        $(_this).text('收起');
        $(_this).parent('.center_rel').find('.center_2').html($(_this).next().html());
        $(_this).attr('data-all','1');
    }else {
        $(_this).text('查看全文');
        $(_this).parent('.center_rel').find('.center_2').html($(_this).next().next().html());
        $(_this).attr('data-all','0');
    }
}
//翻译
function Check(s) {
    var str = s.replace(/%/g, "%25").replace(/\+/g, "%2B").replace(/\s/g, "+"); // % + \s 3
    str = str.replace(/-/g, "%2D").replace(/\*/g, "%2A").replace(/\//g, "%2F"); // - * / 4
    str = str.replace(/\&/g, "%26").replace(/!/g, "%21").replace(/\=/g, "%3D"); // & ! = 5
    str = str.replace(/\?/g, "%3F").replace(/:/g, "%3A").replace(/\|/g, "%7C"); // ? : | 6
    str = str.replace(/\,/g, "%2C").replace(/\./g, "%2E").replace(/#/g, "%23"); // , . # 7
    return str;
}
var translateWordThis='';
function translateWord(_this) {
    var t=$(_this).parents('.center_rel').find('.center_2').text();
    var txt=Check(t);
    translateWordThis=_this;
    var translate_url='/index/text_trans/?q='+txt;
    public_ajax.call_request('get',translate_url,transSUCCESS)
}
function transSUCCESS(data) {
    if (data.length==0){data='暂无翻译内容';}
    $(translateWordThis).parents('.center_rel').find('.tsWord').text(data);
    $(translateWordThis).parent().prev('._translate').show();
}
//私信该用户
function emailThis(_this) {
    $(_this).parents('.center_rel').find('.emailDown').show();
}
function letter(_this) {
    var uid = $(_this).parents('.center_rel').find('.uid').text();
    var txt = Check($(_this).prev().val());
    var post_url_letter='/twitter_xnr_operate/private_operate/?xnr_user_no='+ID_Num+'&uid='+uid+
        '&text='+txt;
    public_ajax.call_request('get',post_url_letter,operatSuccess)
}
var urlFirst_zpd='',mft_id,ft,first_url,reportWaring,reportInfo,
    reply_retweet='retweet_operate',reply_comment='comment_operate';
setTimeout(function () {
    ft=$('.nav_type').text();
    if(ft=='(微博)'){
        urlFirst_zpd='weibo_xnr_operate';mft_id='mid';reportWaring='weibo_xnr_warming_new';
        reply_retweet='reply_retweet',reply_comment='reply_comment';reportInfo='weibo_info';
        first_url='/weibo_xnr_monitor/new_addto_weibo_corpus/';
    }else if(ft=='(FaceBook)'){
        urlFirst_zpd='facebook_xnr_operate';mft_id='fid';reportWaring='facebook_xnr_warning';
        first_url='/facebook_xnr_monitor/addto_facebook_corpus/';reportInfo='fb_info';
    }else if(ft=='(twitter)'){
        urlFirst_zpd='twitter_xnr_operate';mft_id='tid';reportWaring='twitter_xnr_warning';
        first_url='/twitter_xnr_monitor/addto_facebook_corpus/';reportInfo='tw_info';
    }
},1000);
//retweet_operate   comment_operate   like_operate
//转发 分享  转推
var for_type,for_this;
function retweet(_this,type) {
    for_type=type;
    for_this=_this;
    $(_this).parents('.center_rel').find('.forwardingDown').show();
}
function forwardingBtn() {
    var txt = $(for_this).parents('.center_rel').find('.forwardingIput').val();
    if (txt!=''){
        var MFT = $(for_this).parents('.center_rel').find('.'+mft_id).text();
        var forPost_url='/'+urlFirst_zpd+'/'+reply_retweet+'/?tweet_type='+for_type+'&xnr_user_no='+ID_Num+
            '&text='+txt+'&'+mft_id+'='+MFT;
        if (loadingType!='weibo'){
            var uid = $(for_this).parents('.center_rel').find('.uid').text();
            forPost_url+='&uid='+uid;
        }
        public_ajax.call_request('get',forPost_url,operatSuccess);
    }else {
        $('#pormpt p').text('转发内容不能为空。');
        $('#pormpt').modal('show');
    }
}
//评论
function showInput(_this) {
    $(_this).parents('.center_rel').find('.commentDown').show();
};
function comMent(_this,type){
    var txt = Check($(_this).prev().val());
    if (txt!=''){
        var MFT = $(_this).parents('.center_rel').find('.'+mft_id).text();
        var comPost_url='/'+urlFirst_zpd+'/'+reply_comment+'/?tweet_type='+type+'&text='+txt+'&xnr_user_no='+
            ID_Num+'&'+mft_id+'='+MFT;
        if (loadingType!='weibo'){
            var uid = $(_this).parents('.center_rel').find('.uid').text();
            comPost_url+='&uid='+uid;
        }
        public_ajax.call_request('get',comPost_url,operatSuccess);
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}
//点赞  喜欢
function thumbs(_this) {
    var MFT = $(_this).parents('.center_rel').find('.'+mft_id).text();
    var likePost_url='/'+urlFirst_zpd+'/like_operate/?'+mft_id+'='+MFT+'&xnr_user_no='+ID_Num;
    if (loadingType=='faceBook'){
        var uid = $(_this).parents('.center_rel').find('.uid').text();
        likePost_url+='&uid='+uid;
    }
    public_ajax.call_request('get',likePost_url,operatSuccess);
};
//机器人回复
var robotThis;
function robot(_this) {
    robotThis=_this;
    $(_this).parents('.center_rel').find('.commentDown').show();
    var txt= $(_this).parents('.center_rel').find('.center_2').text();
    // var robot_url='/'+urlFirst_zpd+'/robot_reply/?question='+Check(txt);
    var robot_url='/facebook_xnr_operate/robot_reply/?question='+Check(txt);
    public_ajax.call_request('get',robot_url,robotTxt);
}
function robotTxt(data) {
    $(robotThis).parents('.center_rel').find('.robotQuestion').remove();
    var txt=data['tuling'];
    if (isEmptyObject(data)||!txt){txt='机器人无答复'};
    $(robotThis).parents('.center_rel').find('.commentDown').children('input').val(txt);
    var robotType=$(robotThis).parents('.center_rel').find('.commentDown').children('span').attr('onclick').replace(/\(|\)|\'/g,'').split(',')[1];
    var str='<div class="robotQuestion">';
    var robot1='<p style="font-weight: 900;color:#f6a38e;"><i class="icon icon-lightbulb"></i>&nbsp;相关问题</p>' +
        '<p style="text-indent:30px;margin:5px 0;">'+data["own"][0]+'</p>';
    var robot2='<div><p style="font-weight: 900;color:#f6a38e;"><i class="icon icon-lightbulb"></i>&nbsp;相关评论</p>';
    var robot3='';
    $.each(data['own'][1],function (index,item) {
         robot3+='<div class="robotDown" class="r"><input type="text" class="robotIput" value="'+item+'">&nbsp;' +
        '<span class="sureRobot" onclick="comMent(this,\''+robotType+'\')">回复</span></div>'
    });
    robot2+=robot3+'</div>';
    str+=robot1+robot2+'</div>';
    $(robotThis).parents('.center_rel').find('.commentDown').after(str);
}
//加入预警库
function getInfo(_this) {
    var alldata=[];
    var uid = $(_this).parents('.center_rel').eq(0).find('.uid').text();alldata.push(uid);
    var mid = $(_this).parents('.center_rel').eq(0).find('.mid').text();alldata.push(mid);
    var timestamp = $(_this).parents('.center_rel').eq(0).find('.timestamp').text();alldata.push(timestamp);
    return alldata;
};
function joinPolice(_this,type) {
    var info=getInfo(_this);
    var police_url='/'+reportWaring+'/addto_warning_corpus/?xnr_user_no='+ID_Num+'&uid='+info[0]+
        '&mid='+info[1]+'&timestamp='+info[2]+'&warning_source='+type;
    public_ajax.call_request('get',police_url,operatSuccess)
};
//加入语料库
var wordUid,wordMid,wordTime;
function joinlab(_this) {
    wordMid = $(_this).parents('.center_rel').find('.mid').text();
    wordUid = $(_this).parents('.center_rel').find('.uid').text();
    wordTime = $(_this).parents('.center_rel').find('.timestamp').text();
    $('#wordcloud').modal('show');
}
function joinWord() {
    var create_type=$('#wordcloud input:radio[name="xnr"]:checked').val();
    var corpus_type=$('#wordcloud input:radio[name="theday"]:checked').val();
    var theme_daily_name=[],tt=11;
    if (corpus_type=='主题语料'){tt=22};
    $("#wordcloud input:checkbox[name='theme"+tt+"']:checked").each(function (index,item) {
        theme_daily_name.push($(this).val());
    });
    var first_url,mftID;
    if(ft=='(微博)'){
        first_url='/weibo_xnr_monitor/new_addto_weibo_corpus/';mftID='mid';
    }else if(ft=='(FaceBook)'){
        first_url='/facebook_xnr_monitor/addto_facebook_corpus/';mftID='fid';
    }else if(ft=='(twitter)'){
        first_url='/twitter_xnr_monitor/addto_facebook_corpus/';mftID='tid';
    }
    var corpus_url= first_url+'?xnr_user_no='+ID_Num +
        '&corpus_type='+corpus_type+'&theme_daily_name='+theme_daily_name.join(',')+
        '&uid='+wordUid+'&'+mft_id+'='+wordMid+'&timestamp='+wordTime+'&create_type='+create_type;
    public_ajax.call_request('get',corpus_url,operatSuccess);
}
//一键上报
function oneUP(_this,type) {
    var len=$(_this).parents('.everyUser').find('.center_rel');
    if (len){
        var mainUID=$(_this).parents('.everyUser').find('.mainUID').text();
        var mainNAME=$(_this).parents('.everyUser').find('.centerNAME').text();
        var _id=$(_this).parents('.everyUser').find('._id').text();
        var dateTime='';
        var uidList=[],weibo_info=[];
        for (var i=0;i<len.length;i++){
            var uid=$(len[i]).find('.uid').text();uidList.push(uid);
            var mid = $(len[i]).find('.'+mft_id).text();
            var timestamp = $(len[i]).find('.timestamp').text();
            weibo_info.push({'mid':mid,'timestamp':timestamp});
        }
        // var once_url='/weibo_xnr_warming/report_warming_content/?report_type='+type+'&xnr_user_no='+ID_Num+
        //     '&event_name='+mainNAME+'&uid='+mainUID+'&report_id='+_id+'&user_info='+uidList+
        //     '&weibo_info='+weibo_info;
        if (type=='人物'){
            mainNAME='';
        }else if (type=='言论'){
            mainNAME='';mainUID='';
        }else if (type=='事件'){
            mainUID='';
        }else if (type=='时间'){
            mainNAME='';mainUID='';
            dateTime=$(_this).parents('.everyUser').find('.timestamp').text();
        }
        var job={
            'report_type':type,
            'xnr_user_no':ID_Num,
            'report_id':_id,
            //=========
            'date_time':dateTime,
            'event_name':mainNAME,
            'uid':mainUID,
            'user_info':uidList,
            // 'weibo_info':weibo_info,
        }
        job[reportInfo]=weibo_info;
        $.ajax({
            type:'POST',
            url: '/'+reportWaring+'/report_warming_content/',
            contentType:"application/json",
            data: JSON.stringify(job),
            dataType: "json",
            success: operatSuccess,
        });
    }else {
        $('#pormpt p').text('微博内容为空，无法上报。');
        $('#pormpt').modal('show');
    }
}
//操作返回结果
function operatSuccess(data) {
    var f='';
    if (data[0]||data){f='操作成功'}else {f='操作失败'};
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}

//@用户推荐
var recommendUrl='/weibo_xnr_operate/daily_recommend_at_user/?xnr_user_no=WXNR0001';
public_ajax.call_request('get',recommendUrl,recommendlist);
function recommendlist(data) {
    var str='';
    for(var a in data){
        var n=data[a];
        if (n==''){n=a};
        str+='<li uid="'+a+'" title="'+n+'"><a href="###">'+n+'</a></li>';
    }
    $('#user_recommend .user_example_list').html(str);
}
//------
var xnrUser='WXNR0001',weiboMail='13121835733',weiboPhone='13121835733',
    uid='1234567890',mid='4085480909715263';
var operateType,actType;
function obtain(t) {
    if (t == 'o'){
        operateType='origin';
    }else if (t=='r'){
        operateType='retweet';
    }else if (t== 'c'){
        operateType='comment';
    }
    actType=$('#myTabs li.active a').text().toString().trim();
}
$('#sure_post').on('click',function () {
    obtain('o');
    var txt=$('#post-2-content').val();
    var flag=$('.friends button b').text(),rank='';
    if (flag=='公开'){rank=0}else if (flag=='好友圈'){rank=6}if (flag=='仅自己可见'){rank=1}if (flag=='群可见'){rank=7};

    //原创
    var post_url_1='/weibo_xnr_operate/submit_tweet/?tweet_type='+actType+'&operate_type='+operateType+
        '&xnr_user_no='+xnrUser+'&text='+txt+'&weibo_mail_account='+weiboMail+'&weibo_phone_account='+weiboPhone+'&rank='+rank+
        '&p_url=["/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/images/1.jpg","/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/images/2.jpg"]';
    if ($("input[name='demo']")[0].checked){
        if ($('.start').val() && $('.end').val()){
            var a=Date.parse(new Date($('.start').val()))/1000;
            var b=Date.parse(new Date($('.end').val()))/1000;
            //var timeMath=Math.random()*(b-a)+a;
            post_url_1+='&post_time_sts='+a+'&post_time_ets='+b;
        }else {
            $('#pormpt p').text('因为您是定时发送，所以请填写好您定制的时间。');
            $('#pormpt').modal('show');
        }
    }
    if (rank==7){post_url_1+='&rankid=1022:2304914131985239110622'}
    // public_ajax.call_request('get',post_url_1,postYES)
});
function postYES(data) {
    console.log(data)
}
//语料推荐
$('.everyday-2 .ed-2-1 input:radio[name="theme"]').on('click',function () {
    var d=$('.everyday-2 .ed-2-2 .demo-radio');
    for(var e=0;e<d.length;e++){if(d[e].checked) {d[e].checked=false;}};
    var the=$(this).val();
    var the_url='/weibo_xnr_operate/daily_recommend_tweets/?theme='+the;
    // public_ajax.call_request('get',the_url,postYES)
})
$('.everyday-2 .ed-2-2 .demo-radio').on('click',function () {
    var TH=$(this).val();
    var the=$('.everyday-2 .ed-2-1 input:radio[name="theme"]:checked').val();
    var TH_url='/weibo_xnr_operate/daily_recommend_tweets/?theme='+the+'&sort_item='+TH;
    // public_ajax.call_request('get',TH_url,postYES)
})





//转发
$('.post_perfect .cen3-1').on('click',function () {
    obtain('r');
    var txt = $(this).parent().prev().text();
    var post_url_2='/weibo_xnr_operate/reply_retweet/?tweet_type='+actType+'&operate_type='+operateType+'&uid='+uid+
        '&text='+txt+'&weibo_mail_account='+weiboMail+'&weibo_phone_account='+weiboPhone+'&mid='+mid;
    //public_ajax.call_request('get',post_url_2,postYES)
});
//评论
$('.post_perfect .cen3-2').on('click',function () {
    $(this).parents('.post_perfect').find('.commentDown').show();
});
$('.commentDown .sureCom').on('click',function () {
    var txt = $('.comtnt').val();
    if (txt!=''){
        var post_url_3='/weibo_xnr_operate/reply_comment/?text='+txt+'&weibo_mail_account='+weiboMail+
            '&weibo_phone_account='+weiboPhone+'&mid='+mid;
        console.log(post_url_3)
        //public_ajax.call_request('get',post_url_3,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
});

//点赞
$('.post_perfect .cen3-3').on('click',function () {
    var post_url_4='/weibo_xnr_operate/like_operate/?weibo_mail_account='+weiboMail+'&weibo_phone_account='+weiboPhone+'&mid='+mid;
    //public_ajax.call_request('get',post_url_4,postYES)
});


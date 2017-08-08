var flag='';
var xnrUser='WXNR0001',weiboMail='13121835733',weiboPhone='13121835733',
    uid='1234567890',mid='4085480909715263';
$('.copyFinish').on('click',function () {
    flag=$('#myTabs li.active').attr('flag');
    var _name=$(this).parent().prev().prev().find('b').text();
    var _dataType=$(this).attr('datatype');
    $('#container .type_page #content .'+_dataType+' .clone-1').attr('placeholder','回复'+_name);
    $('#container .type_page #content .'+_dataType).show(40);
})

//评论回复
$('.commentClone .clone-2-4').on('click',function () {
    var txt = $(this).parent().prev().val();
    if (txt!=''){
        var post_url_1='/weibo_xnr_operate/reply_comment/?text='+txt+'&weibo_mail_account='+weiboMail+
            '&weibo_phone_account='+weiboPhone+'&mid='+mid;
        console.log(post_url_1)
        // public_ajax.call_request('get',post_url_1,postYES)
    }else {
        $('#pormpt p').text('回复内容不能为空。');
        $('#pormpt').modal('show');
    }
});

//转发
$('.forwardClone .clone-2-4').on('click',function () {
    var txt = $(this).parent().prev().val();
    var post_url_2='/weibo_xnr_operate/reply_retweet/?tweet_type='+actType+'&operate_type='+operateType+'&uid='+uid+
        '&text='+txt+'&weibo_mail_account='+weiboMail+'&weibo_phone_account='+weiboPhone+'&mid='+mid;
    //public_ajax.call_request('get',post_url_2,postYES)
});

//@用户
$('.replyClone .clone-2-4').on('click',function () {
    var txt = $(this).parent().prev().val();
    var post_url_3='/weibo_xnr_operate/reply_comment/?text='+txt+'&weibo_mail_account='+weiboMail+
        '&weibo_phone_account='+weiboPhone+'&mid='+mid;
    //public_ajax.call_request('get',post_url_3,postYES)
});

//私信
$('.letterClone .clone-2-4').on('click',function () {
    var txt = $(this).parent().prev().val();
    var post_url_4='/weibo_xnr_operate/reply_private/?text='+txt+'&weibo_mail_account='+weiboMail+
        '&weibo_phone_account='+weiboPhone+'&uid='+uid;
    //public_ajax.call_request('get',post_url_4,postYES)
});


//关注回粉
// 关注
$('.foc-join').on('click',function () {
    var post_url_5='/weibo_xnr_operate/follow_operate/?weibo_mail_account='+weiboMail+
        '&weibo_phone_account='+weiboPhone+'&uid='+uid;
    //public_ajax.call_request('get',post_url_5,postYES)
});
//取消关注
$('.foc-join').on('click',function () {
    var post_url_6='/weibo_xnr_operate/unfollow_operate/?weibo_mail_account='+weiboMail+
        '&weibo_phone_account='+weiboPhone+'&uid='+uid;
    //public_ajax.call_request('get',post_url_6,postYES)
});

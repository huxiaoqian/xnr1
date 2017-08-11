var xnrUser='WXNR0001',
//weiboMail='13121835733',weiboPhone='13121835733','&weibo_mail_account='+weiboMail+'&weibo_phone_account='+weiboPhone+
    uid='1234567890',mid='4085480909715263';
//@用户推荐
var recommendUrl='/weibo_xnr_operate/daily_recommend_at_user/?xnr_user_no='+xnrUser;
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
        '&xnr_user_no='+xnrUser+'&text='+txt+'&rank='+rank+
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
var defalutWeiboUrl='/weibo_xnr_operate/daily_recommend_tweets/?theme=旅游&sort_item=timestamp';
public_ajax.call_request('get',defalutWeiboUrl,defalutWords)
$('.everyday-2 .ed-2-1 input:radio[name="theme"]').on('click',function () {
    //var d=$('.everyday-2 .ed-2-2 .demo-radio');
    // for(var e=0;e<d.length;e++){if(d[e].checked) {d[e].checked=false;}};
    var the=$(this).val();
    var theSort=$('.everyday-2 .ed-2-2 input:radio[name="th"]:checked').val();
    var the_url='/weibo_xnr_operate/daily_recommend_tweets/?theme='+the+'&sort_item='+theSort;
    // public_ajax.call_request('get',the_url,postYES)
});
$('.everyday-2 .ed-2-2 .demo-radio').on('click',function () {
    var TH=$(this).val();
    var the=$('.everyday-2 .ed-2-1 input:radio[name="theme"]:checked').val();
    var TH_url='/weibo_xnr_operate/daily_recommend_tweets/?theme='+the+'&sort_item='+TH;
    console.log(TH_url)
    // public_ajax.call_request('get',TH_url,postYES)
});
function defalutWords(data) {
    console.log(data)
    $('#defaultWeibo').bootstrapTable('load', data);
    $('#defaultWeibo').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
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
                    if (row._source.nickname==''||row._source.speaker_nickname=='null'||row._source.speaker_nickname=='unknown'){
                        name=row._source.speaker_qq_number;
                    }else {
                        name=row._source.speaker_nickname;
                    };
                    if (row._source.text==''||row._source.text=='null'||row._source.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row._source.text;
                    };
                    var str=
                        '<div class="post_perfect">'+
                        '   <div class="post_center-hot">'+
                        '       <img src="/static/images/post-6.png" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>：'+
                        '           <i class="mid" style="display: none;">'+row._source.mid+'</i>'+
                        '           <i class="uid" style="display: none;">'+row._source.uid+'</i>'+
                        '           <span class="center_2">'+txt+
                        '           </span>'+
                        '        </div>'+
                        '        <div class="center_3">'+
                        '           <span class="cen3-1"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（'+row._source+'）</span>'+
                        '           <span class="cen3-2"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（'+row._source+'）</span>'+
                        '           <span class="cen3-3"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞（'+row._source+'）</span>'+
                        '        </div>'+
                        '        <div class="commentDown" style="width: 100%;display: none;">'+
                        '           <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '           <span class="sureCom">评论</span>'+
                        '        </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                    //评论
                    $('.post_perfect .cen3-2').on('click',function () {
                        $(this).parents('.post_perfect').find('.commentDown').show();
                    });
                }
            },
        ],
    });
    $('.defaultWeibo .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}



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


var xnrUser=nowUser,
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
$('#container .type_page #myTabs a').on('click',function () {
    var arrow=$(this).attr('href'),arrowName='';
    if (arrow == '#everyday'){
        arrowName='@用户推荐';
        recommendUrl='/weibo_xnr_operate/daily_recommend_at_user/?xnr_user_no='+xnrUser;
    }else if (arrow=='#hot'){
        arrowName='@用户推荐';
        public_ajax.call_request('get',hotWeiboUrl,hotWeibo);
        recommendUrl='/weibo_xnr_operate/hot_sensitive_recommend_at_user/?sort_item=retweeted';
    }else if (arrow== '#business'){
        arrowName='@敏感用户推荐';
        public_ajax.call_request('get',busWeiboUrl,businessWeibo);
        recommendUrl='/weibo_xnr_operate/hot_sensitive_recommend_at_user/?sort_item=sensitive';
    }
    $('#user_recommend .tit').text(arrowName);
    public_ajax.call_request('get',recommendUrl,recommendlist);
})

var operateType,actType;
function obtain(t) {
    if (t == 'o'){
        operateType='origin';
        recommendUrl='/weibo_xnr_operate/daily_recommend_at_user/?xnr_user_no='+xnrUser;
        public_ajax.call_request('get',recommendUrl,recommendlist);
    }else if (t=='r'){
        operateType='retweet';
        recommendUrl='/weibo_xnr_operate/hot_sensitive_recommend_at_user/?sort_item=retweeted';
        public_ajax.call_request('get',recommendUrl,recommendlist);
    }else if (t== 'c'){
        operateType='comment';
        recommendUrl='/weibo_xnr_operate/hot_sensitive_recommend_at_user/?sort_item=sensitive';
        public_ajax.call_request('get',recommendUrl,recommendlist);
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
            var c=$('#_timing3').val();
            //var timeMath=Math.random()*(b-a)+a;
            post_url_1+='&post_time_sts='+a+'&post_time_ets='+b+'&remark='+c;
        }else {
            $('#pormpt p').text('因为您是定时发送，所以请填写好您定制的时间。');
            $('#pormpt').modal('show');
        }
    }
    if (rank==7){post_url_1+='&rankid=1022:2304914131985239110622'}
    // public_ajax.call_request('get',post_url_1,postYES)
});

//语料推荐
var defalutWeiboUrl='/weibo_xnr_operate/daily_recommend_tweets/?theme=旅游&sort_item=timestamp';
// public_ajax.call_request('get',defalutWeiboUrl,defalutWords);
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
    $('#defaultWeibo').bootstrapTable('load', data);
    $('#defaultWeibo').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 2,//单页记录数
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
                    var name,txt,img;
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.nick_name;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };
                    var str=
                        '<div class="post_perfect">'+
                        '   <div class="post_center-hot">'+
                        '       <img src="'+img+'" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>：'+
                        '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <span class="center_2">'+txt+
                        '           </span>'+
                        '           <div class="center_3">'+
                        '               <span class="cen3-1" onclick="retweet(this)"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（'+row.retweeted+'）</span>'+
                        '               <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（'+row.comment+'）</span>'+
                        '               <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '           </div>'+
                        '           <div class="commentDown" style="width: 100%;display: none;">'+
                        '               <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '               <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '           </div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#defaultWeibo p').hide();
    $('.defaultWeibo .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}
//评论
function showInput(_this) {
    $(_this).parents('.post_perfect').find('.commentDown').show();
};
function comMent(_this){
    var txt = $(_this).prev().val();
    var mid = $(_this).parents('.post_perfect').find('.mid').text();
    if (txt!=''){
        var post_url_3='/weibo_xnr_operate/reply_comment/?text='+txt+'&xnr_user_no='+xnrUser+'&mid='+mid;
        //public_ajax.call_request('get',post_url_3,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}

//转发
function retweet(_this) {
    obtain('r');
    var txt = $(_this).parent().prev().text();
    var mid = $(_this).parents('.post_perfect').find('.mid').text();
    var uid = $(_this).parents('.post_perfect').find('.uid').text();
    var post_url_2='/weibo_xnr_operate/reply_retweet/?tweet_type='+actType+'&operate_type='+operateType+'&uid='+uid+
        '&text='+txt+'&mid='+mid;
    //public_ajax.call_request('get',post_url_2,postYES)
}

//点赞
function thumbs(_this) {
    var mid = $(_this).parents('.post_perfect').find('.mid').text();
    var post_url_4='/weibo_xnr_operate/like_operate/?mid='+mid;
    //public_ajax.call_request('get',post_url_4,postYES)
};

//操作返回结果
function postYES(data) {
    console.log(data)
}

//=========热点跟随===========
var hotWeiboUrl='/weibo_xnr_operate/hot_recommend_tweets/?topic_field=民生类_法律&sort_item=timestamp';
// public_ajax.call_request('get',hotWeiboUrl,hotWeibo);
function hotWeibo(data) {
    $('#defaultWeibo2').bootstrapTable('load', data);
    $('#defaultWeibo2').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 2,//单页记录数
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
                    var name,txt,img;
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.nick_name;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };
                    var str=
                        '<div class="post_perfect">'+
                        '   <div id="post_center-hot">'+
                        '       <img src="'+img+'" alt="" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>'+
                        '           <span class="time" style="font-weight: 900;color: blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(row.timestamp)+'</span>  '+
                        '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '               <span class="center_2">'+txt+
                        '               </span>'+
                        '           <div class="center_3" style="margin: 10px 0;">'+
                        '               <span data-toggle="modal" data-target="#simliar"><i class="icon icon-check"></i>&nbsp;&nbsp;相似微博</span>'+
                        '               <span onclick="contantREM(this)"><i class="icon icon-reorder"></i>&nbsp;&nbsp;内容推荐</span>'+
                        '               <span onclick="related(this)"><i class="icon icon-stethoscope"></i>&nbsp;&nbsp;事件子观点及相关微博</span>'+
                        '               <span><i class="icon icon-share"></i>&nbsp;&nbsp;转发数<b class="forwarding">（'+row.retweeted+'）</b></span>'+
                        '               <span><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论数<b class="comment">（'+row.comment+'）</b></span>'+
                        '               <span><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '           </div>'+
                        '           <div class="commentDown" style="width: 100%;display: none;">'+
                        '               <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '               <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '           </div>'+
                        '        </div>'+
                        '        <div style="margin: 10px 0;">'+
                        '           <input type="text" class="point-view-1" placeholder="多个关键词请用逗号分开"/>'+
                        '           <button type="button" onclick="submitViews(this)" class="btn btn-primary btn-xs point-view-2" ' +
                        'style="height: 26px;position: relative;top: -1px;">提交子观点任务</button>'+
                        '        </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#defaultWeibo2 p').hide();
    $('.defaultWeibo2 .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}
//子观点判断
function related(_this) {
    var taskID=$(_this).parents('.post_perfect').find('.mid').text();
    var relatedUrl='/weibo_xnr_operate/hot_subopinion/?task_id='+taskID;
    public_ajax.call_request('get',relatedUrl,conViews);
}
//新建内容推荐  和  提交子观点
function submitViews(_this) {
    var taskID=$(_this).parents('.post_perfect').find('.mid').text();
    var vale=$(_this).prev().val();
    if (vale==''){
        $('#pormpt p').text('观点不能为空。');
        $('#pormpt').modal('show');
    }else {
        var conViewsUrl='/weibo_xnr_operate/hot_subopinion/?task_id='+taskID;
        public_ajax.call_request('get',conViewsUrl,conViews);
    }
}
function conViews(data) {
    var x='';
    if (data){
        x='提交成功';
    }else {
        x='提交失败';
    }
    $('#pormpt p').text(x);
    $('#pormpt').modal('show');
}
//内容推荐
function contantREM(_this) {
    var taskID=$(_this).parents('.post_perfect').find('.mid').text();
    var calNot_url='/weibo_xnr_operate/hot_content_recommend/?task_id='+taskID;
    public_ajax.call_request('get',calNot_url,calNot);
}
function calNot(data) {
    if (data=='正在计算'){
        $('#pormpt p').text('正在计算...');
        $('#pormpt').modal('show');
    }else {
        console.log(data)
        //$('#content_recommend').modal('show');
    }
}

//======业务发帖=======
var busWeiboUrl='/weibo_xnr_operate/bussiness_recomment_tweets/?sort_item=timestamp';
// public_ajax.call_request('get',busWeiboUrl,businessWeibo);
function businessWeibo(data) {
    $('#defaultWeibo3').bootstrapTable('load', data);
    $('#defaultWeibo3').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 2,//单页记录数
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
                    var name,txt,img;
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.nick_name;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };
                    var str=
                        '<div class="post_perfect">'+
                        '   <div class="post_center-hot">'+
                        '       <img src="'+img+'" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>：'+
                        '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <span class="center_2">'+txt+
                        '           </span>'+
                        '           <div class="center_3">'+
                        '               <span class="cen3"><i class="icon icon-time"></i>'+getLocalTime(row.timestamp)+'</span>'+
                        '               <span class="cen3-1" onclick="retweet(this)"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（'+row.retweeted+'）</span>'+
                        '               <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（'+row.comment+'）</span>'+
                        '               <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '           </div>'+
                        '           <div class="commentDown" style="width: 100%;display: none;">'+
                        '               <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '               <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '           </div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#defaultWeibo3 p').hide();
    $('.defaultWeibo3 .search .form-control').attr('placeholder','搜索关键词或子观点相关的微博（回车搜索）');
}



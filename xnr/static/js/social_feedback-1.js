var flag='';
var xnrUser=nowUser;
$('.copyFinish').on('click',function () {
    flag=$('#myTabs li.active').attr('flag');
    var _name=$(this).parent().prev().prev().find('b').text();
    var _dataType=$(this).attr('datatype');
    $(this).parents('.commentEvery').find('.'+_dataType+' .clone-1').attr('placeholder','回复'+_name);
    $(this).parent().next().show(40);
})
//type按键
$('#container .type_page #myTabs a').on('click',function () {
    var mmarrow=$(this).attr('tp');
    var comURL='/weibo_xnr_operate/'+mmarrow+'/?xnr_user_no='+xnrUser+'&sort_item=timestamp';
    public_ajax.call_request('get',pointUrl,com);
})
//排序选择
$('#container .desc_index .demo-label').on('click',function () {
    var tp1=$(this).find('input').val();
    var tp2=$('#myTabs li.active').attr('tp');
    var comURL='/weibo_xnr_operate/'+tp2+'/?xnr_user_no='+xnrUser+'&sort_item='+tp;
    public_ajax.call_request('get',comURL,com);
})
//评论回复
var comURL='/weibo_xnr_operate/show_comment/?xnr_user_no='+xnrUser+'&sort_item=timestamp';
public_ajax.call_request('get',comURL,com);
function com(data) {
    console.log(data)
    $('#comment-1').bootstrapTable('load', data);
    $('#comment-1').bootstrapTable({
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
                        '<div class="commentAll">'+
                        '    <div class="commentEvery">'+
                        '        <img src="/static/images/unknown.png" alt="" class="com-head">'+
                        '        <div class="com com-1">'+
                        '            <b class="com-1-name">魅蓝手机</b>'+
                        '            <div class="com-level">'+
                        '                <span style="display: inline-block;">敏感度：</span>'+
                        '                <div class="com-img" style="display: inline-block;">'+
                        '                    <img src="/static/images/level.png" alt="">'+
                        '                    <img src="/static/images/level.png" alt="">'+
                        '                    <img src="/static/images/level.png" alt="">'+
                        '                </div>'+
                        '            </div>'+
                        '        </div>'+
                        '        <div class="com com-2">'+
                        '            <b class="com-2-name" style="color: #fa7d3c;cursor: pointer;">演员的修养</b>的评论：'+
                        '            <span class="com-2-tent">嘿嘿</span>'+
                        '        </div>'+
                        '        <div class="com com-3">'+
                        '            <span class="com-3-time">2017-11-11 11:11</span>'+
                        '            <span>来自<span class="com-3-source">微博用户 weibo.com</span></span>'+
                        '            <a class="com-3-reply copyFinish" datatype="commentClone">回复</a>'+
                        '        </div>'+
                        '        <div class="commentClone">'+
                        '            <input type="text" class="clone-1"/>'+
                        '            <div class="clone-2">'+
                        '                <img src="/static/images/post-1.png" class="clone-2-1">'+
                        '                <img src="/static/images/post-2.png" class="clone-2-2">'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio clone-2-3" type="checkbox" name="desc2">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span> 同时转发到我的微博'+
                        '                </label>'+
                        '                <a href="###" class="clone-2-4">回复</a>'+
                        '            </div>'+
                        '        </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#comment-1 p').hide();
    $('.comment-1 .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}
$('#comment-1 .commentClone .clone-2-4').on('click',function () {
    var txt = $(this).parent().prev().val();
    if (txt!=''){
        var post_url_1='/weibo_xnr_operate/reply_comment/?text='+txt+'&xnr_user_no='+xnrUser+'&mid='+mid;
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

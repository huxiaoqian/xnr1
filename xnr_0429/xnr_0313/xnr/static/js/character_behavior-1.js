var time2=Date.parse(new Date())/1000;//1480176000
var weiboUrl='/weibo_xnr_warming_new/show_personnal_warming/?xnr_user_no='+ID_Num+'&start_time='+todayTimetamp()+'&end_time='+time2;
public_ajax.call_request('get',weiboUrl,weibo);
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
                    //artical=JSON.parse(artical)
                    if (artical.length==0||!artical){
                        str='暂无微博内容';
                    }else {
                        $.each(artical,function (index,item) {
                            var text,time,text2,img,name,all='';
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
                                '   <a class="center_1" style="color: #f98077;">'+name+'</a>'+
                                '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                                '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                                '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                '   <span class="cen3-1" style="font-weight: 900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;'+time+'</span>&nbsp;&nbsp;'+
                                '   <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                                '   <p class="allall1" style="display:none;">'+text+'</p>'+
                                '   <p class="allall2" style="display:none;">'+text2+'</p>'+
                                '   <span class="center_2" style="text-align: left;">'+text2+'</span>'+
                                '   <div class="center_3">'+
                                // '       <span class="cen3-2" onclick="retComLike(this)" type="get_weibohistory_retweet"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                                // '       <span class="cen3-3" onclick="retComLike(this)" type="get_weibohistory_comment"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                                // '       <span class="cen3-4" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                                '       <span class="cen3-1" onclick="retweet(this,\'预警\')"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                                '       <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                                '       <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                                '       <span class="cen3-5" onclick="joinPolice(this,\'人物\')"><i class="icon icon-plus-sign"></i>&nbsp;&nbsp;加入预警库</span>'+
                                '       <span class="cen3-9" onclick="robot(this)"><i class="icon icon-github-alt"></i>&nbsp;&nbsp;机器人回复</span>'+
                                '    </div>'+
                                '    <div class="forwardingDown" style="width: 100%;display: none;">'+
                                '       <input type="text" class="forwardingIput" placeholder="转发内容"/>'+
                                '       <span class="sureFor" onclick="forwardingBtn()">转发</span>'+
                                '    </div>'+
                                '    <div class="commentDown" style="width: 100%;display: none;">'+
                                '        <input type="text" class="comtnt" placeholder="评论内容"/>'+
                                '        <span class="sureCom" onclick="comMent(this,\'预警\')">评论</span>'+
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
                        '<div class="everyUser" style="margin: 0 auto;width: 950px;text-align: left;">'+
                        '        <div class="user_center">'+
                        '            <div style="margin-bottom:10px;text-align: left;">'+
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
    $('#weiboContent p').slideUp(30);
};

//时间选择
$('.choosetime .demo-label input').on('click',function () {
    $('#weiboContent p').show();
    var _val = $(this).val();
    if (_val == 'mize') {
        $(this).parents('.choosetime').find('#start').show();
        $(this).parents('.choosetime').find('#end').show();
        $(this).parents('.choosetime').find('#sure').css({display: 'inline-block'});
    } else {
        $(this).parents('.choosetime').find('#start').hide();
        $(this).parents('.choosetime').find('#end').hide();
        $(this).parents('.choosetime').find('#sure').hide();
        var weiboUrl='/weibo_xnr_warming_new/show_personnal_warming/?xnr_user_no='+ID_Num+'&start_time='+getDaysBefore(_val)+'&end_time='+time2;
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
        var weiboUrl='/weibo_xnr_warming_new/show_personnal_warming/?xnr_user_no='+ID_Num+'&start_time='+
            (Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        public_ajax.call_request('get',weiboUrl,weibo);
    }
});

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
};
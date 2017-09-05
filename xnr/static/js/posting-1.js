var xnrUser=ID_Num;
//@用户推荐
var recommendUrl='/weibo_xnr_operate/daily_recommend_at_user/?xnr_user_no='+xnrUser;
public_ajax.call_request('get',recommendUrl,recommendlist);
function recommendlist(data) {
    var str1='',str2='',b=0;
    for(var a in data){
        var n=data[a];
        if (n==''){n=a};
        if (b<=3){
            str1+='<li uid="'+a+'" title="'+n+'"><a href="###">'+n+'</a></li>';
        }else {
            if (b==4){
                str1+= '<a class="more" href="###" data-toggle="modal" data-target="#moreThing"' +
                    'style="color:#b0bdd0;font-size: 10px;border: 1px solid silver;float:right;' +
                    'padding: 2px 6px;margin:10px 0;border-radius: 7px;">更多</a>'
            };
            str2+='<li uid="'+a+'" title="'+n+'"><a href="###">'+n+'</a></li>';
        }
        b++;
    }
    $('#user_recommend .user_example_list').html(str1);
    if (str2){
        $('#moreThing .moreCon ul').html(str2);
    }
    $('#user_recommend .user_example_list li a').on('click',function(){
        var t1=$(this).text();
        $('#post-2-content').append('@'+t1);
    });
    $('#moreThing .moreCon ul li a').on('click',function(){
        var t2=$(this).text();
        $('#post-2-content').append('@'+t2);
    });
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
        '&xnr_user_no='+xnrUser+'&text='+txt+'&rank='+rank;
        //'&p_url=["/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/images/1.jpg","/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/images/2.jpg"]';
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
    if (rank==7){post_url_1+='&rankid='+rankidList.join(',')};
    public_ajax.call_request('get',post_url_1,postYES)
});
//群可见的情况
var rankidList=[];
function groupSure() {
    $("#grouplist input:checkbox:checked").each(function (index,item) {
        rankidList.push('1022:230491'+$(this).val());
    });
}

//语料推荐
var defalutWeiboUrl='/weibo_xnr_operate/daily_recommend_tweets/?theme=旅游&sort_item=timestamp';
public_ajax.call_request('get',defalutWeiboUrl,defalutWords);
$('.everyday-2 .ed-2-1 input:radio[name="theme"]').on('click',function () {
    //var d=$('.everyday-2 .ed-2-2 .demo-radio');
    // for(var e=0;e<d.length;e++){if(d[e].checked) {d[e].checked=false;}};
    var the=$(this).val();
    var theSort=$('.everyday-2 .ed-2-2 input:radio[name="th"]:checked').val();
    var the_url='/weibo_xnr_operate/daily_recommend_tweets/?theme='+the+'&sort_item='+theSort;
    public_ajax.call_request('get',the_url,defalutWords)
});
$('.everyday-2 .ed-2-2 .demo-radio').on('click',function () {
    var TH=$(this).val();
    var the=$('.everyday-2 .ed-2-1 input:radio[name="theme"]:checked').val();
    var TH_url='/weibo_xnr_operate/daily_recommend_tweets/?theme='+the+'&sort_item='+TH;
    public_ajax.call_request('get',TH_url,defalutWords)
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
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>'+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(row.timestamp)+'</span>  '+
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
        public_ajax.call_request('get',post_url_3,postYES)
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
    var post_url_2='/weibo_xnr_operate/reply_retweet/?tweet_type='+actType+'&xnr_user_no='+xnrUser+
        '&text='+txt+'&mid='+mid;
    public_ajax.call_request('get',post_url_2,postYES)
}

//点赞
function thumbs(_this) {
    var mid = $(_this).parents('.post_perfect').find('.mid').text();
    var post_url_4='/weibo_xnr_operate/like_operate/?mid='+mid+'&xnr_user_no='+xnrUser;
    public_ajax.call_request('get',post_url_4,postYES)
};

//操作返回结果
function postYES(data) {
    var f='';
    if (data[0]){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
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
                        '               <span onclick="simliar(this)"><i class="icon icon-check"></i>&nbsp;&nbsp;相似微博</span>'+
                        '               <span onclick="contantREM(this)"><i class="icon icon-reorder"></i>&nbsp;&nbsp;内容推荐</span>'+
                        '               <span onclick="related(this)"><i class="icon icon-stethoscope"></i>&nbsp;&nbsp;事件子观点及相关微博</span>'+
                        '               <span onclick="retweet(this)"><i class="icon icon-share"></i>&nbsp;&nbsp;转发数<b class="forwarding">（'+row.retweeted+'）</b></span>'+
                        '               <span onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论数<b class="comment">（'+row.comment+'）</b></span>'+
                        '               <span onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
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

//新建内容推荐  和  提交子观点
function submitViews(_this) {
    var taskID=$(_this).parents('.post_perfect').find('.mid').text();
    var vale=$(_this).prev().val();
    if (vale==''){
        $('#pormpt p').text('观点不能为空。');
        $('#pormpt').modal('show');
    }else {
        var conViewsUrl='/weibo_xnr_operate/submit_hot_keyword_task/?xnr_user_no='+xnrUser+'&task_id='+taskID+'&keywords_string='+vale.replace(/，/g,'')+
        'submit_user=admin@qq.com';
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
    var calNot_url='/weibo_xnr_operate/hot_content_recommend/?xnr_user_no='+xnrUser+'&task_id='+taskID//4043450590377035;
    public_ajax.call_request('get',calNot_url,calNot);
}
//内容推荐中的微博直接发布还是定时发布
function sureTiming(_this) {
    var a=$('#recommend-2 input:radio[name="gh"]:checked').val();
    var t=$(_this).parent().prev().text();
    var CNpost_url='';
    if (a=='zhi'){
        CNpost_url='/weibo_xnr_operate/submit_tweet/?tweet_type='+actType+'&operate_type='+operateType+'&xnr_user_no='+xnrUser+'&text='+t;
    }else {
        if ($('#recommend-2 .START').val() && $('#recommend-2 .ENDING').val()){
            var a=Date.parse(new Date($('.START').val()))/1000;
            var b=Date.parse(new Date($('.ENDING').val()))/1000;
            CNpost_url+='&post_time_sts='+a+'&post_time_ets='+b;
        }else {
            $('#pormpt p').text('因为您是定时发送，所以请填写好您定制的时间。');
            $('#pormpt').modal('show');
        }
    }
    public_ajax.call_request('get',CNpost_url,conViews);
}
function calNot(data) {
    if (data=='正在计算'){
        $('#pormpt p').text('正在计算...');
        $('#pormpt').modal('show');
    }else {
        $('#recommend-2').bootstrapTable('load', data);
        $('#recommend-2').bootstrapTable({
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
                        var txt;
                        if (row==''||row=='null'||row=='unknown'){
                            txt='暂无内容';
                        }else {
                            txt=row;
                        };
                        var str=
                            '<div class="post_perfect">'+
                            '   <div id="post_center-recommend">'+
                            '       <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                            '       <div class="center_rel">'+
                            '           <span class="center_2">'+txt+ '</span>'+
                            '           <div class="center_3" style="margin: 10px 0;padding-top: 10px;border-top:1px solid silver;">'+
                            '               <label class="demo-label">'+
                            '                   <input class="demo-radio" type="radio" name="gh" value="zhi" checked>'+
                            '                   <span class="demo-checkbox demo-radioInput"></span> 直接发布'+
                            '               </label>'+
                            '               <label class="demo-label">'+
                            '                   <input class="demo-radio" type="radio" value="time" name="gh">'+
                            '                   <span class="demo-checkbox demo-radioInput"></span> 定时发布'+
                            '               </label>'+
                            '               <input type="text" size="16" class="form_datetime _timing_recommend START" placeholder="选择开始时间" style="line-height:13px;font-size: 10px;'+
                            '                       padding:3px 4px;border: 1px solid silver;background: transparent;text-align: center;">'+
                            '               <input type="text" size="16" class="form_datetime _timing_recommend ENDING" placeholder="选择截止时间" style="line-height:13px;font-size: 10px;'+
                            '                       padding:3px 4px;border: 1px solid silver;background: transparent;text-align: center;">'+
                            '               <button type="button" class="btn btn-info btn-xs" class="sure_not_timing" onclick="sureTiming(_this)">发布</button>'+
                            '           </div>'+
                            '       </div>'+
                            '   </div>'+
                            '</div>';
                        return str;

                    }
                },
            ],
        });
        $('.recommend-2 .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
        $(".form_datetime._timing_recommend").datetimepicker({
            format: "yyyy-mm-dd hh:ii",
            autoclose: true,
            todayBtn: true,
            pickerPosition: "bottom-left"
        });
        $('.START').on('changeDate', function(ev){
            $('.ENDING').datetimepicker('setStartDate',ev.date);
        });
        $('.ENDING').on('changeDate', function(ev){
            $('.START').datetimepicker('setEndDate',ev.date);
        });
        $('#content_recommend').modal('show');
    }
}
//相似微博
function simliar(_this) {
    var str='';
    str+=
        '<label class="demo-label">'+
        '   <input class="demo-radio" type="checkbox" name="mem" value="">'+
        '   <span class="demo-checkbox demo-radioInput"></span> '+
        '</label>'
}
//事件子观点及相关微博
function related(_this) {
    var taskID=$(_this).parents('.post_perfect').find('.mid').text();
    var relatedUrl='/weibo_xnr_operate/hot_subopinion/?xnr_user_no='+xnrUser+'&task_id='+taskID//4043450590377035;
    public_ajax.call_request('get',relatedUrl,relatedWEIbo);
    $('#thingsweibo').modal('show');
}
function relatedWEIbo(data) {
    var dataNew=[];
    for (var key in data){
        var ls={};
        ls['name']=key;
        ls['weibo']=data[key];
        dataNew.push(ls);
    };
    $('#thWeibo').bootstrapTable('load', dataNew);
    $('#thWeibo').bootstrapTable({
        data:dataNew,
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
                title: "子观点",//标题
                field: "name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "子观点代表微博",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var str='';
                    for (var r=0;r<row.weibo.length;r++){
                        str+=
                            '<div class="post_perfect">'+
                            '   <div class="post_center-hot">'+
                            '       <img src="/static/images/post-6.png" class="center_icon">'+
                            '       <div class="center_rel">'+
                            '           <span class="center_2">'+row.weibo[r]+'</span>'+
                            '       </div>'+
                            '   </div>'+
                            '</div>';
                    }
                    return str;
                }

            },
        ],
    });
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
                        '   <div class="post_center-business">'+
                        '       <img src="'+img+'" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>：'+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(row.timestamp)+'</span>  '+
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
    $('#defaultWeibo3 p').hide();
    $('.defaultWeibo3 .search .form-control').attr('placeholder','搜索关键词或子观点相关的微博（回车搜索）');
}


//群成员列表
var gmUrl='';
// public_ajax.call_request('get',gmUrl,gmlist);
function gmlist(data) {

}
//新建一个群
$('.sureADD').on('click',function () {
    var n=$('.groupNUM').val();
    var m=[];
    $("#grouplist input:checkbox:checked").each(function (index,item) {
        m.push($(this).val());
    });
    if (n==''){
        $('#pormpt p').text('群名称不能为空。');
        $('#pormpt').modal('show');
    }else if (m.length==0){
        $('#pormpt p').text('请勾选成员');
        $('#pormpt').modal('show');
    }else {
        var mn='/weibo_xnr_operate/create_group/?xnr_user_no='+nowUser+'&group='+ n +
            '&members='+m.join(',');
        public_ajax.call_request('get',mn,postYES);
    }
})



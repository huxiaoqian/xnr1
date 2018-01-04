var operateType='info_detect';
var from_ts=Date.parse(new Date(new Date().setHours(0,0,0,0)))/1000;
var to_ts=Date.parse(new Date())/1000;
$('.title .perTime .demo-label input').on('click',function () {
    var _val=$(this).val();
    if (_val=='resize'){
        $('.titTime').show();
    }else {
        if (_val==0){
            from_ts=todayTimetamp();
        }else {
            from_ts=getDaysBefore(_val);
        }
        $('#content-1-word p').show();
        $('#hot_post p').show();
        $('#userList p').show();
        public_ajax.call_request('get',word_url,wordCloud);
        public_ajax.call_request('get',hotPost_url,hotPost);
        public_ajax.call_request('get',activePost_url,activeUser);
        $('.titTime').hide();
    }
});
//选择时间范围
$('.timeSure').on('click',function () {
    $('#content-1-word p').show();
    $('#hot_post p').show();
    $('#userList p').show();
    var from = $('.start').val();
    var to = $('.end').val();
    from_ts=Date.parse(new Date(from))/1000;
    to_ts=Date.parse(new Date(to))/1000;
    if (from_ts==''||to_ts==''){
        $('#pormpt p').text('请检查选择的时间（不能为空）');
        $('#pormpt').modal('show');
    }else {
        public_ajax.call_request('get',word_url,wordCloud);
        public_ajax.call_request('get',hotPost_url,hotPost);
        public_ajax.call_request('get',activePost_url,activeUser);
    }
});
//----关键词云
var word_url='/facebook_xnr_monitor/lookup_weibo_keywordstring/?from_ts='+from_ts+'&to_ts='+to_ts+'&xnr_no='+ID_Num;
public_ajax.call_request('get',word_url,wordCloud);
require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
function wordCloud(data) {
    $('#content-1-word p').show();
    if (data.length==0||isEmptyObject(data)){
        $('#content-1-word').css({textAlign:"center",lineHeight:"300px",fontSize:'24px'}).text('暂无数据');
    }else {
        var wordSeries=[];
        for (var k in data){
            wordSeries.push(
                {
                    name: k,
                    value: data[k]*200,
                    itemStyle: createRandomItemStyle()
                }
            )
        }
        require(
            [
                'echarts',
                'echarts/chart/wordCloud'
            ],
            //关键词
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById('content-1-word'));
                option = {
                    title: {
                        text: '',
                    },
                    // tooltip: {
                    //     show: true,
                    // },
                    series: [{
                        type: 'wordCloud',
                        size: ['100%', '100%'],
                        textRotation : [0, 0, 0, 0],
                        textPadding: 0,
                        autoSize: {
                            enable: true,
                            minSize: 18
                        },
                        data: wordSeries
                    }]
                };
                myChart.setOption(option);
            }
        );
    }
    $('#content-1-word p').slideUp(700);
}
//热门帖子
$('#theme-2 .demo-radio').on('click',function () {
    $('#hot_post p').show();
    var classify_id=$(this).val();
    var order_id=$('#theme-3 input:radio[name="demo"]:checked').val();
    var NEWhotPost_url='/facebook_xnr_monitor/lookup_hot_posts/?from_ts='+from_ts+'&to_ts='+to_ts+
        '&xnr_no='+ID_Num+'&classify_id='+classify_id+'&order_id='+order_id;
    public_ajax.call_request('get',NEWhotPost_url,hotPost);
});
$('#theme-3 .demo-radio').on('click',function () {
    $('#hot_post p').show();
    var classify_id=$('#theme-2 input:radio[name="demo-radio"]:checked').val();
    var order_id=$(this).val();
    var NEWhotPost_url='/facebook_xnr_monitor/lookup_hot_posts/?from_ts='+from_ts+'&to_ts='+to_ts+
        '&xnr_no='+ID_Num+'&classify_id='+classify_id+'&order_id='+order_id;
    public_ajax.call_request('get',NEWhotPost_url,hotPost);
});
var hotPost_url='/facebook_xnr_monitor/lookup_hot_posts/?from_ts='+from_ts+'&to_ts='+to_ts+
    '&xnr_no='+ID_Num+'&classify_id=0&order_id=1';
public_ajax.call_request('get',hotPost_url,hotPost);
function hotPost(data) {
    $('#hot_post').bootstrapTable('load', data);
    $('#hot_post').bootstrapTable({
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
                    var name,txt,img,txt2,all='';
                    if (row.name==''||row.name=='null'||row.name=='unknown'||!row.name){
                        name='未命名';
                    }else {
                        name=row.uid;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'||!row.photo_url){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        if (row.sensitive_words_string||!isEmptyObject(row.sensitive_words_string)){
                            var keyword=row.sensitive_words_string.split('&');
                            for (var f of keyword){
                                txt=row.text.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                            var rrr=row.text;
                            if (rrr.length>=160){
                                rrr=rrr.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                rrr=row.text;
                                all='none';
                            }
                            for (var f of keyword){
                                txt2=rrr.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                        }else {
                            txt=row.text;
                            if (txt.length>=160){
                                txt2=txt.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                txt2=txt;
                                all='none';
                            }
                        };
                    };
                    var str=
                        '<div class="post_perfect" style="margin-bottom:10px;width:920px;">'+
                        '   <div class="post_center-hot">'+
                        '       <img src="'+img+'" alt="" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>&nbsp;'+
                        '           <i class="fid" style="display: none;">'+row.fid+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                        '           <span class="time" style="font-weight: 900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(row.timestamp)+'</span>  '+
                        '           <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                        '           <p class="allall1" style="display:none;">'+txt+'</p>'+
                        '           <p class="allall2" style="display:none;">'+txt2+'</p>'+
                        '           <span class="center_2">'+txt2+'</span>'+
                        '           <div class="_translate" style="display: none;"><b style="color: #f98077;">译文：</b><span class="tsWord"></span></div>'+
                        '           <div class="center_3">'+
                        '               <span class="cen3-1" onclick="retweet(this)"><i class="icon icon-share"></i>&nbsp;&nbsp;转推</span>'+
                        '               <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论</span>'+
                        '               <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;喜欢</span>'+
                        '               <span class="cen3-4" onclick="focusThis(this)"><i class="icon icon-heart-empty"></i>&nbsp;&nbsp;关注该用户</span>'+
                        '               <span class="cen3-5" onclick="joinlab(this)"><i class="icon icon-signin"></i>&nbsp;&nbsp;加入语料库</span>'+
                        '               <span class="cen3-5" onclick="translateWord(this)"><i class="icon icon-exchange"></i>&nbsp;&nbsp;翻译</span>'+
                        '           </div>'+
                        '           <div class="commentDown" style="width: 100%;display: none;">'+
                        '               <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '               <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '           </div>'+
                        '       </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#hot_post p').slideUp(700);
    $('.hot_post .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}

//活跃用户
$('#user-1 .demo-radio').on('click',function () {
    var classify_id=$('#user-1 input:radio[name="deadio"]:checked').val();
    var NEWactivePost_url='/facebook_xnr_monitor/lookup_active_user/?xnr_no='+ID_Num+'&from_ts='+
        from_ts+'&to_ts='+to_ts+'&classify_id=0';
    public_ajax.call_request('get',NEWactivePost_url,activeUser);
});
var activePost_url='/facebook_xnr_monitor/lookup_active_user/?xnr_no='+ID_Num+'&from_ts='+
    from_ts+'&to_ts='+to_ts+'&classify_id=0';
public_ajax.call_request('get',activePost_url,activeUser);
var act_user_list=[];
function activeUser(persondata) {
    $('#userList p').show();
    $('.userList #userList').bootstrapTable('load', persondata);
    $('.userList #userList').bootstrapTable({
        data:persondata,
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
                title: "添加关注",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },
            {
                title: "头像",//标题
                field: "url",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.url==''||row.url=='null'||row.url=='unknown'||!row.url){
                        return '<img style="width: 20px;height: 20px;" src="/static/images/unknown.png"/>';
                    }else {
                        return '<img style="width: 20px;height: 20px;" src="'+row.url+'"/>';
                    };
                }
            },
            {
                title: "用户ID",//标题
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[1];
                // }
            },
            {
                title: "昵称",//标题
                field: "uname",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uname==''||row.uname=='null'||row.uname=='unknown'){
                        return '无昵称';
                    }else {
                        return row.uname;
                    };
                }
            },
            {
                title: "注册地",//标题
                field: "location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.location==''||row.location=='null'||row.location=='unknown'){
                        return '未知';
                    }else {
                        return row.location;
                    };
                }
            },
            {
                title: "粉丝数",//标题
                field: "fans_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "微博数",//标题
                field: "total_number",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.total_number==''||row.total_number=='null'||row.total_number=='unknown'||!row.total_number){
                        return '0';
                    }else {
                        return row.total_number;
                    };
                }
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.influence==''||row.influence=='null'||row.influence=='unknown'||!row.influence){
                        return '0';
                    }else {
                        return row.influence.toFixed(2);
                    };
                }
            },
            // {
            //     title: "网民详情",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return '<span style="cursor: pointer;" onclick="networkPeo(\''+row.id+'\')" ' +
            //             'title="查看详情"><i class="icon icon-link"></i></span>'
            //     },
            // },
        ],
        onCheck:function (row) {
            act_user_list.push(row.uid);_judge()
        },
        onUncheck:function (row) {
            act_user_list.removeByValue(row.uid);_judge()
        },
        onCheckAll:function (row) {
            act_user_list.push(row.uid);_judge()
        },
        onUncheckAll:function (row) {
            act_user_list.removeByValue(row.uid);_judge()
        },
    });
    $('#userList p').slideUp(700);
};
function _judge() {
    if (act_user_list.length==0){
        $('.userList .addFocus').addClass('disableCss');
    }else {
        $('.userList .addFocus').removeClass('disableCss');
    }
}
$('.userList .addFocus').on('click',function () {
    var add_url='/facebook_xnr_monitor/attach_fans_batch/?xnr_user_no_list='+ID_Num+'&fans_id_list='+act_user_list.join(',');
    public_ajax.call_request('get',add_url,postYES);
})
//-------------------颜色----------------------
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
//加入语料库  data-toggle="modal" data-target="#wordcloud"
function joinWord() {
    var create_type=$('#wordcloud input:radio[name="xnr"]:checked').val();
    var corpus_type=$('#wordcloud input:radio[name="theday"]:checked').val();
    var theme_daily_name=[],tt='';
    if (corpus_type=='主题语料'){tt=2};
    $("#wordcloud input:checkbox[name='theme"+tt+"']:checked").each(function (index,item) {
        theme_daily_name.push($(this).val());
    });
    var corpus_url='/weibo_xnr_monitor/addto_weibo_corpus/?corpus_type='+corpus_type+'&theme_daily_name='+theme_daily_name.join(',')+'&text='+text+
        '&uid='+uid+'&mid='+mid+'&retweeted='+retweeted+'&comment='+comment+'&like=0&create_type='+create_type;
    public_ajax.call_request('get',corpus_url,postYES);
}
//查看网民详情
function networkPeo(_id) {
    var detail_url='/weibo_xnr_monitor/weibo_user_detail/?user_id='+_id;
    public_ajax.call_request('get',detail_url,networkPeoDetail);
}
function networkPeoDetail(data) {

}

//评论
function showInput(_this) {
    $(_this).parents('.post_perfect').find('.commentDown').show();
};
function comMent(_this){
    var txt = $(_this).prev().val().replace(/\&/g,'%26').replace(/\#/g,'%23');
    var uid = $(_this).parents('.post_perfect').find('.uid').text();
    var fid = $(_this).parents('.post_perfect').find('.fid').text();
    if (txt!=''){
        var post_url_3='/facebook_xnr_operate/comment_operate/?tweet_type='+operateType+'&xnr_user_no='+ID_Num+
            '&text='+txt+'&r_fid='+fid+'&r_uid='+uid;
        public_ajax.call_request('get',post_url_3,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}
//转发
function retweet(_this) {
    var txt = $(_this).parent().prev().text().replace(/\&/g,'%26').replace(/\#/g,'%23');
    var uid = $(_this).parents('.post_perfect').find('.uid').text();
    var fid = $(_this).parents('.post_perfect').find('.fid').text();
    var post_url_2='/facebook_xnr_operate/retweet_operate/?tweet_type='+operateType+'&xnr_user_no='+ID_Num+
        '&text='+txt+'&r_fid='+fid+'&r_uid='+uid;
    public_ajax.call_request('get',post_url_2,postYES)
}
//点赞
function thumbs(_this) {
    var uid = $(_this).parents('.post_perfect').find('.uid').text();
    var fid = $(_this).parents('.post_perfect').find('.fid').text();
    var post_url_4='/facebook_xnr_operate/like_operate/?xnr_user_no='+ID_Num+
        '&r_fid='+fid+'&r_uid='+uid;
    public_ajax.call_request('get',post_r_s_url,postYES);
};

//关注该用户
function focusThis(_this) {
    var uid = $(_this).parents('.post_perfect').find('.uid').text();
    var post_url_6='/weibo_xnr_monitor/attach_fans_follow/?xnr_user_no='+ID_Num+'&uid='+uid;
    public_ajax.call_request('get',post_url_6,postYES)
}

//加入语料库
var wordUid,wordMid,wordTxt,wordRetweeted,wordComment;
function joinlab(_this) {
    wordMid = $(_this).parents('.post_perfect').find('.mid').text();
    wordUid = $(_this).parents('.post_perfect').find('.uid').text();
    wordTxt = $(_this).parents('.post_perfect').find('.center_2').text().replace(/\&/g,'%26').replace(/\#/g,'%23');
    wordRetweeted = $(_this).parents('.post_perfect').find('.forwarding').text();
    wordComment = $(_this).parents('.post_perfect').find('.comment').text();
    $('#wordcloud').modal('show');
}
function joinWord() {
    var create_type=$('#wordcloud input:radio[name="xnr"]:checked').val();
    var corpus_type=$('#wordcloud input:radio[name="theday"]:checked').val();
    var theme_daily_name=[],tt='11';
    if (corpus_type=='主题语料'){tt=22};
    $("#wordcloud input:checkbox[name='theme"+tt+"']:checked").each(function (index,item) {
        theme_daily_name.push($(this).val());
    });
    var corpus_url='/weibo_xnr_monitor/addto_weibo_corpus/?xnr_user_no='+ID_Num +
        '&corpus_type='+corpus_type+'&theme_daily_name='+theme_daily_name.join(',')+
        '&text='+wordTxt+ '&uid='+wordUid+'&mid='+wordMid+'&retweeted='+wordRetweeted+'&comment='+wordComment+
        '&like=0&create_type='+create_type;
    public_ajax.call_request('get',corpus_url,postYES);
}

//操作返回结果
function postYES(data) {
    var f='';
    if (data[0]||data||data[0][0]){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
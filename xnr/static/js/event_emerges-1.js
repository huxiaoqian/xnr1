var weiboUrl='/weibo_xnr_warming/show_event_warming/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',weiboUrl,weibo);
var contentList = {};
function weibo(data) {
    //console.log(data)
    $('#weiboContent').bootstrapTable('load', data);
    $('#weiboContent').bootstrapTable({
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
                    contentList['exo_'+index]=row;
                    var str=
                        '<div class="everyEvent" style="margin:0 auto 20px;text-align: left;">'+
                        '        <div class="event_center">'+
                        '            <div style="margin: 10px 0;">'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio" type="checkbox" name="demo-checkbox">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        '                </label>'+
                        '                <img src="/static/images/post-6.png" class="center_icon">'+
                        '                <a class="center_1">'+row.event_name+'</a>'+
                        '                <a class="report" onclick="oneUP(this)" style="margin-left: 50px;"><i class="icon icon-upload-alt"></i>  上报</a>'+
                        '            </div>'+
                        '            <div class="centerdetails" style="padding-left:40px;">'+
                        '                <div class="event-1">'+
                        '                    <p style="font-size: 16px;color:#01b4ff;"><i class="icon icon-bookmark"></i> 主要参与用户</p>'+
                        '                    <div class="mainJoin">'+
                        '                        <div class="mainJoinTable'+index+'"></div>'+
                        '                    </div>'+
                        '                </div>'+
                        '                <div class="event-2" style="margin: 20px 0;">'+
                        '                    <p style="font-size: 16px;color:#01b4ff;"><i class="icon icon-bookmark"></i> 相关典型微博</p>'+
                        '                    <div class="mainWeibo">'+
                        '                        <div class="mainWeiboTable'+index+'"></div>'+
                        '                    </div>'+
                        '                </div>'+
                        '            </div>'+
                        '        </div>'+
                        '    </div>';
                    return str;
                }
            },
        ],
    });
    startTable();
}
function startTable() {
    for (var k in contentList){
        var index=k.toString().charAt(k.toString().length-1);
        mainJoin(contentList['exo_'+index]['main_user_info'],index)
        mainWeibo(contentList['exo_'+index]['main_weibo_info'],index);
    }
}
function mainJoin(data,idx) {
    console.log(data)
    $('.mainJoinTable'+idx).bootstrapTable('load', data);
    $('.mainJoinTable'+idx).bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 10,//单页记录数
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
                title: "编号",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[1];
                // }
            },
            {
                title: "用户UID",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[2];
                // }
            },
            {
                title: "用户昵称",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[5];
                // },
            },
            {
                title: "关注数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "粉丝数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: '操作',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a style="cursor: pointer;" onclick="details()" title="查看详情"><i class="icon icon-edit"></i></a>';
                },
            },
        ],
    });
}
function mainWeibo(data,idx) {
    var rel_str='';
    $('.mainWeiboTable'+idx).bootstrapTable('load', data);
    $('.mainWeiboTable'+idx).bootstrapTable({
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
                    var text,time;
                    if (row.text==''||row.text=='null'||row.text=='unknown'||!row.text){
                        text='暂无内容';
                    }else {
                        text=row.text;
                    };
                    if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'||!row.timestamp){
                        time='未知';
                    }else {
                        time=getLocalTime(row.timestamp);
                    };
                    var sye_1='',sye_2='';
                    if (Number(row.sensitive) < 50){
                        sye_1='border-color: transparent transparent #131313';
                        sye_2='color: yellow';
                    }
                    rel_str+=
                        '<div class="center_rel">'+
                        '   <div class="icons" style="'+sye_1+'">'+
                        '       <i class="icon icon-warning-sign weiboFlag" style="'+sye_2+'"></i>'+
                        '   </div>'+
                        '   <a class="mid" style="display: none;">'+row.mid+'</a>'+
                        '   <a class="uid" style="display: none;">'+row.uid+'</a>'+
                        '   <a class="timestamp" style="display: none;">'+row.timestamp+'</a>'+
                        '   <span class="center_2" style="display:block;text-align:left;">'+text+'</span>'+
                        '   <div class="center_3">'+
                        '       <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                        '       <span class="cen3-2" onclick="retComLike(this)" type="get_weibohistory_retweet"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+row.retweeted+'</b>）</span>'+
                        '       <span class="cen3-3" onclick="retComLike(this)" type="get_weibohistory_comment"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+row.comment+'</b>）</span>'+
                        '       <span class="cen3-4" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '    </div>'+
                        '    <div class="commentDown" style="width: 100%;display: none;">'+
                        '        <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '        <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '    </div>'+
                        '</div>'

                    // var rel_str=
                    //     '<div class="everyEvent" style="margin: 0 auto;">'+
                    //     '        <div class="event_center">'+
                    //     '            <div style="margin: 10px 0;">'+
                    //     '                <label class="demo-label">'+
                    //     '                    <input class="demo-radio" type="checkbox" name="demo-checkbox">'+
                    //     '                    <span class="demo-checkbox demo-radioInput"></span>'+
                    //     '                </label>'+
                    //     '                <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                    //     '                <a class="center_1" href="###">'+row.user_name+'</a>'+
                    //     '                <a class="mainUID" style="display: none;">'+row.user_name+'</a>'+
                    //     '                <a onclick="oneUP(this)" class="report" style="margin-left: 50px;cursor: pointer;"><i class="icon icon-upload-alt"></i>  上报</a>'+
                    //     '            </div>'+
                    //     '           <div>'+str+'</div>'+
                    //     '        </div>'+
                    //     '    </div>';

                    return rel_str;

                }
            },
        ],
    });
};
// 转发===评论===点赞
function retComLike(_this) {
    var mid=$(_this).parents('.everySpeak').find('.mid').text();
    var middle=$(_this).attr('type');
    var opreat_url;
    if (middle=='get_weibohistory_like'){
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid;
        public_ajax.call_request('get',opreat_url,postYES);
    }else if (middle=='get_weibohistory_comment'){
        $(_this).parents('.everySpeak').find('.commentDown').show();
    }else {
        var txt=$(_this).parents('.everySpeak').find('.center_2').text();
        if (txt=='暂无内容'){txt=''};
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&text='+txt;
        public_ajax.call_request('get',opreat_url,postYES);
    }
}
function comMent(_this){
    var txt = $(_this).prev().val();
    var mid = $(_this).parents('.everySpeak').find('.mid').text();
    if (txt!=''){
        var post_url='/weibo_xnr_report_manage/get_weibohistory_comment/?text='+txt+'&xnr_user_no='+ID_Num+'&mid='+mid;
        public_ajax.call_request('get',post_url,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}

//事件预警
function oneUP() {

}
// '/weibo_xnr_warming/report_warming_content/?report_type=事件&xnr_user_no=WXNR0002' +
// '&event_name=杨振宁95岁生日恢复中国国籍&user_info=5537979196,兰德科特,100,200*3969238480,后会无期25799,88,179*3302557313,' +
// '东南老曹,600,50&weibo_info=4044828436797896,\'欢迎杨振宁先生恢复中国国籍\',1503450000,1071,250,55*4044828486221158,' +
// '\'欢迎杨振宁先生恢复中国国籍，转为中科院资深\',' +
// '1503450000,1071,250,55*4044828503513100,\'欢迎杨振宁先生恢复中国国籍，转为中科院资深\',1503450000,1071,250,55\n'
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
//查看详情
function details() {

}
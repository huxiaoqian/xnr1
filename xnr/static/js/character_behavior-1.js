// var time=Date.parse(new Date())/1000;
var weiboUrl='/weibo_xnr_warming/show_personnal_warming/?xnr_user_no='+ID_Num+'&day_time=1480176000'//+time;
public_ajax.call_request('get',weiboUrl,weibo);
function weibo(data) {
    console.log(data)
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
                field: "content",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var artical=row.content,str='';
                    $.each(artical,function (index,item) {
                        var text,time;
                        if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text){
                            text='暂无内容';
                        }else {
                            text=item.text;
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
                            '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                            '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                            '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                            '   <span class="center_2">'+text+'</span>'+
                            '   <div class="center_3">'+
                            '       <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                            '       <span class="cen3-2" onclick="retComLike(this)" type="get_weibohistory_retweet"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                            '       <span class="cen3-3" onclick="retComLike(this)" type="get_weibohistory_comment"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                            '       <span class="cen3-4" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                            '    </div>'+
                            '    <div class="commentDown" style="width: 100%;display: none;">'+
                            '        <input type="text" class="comtnt" placeholder="评论内容"/>'+
                            '        <span class="sureCom" onclick="comMent(this)">评论</span>'+
                            '    </div>'+
                            '</div>'
                    });
                    var nameuid;
                    if (row.user_name==''||row.user_name=='null'||row.user_name=='unknown'||!row.user_name){
                        nameuid=row.uid;
                    }else {
                        nameuid=row.user_name;
                    };
                    var rel_str=
                        '<div class="everyUser" style="margin: 0 auto;">'+
                        '        <div class="user_center">'+
                        '            <div style="margin: 10px 0;">'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio" type="checkbox" name="demo-checkbox">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        '                </label>'+
                        '                <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                        '                <a class="center_1" href="###">'+nameuid+'</a>'+
                        '                <a class="mainUID" style="display: none;">'+row.uid+'</a>'+
                        '                <a onclick="oneUP(this)" class="report" style="margin-left: 50px;cursor: pointer;"><i class="icon icon-upload-alt"></i>  一键上报</a>'+
                        '            </div>'+
                        '           <div>'+str+'</div>'+
                        '        </div>'+
                        '    </div>';
                    return rel_str;

                }
            },
        ],
    });
};

// 转发===评论===点赞
function retComLike(_this) {
    var mid=$(_this).parents('.center_rel').find('.mid').text();
    var middle=$(_this).attr('type');
    var opreat_url;
    if (middle=='get_weibohistory_like'){
        var uid=$(_this).parents('.center_rel').find('.uid').text();
        var timestamp=$(_this).parents('.center_rel').find('.timestamp').text();
        var text=$(_this).parents('.center_rel').find('.center_2').text();
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&uid='+uid+'&text='+text+
        '&timestamp='+timestamp+'&nick_name='+REL_name;
        public_ajax.call_request('get',opreat_url,postYES);
    }else if (middle=='get_weibohistory_comment'){
        $(_this).parents('.center_rel').find('.commentDown').show();
    }else {
        var txt=$(_this).parents('.center_rel').find('.center_2').text();
        if (txt=='暂无内容'){txt=''};
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&text='+txt;
        public_ajax.call_request('get',opreat_url,postYES);
    }
}
function comMent(_this){
    var txt = $(_this).prev().val();
    var mid = $(_this).parents('.center_rel').find('.mid').text();
    if (txt!=''){
        var post_url='/weibo_xnr_report_manage/get_weibohistory_comment/?text='+txt+'&xnr_user_no='+ID_Num+'&mid='+mid;
        public_ajax.call_request('get',post_url,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}
//一键上报
function oneUP(_this) {
    //[mid,text,timestamp,retweeted,like,comment]
    var len=$(_this).parents('.everyUser').find('.center_rel');
    var mainUID=$(_this).parents('.everyUser').find('.mainUID').text();
    var dataStr='';
    for (var i=0;i<len.length;i++){
        var alldata=[];
        var mid = $(len[i]).find('.mid').text();alldata.push(mid);
        var txt=$(len[i]).find('.center_2').text().toString().replace(/#/g,'%23');alldata.push(txt);
        var timestamp = $(len[i]).find('.timestamp').text();alldata.push(timestamp);
        var forwarding = $(len[i]).find('.forwarding').text();alldata.push(forwarding);alldata.push(0);
        var comment = $(len[i]).find('.comment').text();alldata.push(comment);
        dataStr+=alldata.join(',').toString();
        if (i!=len.length-1){dataStr+='*'}
    }
    var once_url='/weibo_xnr_warming/report_warming_content/?report_type=人物&xnr_user_no='+ID_Num+'&uid='+mainUID+
    '&weibo_info='+dataStr;
    console.log(once_url)
    public_ajax.call_request('get',once_url,postYES);
}
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

//导出文件
function exportTableToCSV(filename) {
    var str =  '';
    for (var k in currentData){
        var name='',time='',type='',user='',uid='',txt='';
        if (currentData[k].event_name==''||currentData[k].event_name=='unknown'||currentData[k].event_name=='null'){
            name='暂无';
        }else {
            name=currentData[k].event_name;
        };
        if (currentData[k].report_time==''||currentData[k].report_time=='unknown'||currentData[k].report_time=='null'){
            time='暂无';
        }else {
            time=getLocalTime(currentData[k].report_time);
        };
        if (currentData[k].report_type==''||currentData[k].report_type=='unknown'||currentData[k].report_type=='null'){
            type='暂无';
        }else {
            type=currentData[k].report_type;
        };
        if (currentData[k].uid==''||currentData[k].uid=='unknown'||currentData[k].uid=='null'){
            uid='暂无';
        }else {
            uid=currentData[k].uid;
        };
        if (currentData[k].xnr_user_no==''||currentData[k].xnr_user_no=='unknown'||currentData[k].xnr_user_no=='null'){
            user='暂无';
        }else {
            user=currentData[k].xnr_user_no;
        };
        if (currentData[k].report_content['weibo_list'].length==0){
            txt='暂无内容';
        }else {
            $.each(currentData[k].report_content['weibo_list'],function (index,item) {
                if (item.text==''||item.text=='null'||item.text=='unknown'){
                    txt='暂无内容';
                }else {
                    txt=item.text;
                };
            })
        };
        str+='上报名称：'+name+'\n上报时间：'+time+'\n上报类型：'+type+'\n虚拟人：'+user+'\n人物UID：'+uid+
            '\n'+'上报内容：'+txt+'\n\n\n';
    };

    str =  encodeURIComponent(str);
    csvData = "data:text/csv;charset=utf-8,\ufeff"+str;
    $(this).attr({
        'download': filename,
        'href': csvData,
        'target': '_blank'
    });
    // $('#pormpt p').text('素材导出成功。');
    // $('#pormpt').modal('show');
}

$("a[id='output1']").on('click', function (event) {
    filename="上报数据列表EXCEL.csv";
    exportTableToCSV.apply(this, [filename]);
});
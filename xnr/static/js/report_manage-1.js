var reportDefaul_url='/weibo_xnr_report_manage/show_report_content/'
public_ajax.call_request('get',reportDefaul_url,reportDefaul);
var currentData;
function reportDefaul(data) {
    console.log(data);
    currentData=data;
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 10,//单页记录数
        pageList: [15,25,35],//分页步进值
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
                title: "上报名称",//标题
                field: "event_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.event_name==''||row.event_name=='null'||row.event_name=='unknown'){
                        return '暂无';
                    }else {
                        return row.event_name;
                    }
                }
            },
            {
                title: "上报时间",//标题
                field: "report_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.report_time==''||row.report_time=='null'||row.report_time=='unknown'){
                        return '暂无';
                    }else {
                        return getLocalTime(row.report_time);
                    }
                }
            },
            {
                title: "上报类型",//标题
                field: "report_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.report_type==''||row.report_type=='null'||row.report_type=='unknown'){
                        return '暂无';
                    }else {
                        return row.report_type;
                    }
                }
            },
            {
                title: "虚拟人",//标题
                field: "xnr_user_no",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.xnr_user_no==''||row.xnr_user_no=='null'||row.xnr_user_no=='unknown'){
                        return '暂无';
                    }else {
                        return row.xnr_user_no;
                    }
                },
            },
            {
                title: "人物UID",//标题
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.uid==''||row.uid=='null'||row.uid=='unknown'){
                        return '暂无';
                    }else {
                        return row.uid;
                    }
                },
            },
            {
                title: '上报内容',//标题
                field: "report_content",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var repData=row.report_content['weibo_list'];
                    var str='';
                    $.each(repData,function (index,item) {
                        var txt;
                        if (item.text==''||item.text=='null'||item.text=='unknown'){
                            txt='暂无内容';
                        }else {
                            txt=item.text;
                        };
                        str+=
                            '<div class="post_center-every">'+
                            '    <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                            '    <div class="center_rel">'+
                            '        <i class="uid" style="display: none;">'+row.uid+'</i>'+
                            '        <i class="mid" style="display: none;">'+item.mid+'</i>'+
                            '        <i class="tamp" style="display: none;">'+row.report_time+'</i>'+
                            '        <i class="name" style="display: none;">'+row.event_name+'</i>'+
                            '        <span class="time" style="font-weight: 900;color: blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(item.timestamp)+'</span>'+
                            '        <span class="center_2">'+txt+
                            '        </span>'+
                            '        <div class="center_3">'+
                            '            <span class="cen3-1" onclick="retComLike(this)" type="get_weibohistory_retweet"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                            '            <span class="cen3-2" onclick="retComLike(this)" type="get_weibohistory_comment"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                            '            <span class="cen3-3" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞（<b class="praise">'+item.like+'</b>）</span>'+
                            '        </div>'+
                            '        <div class="commentDown" style="width: 100%;display: none;">'+
                            '            <input type="text" class="comtnt" placeholder="评论内容"/>'+
                            '            <span class="sureCom" onclick="comMent(this)">评论</span>'+
                            '        </div>'+
                            '    </div>'+
                            '</div>';
                    })
                    return str;
                },
            },
        ],
    });
    $('.person .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
//切换类型
$('.type2 .demo-label').on('click',function () {
    var thisType=$(this).attr('value');
    var newReport_url='/weibo_xnr_report_manage/show_report_typecontent/?report_type='+thisType;
    public_ajax.call_request('get',newReport_url,reportDefaul);
});
//转发===评论===点赞
function retComLike(_this) {
    var mid=$(_this).parents('.post_center-every').find('.mid').text();
    var txt=$(_this).parents('.post_center-every').find('.center_2').text();
    var middle=$(_this).attr('type');
    if (txt=='暂无内容'){txt=''};
    var opreat_url;
    if (middle=='get_weibohistory_like'){
        var uid=$(_this).parents('.post_center-every').find('.uid').text();
        var tamp=$(_this).parents('.post_center-every').find('.tamp').text();
        var nickName=$(_this).parents('.post_center-every').find('.name').text();
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+
        '&uid='+uid+'&nick_name='+nickName+'&text='+txt+'&timestamp='+tamp;
    }else {
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&text='+txt;
    }
    public_ajax.call_request('get',opreat_url,postYES);
}

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
//导出文件
function exportTableToCSV(filename) {
    var str =  '';
    $.each(currentData,function (index,item) {
        
    })
    str =  encodeURIComponent(str);
    csvData = "data:text/csv;charset=utf-8,\ufeff"+str;
    $(this).attr({
        'download': filename,
        'href': csvData,
        'target': '_blank'
    });
    $('#pormpt p').text('素材导出成功。');
    $('#pormpt').modal('show');
}

$("a[id='output']").on('click', function (event) {
    filename="上报数据列表EXCEL.csv";
    exportTableToCSV.apply(this, [filename]);
});



var reportDefaul_url;
console.log(flagType)
if(flagType == 3){//微信
    weiboORqq('WX');
    console.log(ID_Num);
    reportDefaul_url = '/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period=30';
    public_ajax.call_request('get',reportDefaul_url,WXreportDefaul);
}else if(flagType == 1){//微博
    weiboORqq('weibo');
    console.log(ID_Num);
    reportDefaul_url='/weibo_xnr_report_manage/show_report_content/';
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}else if(flagType == 2){//QQ
    weiboORqq('QQ');
    console.log(ID_Num);
    var start_ts=getDaysBefore(7);
    var end_ts= todayTimetamp();
    reportDefaul_url='/qq_xnr_report_manage/show_report_content/?qq_xnr_no='+ID_Num+'&report_type=content&start_ts='+start_ts+'&end_ts='+end_ts;
    console.log(reportDefaul_url)
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}

// var reportDefaul_url='/weibo_xnr_report_manage/show_report_content/';
// public_ajax.call_request('get',reportDefaul_url,reportDefaul);
var currentData={},wordCurrentData={},currentDataPrival={};
function reportDefaul(data) {
    console.log(data)
    $.each(data,function (index,item) {
        currentDataPrival[item.report_time]=item;
    });
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var artical=row.report_content.weibo_list,str='';
                    $.each(artical,function (index,item) {
                        var text,time;
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
                            }else {
                                text=item.text;
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
                            '<div class="center_rel" style="margin-bottom: 10px;background:#06162d;padding: 5px 10px;">'+
                            '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                            // '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                            '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                            '   <span class="center_2">'+text+'</span>'+
                            '   <div class="center_3">'+
                            '       <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                            '       <span class="cen3-2"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                            '       <span class="cen3-3"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                            '       <span class="cen3-4"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                            '    </div>'+
                            '</div>'
                    });
                    var nameuid,time,report_type,xnr;
                    if (row.event_name==''||row.event_name=='null'||row.event_name=='unknown'){
                        nameuid = row.uid;
                    }else {
                        nameuid = row.event_name;
                    };
                    if (row.report_time==''||row.report_time=='null'||row.report_time=='unknown'){
                        time = '未知';
                    }else {
                        time = getLocalTime(row.report_time);
                    };
                    if (row.report_type==''||row.report_type=='null'||row.report_type=='unknown'){
                        report_type = '暂无';
                    }else {
                        report_type = row.report_type;
                    };
                    if (row.xnr_user_no==''||row.xnr_user_no=='null'||row.xnr_user_no=='unknown'){
                        xnr = '暂无';
                    }else {
                        xnr = row.xnr_user_no;
                    }
                    var rel_str=
                        '<div class="post_center-every" style="margin: 10px auto 0;text-align: left;">'+
                        '        <div class="user_center">'+
                        '            <div style="margin: 10px 0;">'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio" YesNo="0" type="checkbox" name="printData" value="'+row.report_time+'" onclick="chooseNo(this)">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        '                </label>'+
                        '                <img src="/static/images/post-6.png" class="center_icon">'+
                        '                <a class="ID" style="display: none;">'+row.report_time+'</a>'+
                        '                <a class="center_1">上报名称：'+nameuid+'</a>&nbsp;&nbsp;'+
                        '                <a class="center_1">上报时间：'+time+'</a>&nbsp;&nbsp;'+
                        '                <a class="center_1">上报类型：'+report_type+'</a>&nbsp;&nbsp;'+
                        '                <a class="center_1">虚拟人：'+xnr+'</a>'+
                        '                <a class="mainUID" style="display: none;">'+row.uid+'</a>'+
                        '            </div>'+
                        '           <div class="weiboContent">'+str+'</div>'+
                        '        </div>'+
                        '    </div>';
                    return rel_str;
                }
            },
        ],
        onPageChange:function (number, size) {
            var ft=$('.filesList .everyCopy');
            for(var a=0;a<ft.length;a++){
                var b=$(ft[a]).find('i').attr('pointIds');
                var tt=$("#person input[type='checkbox'][value='"+b+"']");
                $(tt[0]).prop('checked', true);
                $(tt[0]).attr('YesNo','1');
            }
        }
    });
    $('.person .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
// 复制了一份上面的函数给微信
function WXreportDefaul(data) {
    console.log(data)
    $.each(data,function (index,item) {
        currentDataPrival[item.report_time]=item;
    });
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    /*var artical=row.report_content.weibo_list,str='';
                    $.each(artical,function (index,item) {
                        var text,time;
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
                            }else {
                                text=item.text;
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
                            '<div class="center_rel" style="margin-bottom: 10px;background:#06162d;padding: 5px 10px;">'+
                            '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                            // '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                            '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                            '   <span class="center_2">'+text+'</span>'+
                            // '   <div class="center_3">'+
                            // '       <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                            // '       <span class="cen3-2"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                            // '       <span class="cen3-3"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                            // '       <span class="cen3-4"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                            // '    </div>'+
                            '</div>'
                    });
                    */
                    var text = row.report_content;
                    var str =
                        '<div class="center_rel" style="margin-bottom: 10px;background:#06162d;padding: 5px 10px;">'+
                        // '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                        // '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                        // '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                        '   <span class="center_2">'+text+'</span>'+
                        // '   <div class="center_3">'+
                        // '       <span class="cen3-1"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                        // '       <span class="cen3-2"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                        // '       <span class="cen3-3"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                        // '       <span class="cen3-4"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        // '    </div>'+
                        '</div>';

                    var nameuid,time,report_type,xnr;
                    // if (row.event_name==''||row.event_name=='null'||row.event_name=='unknown'){
                    //     nameuid = row.uid;
                    // }else {
                    //     nameuid = row.event_name;
                    // };
                    nameuid='未知';//上报名称暂时设为未知。。。11-17


                    if (row.report_time==''||row.report_time=='null'||row.report_time=='unknown'){
                        time = '未知';
                    }else {
                        time = getLocalTime(row.report_time);
                    };
                    if (row.report_type==''||row.report_type=='null'||row.report_type=='unknown'){
                        report_type = '暂无';
                    }else {
                        report_type = row.report_type;
                    };
                    if (row.xnr_user_no==''||row.xnr_user_no=='null'||row.xnr_user_no=='unknown'){
                        xnr = '暂无';
                    }else {
                        xnr = row.xnr_user_no;
                    }
                    var rel_str=
                        '<div class="post_center-every" style="margin: 10px auto 0;text-align: left;">'+
                        '        <div class="user_center">'+
                        '            <div style="margin: 10px 0;">'+
                        '                <label class="demo-label">'+
                        '                    <input class="demo-radio" YesNo="0" type="checkbox" name="printData" value="'+row.report_time+'" onclick="chooseNo(this)">'+
                        '                    <span class="demo-checkbox demo-radioInput"></span>'+
                        '                </label>'+
                        '                <img src="/static/images/post-6.png" class="center_icon">'+
                        '                <a class="ID" style="display: none;">'+row.report_time+'</a>'+
                        '                <a class="center_1">上报名称：'+nameuid+'</a>&nbsp;&nbsp;'+
                        '                <a class="center_1">上报时间：'+time+'</a>&nbsp;&nbsp;'+
                        '                <a class="center_1">上报类型：'+report_type+'</a>&nbsp;&nbsp;'+
                        '                <a class="center_1">虚拟人：'+xnr+'</a>'+
                        '                <a class="mainUID" style="display: none;">'+row.uid+'</a>'+
                        '            </div>'+
                        '           <div class="weiboContent">'+str+'</div>'+
                        '        </div>'+
                        '    </div>';
                    return rel_str;
                }
            },
        ],
        onPageChange:function (number, size) {
            var ft=$('.filesList .everyCopy');
            for(var a=0;a<ft.length;a++){
                var b=$(ft[a]).find('i').attr('pointIds');
                var tt=$("#person input[type='checkbox'][value='"+b+"']");
                $(tt[0]).prop('checked', true);
                $(tt[0]).attr('YesNo','1');
            }
        }
    });
    $('.person .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
//=========

var $this_point;
function chooseNo(_this) {
    $this_point=_this;
    var yesNO=$(_this).attr('YesNo'),_id=$(_this).parents('.post_center-every').find('.ID').text();
    $('.filesList').show();
    if (yesNO==0){
        currentData[_id]=currentDataPrival[_id];
        wordCurrentData[_id]=$(_this).parents('.post_center-every').parents('tr')[0];
        var dataIndex=$(_this).parents('.post_center-every').parent().parent().attr('data-index');
        var $Index=Number(dataIndex)+1;
        var t='<span class="everyCopy">第 '+($Index)+' 条数据&nbsp;&nbsp;<i class="icon icon-remove" style="cursor: pointer;" ' +
            'pointIds="'+_id+'" onclick="deltPointData(this)"></i></span>';
        $('.filesName').append(t);
        $(_this).attr('YesNo','1');
    }else {
        delete currentData[_id];
        delete wordCurrentData[_id];
        $(_this).attr('YesNo','0');
        var ft=$('.filesList .everyCopy');
        for(var a=0;a<ft.length;a++){
            var b=$(ft[a]).find('i').attr('pointIds');
            if (_id==b){
                $(ft[a]).remove();
                $(_this).attr('YesNo','0');
            }
        }
    }
}
function deltPointData(_this) {
    var pointID=$(_this).attr('pointIds');
    $(_this).parent().remove();
    delete currentData[pointID];
    delete wordCurrentData[pointID];
    $($this_point).attr('YesNo','0');
    var tt=$("input[type='checkbox'][value='"+pointID+"']");
    $(tt[0]).prop('checked', false);
    var h=$('.filesList .everyCopy').length;
    if (h==0){$('.filesList').hide()}
}
//切换类型
var types=[];
$('.type2 .demo-label').on('click',function () {
    var thisType=$(this).attr('value');
    $(".type2 input:checkbox:checked").each(function (index,item) {
        types.push($(this).val());
    });
    var newReport_url='/weibo_xnr_report_manage/show_report_typecontent/?report_type='+thisType;
    public_ajax.call_request('get',newReport_url,reportDefaul);
});

//转发===评论===点赞
// function retComLike(_this) {
//     var mid=$(_this).parents('.post_center-every').find('.mid').text();
//     var middle=$(_this).attr('type');
//     var opreat_url;
//     if (middle=='get_weibohistory_like'){
//         opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid;
//         public_ajax.call_request('get',opreat_url,postYES);
//     }else if (middle=='get_weibohistory_comment'){
//         $(_this).parents('.post_center-every').find('.commentDown').show();
//     }else {
//         var txt=$(_this).parents('.post_center-every').find('.center_2').text();
//         if (txt=='暂无内容'){txt=''};
//         opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&text='+txt;
//         public_ajax.call_request('get',opreat_url,postYES);
//     }
// }
// function comMent(_this){
//     var txt = $(_this).prev().val();
//     var mid = $(_this).parents('.post_center-every').find('.mid').text();
//     if (txt!=''){
//         var post_url='/weibo_xnr_report_manage/get_weibohistory_comment/?text='+txt+'&xnr_user_no='+ID_Num+'&mid='+mid;
//         public_ajax.call_request('get',post_url,postYES)
//     }else {
//         $('#pormpt p').text('评论内容不能为空。');
//         $('#pormpt').modal('show');
//     }
// }

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
//导出excel
$('#output1').click(function(){
    var all=[];
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
                txt+=item.text;
            });
        };
        all.push(
            [
                {"value":name, "type":"ROW_HEADER"},
                {"value":time, "type":"ROW_HEADER"},
                {"value":type, "type":"ROW_HEADER"},
                {"value":user, "type":"ROW_HEADER"},
                {"value":uid, "type":"ROW_HEADER"},
                {"value":txt, "type":"ROW_HEADER"},
            ]
        )
    };

    var data = {
        "title":[
            {"value":"上报名称", "type":"ROW_HEADER_HEADER", "datatype":"string"},
            {"value":"上报时间", "type":"ROW_HEADER_HEADER", "datatype":"string"},
            {"value":"上报类型", "type":"ROW_HEADER_HEADER", "datatype":"string"},
            {"value":"虚拟人", "type":"ROW_HEADER_HEADER", "datatype":"string"},
            {"value":"人物UID", "type":"ROW_HEADER_HEADER", "datatype":"string"},
            {"value":"上报内容", "type":"ROW_HEADER_HEADER", "datatype":"string"},
        ],
        "data":all
    };
    if(data == '')
        return;
    JSONToExcelConvertor(data.data, "Report", data.title);
});

function JSONToExcelConvertor(JSONData, FileName, ShowLabel) {
    //先转化json
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

    var excel = '<table>';

    //设置表头
    var row = "<tr>";
    for (var i = 0, l = ShowLabel.length; i < l; i++) {
        row += "<td>" + ShowLabel[i].value + '</td>';
    }

    //换行
    excel += row + "</tr>";

    //设置数据
    for (var i = 0; i < arrData.length; i++) {
        var row = "<tr>";
        for (var index in arrData[i]) {
            var value = arrData[i][index].value === "." ? "" : arrData[i][index].value;
            if (value){
                row += '<td>' + value + '</td>';
            }
        }

        excel += row + "</tr>";
    }

    excel += "</table>";

    var excelFile = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:x='urn:schemas-microsoft-com:office:excel' xmlns='http://www.w3.org/TR/REC-html40'>";
    excelFile += '<meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8">';
    excelFile += '<meta http-equiv="content-type" content="application/vnd.ms-excel';
    excelFile += '; charset=UTF-8">';
    excelFile += "<head>";
    excelFile += "<!--[if gte mso 9]>";
    excelFile += "<xml>";
    excelFile += "<x:ExcelWorkbook>";
    excelFile += "<x:ExcelWorksheets>";
    excelFile += "<x:ExcelWorksheet>";
    excelFile += "<x:Name>";
    excelFile += "{worksheet}";
    excelFile += "</x:Name>";
    excelFile += "<x:WorksheetOptions>";
    excelFile += "<x:DisplayGridlines/>";
    excelFile += "</x:WorksheetOptions>";
    excelFile += "</x:ExcelWorksheet>";
    excelFile += "</x:ExcelWorksheets>";
    excelFile += "</x:ExcelWorkbook>";
    excelFile += "</xml>";
    excelFile += "<![endif]-->";
    excelFile += "</head>";
    excelFile += "<body>";
    excelFile += excel;
    excelFile += "</body>";
    excelFile += "</html>";


    var uri = 'data:application/vnd.ms-excel;charset=utf-8,' + encodeURIComponent(excelFile);

    var link = document.createElement("a");
    link.href = uri;

    link.style = "visibility:hidden";
    link.download = FileName + ".xls";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
//导出word
$('#output2').on('click',function () {
    tableExport('person', 'Report', 'doc');
});




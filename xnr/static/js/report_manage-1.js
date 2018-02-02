var reportDefaul_url;
var time2=Date.parse(new Date())/1000;
if(flagType == 3){
    //微信
    //===============时间搜索添加11---21 ===============
    var choosetimeStr = '<div class="choosetime" style="margin: 10px 0;">'
        +'<label class="demo-label">'
            +'<input class="demo-radio" type="radio" name="time1" value="0">'
            +'<span class="demo-checkbox demo-radioInput"></span> 今天'
        +'</label>'
        +'<label class="demo-label">'
            +'<input class="demo-radio" type="radio" name="time1" value="1">'
            +'<span class="demo-checkbox demo-radioInput"></span> 昨天'
        +'</label>'
        +'<label class="demo-label">'
            +'<input class="demo-radio" type="radio" name="time1" value="7" checked>'
            +'<span class="demo-checkbox demo-radioInput"></span> 7天'
        +'</label>'
        +'<label class="demo-label">'
           +'<input class="demo-radio" type="radio" name="time1" value="30">'
            +'<span class="demo-checkbox demo-radioInput"></span> 30天'
        +'</label>'
        +'<label class="demo-label">'
            +'<input class="demo-radio" type="radio" name="time1" value="mize">'
            +'<span class="demo-checkbox demo-radioInput"></span> 自定义'
        +'</label>'
        +'<input type="text" size="16" id="start_1" class="form_datetime" placeholder="开始时间"'
               +'style="display:none;height: 20px;font-size: 10px;color: white;text-align: center;'
                        +'padding:2px 4px;border: 1px solid silver;background: rgba(8,23,44,0.25);">'
        +'<input type="text" size="16" id="end_1" class="form_datetime" placeholder="结束时间"'
               +'style="display:none;height: 20px;font-size: 10px;color: white;text-align: center;'
                        +'padding:2px 4px;border: 1px solid silver;background: rgba(8,23,44,0.25);">'
        +'<span id="sure" class="sureTime">确定</span>'
    +'</div>';
    $('#container .title').after(choosetimeStr)

    // 时间选项
    $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd",
        minView:2, //控制时分秒
        autoclose: true,
        todayBtn: true,
        pickerPosition: "bottom-left"
    });
    $('.choosetime .demo-label input').on('click',function () {
        var _val=$(this).val();
        if (_val=='mize'){
            $('#start_1').show();
            $('#end_1').show();
            $('.sureTime').show();
        }else {
            $('#start_1').hide();
            $('#end_1').hide();
            $('.sureTime').hide();
            reportDefaul_url = '/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period='+_val;
            public_ajax.call_request('get',reportDefaul_url,WXreportDefaul);
        }
    });
    // 确定时间搜索
    $('.sureTime').on('click',function () {
        var s=$('#start_1').val();
        var d=$('#end_1').val();
        if (s==''||d==''){
            $('#pormpt p').text('请检查时间，不能为空。');
            $('#pormpt').modal('show');
        }else {
            reportDefaul_url = '/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&startdate='+s+'&enddate='+d;
        }
    });
    weiboORqq('WX');
    reportDefaul_url = '/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period=7';
    public_ajax.call_request('get',reportDefaul_url,WXreportDefaul);
}else if(flagType == 1){//微博
    weiboORqq('weibo');
    reportDefaul_url='/weibo_xnr_report_manage/show_reportcontent_new/?report_type=人物,言论,事件,时间&start_time='+todayTimetamp()+'&end_time='+time2;
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}else if(flagType == 2){//QQ
    weiboORqq('QQ');
    var start_ts=getDaysBefore(7);
    var end_ts= todayTimetamp();
    reportDefaul_url='/qq_xnr_report_manage/show_reportcontent_new/?qq_xnr_no='+ID_Num+'&report_type=content&start_ts='+start_ts+'&end_ts='+end_ts;
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}
// var reportDefaul_url='/weibo_xnr_report_manage/show_report_content/';
// public_ajax.call_request('get',reportDefaul_url,reportDefaul);
var currentData={},wordCurrentData={},currentDataPrival={};
function reportDefaul(data) {
    $.each(data,function (index,item) {
        currentDataPrival[item.report_time]=item;
    });
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
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
                    if (artical.length==0){
                        str='<div style="text-align:center;margin: 10px 0;background:#06162d;padding: 10px 0;">暂无内容</div>';
                    }else {
                        $.each(artical,function (index,item) {
                            var text,time,name,img,row,text2,all;
                            if (item.nick_name==''||item.nick_name=='null'||item.nick_name=='unknown'||!item.nick_name){
                                name=item.uid||'未命名';
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
                                    if (txt.length>=160){
                                        text2=txt.substring(0,160)+'...';
                                        all='inline-block';
                                    }else {
                                        text2=txt;
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
                                '<div class="center_rel" style="margin-bottom: 10px;background:#06162d;padding: 5px 10px;">'+
                                '   <img src="'+img+'" alt="" class="center_icon">'+
                                '   <a class="center_1" style="color:#f98077;">'+name+'</a>'+
                                '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                                // '   <a class="uid" style="display: none;">'+item.uid+'</a>'+
                                '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                '   <span class="cen3-1" style="color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>'+
                                '   <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                                '   <p class="allall1" style="display:none;">'+text+'</p>'+
                                '   <p class="allall2" style="display:none;">'+text2+'</p>'+
                                '   <span class="center_2">'+text2+'</span>'+
                                // '   <div class="center_3">'+
                                // '       <span class="cen3-2"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                                // '       <span class="cen3-3"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                                // '       <span class="cen3-4"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                                // '    </div>'+
                                '</div>'
                        });
                    }
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
                        '<div class="post_center-every" style="text-align: left;">'+
                        '        <div class="user_center">'+
                        '            <div>'+
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
    $('.personContent p').slideUp(300);
    $('.person').show();
}
// 复制了一份上面的函数给微信
function WXreportDefaul(data) {
    $.each(data,function (index,item) {
        currentDataPrival[item.report_time]=item;
    });
    $('#person').bootstrapTable('load', data);
    $('#person').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
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
                    var text = row.report_content;
                    var str =
                        '<div class="center_rel" style="margin-bottom: 10px;background:#06162d;padding: 5px 10px;">'+
                        '   <span class="center_2">'+text+'</span>'+
                        '</div>';

                    var nameuid,time,report_type,xnr;
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
                        '<div class="post_center-every" style="text-align: left;">'+
                        '        <div class="user_center">'+
                        '            <div>'+
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
    $('.personContent p').slideUp(300);
    $('.person').show();
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

$('.type2 .demo-label').on('click',function () {
    $('.person p').show();
    var types=[];
    $(".type2 input:checkbox:checked").each(function (index,item) {
        types.push($(this).val());
    });
    var time=$('.choosetime input:radio[name="time"]:checked').val();
    var time1=getDaysBefore(time);
    if (time=='mize'){
        var s=$('.choosetime').find('#start').val();
        var d=$('.choosetime').find('#end').val();
        if (s==''||d==''){
            $('#pormpt p').text('时间不能为空。');
            $('#pormpt').modal('show');
            return false;
        }else {
            time1=(Date.parse(new Date(s))/1000);
            time2=(Date.parse(new Date(d))/1000);
        }
    }
    $('.personContent p').show();
    $('.person').hide();
    var newReport_url='/weibo_xnr_report_manage/show_reportcontent_new/?report_type='+types.join(',')+
        '&start_time='+time1+'&end_time='+time2;
    public_ajax.call_request('get',newReport_url,reportDefaul);
});
//时间选择
$('.choosetime .demo-label input').on('click',function () {
    var _val = $(this).val();
    if (_val == 'mize') {
        $(this).parents('.choosetime').find('#start').show();
        $(this).parents('.choosetime').find('#end').show();
        $(this).parents('.choosetime').find('#sure').css({display: 'inline-block'});
    } else {
        $('.personContent p').show();
        $('.person').hide();
        var valCH=[];
        $(".type2 input:checkbox:checked").each(function (index,item) {
            valCH.push($(this).val());
        });
        $(this).parents('.choosetime').find('#start').hide();
        $(this).parents('.choosetime').find('#end').hide();
        $(this).parents('.choosetime').find('#sure').hide();
        var weiboUrl='/weibo_xnr_report_manage/show_reportcontent_new/?report_type='+valCH.join(',')+'&start_time='+getDaysBefore(_val)+'&end_time='+time2;
        public_ajax.call_request('get',weiboUrl,reportDefaul);
    }//show_reportcontent_new
});
$('#sure').on('click',function () {
    $('.personContent p').show();
    $('.person').hide();
    var valCH=[];
    $(".type2 input:checkbox:checked").each(function (index,item) {
        valCH.push($(this).val());
    });
    var s=$(this).parents('.choosetime').find('#start').val();
    var d=$(this).parents('.choosetime').find('#end').val();
    if (s==''||d==''){
        $('#pormpt p').text('时间不能为空。');
        $('#pormpt').modal('show');
    }else {
        var weiboUrl='/weibo_xnr_report_manage/show_reportcontent_new/?report_type='+valCH.join(',')+
            '&start_time='+(Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        public_ajax.call_request('get',weiboUrl,reportDefaul);
    }
});

//导出excel
$('#output1').click(function(){
    outputFun($(this).attr('type'));
});
//导出word
$('#output2').on('click',function () {
    outputFun($(this).attr('type'));
});
function outputFun(_type) {
    var _ids=[],times=[];
    for(var k in currentData){
        _ids.push(currentData[k]['_id']);
        times.push(k);
    }
    $('#loadingDown .downInfo').show();
    $('#loadingDown').modal('show');
    var output_url='/weibo_xnr_report_manage/output_excel_word/?id_list='+_ids.join(',')+
        '&out_type='+_type+'&report_timelist='+times.join(',');
    public_ajax.call_request('get',output_url,outputRead);
}
function outputRead(data) {
    $('#loadingDown .downInfo').hide();
    $('#loadingDown').modal('hide');
    var path=data.substring(3);
    var a = document.getElementById("downFile");
    a.href=path;
    a.download=data.substring(15);
    a.click();
}






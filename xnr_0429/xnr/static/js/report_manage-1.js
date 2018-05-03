var reportDefaul_url,beginUrl;
var time2=Date.parse(new Date())/1000;
if(flagType == 1){//微博
    beginUrl='weibo_xnr_report_manage';
    weiboORqq('weibo');
    reportDefaul_url='/weibo_xnr_report_manage/show_reportcontent_new/?report_type=人物,言论,事件,时间&start_time='+todayTimetamp()+'&end_time='+time2;
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}else if(flagType == 2){//QQ
    weiboORqq('QQ');
    $('.qqHide').hide();
    var start_ts=getDaysBefore(7);
    var end_ts= todayTimetamp();
    reportDefaul_url='/qq_xnr_report_manage/show_report_content/?qq_xnr_no='+ID_Num+'&report_type=人物,言论&start_ts='+start_ts+'&end_ts='+end_ts;
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}else if(flagType == 3){
    weiboORqq('WX');
    reportDefaul_url ='/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period=0';
    public_ajax.call_request('get',reportDefaul_url,WXreportDefaul);
}else if (flagType == 4){
    beginUrl='facebook_xnr_report_manage';
    weiboORqq('faceBook');
    var start_ts=getDaysBefore(7);
    var end_ts= todayTimetamp();
    reportDefaul_url='/facebook_xnr_report_manage/show_report_content/?report_type=人物,言论,事件,时间&start_time='+todayTimetamp()+'&end_time='+end_ts;
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
}else if (flagType == 5){
    beginUrl='twitter_xnr_report_manage';
    weiboORqq('twitter');
    var start_ts=getDaysBefore(7);
    var end_ts= todayTimetamp();
    reportDefaul_url='/twitter_xnr_report_manage/show_report_content/?report_type=人物,言论,事件,时间&start_time='+todayTimetamp()+'&end_time='+end_ts;
    public_ajax.call_request('get',reportDefaul_url,reportDefaul);
};
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
                    var artical=(row.report_content.weibo_list||JSON.parse(row.report_content)),str='';
                    if (artical.length==0||artical==''){
                        str='<div style="text-align:center;margin: 10px 0;background:#06162d;padding: 10px 0;">暂无内容</div>';
                    }else {
                        $.each(artical,function (index,item) {
                            var text,time,name,img,row,text2,all;
                            if (item.nick_name==''||item.nick_name=='null'||item.nick_name=='unknown'||
                                item.qq_group_nickname==''||item.qq_group_nickname=='null'||item.qq_group_nickname=='unknown'){
                                name=item.uid||item.qq_group_number||'未命名';
                            }else {
                                name=item.nick_name||item.qq_group_nickname;
                            };
                            if (item.photo_url==''||item.photo_url=='null'||item.photo_url=='unknown'||!item.photo_url){
                                img='/static/images/unknown.png';
                            }else {
                                img=item.photo_url;
                            };
                            if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text||item.text.length==0){
                                text='暂无内容';
                            }else {
                                if(!(item.text instanceof Object)){
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
                                    if (item.timestamp==''||item.timestamp=='null'||item.timestamp=='unknown'){
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
                                        // '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                                        // '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                        '   <span class="cen3-1" style="color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;'+time+'</span>'+
                                        '   <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                                        '   <p class="allall1" style="display:none;">'+text+'</p>'+
                                        '   <p class="allall2" style="display:none;">'+text2+'</p>'+
                                        '   <span class="center_2">'+text2+'</span>'+
                                        '</div>';
                                }else {
                                    if(!name){
                                        name=Object.values(item.qq_groups)[0];
                                    }
                                    var relTxt=item.text.text;
                                    var text,time,text2;
                                    $.each(relTxt,function (index,item) {
                                        if (item[2]){
                                            var s=item[0];
                                            var keywords=item[2];
                                            s=s.toString().replace(new RegExp(keywords,'g'),'<b style="color:#ef3e3e;">'+keywords+'</b>');
                                            text=s;

                                            var rrr=item[0];
                                            if (rrr.length>=160){
                                                rrr=rrr.substring(0,160)+'...';
                                                all='inline-block';
                                            }else {
                                                rrr=item[0];
                                                all='none';
                                            }
                                            rrr=rrr.toString().replace(new RegExp(keywords,'g'),'<b style="color:#ef3e3e;">'+keywords+'</b>');
                                            text2=rrr;
                                        }else {
                                            text=item[0];
                                            if (text.length>=160){
                                                text2=text.substring(0,160)+'...';
                                                all='inline-block';
                                            }else {
                                                text2=text;
                                                all='none';
                                            }
                                        };
                                        if (item[1]==''||item[1]=='null'||item[1]=='unknown'){
                                            time='未知';
                                        }else {
                                            time=getLocalTime(item[1]);
                                        };
                                        str+=
                                            '<div class="center_rel" style="margin-bottom: 10px;background:#06162d;padding: 5px 10px;">'+
                                            '   <img src="'+img+'" alt="" class="center_icon">'+
                                            '   <a class="center_1" style="color:#f98077;">'+name+'</a>'+
                                            // '   <a class="mid" style="display: none;">'+item.mid+'</a>'+
                                            // '   <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                                            '   <span class="cen3-1" style="color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;'+time+'</span>'+
                                            '   <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                                            '   <p class="allall1" style="display:none;">'+text+'</p>'+
                                            '   <p class="allall2" style="display:none;">'+text2+'</p>'+
                                            '   <span class="center_2">'+text2+'</span>'+
                                            '</div>';
                                    })
                                }
                            };

                        });
                    }
                    var nameuid,time,report_type,xnr;
                    if (row.event_name==''||row.event_name=='null'||row.event_name=='unknown'||
                        row.qq_nickname==''||row.qq_nickname=='null'||row.qq_nickname=='unknown'){
                        nameuid = row.uid||row.qq_number||'未知';
                    }else {
                        nameuid = row.event_name||row.qq_nickname||'未知';
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
    var newReport_url;
    if (flagType==1||flagType==4||flagType==5){
        newReport_url='/'+beginUrl+'/show_reportcontent_new/?report_type='+types.join(',')+
            '&start_time='+time1+'&end_time='+time2;
    }else if(flagType==2){
        newReport_url='/qq_xnr_report_manage/show_report_content/?qq_xnr_no='+ID_Num+
            '&report_type='+types.join(',')+'&start_ts='+time1+'&end_ts='+time2;
    }else if(flagType==3){
        newReport_url='/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period=7';
        public_ajax.call_request('get',newReport_url,WXreportDefaul);
        return false;
    }
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
        var weiboUrl;
        if (flagType==1||flagType==4||flagType==5){
            weiboUrl='/'+beginUrl+'/show_reportcontent_new/?report_type='+valCH.join(',')+
                '&start_time='+getDaysBefore(_val)+'&end_time='+time2;
        }else if(flagType==2){
            weiboUrl='/qq_xnr_report_manage/show_report_content/?qq_xnr_no='+ID_Num+
                '&report_type='+valCH.join(',')+'&start_ts='+getDaysBefore(_val)+'&end_ts='+time2;
        }else if(flagType==3){
            newReport_url='/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period='+_val;
            public_ajax.call_request('get',newReport_url,WXreportDefaul);
            return false;
        }
        public_ajax.call_request('get',weiboUrl,reportDefaul);
    }
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
        var weiboUrl;
        if (flagType==1||flagType==4||flagType==5){
            weiboUrl='/'+beginUrl+'/show_reportcontent_new/?report_type='+valCH.join(',')+
                '&start_time='+(Date.parse(new Date(s))/1000)+'&end_time='+(Date.parse(new Date(d))/1000);
        }else if(flagType==2){
            weiboUrl='/qq_xnr_report_manage/show_report_content/?qq_xnr_no='+ID_Num+
                '&report_type='+valCH.join(',')+'&start_ts='+(Date.parse(new Date(s))/1000)+
                '&end_ts='+(Date.parse(new Date(d))/1000);
        }else if(flagType==3){
            weiboUrl='/wx_xnr_report_manage/show_report_content/?wxbot_id='+ID_Num+'&report_type=content&period='+_val;
            public_ajax.call_request('get',weiboUrl,WXreportDefaul);
            return false;
        }
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






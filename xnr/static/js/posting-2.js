// ===智能发帖
$('.point-view-2').on('focus',function () {
    var a=$('.point-view-1').val();
    $(this).val(a);
});
var chooseThisIntel='no',chooseThisIntelID='';
$('#intell_type .intel_1').on('click',function () {
    if (chooseThisIntel!='yes'){
        $('#pormpt p').text('请选择下方的一个事件再进行操作。');
        $('#pormpt').modal('show');
    }
})
$('#intell_type .intel_1 input').on('click',function () {
    var _val1=$(this).val();
    if (_val1=='double'){
        $('#intell_type .intelDownType').hide();
        $('#intell_type .intel_3').show();
        var val3=$('#intell_type .intel_3 input[name="intel3"]:checked').val();
        if (val3){
            var intelPostUrl='/intelligent_writing/model_text/?task_id='+chooseThisIntelID+
                '&model_type='+_val1+'&text_type='+val3;
            public_ajax.call_request('get',intelPostUrl,intelPostWord);
        }
    }else {
        $('#intell_type .intelDownType').hide();
        $('#intell_type .intel_2').show();
        var val12=$('#intell_type .intel_2 input[name="intel2"]:checked').val();
        if (val12){
            var intelPostUrl='/intelligent_writing/model_text/?task_id='+chooseThisIntelID+
                '&model_type='+_val1+'&text_type='+val12;
            public_ajax.call_request('get',intelPostUrl,intelPostWord);
        }
    }
});
$('#intell_type .intelDownType input').on('click',function () {
    var argument1=$('#intell_type .intel_1 input[name="intel1"]:checked').val();
    var argument2=$(this).val();
    // var intelPostUrl='/intelligent_writing/model_text/?task_id=twitter_txnr0001_ce_shi_ren_wu___0_2_2_8'+
    //     '&model_type='+argument1+'&text_type='+argument2;
    var intelPostUrl='/intelligent_writing/model_text/?task_id='+chooseThisIntelID+
        '&model_type='+argument1+'&text_type='+argument2;
    public_ajax.call_request('get',intelPostUrl,intelPostWord);
})
function intelPostWord(data) {
    if (data){
        $('#post-2-content').text(data);
    }else {
        $('#post-2-content').text('未计算出任何发帖内容');
    }
}
//创建任务
$('#create').on('click',function () {
    var taskName=$('.point-view-1').val();
    var eventWord=$('.point-view-2').val();
    var myWord=$('.point-view-3').val();
    if (!taskName||!eventWord||!myWord){
        $('#pormpt p').text('请检查您输入的内容，不能为空。');
        $('#pormpt').modal('show');
    }else {
        var opinionType=$('.intelliGence-2 .ed-2-1-bottom input[name="polar"]:checked').val();
        var build_intelligent_url='/intelligent_writing/create_writing_task/?task_source='+intelligentType+'&xnr_user_no='+ID_Num+'&task_name='+
            taskName+'&event_keywords='+eventWord.replace(/,/g,'，')+'&opinion_keywords='+myWord.replace(/,/g,'，')+
            '&opinion_type='+opinionType+'&submitter='+admin;
        public_ajax.call_request('get',build_intelligent_url,reshIntelligent);
    }
});
function reshIntelligent(data) {
    var f='操作失败。';
    if (data=='true'){
        f='操作成功。';
    }else if (data== 'exists'){
        f='请更换一个事件名称。';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
//任务列表
var intelligent_writing_url='/intelligent_writing/show_writing_task/?task_source='+intelligentType+'&xnr_user_no='+ID_Num;
// var intelligent_writing_url='/intelligent_writing/show_writing_task/?task_source=facebook&xnr_user_no=FXNR0005';
// public_ajax.call_request('get',intelligent_writing_url,intelligentList);
function intelligentList(data) {
    $('#eventList').bootstrapTable('load', data);
    $('#eventList').bootstrapTable({
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
                title: "事件名称",//标题
                field: "task_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row.task_name==''||row.task_name=='null'||row.task_name=='unknown'||!row.task_name){
                        name=row.task_name_pinyin;
                    }else {
                        name=row.task_name;
                    };
                    return name;
                }
            },
            {
                title: "事件关键词",//标题
                field: "event_keywords",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var word;
                    if (row.event_keywords==''||row.event_keywords=='null'||row.event_keywords=='unknown'||!row.event_keywords){
                        word='暂无关键词';
                    }else {
                        word=row.event_keywords.replace(/&/g,',');
                    };
                    return word;
                }
            },
            {
                title: "我的观点关键词",//标题
                field: "opinion_keywords",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var word;
                    if (row.opinion_keywords==''||row.opinion_keywords=='null'||
                        row.opinion_keywords=='unknown'||!row.opinion_keywords){
                        word='暂无关键词';
                    }else {
                        word=row.opinion_keywords.replace(/&/g,',');
                    };
                    return word;
                }
            },
            {
                title: "我的观点极性",//标题
                field: "opinion_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var view;
                    if (row.opinion_type==''||row.opinion_type=='null'||
                        row.opinion_type=='unknown'||!row.opinion_type){
                        view='暂无关键词';
                    }else {
                        var t=row.opinion_type;
                        if (t=='all'){view='全部'}else
                        if (t=='positive'){view='积极'}else
                        if (t=='negtive'){view='消极'}else {name='未知';}
                    };
                    return view;
                }
            },
            {
                title: "任务来源",//标题
                field: "task_source",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row.task_source==''||row.task_source=='null'||
                        row.task_source=='unknown'||!row.task_source){
                        name='未知';
                    }else {
                        var t=row.task_source;
                        if (t=='weibo'){name='微博'}else
                        if (t=='facebook'){name='facebook'}else
                        if (t=='twitter'){name='twitter'}else {name='未知';}
                    };
                    return name;
                }
            },
            {
                title: "计算状态",//标题
                field: "compute_status",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var status;
                    if (row.compute_status=='null'||row.compute_status=='unknown'){
                        status='未知';
                    }else {
                        var t=row.compute_status;
                        if (t==0){status='尚未计算'}else
                        if (t==1){status='正在计算'}else
                        if (t==2){status='计算完成'}else
                        {status='未知';}
                    };
                    return status;
                }
            },
            {
                title: "创建时间",//标题
                field: "create_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var time;
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'||!row.create_time){
                        time='未知';
                    }else {
                        time=getLocalTime(row.create_time);
                    };
                    return time;
                }
            },
            {
                title: "创建人",//标题
                field: "submitter",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name;
                    if (row.submitter==''||row.submitter=='null'
                        ||row.submitter=='unknown'||!row.submitter){
                        name='未知';
                    }else {
                        name=row.submitter;
                    };
                    return name;
                }
            },

            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<i class="icon icon-file" onclick="lookType(\''+row.task_id+'\',\''+row.create_time+'\')" title="查看" style="color: white;font-size: 12px;cursor: pointer;"></i>&nbsp;&nbsp;&nbsp;'+
                        '<i class="icon icon-trash" onclick="delEvent(\''+row.task_id+'\')" title="删除" style="color: white;font-size: 12px;cursor: pointer;"></i>'
                }
            },
        ],
    });
    $('#eventList p').slideUp(700);
}
$('#eventList').on('click-row.bs.table', function (e, row, element){
    $('.point-view-1').val(row.task_name);
    $('.point-view-2').val(row.event_keywords);
    $('.point-view-3').val(row.opinion_keywords);
    $('.intelliGence-2 .ed-2-1-bottom input[value="'+row.opinion_type+'"]').attr('checked','true');
    //
    chooseThisIntelID=row.task_id;
    $('.telChoose').removeClass('telChoose');//去除之前选中的行的，选中样式
    $(element).addClass('telChoose');//添加当前选中的success样式用于区别
    chooseThisIntel='yes';
    $('#intell_type .intel_1 .demo-label').removeClass('disableCss');
});
var task_id,task_start,task_end;
function lookType(_id,endTime) {
    task_id=_id;task_end=endTime;
    task_start=endTime-5*36*2400;
    // var river_url='/intelligent_writing/topics_river/?task_id=weibo_wxnr0004_ce_shi_ren_wu_3' +
    // '&task_source=weibo&pointInterval=3600&start_ts=1517461822&end_ts=1517893822'
    // var time_event_url='#http://219.224.134.213:9090/intelligent_writing/symbol_weibos/?task_source=weibo&task_id=' +
    //     'facebook_fxnr0005_ce_shi_ren_wu&pointInterval=3600&start_ts=1517461822&end_ts=1517893822';
    var river_url='/intelligent_writing/topics_river/?task_id='+task_id+'&task_source='+intelligentType+
        '&pointInterval=3600&start_ts='+task_start+'&end_ts='+task_end;
    public_ajax.call_request('get',river_url,river);
    var time_event_url='/intelligent_writing/symbol_weibos/?task_source='+intelligentType+'&task_id='+task_id+
    '&pointInterval=3600&start_ts='+task_start+'&end_ts='+task_end;
    public_ajax.call_request('get',time_event_url,timeEvent);
    $('#intelligenceTabs li').eq(0).removeClass('active');
    $('.radyType').show();
    $('.radyType1').addClass('active');
    $('#z-0').eq(0).removeClass('active');
    $('#z-1').addClass('active');
}
var intelligentID;
function delEvent(id) {
    intelligentID=id;
    $('#intelligentDEL').modal('show');
}
function sureIntelligentDEL() {
    var del_intelligent_url='/intelligent_writing/delete_writing_task/?task_id='+intelligentID;
    public_ajax.call_request('get',del_intelligent_url,postYES);
}
// 事件主题河
$('#z-1 .interval-1 input').on('click',function () {
    $('#eventRiver-1 p').show();
    var pointIntervalTime=$(this).val();
    var river_url='intelligent_writing/topics_river/?task_id='+task_id+'&task_source='+intelligentType+
        '&pointInterval='+pointIntervalTime+'&start_ts='+task_start+'&end_ts='+task_end;
    public_ajax.call_request('get',river_url,river);
})
function river(data) {
    if (isEmptyObject(data)){
        $('#eventRiver-1').html('<center>暂无内容</center>');
    }else {
        var lenged=[],seriesData=[];
        for (var k in data){
            lenged.push(k);
            $.each(data[k],function (index,item) {
                seriesData.push(
                    [item[0],item[1],k]
                )
            });
        }
        // 基于准备好的dom，初始化echarts图表
        var myChart = echarts.init(document.getElementById('eventRiver-1'),'chalk');
        var option = {
            backgroundColor:'transparent',
            title: {
                text: '事件主题河'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line',
                    lineStyle: {
                        color: 'rgba(0,0,0,0.2)',
                        width: 1,
                        type: 'solid'
                    }
                }
            },
            legend: {
                data: lenged
            },
            singleAxis: {
                top: 50,
                bottom: 50,
                axisTick: {},
                axisLabel: {},
                type: 'time',
                axisPointer: {
                    animation: true,
                    label: {
                        show: true,
                        backgroundColor:'#333'
                    }
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        type: 'dashed',
                        opacity: 0.2
                    }
                }
            },

            series: [
                {
                    type: 'themeRiver',
                    label: {
                        show: true,
                        color:'#333',
                    },
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 20,
                            shadowColor: 'rgba(0, 0, 0, 0.8)'
                        }
                    },
                    data: seriesData
                }
            ]
        };
        // 为echarts对象加载数据
        myChart.setOption(option);
    }
    $('#eventRiver-1 p').slideUp(300);
}
//时间轴
$('#z-1 .interval-2 input').on('click',function () {
    $('#eventSurvey .VivaTimeline p').show();
    var pointIntervalTime=$(this).val();
    var time_event_url='/intelligent_writing/symbol_weibos/?task_source='+intelligentType+'&task_id='+task_id+
        '&pointInterval='+pointIntervalTime+'&start_ts='+task_start+'&end_ts='+task_end;
    public_ajax.call_request('get',time_event_url,timeEvent);
});
function timeEvent(data) {
    if (isEmptyObject(data)){
        $('#eventSurvey .VivaTimeline').html('<center>暂无内容</center>');
    }else{
        var str='<dl>',kIndex=0;
        for(var h in data){
            var str_content='';
            $.each(data[h],function (index,item) {
                str_content+=
                    '<div class="row">'+
                    '    <div class="events-desc">'+
                    '       <span>'+item.datetime+'</span>&nbsp;&nbsp;'+item.text+
                    '    </div>'+
                    '</div>';
            });
            var leftRight='pos-right';
            if (kIndex%2==0){leftRight='pos-left'};
            str+=
                '<dd class="'+leftRight+' clearfix">'+
                '    <div class="circ"></div>'+
                '    <div class="time"></div>'+
                '    <div class="events">'+
                '        <div class="events-header">'+h+'</div>'+
                '        <div class="events-body">'+str_content+'</div>'+
                '        <div class="events-footer"></div>'+
                '    </div>'+
                '</dd>';
            kIndex++;
        }
        $('#eventSurvey .VivaTimeline').html(str+'</dl>');
        $('.VivaTimeline').vivaTimeline({
            carousel: true,
            carouselTime: 3000
        });
    }
    $('#eventSurvey .VivaTimeline p').slideUp(300);
}
//各种观点
var boxView='',tableView;
$('#intelligenceTabs a.viewHave').on('click',function () {
    boxView=$(this).attr('href');
    tableView=$(this).attr('table-view');
    var viewThis_url;
    if (tableView=='view-5'){
        viewThis_url='/intelligent_writing/show_opinion_corpus_name/';
        // public_ajax.call_request('get',viewThis_url,intelligentCorpus);
        // return false;
    }else {
        var view_type=$(this).attr('view-type');
        viewThis_url='/intelligent_writing/opinions_all/?task_id='+task_id+'&intel_type='+view_type;
    }
    // var viewThis_url='/intelligent_writing/opinions_all/?task_id=twitter_txnr0001_ce_shi_ren_wu___0_2_2_6___0_4&intel_type='+view_type;
    public_ajax.call_request('get',viewThis_url,viewData);
});
var viewButton={};
function viewData(data) {
    if ('subopinion_tweets' in data){
        if (isEmptyObject(JSON.parse(data['subopinion_tweets']))){
            $(boxView).html('<center>暂无内容</center>');
        }
        return false;
    }else if (isEmptyObject(data)){
        $(boxView).html('<center>暂无内容</center>');
        return false;
    }
    var viewAllData;
    if ('subopinion_tweets' in data){
        viewAllData=JSON.parse(data['subopinion_tweets']);
    }else {
        viewAllData=data;
    }
    if ('subopinion_tweets' in data){
        if (data['summary']==''){$(boxView+' .summary span').text('暂无摘要内容');}
        else{$(boxView+' .summary span').text(data['summary']);}
        viewButton=viewAllData;
    }
    var butAry='',showDeafult=0,_act='';
    for(var t in viewAllData){
        var _act='';
        if (showDeafult==0){
            if ('subopinion_tweets' in data){thisButton_Content(viewButton[t])}
            else {
                var klb_url='/intelligent_writing/show_opinion_corpus_content/?corpus_name='+t+'&task_id='+task_id;
                public_ajax.call_request('get',klb_url,thisButton_Content);
            };
            _act='active';
        };
        if ('subopinion_tweets' in data){
            butAry+='<button type="button" class="btn btn-primary btn-xs '+_act+'" ' +
                'onclick="z_Content(this)" style="margin: 5px;">'+t+'</button>';
        }else {
            butAry+='<button type="button" class="btn btn-primary btn-xs '+_act+'" ' +
                'onclick="z_Content(this)" style="margin: 5px;"><span>'+t+'</span>&nbsp;&nbsp;<i class="icon icon-remove" onclick="delThisCorpus(\''+t+'\',this,event);return false;" style="cursor: pointer;"></i></button>';
        }
        showDeafult++;
    }
    $(boxView+' .view-1-button').html(butAry);
}
//
$('.sureAddCorpus').on('click',function () {
    var _val=$('.corpusVal').val();
    if (_val){
        var kus_url='/intelligent_writing/add_opinion_corpus/?corpus_name='+_val+'&submitter='+admin;
        public_ajax.call_request('get',kus_url,addpostYES);
    }else {
        $('#pormpt p').text('请输入观点语料库名称，不能为空。');
        $('#pormpt').modal('show');
    }
});
function addpostYES(data) {
    var f='操作失败';
    if (data[0]||data){
        f='操作成功';
        setTimeout(function () {
            var viewThis_url='/intelligent_writing/show_opinion_corpus_name/';
            public_ajax.call_request('get',viewThis_url,intelligentCorpus);
        },700);
    };
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
var IamdelThisCorpus_id,ThisCorpus_this;
function delThisCorpus(n,_this,e) {
    e.stopPropagation();
    IamdelThisCorpus_id=n,ThisCorpus_this=_this;
    $('#delCorpus').modal('show');
}
function IamdelThisCorpus() {
    var del_url='/intelligent_writing/delete_opinion_corpus/?corpus_name='+IamdelThisCorpus_id+'&submitter='+admin;
    public_ajax.call_request('get',del_url,delpostYES);
}
function delpostYES(data) {
    var f='操作失败';
    if (data[0]||data){
        f='操作成功';
        $(ThisCorpus_this).parent().remove();
        setTimeout(function () {
            var viewThis_url='/intelligent_writing/show_opinion_corpus_name/';
            public_ajax.call_request('get',viewThis_url,intelligentCorpus);
        },700);
    };
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
// 公用
function z_Content(_this) {
    var ThisData;
    if ($(_this).find('span').text()){
        ThisData=$(_this).find('span').text();
    }else {
        ThisData=$(_this).text();
    }
    $(_this).siblings('button').removeClass('active');
    $(_this).addClass('active');
    if (ThisData in viewButton){
        if (isEmptyObject(viewButton[ThisData])){
            $(boxView+' .'+tableView).html('<center>暂无内容</center>');
            return false;
        }else {
            thisButton_Content(viewButton[ThisData]);
        }
    }else {
        var klb_url='/intelligent_writing/show_opinion_corpus_content/?corpus_name='+ThisData+'&task_id='+task_id;
        public_ajax.call_request('get',klb_url,thisButton_Content);
    }

}
function thisButton_Content(data) {
    $(boxView+' .'+tableView).hide();
    $(boxView).find('center').show();
    var modifyData=[];
    $.each(data,function (index,item) {
        modifyData.push({'text':item});
    });
    $('#'+tableView).bootstrapTable('load', modifyData);
    $('#'+tableView).bootstrapTable({
        data:modifyData,
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
                field: "text",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var str='<p>• '+value+'</p>';
                    return str;
                }
            },
        ],
    });
    $(boxView).find('center').slideUp(700);
    $(boxView+' .'+tableView).show();
}

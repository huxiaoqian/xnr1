//语料
var material_url='/'+urlTotal+'/show_different_corpus/?corpus_type=&corpus_status=0'+
    '&request_type=all&theme_type_1=&theme_type_2=&theme_type_3=';
public_ajax.call_request('get',material_url,material);
function material(data) {
    console.log(data);
    var str=''
    $.each(data['opinion_corpus_type'],function (index,item) {
        str+='<label class="demo-label" title="'+item+'">' +
            '    <input class="demo-radio" type="checkbox" name="yuliao" value="'+item+'">' +
            '    <span class="demo-checkbox demo-radioInput"></span> ' +item+
            '</label>';
    })
    $('.yuliao').html(str);
    $(".yuliao input[name='yuliao']").on('click',function () {
        var t=$(".tit-2 input[name='mine']:checked").val();
        if (!t){t=''};
        var c=[];
        $(".yuliao input[name='yuliao']:checkbox:checked").each(function (index,item) {
            c.push($(this).val());
        });
        var yuliaoUrl='/'+urlTotal+'/show_different_corpus/?corpus_type='+t+'&corpus_status=1'+
            '&request_type=one&theme_type_1=&theme_type_2=&theme_type_3='+c.join(',');
        public_ajax.call_request('get',yuliaoUrl,day);
    });
    themeWord(data['theme_corpus']);
    day(data['daily_corpus']);
    view(data['opinion_corpus']);
}
$(".zhuti input[name='zhuti']").on('click',function () {
    var t=$(".tit-2 input[name='mine']:checked").val();
    if (!t){t=''};
    var a=[];
    $(".zhuti input[name='zhuti']:checkbox:checked").each(function (index,item) {
        a.push($(this).val());
    });
    var zhutiUrl='/'+urlTotal+'/show_different_corpus/?corpus_type='+t+'&corpus_status=1'+
        '&request_type=one&theme_type_1='+a.join(',')+'&theme_type_2=&theme_type_3=';
    public_ajax.call_request('get',zhutiUrl,themeWord);
});
$(".richang input[name='richang']").on('click',function () {
    var t=$(".tit-2 input[name='mine']:checked").val();
    if (!t){t=''};
    var a=[];
    $(".zhuti input[name='richang']:checkbox:checked").each(function (index,item) {
        a.push($(this).val());
    });
    var zhutiUrl='/'+urlTotal+'/show_different_corpus/?corpus_type='+t+'&corpus_status=1'+
        '&request_type=one&theme_type_1=&theme_type_2='+a.join(',')+'&theme_type_3=';
    public_ajax.call_request('get',zhutiUrl,day);
});
$('#container .title .tit-2 .allMY').on('click',function () {
    var tp=$(this).attr('value');
    var theme1=[],theme2=[],theme3=[];
    $(".zhuti input[name='zhuti']:checkbox:checked").each(function (index,item) {
        theme1.push($(this).val());
    });
    $(".richang input[name='richang']:checkbox:checked").each(function (index,item) {
        theme2.push($(this).val());
    });
    var theUrl='/'+urlTotal+'/show_different_corpus/?corpus_type='+tp+'&corpus_status=1'+
        '&request_type=all&theme_type_1='+theme1.join(',')+'&theme_type_2='+theme2.join(',')+'&theme_type_3='+theme3.join(',');
    public_ajax.call_request('get',theUrl,material);
});
//主题语料库
function themeWord(data) {
    var data=data['theme_corpus']||data;
    $('#theme').bootstrapTable('load', data);
    $('#theme').bootstrapTable({
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
                    var theme,time,img;
                    if (row.theme_daily_name==''||row.theme_daily_name=='null'||row.theme_daily_name=='unknown'){
                        theme = '暂无';
                    }else {
                        theme = row.theme_daily_name;
                    }
                    if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'){
                        time = '暂无';
                    }else {
                        time = getLocalTime(row.timestamp);
                    }
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };
                    var str=
                        '<div class="post_perfect" style="margin:0 auto 10px;">' +
                        '   <div class="post_center_hot">' +
                        '    <img src="/static/images/post-6.png" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">主题类型：'+theme+'</a>&nbsp;'+
                        '           <i class="mid" style="display: none;">'+(row.mid||row.fid||row.tid)+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '           <span class="centerDel" style="cursor: pointer;" onclick="del(\''+row.id+'\',\''+11+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '           <span class="centerEdit" style="cursor: pointer;" onclick="modify(\''+row.id+'\',\''+row.corpus_type+'\',\''+row.create_type+'\',\''+row.theme_daily_name+'\',\''+33+'\')"><i title="修改" class="icon icon-edit"></i></span>'+
                        '           <div class="center_2" style="text-align: left;margin: 10px 0;"><b style="color:#f98077;">摘要内容：</b>'+txt+'</div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>'
                    return str;
                }
            },
        ],

    });
}
//日常发帖语料库
function day(data) {
    var data=data['daily_corpus']||data;
    $('#everypost').bootstrapTable('load', data);
    $('#everypost').bootstrapTable({
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
                    var theme,time,img;
                    if (row.theme_daily_name==''||row.theme_daily_name=='null'||row.theme_daily_name=='unknown'){
                        theme = '暂无';
                    }else {
                        theme = row.theme_daily_name;
                    }
                    if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'){
                        time = '暂无';
                    }else {
                        time = getLocalTime(row.timestamp);
                    }
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };
                    var str=
                        '<div class="post_perfect" style="margin-top: 8px;">' +
                        '   <div class="post_center_hot">' +
                        '    <img src="/static/images/post-6.png" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">主题类型：'+theme+'</a>&nbsp;'+
                        '           <i class="mid" style="display: none;">'+(row.mid||row.fid||row.tid)+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '           <span class="centerDel" style="cursor: pointer;" onclick="del(\''+row.id+'\',\''+11+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '           <span class="centerEdit" style="cursor: pointer;" onclick="modify(\''+row.id+'\',\''+row.corpus_type+'\',\''+row.create_type+'\',\''+row.theme_daily_name+'\',\''+33+'\')"><i title="修改" class="icon icon-edit"></i></span>'+
                        '           <div class="center_2" style="text-align: left;margin: 10px 0;"><b style="color:#f98077;">摘要内容：</b>'+txt+'</div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>'
                    return str;
                }
            },
        ],

    });
};
//观点语料库
//var view_url='/intelligent_writing/show_opinion_corpus_name/';
// public_ajax.call_request('get',view_url,view);
function view(data) {
    $('#viewpoint').bootstrapTable('load', data);
    $('#viewpoint').bootstrapTable({
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
                    var theme,time,img;
                    if (row.label==''||row.label=='null'||row.label=='unknown'){
                        theme = '暂无';
                    }else {
                        theme = row.label;
                    }
                    if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'){
                        time = '暂无';
                    }else {
                        time = getLocalTime(row.timestamp);
                    }
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };
                    var str=
                        '<div class="post_perfect" style="margin-top: 8px;">' +
                        '   <div class="post_center_hot">' +
                        '    <img src="/static/images/post-6.png" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">主题类型：'+theme+'</a>&nbsp;'+
                        '           <i class="mid" style="display: none;">'+(row.mid||row.fid||row.tid)+'</i>'+
                        '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '           <span class="centerDel" style="cursor: pointer;" onclick="del(\''+row.id+'\',\''+11+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '           <span class="centerEdit" style="cursor: pointer;" onclick="modify(\''+row.id+'\',\''+row.corpus_type+'\',\''+row.create_type+'\',\''+row.theme_daily_name+'\',\''+33+'\')"><i title="修改" class="icon icon-edit"></i></span>'+
                        '           <div class="center_2" style="text-align: left;margin: 10px 0;"><b style="color:#f98077;">摘要内容：</b>'+txt+'</div>'+
                        '       </div>'+
                        '   </div>'+
                        '</div>'
                    return str;
                }
            },
        ],

    });
};
$('.sureAddCorpus').on('click',function () {
    var _val=$('.corpusVal').val();
    if (_val){
        var kus_url='/intelligent_writing/add_opinion_corpus/?corpus_name='+_val+'&submitter='+admin;
        public_ajax.call_request('get',kus_url,sucfail);
    }else {
        $('#pormpt p').text('请输入观点语料库名称，不能为空。');
        $('#pormpt').modal('show');
    }
});
//=====编辑=====
var id,corpus_type,mod_type,modNUM,_val_;
function modify(_id,corpusType,create_type,theme_daily_name,num) {
    id=_id;corpus_type=corpusType;mod_type=create_type;modNUM=num;
    if (corpusType=='主题语料'){
        $('#themelist1').hide();$('#themelist2').show();_val_='theme2';
    }else if (corpusType=='日常语料'){
        $('#themelist1').show();$('#themelist2').hide();_val_='theme';
    }else{

    }
    $('#themetype .the').val(theme_daily_name);
    $('#themetype').modal('show');
}
function suretheme() {
    var theme=[];
    $("#themetype input[name='"+_val_+"']:checkbox:checked").each(function (index,item) {
        theme.push($(this).val());
    });
    if (theme.length==0){
        $('#pormpt p').text('新的主题类型不能为空，请选择。');
        $('#pormpt').modal('show');
    }else {
        var newTheurl='/'+urlTotal+'/change_select_corpus/?corpus_id='+id+'&corpus_type='+corpus_type
            +'&create_type='+mod_type+'&theme_daily_name='+theme.join(',');
        public_ajax.call_request('get',newTheurl,sucfail);
    }
}
//====删除=========
var nowNUM;
function del(_id,num) {
    nowNUM=num;
    var deltUrl='/'+urlTotal+'/delete_corpus/?corpus_id='+_id;
    public_ajax.call_request('get',deltUrl,sucfail);
}
function sucfail(data) {
    var f='';
    if (data||data[0]){
        f='操作成功';
        if (nowNUM||modNUM){
            var nowurl='',fun='';
            if (Number(nowNUM)==11||Number(modNUM)==33){nowurl=theme_url;fun=themeWord}else {nowurl=day_url;fun=day;};
            setTimeout(function () {
                public_ajax.call_request('get',nowurl,fun);
            },1000)
        };
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
//判断哪个选中的
var creat_type='';
function creatTYPE() {
    var pl=$('.tit-2 input:radio[name="mine"]:checked').val();
    if (pl){creat_type=pl}else{creat_type=''};
}
$('#container .title .tit-2 .allMY').on('click',function () {
    var tp=$(this).attr('value');
    var theUrl='/weibo_xnr_knowledge_base_management/show_corpus_class/?corpus_type=主题语料&create_type='+tp;
    var dayUrl='/weibo_xnr_knowledge_base_management/show_corpus_class/?corpus_type=日常语料&create_type='+tp;
    public_ajax.call_request('get',theUrl,themeWord);
    public_ajax.call_request('get',dayUrl,day);
});
//主题语料库
var theme_url='/weibo_xnr_knowledge_base_management/show_corpus/?corpus_type=主题语料';
public_ajax.call_request('get',theme_url,themeWord);
function themeWord(data) {
    console.log(data);
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
                        '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
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
            // {
            //     title: "主题类型",//标题
            //     field: "theme_daily_name",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.theme_daily_name==''||row.theme_daily_name=='null'||row.theme_daily_name=='unknown'){
            //             return '暂无';
            //         }else {
            //             return row.theme_daily_name;
            //         }
            //     }
            // },
            // {
            //     title: "创建时间",//标题
            //     field: "timestamp",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'){
            //             return '暂无';
            //         }else {
            //             return getLocalTime(row.timestamp);
            //         }
            //     }
            // },
            // {
            //     title: "内容",//标题
            //     field: "text",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.text==''||row.text=='null'||row.text=='unknown'){
            //             return '暂无';
            //         }else {
            //             var str='';
            //             str+=
            //                 '<div class="post_perfect">'+
            //                 '   <div class="post_center-hot">'+
            //                 '       <div class="center_rel">'+
            //                 '           <a class="center_1" href="###" style="color: #f98077;display: none;">'+row.uid+'</a>'+
            //                 '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
            //                 '           <i class="uid" style="display: none;">'+row.id+'</i>'+
            //                 '           <span class="center_2">'+row.text+
            //                 '           </span>'+
            //                 '           <div class="center_3">'+
            //                 '               <span class="cen3-1"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（'+row.retweeted+'）</span>'+
            //                 '               <span class="cen3-2"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（'+row.comment+'）</span>'+
            //                 '               <span class="cen3-3"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞（'+row.like+'）</span>'+
            //                 '           </div>'+
            //                 '       </div>'+
            //                 '   </div>'+
            //                 '</div>';
            //             return str;
            //         }
            //     }
            // },
            // {
            //     title: "操作",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return '<span style="cursor: pointer;" onclick="del(\''+row.id+'\',\''+11+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
            //             '<span style="cursor: pointer;" onclick="modify(\''+row.id+'\',\''+row.corpus_type+'\',\''+row.create_type+'\',\''+row.theme_daily_name+'\',\''+33+
            //             '\')"><i title="修改" class="icon icon-edit"></i></span>';
            //     }
            // },
        ],

    });
    $('.theme .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
//日常发帖语料库
var day_url='/weibo_xnr_knowledge_base_management/show_corpus/?corpus_type=日常语料';
public_ajax.call_request('get',day_url,day);
function day(data) {
    console.log(data);
    $('#everypost').bootstrapTable('load', data);
    $('#everypost').bootstrapTable({
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
                        '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
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
            // {
            //     title: "主题类型",//标题
            //     field: "theme_daily_name",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.theme_daily_name==''||row.theme_daily_name=='null'||row.theme_daily_name=='unknown'){
            //             return '暂无';
            //         }else {
            //             return row.theme_daily_name;
            //         }
            //     }
            // },
            // {
            //     title: "创建时间",//标题
            //     field: "timestamp",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'){
            //             return '暂无';
            //         }else {
            //             return getLocalTime(row.timestamp);
            //         }
            //     }
            // },
            // {
            //     title: "内容",//标题
            //     field: "text",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.text==''||row.text=='null'||row.text=='unknown'){
            //             return '暂无';
            //         }else {
            //             var str='';
            //             str+=
            //                 '<div class="post_perfect">'+
            //                 '   <div class="post_center-hot">'+
            //                 '       <div class="center_rel">'+
            //                 '           <a class="center_1" href="###" style="color: #f98077;display: none;">'+row.uid+'</a>'+
            //                 '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
            //                 '           <i class="uid" style="display: none;">'+row.id+'</i>'+
            //                 '           <span class="center_2">'+row.text+
            //                 '           </span>'+
            //                 '           <div class="center_3">'+
            //                 '               <span class="cen3-1"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（'+row.retweeted+'）</span>'+
            //                 '               <span class="cen3-2"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（'+row.comment+'）</span>'+
            //                 '               <span class="cen3-3"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞（'+row.like+'）</span>'+
            //                 '           </div>'+
            //                 '       </div>'+
            //                 '   </div>'+
            //                 '</div>';
            //             return str;
            //         }
            //     }
            // },
            // {
            //     title: "操作",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return '<span style="cursor: pointer;" onclick="del(\''+row.id+'\',\''+22+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
            //             '<span style="cursor: pointer;" onclick="modify(\''+row.id+'\',\''+row.corpus_type+'\',\''+row.create_type+'\',\''+row.theme_daily_name+'\',\''+44+
            //             '\')"><i title="修改" class="icon icon-edit"></i></span>';
            //     }
            // },
        ],

    });
    $('.everypost .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
};
//=====编辑=====
var id,corpus_type,mod_type,modNUM;
function modify(_id,corpusType,create_type,theme_daily_name,num) {
    id=_id;corpus_type=corpusType;mod_type=create_type;modNUM=num;
    $('#themetype .the').val(theme_daily_name);
    $('#themetype').modal('show');
}
function suretheme() {
    var theme=[];
    $("#themetype input:checkbox:checked").each(function (index,item) {
        theme.push($(this).val());
    });
    if (theme.length==0){
        $('#pormpt p').text('新的主题类型不能为空，请选择。');
        $('#pormpt').modal('show');
    }else {
        var newTheurl='/weibo_xnr_knowledge_base_management/change_select_corpus/?corpus_id='+id+'&corpus_type='+corpus_type
            +'&create_type='+mod_type+'&theme_daily_name='+theme.join(',');
        public_ajax.call_request('get',newTheurl,sucfail);
    }
}
//====删除=========
var nowNUM;
function del(_id,num) {
    nowNUM=num;
    var deltUrl='/weibo_xnr_knowledge_base_management/delete_corpus/?corpus_id='+_id;
    public_ajax.call_request('get',deltUrl,sucfail);
}
function sucfail(data) {
    var f='';
    if (data){
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
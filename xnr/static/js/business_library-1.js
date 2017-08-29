var keywords_url='/weibo_xnr_knowledge_base_management/show_sensitive_words_default/';
public_ajax.call_request('get',keywords_url,keywords);
function keywords(data) {
    $('#keywords').bootstrapTable('load', data);
    $('#keywords').bootstrapTable({
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
                title: "敏感词",//标题
                field: "sensitive_words",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.sensitive_words==''||row.sensitive_words=='null'||row.sensitive_words=='unknown'){
                        return '暂无';
                    }else {
                        return row.sensitive_words;
                    }
                },
            },
            {
                title: "创建时间",//标题
                field: "create_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'){
                        return '暂无';
                    }else {
                        return getLocalTime(row.create_time);
                    }
                }
            },
            {
                title: "等级",//标题
                field: "rank",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor: pointer;" onclick="del(\''+row.sensitive_words+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                     '<span style="cursor: pointer;" onclick="modify(\''+row.sensitive_words+'\',\''+row.create_type+
                        '\')"><i title="修改关键词" class="icon icon-edit"></i></span>';
                }
            },
        ],

    });
    $('.keywords .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
//点击选择全部还是我的
$('#container .title .tit-2 .allMY').on('click',function () {
    var tp=$(this).attr('value');
    var rk=$('.rankcon input:radio[name="rank"]:checked').val();
    var rankUrl='/weibo_xnr_knowledge_base_management/show_sensitive_words_condition/?create_type='+tp+'&rank='+rk;
    public_ajax.call_request('get',rankUrl,keywords);
});
//按指定等级显示
$('#container .options-1 .opt-1-1 .rankcon .demo-label').on('click',function () {
    creatTYPE();
    var r=$(this).attr('rank');
    var rankUrl='/weibo_xnr_knowledge_base_management/show_sensitive_words_condition/?create_type='+creat_type+'&rank='+r;
    public_ajax.call_request('get',rankUrl,keywords);
    var time_url='/weibo_xnr_knowledge_base_management/show_date_remind_condition/?create_type='+creat_type;
    public_ajax.call_request('get',time_url,time);
});
//添加敏感词
var ad=0;
$('.addKey').on('click',function () {
    var rank=$('.rankcon input:radio[name="rank"]:checked').val();
    if (ad==0){
        $(this).text('确定');
        $(".keyVal").css({
            '-webkit-transform': 'translate(0%)',
            '-moz-transform': 'translate(0%)',
            '-ms-transform': 'translate(0%)',
            '-o-transform': 'translate(0%)',
            'transform': 'translate(0%)'
        });
        ad=1;
    }else {
        var word=$('.keyVal').val().toString().replace(/,/g,'，');
        if (word==''){
            $('#pormpt p').text('敏感词不能为空。');
            $('#pormpt').modal('show');
            $(this).html('<i class="icon icon-plus"></i>&nbsp;&nbsp;<b>添加敏感词</b>');
            $(".keyVal").css({
                '-webkit-transform': 'translate(150%)',
                '-moz-transform': 'translate(150%)',
                '-ms-transform': 'translate(150%)',
                '-o-transform': 'translate(150%)',
                'transform': 'translate(150%)'
            });
            ad=0;
        }else {
            creatTYPE();
            var addUrl='/weibo_xnr_knowledge_base_management/create_sensitive_words_batch/?rank='+rank+
                '&sensitive_words_string='+word+'&create_type='+creat_type;
            public_ajax.call_request('get',addUrl,addYES);
        }
    }


})
//删除敏感词
function del(word) {
    var delURL='/weibo_xnr_knowledge_base_management/delete_sensitive_words/?words_id='+word;
    public_ajax.call_request('get',delURL,addYES);
}
//修改敏感词
var senW='',word_type='';
function modify(word,type) {
    $('#words .nowd1').val(word);
    senW=word;
    word_type=type;
    $('#words').modal('show');
}
function sureword() {
    var newWords=$('#words .nowd2').val();
    if (newWords==''){
        $('#pormpt p').text('新的敏感词不能为空。');
        $('#pormpt').modal('show');
    }else {
        var rk=$('.rankcon input:radio[name="rank"]:checked').val();
        var plyURL='/weibo_xnr_knowledge_base_management/change_sensitive_words/?words_id='+senW+
            '&rank='+rk+'&sensitive_words='+newWords+'&create_type='+word_type;
        public_ajax.call_request('get',plyURL,addYES);
    }

}
//操作返回结果
function addYES(data) {
    var f='';
    if (data){
        f='操作成功';
        setTimeout(function () {
            public_ajax.call_request('get',keywords_url,keywords);
        },1000)
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
//判断哪个选中的
var creat_type='';
function creatTYPE() {
    var pl=$('.tit-2 input:radio[name="mine"]:checked').val();
    if (pl){creat_type=pl}else{creat_type=''};
}

//============时间预警节点-------------------
var time_url='/weibo_xnr_knowledge_base_management/show_date_remind/';
public_ajax.call_request('get',time_url,time);
function time(data) {
    $('#timeWarn').bootstrapTable('load', data);
    $('#timeWarn').bootstrapTable({
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
                title: "日期节点",//标题
                field: "date_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "关键词",//标题
                field: "keywords",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.keywords==''||row.keywords=='null'||row.keywords=='unknown'){
                        return '暂无';
                    }else {
                        return row.keywords;
                    }
                },
            },
            {
                title: "创建时间",//标题
                field: "create_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'){
                        return '暂无';
                    }else {
                        return getLocalTime(row.create_time);
                    }
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
                    return '<span style="cursor: pointer;" onclick="delTime(\''+row.create_time+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<span style="cursor: pointer;" onclick="modifyTime(\''+row.id+'\',\''+row.keywords+'\',\''+row.create_type+
                        '\')"><i title="修改节点" class="icon icon-edit"></i></span>';
                }
            },
        ],

    });
    $('.timeWarn .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
};
//添加时间节点
var adT=0;
$('.addNode').on('click',function () {
    if (adT==0){
        $(this).text('确定');
        $(".timeVal1").css({
            '-webkit-transform': 'translate(0%)',
            '-moz-transform': 'translate(0%)',
            '-ms-transform': 'translate(0%)',
            '-o-transform': 'translate(0%)',
            'transform': 'translate(0%)'
        });
        $(".timeVal2").css({
            '-webkit-transform': 'translate(0%)',
            '-moz-transform': 'translate(0%)',
            '-ms-transform': 'translate(0%)',
            '-o-transform': 'translate(0%)',
            'transform': 'translate(0%)'
        });
        adT=1;
    }else {
        var word=$('.timeVal2').val().toString().replace(/,/g,'，');
        var time=$('.timeVal1').val();
        if (word==''||time==''){
            $('#pormpt p').text('敏感词或事件节点不能为空。');
            $('#pormpt').modal('show');
            $(this).html('<i class="icon icon-plus"></i>&nbsp;&nbsp;<b>添加敏感词</b>');
            $(".timeVal1").css({
                '-webkit-transform': 'translate(280%)',
                '-moz-transform': 'translate(280%)',
                '-ms-transform': 'translate(280%)',
                '-o-transform': 'translate(280%)',
                'transform': 'translate(280%)'
            });
            $(".timeVal2").css({
                '-webkit-transform': 'translate(280%)',
                '-moz-transform': 'translate(280%)',
                '-ms-transform': 'translate(280%)',
                '-o-transform': 'translate(280%)',
                'transform': 'translate(280%)'
            });
            adT=0;
        }else {
            creatTYPE();
            var addUrl='/weibo_xnr_knowledge_base_management/create_date_remind/?timestamp='+time+
                '&keywords='+word+'&create_type='+creat_type;
            public_ajax.call_request('get',addUrl,addYES_time);
        }
    }


})
//删除时间节点
function delTime(time) {
    var delURL='/weibo_xnr_knowledge_base_management/delete_date_remind/?task_id='+time;
    public_ajax.call_request('get',delURL,addYES_time);
}
//修改时间节点敏感词
var taskID='',timetype='';
function modifyTime(_id,key,type) {
    taskID=_id;
    timetype=type;
    $('#time .time1').val(key);
    $('#time').modal('show');
}
function sureTime() {
    var newWords=$('#time .time2').val();
    if (newWords==''){
        $('#pormpt p').text('新的时间节点敏感词不能为空。');
        $('#pormpt').modal('show');
    }else {
        var plyURL='/weibo_xnr_knowledge_base_management/change_date_remind/?task_id='+taskID+'&keywords='+newWords
        +'&create_type='+timetype;
        public_ajax.call_request('get',plyURL,addYES_time);
    }
}
//操作返回结果
function addYES_time(data) {
    var f='';
    if (data){
        f='操作成功';
        setTimeout(function () {
            public_ajax.call_request('get',time_url,time);
        },1000)
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}

//=================隐喻式----------
var hidden_url='/weibo_xnr_knowledge_base_management/show_hidden_expression/';
public_ajax.call_request('get',hidden_url,hidden);
function hidden(data) {
    console.log(data);
    $('#expression').bootstrapTable('load', data);
    $('#expression').bootstrapTable({
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
                title: "创建时间",//标题
                field: "create_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'){
                        return '暂无';
                    }else {
                        return getLocalTime(row.create_time);
                    }
                }
            },
            {
                title: "原词",//标题
                field: "origin_word",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.origin_word==''||row.origin_word=='null'||row.origin_word=='unknown'){
                        return '暂无';
                    }else {
                        return row.origin_word;
                    }
                },
            },
            {
                title: "变形词",//标题
                field: "evolution_words_string",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.evolution_words_string==''||row.evolution_words_string=='null'||row.evolution_words_string=='unknown'){
                        return '暂无';
                    }else {
                        return row.evolution_words_string.replace(/&/g,',');
                    }
                },
            },
            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor: pointer;" onclick="delHidden(\''+row.origin_word+'\')"><i title="删除" class="icon icon-trash"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<span style="cursor: pointer;" onclick="modifyHidden(\''+row.id+'\',\''+row.origin_word+'\',\''+row.evolution_words_string+'\',\''+row.create_type+
                        '\')"><i title="修改关键词" class="icon icon-edit"></i></span>';
                }
            },
        ],

    });
    $('.expression .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
//添加隐喻式词语
var adH=0;
$('.addhid').on('click',function () {
    if (adH==0){
        $(this).text('确定');
        $(".hidVal1").css({
            '-webkit-transform': 'translate(0%)',
            '-moz-transform': 'translate(0%)',
            '-ms-transform': 'translate(0%)',
            '-o-transform': 'translate(0%)',
            'transform': 'translate(0%)'
        });
        $(".hidVal2").css({
            '-webkit-transform': 'translate(0%)',
            '-moz-transform': 'translate(0%)',
            '-ms-transform': 'translate(0%)',
            '-o-transform': 'translate(0%)',
            'transform': 'translate(0%)'
        });
        adH=1;
    }else {
        var word1=$('.hidVal1').val().toString();
        var word2=$('.hidVal2').val().toString().replace(/,/g,'，');
        if (word1==''||word2==''){
            $('#pormpt p').text('原词或变形词不能为空。');
            $('#pormpt').modal('show');
            $(this).html('<i class="icon icon-plus"></i>&nbsp;&nbsp;<b>添加原词</b>');
            $(".hidVal1").css({
                '-webkit-transform': 'translate(280%)',
                '-moz-transform': 'translate(280%)',
                '-ms-transform': 'translate(280%)',
                '-o-transform': 'translate(280%)',
                'transform': 'translate(280%)'
            });
            $(".hidVal2").css({
                '-webkit-transform': 'translate(280%)',
                '-moz-transform': 'translate(280%)',
                '-ms-transform': 'translate(280%)',
                '-o-transform': 'translate(280%)',
                'transform': 'translate(280%)'
            });
            adH=0;
        }else {
            var reg=new RegExp("^[A-Za-z0-9\u4e00-\u9fa5]+$");
            if (reg.test(word1)){
                creatTYPE();
                var addUrl='/weibo_xnr_knowledge_base_management/create_hidden_expression/?origin_word='+word1+
                    '&evolution_words='+word2.replace(/,/g,'，')+'&create_type='+creat_type;
                public_ajax.call_request('get',addUrl,addYES_hid);
            }else {
                $('#pormpt p').text('原词不能含有标点符号及其它特殊符号，只能是汉字、数字、英文。');
                $('#pormpt').modal('show');
            }

        }
    }
})
//删除隐喻式节点
function delHidden(originWord) {
    var delURL='/weibo_xnr_knowledge_base_management/delete_hidden_expression/?express_id='+originWord;
    public_ajax.call_request('get',delURL,addYES_hid);
}
//修改隐喻式词语
var hideID='',hidetype='';
function modifyHidden(_id,origin,evolution,type) {
    hideID=_id;
    hidetype=type;
    $('#hide .hide1').val(origin);
    $('#hide .hide3').val(evolution);
    $('#hide').modal('show');
}
function sureHide() {
    var newWords1=$('#hide .hide2').val();
    var newWords2=$('#hide .hide4').val();
    if (newWords1==''||newWords2==''){
        $('#pormpt p').text('新的隐喻式敏感词不能为空。');
        $('#pormpt').modal('show');
    }else {
        var plyURL='/weibo_xnr_knowledge_base_management/change_hidden_expression/?express_id='+hideID+
        '&origin_word='+newWords1+'&evolution_words='+newWords2.replace(/,/g,'，')+'&create_type='+hidetype;
        public_ajax.call_request('get',plyURL,addYES_hid);
    }
}
//操作返回结果
function addYES_hid(data) {
    var f='';
    if (data){
        f='操作成功';
        setTimeout(function () {
            public_ajax.call_request('get',hidden_url,hidden);
        },1000)
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
var keywords_url='/weibo_xnr_knowledge_base_management/show_sensitive_words_default/';
public_ajax.call_request('get',keywords_url,keywords);
function keywords(data) {
    console.log(data);
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
                    return '<span style="cursor: pointer;" onclick="del(\''+row.sensitive_words.toString().replace(/'/g,"")+'\')">删除</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                     '<span style="cursor: pointer;" onclick="modify(\''+row.sensitive_words.toString().replace(/'/g,"")+'\')">修改</span>';
                }
            },
        ],

    });
    $('.keywords .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
}
//按指定等级显示
$('#container .options-1 .opt-1-1 .rankcon .demo-label').on('click',function () {
    creatTYPE();
    var r=$(this).attr('rank');
    var rankUrl='/weibo_xnr_knowledge_base_management/show_sensitive_words_condition/?create_type='+creat_type+'&rank='+r;
    public_ajax.call_request('get',rankUrl,keywords);
})
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
        var word=$('.keyVal').val().toString().replace(/，/g,',');
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
            var addUrl='/weibo_xnr_knowledge_base_management/create_sensitive_words/?rank='+rank+
                '&sensitive_words='+word+'&create_type='+creat_type;
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
var senW='';
function modify(word) {
    $('#words .nowd1').val(word);
    senW=word;
    $('#words').modal('show');
}
function sureword() {
    var newWords=$('#words .nowd2').val();
    if (newWords==''){
        $('#pormpt p').text('新的敏感词不能为空。');
        $('#pormpt').modal('show');
    }else {
        creatTYPE();
        var rk=$('.rankcon input:radio[name="rank"]:checked').val();
        var plyURL='/weibo_xnr_knowledge_base_management/change_sensitive_words/?words_id='+senW+
            '&rank='+rk+'&sensitive_words='+newWords+'&create_type='+creat_type;
        public_ajax.call_request('get',plyURL,addYES);
    }

}
//操作返回结果
function addYES(data) {
    console.log(data)
    var f='';
    if (data){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
//判断哪个选中的
var creat_type='all_xnrs';
function creatTYPE() {
    creat_type=$('.tit-2 input:radio[name="mine"]:checked').val();
}
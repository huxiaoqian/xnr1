var relatedUrl='/weibo_xnr_operate/related_recommendation/?xnr_user_no='+nowUser+'&sort_item=influence';
public_ajax.call_request('get',relatedUrl,related);
function related(data) {
    console.log(data)
    $('#influence').bootstrapTable('load', data);
    $('#influence').bootstrapTable({
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
                title: "编号",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return index+1;
                }
            },
            {
                title: "创建时间",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[2];
                // }
            },
            {
                title: "渗透领域",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[5];
                // },
            },
            {
                title: "角色定位",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: "活跃时间",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {

                },
            },
            {
                title: '操作',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<a style="cursor: pointer;" onclick="">继续</a>'+
                        '<a style="cursor: pointer;" onclick="">删除</a>';
                },
            },
        ],
        onClickCell: function (field, value, row, $element) {
            if ($element[0].innerText=='查看') {
                window.open();
            }else if ($element[0].innerText=='') {
                window.open();
            }
        }
    });
}

$('#container .suggestion #myTabs li').on('click',function () {
    var ty=$(this).attr('tp');
    var relatedUrl='/weibo_xnr_operate/related_recommendation/?xnr_user_no='+nowUser+'&sort_item='+ty;
    public_ajax.call_request('get',relatedUrl,related);
})
//直接搜索
$('.findSure').on('click',function () {
    var ids=$('.active-1-find').val();
    if (ids==''){
        $('#pormpt p').text('搜索内容不能为空。');
        $('#pormpt').modal('show');
    }else {
        ids=ids.replace(/，/g,',');
        $('#container .suggestion #myTabs li').removeClass('active');
        $('#container .suggestion #myTabs li').eq(0).addClass('active');
        var searchUrl='/weibo_xnr_operate/direct_search/?xnr_user_no='+nowUser+'&sort_item=influence&uids='+ids;
        public_ajax.call_request('get',searchUrl,related);
    }
});
//查看详情

//直接关注
function driectFocus(_this) {

}
//提示
function sucFai(data) {
    if (data[0]){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}





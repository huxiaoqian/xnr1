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
                field: "",//键名
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
                    var repData=JSON.parse(row.report_content);
                    console.log(repData)
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



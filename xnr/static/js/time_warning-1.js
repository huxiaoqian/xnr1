var timeUrl='/weibo_xnr_warming/show_date_warming/'//?xnr_user_no='+ID_Num;
public_ajax.call_request('get',timeUrl,calendar);
function calendar(data) {
    console.log(data)
    $('#remind').bootstrapTable('load', data);
    $('#remind').bootstrapTable({
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
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'||!row.create_time){
                        return '未知';
                    }else {
                        return getLocalTime(row.create_time);
                    };
                }
            },
            {
                title: "日期",//标题
                field: "date_time",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.date_time==''||row.date_time=='null'||row.date_time=='unknown'||!row.date_time){
                        return '未知';
                    }else {
                        return row.date_time;
                    };
                }
            },
            {
                title: "距离今天天数",//标题
                field: "countdown_days",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "描述",//标题
                field: "keywords",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.keywords==''||row.keywords=='null'||row.keywords=='unknown'||!row.keywords){
                        return '暂无描述';
                    }else {
                        return row.keywords;
                    };
                },
            },
            {
                title: "发帖内容推荐",//标题
                field: "content_recommend",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.content_recommend==''||row.content_recommend=='null'||row.content_recommend.length==0||
                        row.content_recommend=='unknown'||!row.content_recommend){
                        return '暂无内容';
                    }else {
                        var cot=row.content_recommend,str='';
                        for (var t of cot){
                            str+=
                                '<div class="post_center">'+
                                '    <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                                '    <div class="center_rel">'+
                                '        <span class="center_2">'+t+'</span>'+
                                '    </div>'+
                                '</div>';
                        }
                    };
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
};
var libGroup_url='/weibo_xnr_knowledge_base_management/show_domain_group_summary/?xnr_user_no='+ID_Num;
public_ajax.call_request('get',libGroup_url,group);
function group(data) {
    var person=eval(data)
    console.log(person)
    $('#group-2').bootstrapTable('load', person);
    $('#group-2').bootstrapTable({
        data:person,
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
                title: "群体名称",//标题
                field: "domain_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[1];
                // }
            },
            {
                title: "群体人数",//标题
                field: "group_size",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
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
                },
            },
            {
                title: "创建方式",//标题
                field: "create_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "创建进度",//标题
                field: "compute_status",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "描述",//标题
                field: "description",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.description==''||row.description=='null'||row.description=='unknown'||!row.description){
                        return '无描述';
                    }else {
                        return row.description;
                    };
                },
            },
            {
                title: "备注",//标题
                field: "remark",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.remark==''||row.remark=='null'||row.remark=='unknown'||!row.remark){
                        return '无备注';
                    }else {
                        return row.remark;
                    };
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
                    return '<a style="cursor: pointer;color: white;" onclick="seeDesGroup(\''+row.domain_name+'\',\'show_domain_group_detail_portrait\')" class="icon icon-group" title="查看群体"></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color: white;" onclick="seeDesGroup(\''+row.domain_name+'\',\'show_domain_description\')" class="icon icon-paste" title="查看描述"></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color: white;" onclick="refresh(\''+row.domain_name+'\',\'show_domain_role_info\')" class="icon icon-repeat" title="更新"></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color: white;" onclick="delt()" class="icon icon-trash" title="删除"></a>';
                },
            },
        ],
    });
};
//查看描述
var g='',$domain='';
function seeDesGroup(name,midUrl) {
    g=midUrl;$domain=name;
    var seeDesGroup_url='/weibo_xnr_knowledge_base_management/'+midUrl+'/?xnr_user_no='+ID_Num+'&domain_name='+name;
    public_ajax.call_request('get',seeDesGroup_url,DesGroup)
}
//'/weibo_xnr_knowledge_base_management/show_domain_role_info/?domain_name='+$domain+'&role_name=草根'
function DesGroup(data) {
    console.log(data);
    if (g=='show_domain_description'){
        var desc=data['description'],des='';
        if (desc==''||desc=='null'||desc=='unknown'||!desc){
            des='无描述';
        }else {
            des = desc;
        };
        $('#groupDepict #gd-1').text(des);
        character_topic(data['role_distribute'],'gd-2','角色分类');
        character_topic(data['topic_preference'],'gd-3','词汇偏好');
        words(data['word_preference']);
        $('#groupDepict').modal('show');
    }else {
        groupList(data);
        $('#allGroup').modal('show');
    }
}
//角色分类-----词汇偏好
function character_topic(data,box,title) {
    var leg=[],every=[];
    $.each(data,function (index,item) {
        leg.push(item[0]);
        every.push({value:item[1], name:item[0]});
    })
    var myChart = echarts.init(document.getElementById(box),'dark');
    var option = {
        backgroundColor:'transparent',
        title : {
            text: title,
            left:'right'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: leg
        },
        series : [
            {
                name: title.substring(0,2),
                type: 'pie',
                radius : '55%',
                center: ['550', '50%'],
                data:every,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    myChart.setOption(option);
}
//话题偏好
function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')'
        }
    };
}
function words(data) {
    var word=[];
    $.each(data,function (index,item) {
        word.push(
            {
                name: item[0],
                value: item[1],
                textStyle: createRandomItemStyle()
            }
        )
    })
    var myChart = echarts.init(document.getElementById('gd-4'),'dark');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: '话题偏好',
            left:'right'
        },
        tooltip: {
            show: true
        },
        series: [{
            name: '话题',
            type: 'wordCloud',
            size: ['80%', '80%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            data: word
        }]
    };
    myChart.setOption(option);
}
//群体成员
function groupList(data) {
    $('#grouplist').bootstrapTable('load', data);
    $('#grouplist').bootstrapTable({
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
                title: "头像",//标题
                field: "photo_url",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'||!row.photo_url){
                        return '<img src="/static/images/unknown.png" style="width: 30px;height: 30px;"/>';
                    }else {
                        return '<img src="'+row.photo_url+'" style="width: 30px;height: 30px;"/>';
                    };
                }
            },
            {
                title: "用户ID",//标题
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "昵称",//标题
                field: "nick_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'||!row.nick_name){
                        return '<a style="cursor: pointer;color: white;text-decoration: underline;" href="'+row.home_page+'">'+row.uid+'</a>';
                    }else {
                        return '<a style="cursor: pointer;color: white;text-decoration: underline;" href="'+row.home_page+'">'+row.nick_name+'</a>';
                    };
                }
            },
            {
                title: "身份敏感度",//标题
                field: "sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.sensitive==''||row.sensitive=='null'||row.sensitive=='unknown'||!row.sensitive){
                        return 0;
                    }else {
                        return row.sensitive;
                    };
                }
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.influence==''||row.influence=='null'||row.influence=='unknown'||!row.influence){
                        return 0;
                    }else {
                        return row.influence.toFixed(2);
                    };
                }
            },
            {
                title: "粉丝数",//标题
                field: "fans_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.fans_num==''||row.fans_num=='null'||row.fans_num=='unknown'||!row.fans_num){
                        return 0;
                    }else {
                        return row.fans_num;
                    };
                }
            },
            {
                title: "朋友数",//标题
                field: "friends_num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.friends_num==''||row.friends_num=='null'||row.friends_num=='unknown'||!row.friends_num){
                        return 0;
                    }else {
                        return row.friends_num;
                    };
                }
            },
            {
                title: "活跃地",//标题
                field: "location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.location==''||row.location=='null'||row.location=='unknown'||!row.location){
                        return '未知';
                    }else {
                        return row.location;
                    };
                }
            },
            {
                title: "关系",//标题
                field: "weibo_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.weibo_type==''||row.weibo_type=='null'||row.weibo_type=='unknown'||!row.weibo_type){
                        return '未知';
                    }else {
                        return row.weibo_type;
                    };
                },
            },
        ],
    });
}

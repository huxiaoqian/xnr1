//创建一个知识库
$('.way').attr('placeholder','请输入关键词（多个请用逗号分隔）');
$('.b-1-2 .keyUser input:radio[name="deadio"]').on('click',function () {
    var _val=$(this).val();
    if(_val=='by_keywords&keywords_string'){
        $('.way').val('').attr('placeholder','请输入关键词（多个请用逗号分隔）').show();
        $('.uidlist').hide();
    }else if(_val=='by_seed_users&seed_users'){
        $('.way').val('').attr('placeholder','请输入用户UID（多个请用逗号分隔）').show();
        $('.uidlist').hide();
    }else {
        $('.way').hide();
        $('.uidlist').show();
    }
});
var lab_list={'by_seed_users':'按种子用户','by_keywords':'按关键词','by_all_users':'按所有用户'};
var labType_list={'by_seed_users':'seed_users','by_keywords':'keywords_string','by_all_users':'all_users'};
var filesUID='';
function filelist(files) {
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var uidLIST = oFREvent.target.result;
            filesUID = uidLIST.toString().replace(/,/g,'，');
        };
        reader.readAsText(f,'GB2312');
    }
}
$('.addBuild').on('click',function () {
    var domainName=$('.name').val();
    var description=$('.description').val();
    var remark=$('.remarks').val();
    var word_user='';
    var Type=$('.b-1-2 .keyUser input:radio[name="deadio"]:checked').val();
    var param=Type.split('&');
    if(Type=='by_keywords&keywords_string'||Type=='by_seed_users&seed_users'){
        word_user=$('.way').val().toString().replace(/,/g,'，');
    }else {
        word_user=filesUID;
    }
    if (domainName||description||word_user){
        var creat_url='/weibo_xnr_knowledge_base_management/create_domain/?xnr_user_no='+ID_Num+'&domain_name='+domainName+
            '&description='+description+'&submitter='+admin+'&remark='+remark+
            '&create_type='+param[0]+'&'+param[1]+'='+word_user;
        public_ajax.call_request('get',creat_url,successFail);
    }else {
        $('#pormpt p').text('检查输入的信息（不能为空）');
        $('#pormpt').modal('show');
    }

})
function successFail(data) {
    var f='操作成功';
    if(!data){f='操作失败'}else {public_ajax.call_request('get',libGroup_url,group)};
    if ($$new=='0'&&data=='domain name exists!'){
        f='该领域名称已经存在了，请换一个。';
    }else {
        $$new='0';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
var libGroup_url='/weibo_xnr_knowledge_base_management/show_domain_group_summary/?submitter='+admin;
public_ajax.call_request('get',libGroup_url,group);
function group(data) {
    var person=eval(data);
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
                formatter: function (value, row, index) {
                    if (row.domain_name==''||row.domain_name=='null'||row.domain_name=='unknown'||!row.domain_name){
                        return '未知';
                    }else {
                        return row.domain_name;
                    };
                }
            },
            {
                title: "群体人数",//标题
                field: "group_size",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.compute_status=='0'){return '未知'} else {return row.group_size}
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
                formatter: function (value, row, index) {
                    if (row.create_type==''||row.create_type=='null'||row.create_type=='unknown'||!row.create_type){
                        return '未知';
                    }else {
                        var crType=JSON.parse(row.create_type);
                        for (var k in crType){
                            if (crType[k].length!=0){
                                return lab_list[k];
                            }
                        }
                    };
                },
            },
            {
                title: "创建进度",//标题
                field: "compute_status",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.compute_status=='0'){return '尚未计算'}
                    else if (row.compute_status=='1'){return '正在计算'}
                    else {return '计算完成'}
                },
            },
            {
                title: "关键词",//标题
                field: "create_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var crType=JSON.parse(row.create_type);
                    for (var k in crType){
                        if (crType[k].length!=0){
                            if (crType[k][0]==""){
                                return '无';
                            }else{
                                return crType[k].join(',');
                            };
                        }else {
                            return '未知';
                        }
                    }
                },
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
                    var crType=JSON.parse(row.create_type),thisType,thisUser;
                    for (var k in crType){
                        if (crType[k].length!=0){
                            thisType = k;
                            thisUser =crType[k];
                        }
                    }
                    var dis1='disabled',dis2='disabled';
                    if (row.compute_status=='1'){dis1=''}
                    else if (Number(row.compute_status) > 1){dis1='';dis2=''}
                    return '<a style="cursor: pointer;color: white;" onclick="seeDesGroup(\''+row.domain_name+'\',\'show_domain_description\',\'show_domain_group_detail_portrait\')" class="icon icon-paste '+dis2+'" title="查看详情"></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color: white;" onclick="refresh(\''+row.domain_name+'\',\''+row.description+'\',\''+row.remark+'\',\''+thisType+'\',\''+thisUser+'\')" class="icon icon-repeat" title="更新"></a>&nbsp;&nbsp;'+
                        '<a style="cursor: pointer;color: white;" onclick="deltDomain(\''+row.domain_name+'\')" class="icon icon-trash" title="删除"></a>';
                        // '<a style="cursor: pointer;color: white;" onclick="seeDesGroup(\''+row.domain_name+'\',\'show_domain_group_detail_portrait\')" class="icon icon-group '+dis1+'" title="查看群体"></a>&nbsp;&nbsp;'+
                        // '<a style="cursor: pointer;color: white;" onclick="seeDesGroup(\''+row.domain_name+'\',\'show_domain_description\')" class="icon icon-paste '+dis2+'" title="查看描述"></a>&nbsp;&nbsp;'+
                        // '<a style="cursor: pointer;color: white;" onclick="refresh(\''+row.domain_name+'\',\''+row.description+'\',\''+row.remark+'\',\''+thisType+'\',\''+thisUser+'\')" class="icon icon-repeat" title="更新"></a>&nbsp;&nbsp;'+
                        // '<a style="cursor: pointer;color: white;" onclick="delt(\''+row.domain_name+'\')" class="icon icon-trash" title="删除"></a>';
                },
            },
        ],
    });
};
//查看描述
var g='',$domain='';
// function seeDesGroup(name,midUrl) {
//     g=midUrl;$domain=name;
//     var seeDesGroup_url='/weibo_xnr_knowledge_base_management/'+midUrl+'/?xnr_user_no='+ID_Num+'&domain_name='+name;
//     public_ajax.call_request('get',seeDesGroup_url,DesGroup)
// }
function seeDesGroup(name,midUrl_1,midUrl_2) {
    $domain=name;
    var seeDesGroup_url_1='/weibo_xnr_knowledge_base_management/'+midUrl_1+'/?domain_name='+name;
    public_ajax.call_request('get',seeDesGroup_url_1,DesGroup_1)
    var seeDesGroup_url_2='/weibo_xnr_knowledge_base_management/'+midUrl_2+'/?domain_name='+name;
    public_ajax.call_request('get',seeDesGroup_url_2,groupList);
    $('.titleMain').text(name);
}
function DesGroup_1(data) {
    var desc=data['description'],des='';
    if (desc==''||desc=='null'||desc=='unknown'||!desc){
        des='无描述';
    }else {
        des = desc;
    };
    $('.allGroup_div #_gd').text(des);
    character_topic(data['role_distribute'],'gd-2','角色分类');
    character_topic(data['topic_preference'],'gd-3','话题偏好');
    words(data['word_preference']);
    $('.allGroup_div').show();
    // $('.loadGO').hide();
}
// function DesGroup(data) {
//     console.log(data);
//     if (g=='show_domain_description'){
//         var desc=data['description'],des='';
//         if (desc==''||desc=='null'||desc=='unknown'||!desc){
//             des='无描述';
//         }else {
//             des = desc;
//         };
//         $('#groupDepict #gd-1').text(des);
//         character_topic(data['role_distribute'],'gd-2','词汇偏好');
//         character_topic(data['topic_preference'],'gd-3','角色分类');
//         words(data['word_preference']);
//         $('#groupDepict').modal('show');
//     }else {
//         groupList(data);
//         $('#allGroup').modal('show');
//     }
// }
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
            text: '词汇偏好',
            left:'right'
        },
        tooltip: {
            show: true
        },
        series: [{
            name: '词汇',
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
function goPeople($href) {
    window.open($href);
}
function groupList(data) {
    console.log(data)
    $('#grouplist').bootstrapTable('load', data);
    $('#grouplist').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 5,//单页记录数
        pageList: [15,20,25],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: true,//回车搜索
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
                        return '<img src="/static/images/unknown.png" style="width: 30px;height: 30px;cursor: pointer;"  onclick="goPeople(\''+row.home_page+'\')"/>';
                    }else {
                        return '<img src="'+row.photo_url+'" style="width: 30px;height: 30px;cursor: pointer;" onclick="goPeople(\''+row.home_page+'\')"/>';
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
            // {
            //     title: "关系",//标题
            //     field: "weibo_type",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         if (row.weibo_type==''||row.weibo_type=='null'||row.weibo_type=='unknown'||!row.weibo_type){
            //             return '未知';
            //         }else {
            //             var user='';
            //             if (row.weibo_type=='follow'){
            //                 user='已关注用户';
            //             }else if (row.weibo_type=='friend'){
            //                 user='相互关注用户';
            //             }else if (row.weibo_type=='stranger'||row.weibo_type=='followed'){
            //                 user='未关注用户';
            //             }
            //             return user;
            //         };
            //     },
            // },
        ],
    });
    $('#grouplist p').hide();
    // $('.groupDepict_div').show();
}
//更新
var $$new='0';
function refresh(domainName,description,remark,create_type,word_user) {
    $$new='1';
    var upNew_url='/weibo_xnr_knowledge_base_management/create_domain/?domain_name='+domainName+
        '&description='+description+'&submitter='+admin+'&remark='+remark+
        '&create_type='+create_type+'&'+labType_list[create_type]+'='+word_user;
    public_ajax.call_request('get',upNew_url,successFail);
}
//删除
var del_Domain_id='';
function deltDomain(domain) {
    del_Domain_id=domain;
    $('#delt').modal('show');
}
function delt() {
    var delte_url='/weibo_xnr_knowledge_base_management/delete_domain/?domain_name='+del_Domain_id;
    public_ajax.call_request('get',delte_url,successFail);
}
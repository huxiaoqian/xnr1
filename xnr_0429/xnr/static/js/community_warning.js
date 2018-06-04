// 跟踪社区列表
var fg=1;
var community_1_url='/weibo_xnr_community/show_trace_community/?xnr_user_no='+ID_Num;
public_ajax.call_request('GET',community_1_url,trackCommunity);
// 新发现社区列表
function newCommunity() {
    setTimeout(function () {
        fg=0;
        var community_2_url='/weibo_xnr_community/show_new_community/?xnr_user_no='+ID_Num;
        public_ajax.call_request('GET',community_2_url,trackCommunity);
    },500);
}
var idBOX='#track-community',_visable=false;
var trackCommunityData={};
function trackCommunity(data){
    $(idBOX).bootstrapTable('load', data);
    $(idBOX).bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize:10,//单页记录数
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
                title: "社区名称",//标题
                field: "community_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.community_name == '' || row.community_name == 'null' || row.community_name == 'unknown'||!row.community_name) {
                        return row.community_id;
                    } else {
                        var b='<i class="icon icon-bell-alt" onclick="isSuretrack(\''+row.community_id+'\')" ' +
                            'style="display:inline-block;margin-right:10px;cursor: pointer;color: #fa7d3c;"></i>';
                        // if (row.trace_message){}
                        var str = b + row.community_name;
                        return str;
                    };
                }
            },
            {
                title: "预警级别",//标题
                field: "warning_rank",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if(row.warning_rank=='null'||row.warning_rank=='unknown'||row.warning_rank<0){row.warning_rank=0}
                    var a='<i class="icon icon-star" style="color:#fa7d3c;"></i>  ';
                    var b='<i class="icon icon-star-empty" style="color:#fa7d3c;"></i>  ';
                    return a.repeat(row.warning_rank)+b.repeat(4-row.warning_rank);
                }
            },
            {
                title: "预警原因",//标题
                field: "warning_type",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.warning_type==''||row.warning_type=='null'||row.warning_type=='unknown'||!row.warning_type){
                        return '无预警';
                    }else {
                        return row.warning_type.join('，');
                    }
                }
            },
            {
                title: "人数",//标题
                field: "num",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.num == 'null' || row.num == 'unknown') {
                        return '未知';
                    } else {
                        return row.num;
                    };
                }
            },
            {
                title: "聚集系数",//标题
                field: "density",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.density==''||row.density=='null'||row.density=='unknown'||!row.density){
                        return '未知';
                    }else {
                        return row.density.toFixed(4);
                    }
                }
            },
            {
                title: "最大影响力",//标题
                field: "max_influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.max_influence=='null'||row.max_influence=='unknown'){
                        return '未知';
                    }else {
                        return row.max_influence.toFixed(4);
                    }
                }
            },
            {
                title: "平均影响力",//标题
                field: "mean_influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.mean_influence==''||row.mean_influence=='null'||row.mean_influence=='unknown'||!row.mean_influence){
                        return '未知';
                    }else {
                        return row.mean_influence.toFixed(4);
                    }
                }
            },
            {
                title: "最大敏感度",//标题
                field: "max_sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.max_sensitive==''||row.max_sensitive=='null'||row.max_sensitive=='unknown'||!row.max_sensitive){
                        return '未知';
                    }else {
                        return row.max_sensitive.toFixed(4);
                    }
                }
            },
            {
                title: "平均敏感度",//标题
                field: "mean_sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.mean_sensitive=='null'||row.mean_sensitive=='unknown'){
                        return '未知';
                    }else {
                        return row.mean_sensitive.toFixed(4);
                    }
                }
            },
            {
                title: "综合评分",//标题
                field: "total_score",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:_visable,
                formatter: function (value, row, index) {
                    if (row.total_score=='null'||row.total_score=='unknown'){
                        return '未知';
                    }else {
                        return row.total_score.toFixed(4);
                    }
                }
            },
            {
                title: "社区操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor:pointer;color:white;" onclick="communityIntroduction(\''+row.community_id+'\')" title="社区简介"><i class="icon icon-info-sign"></i></span>'+
                        '<span style="cursor:pointer;color:white;margin:0 15px;" onclick="jumpFrame(\''+row.community_id+'\',1)" title="社区详情"><i class="icon icon-file-alt"></i></span>'+
                        '<span style="cursor:pointer;color:white;" onclick="jumpFrame_1(\''+row.community_id+'\',\''+fg+'\')" title="预警详情"><i class="icon icon-warning-sign"></i></span>';
                }
            },
        ],
    });
    $(idBOX+' p').slideUp(30);
    $.each(data,function (index,item) {
        trackCommunityData[item.community_id]=item;
    });
    if(idBOX=='#track-community'){idBOX='#new-track-community',_visable=true;newCommunity()};
};
//弹出是否强制、取消跟踪
var this_community_id='';
function isSuretrack(_id) {
    this_community_id=_id;
    if(trackCommunityData[_id].trace_message){$('.tk1').hide();$('.tk2').show()}
    else {$('.tk1').show();$('.tk2').hide()}
    $('#trackModal h5').text(trackCommunityData[_id].trace_message||'该社区暂无预警信息。');
    $('#trackModal').modal('show');
}
function sureTrackModal() {
    var status=$('#trackModal input[name="trackIS"]:checked').val();
    var sureTrack_url='/weibo_xnr_community/update_trace_status/?community_id='+this_community_id+'&trace_status='+status;
    public_ajax.call_request('GET',sureTrack_url,SF);
}
function SF(data) {
    var s='操作失败';
    if (data){s='操作成功'}
    $('#pormpt p').text(s);
    $('#pormpt').modal('show');
}

// 跳转社区详情页
function jumpFrame(id,flag){
    // 阻止默认事件
    // e.stopPropagation();
    var communityName=trackCommunityData[id]['community_name'],communityTime=trackCommunityData[id]['update_time'],
        communityPeople=trackCommunityData[id]['num'];
    var html = '/monitor/communityDetails/?communityID='+Check(id)+'&communityName='+communityName+'&communityTime='+communityTime
    +'&communityPeople='+communityPeople+'&flag='+flag;
    window.open(html);
}
// 跳转预警详情页
function jumpFrame_1(id,flag){
    // 阻止默认事件
    // e.stopPropagation();
    var html = '/monitor/communityWaringdetails/?comId='+id+'&oldNew='+flag+'&flag='+flag;
    window.open(html);
}
//社区简介
function communityIntroduction(_id) {
    var m=JSON.parse(trackCommunityData[_id]['core_user']);
    show_influ_users(m);
    var n=JSON.parse(trackCommunityData[_id]['socail_keyword']);
    basic(n)
    $('#introduction').modal('show');
}
// 核心人物列表
function show_influ_users(data){
    $('#person-list').bootstrapTable('load', data);
    $('#person-list').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize:5,//单页记录数
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
                title: "昵称",//标题
                field: "nick_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if(row.photo_url == '' || row.photo_url == 'null' || row.photo_url == 'unknown'||!row.photo_url){
                        img='<img style="width: 32px;height: 32x;" src="/static/images/unknown.png"/>  ';
                    }else {
                        img='<img style="width: 32px;height: 32px;" src="'+row.photo_url+'"/>   ';
                    };
                    if (row.nick_name == '' || row.nick_name == 'null' || row.nick_name == 'unknown'||!row.nick_name) {
                        return img+row.uid;
                    } else {
                        return img+row.nick_name;
                    };
                }
            },
            {
                title: "性别",//标题
                field: "sex",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.sex==''||row.sex=='null'||row.sex=='unknown'||!row.sex){
                        return '未知';
                    }else {
                        if (row.sex==1){return '男'}else
                        if (row.sex==2){return '女'}else
                        {return '未知'}
                    }
                }
            },
            {
                title: "注册地",//标题
                field: "user_location",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.user_location == 'null' || row.user_location == 'unknown'||row.user_location==''||!row.user_location) {
                        return '未知';
                    } else {
                        return row.user_location;
                    };
                }
            },
            {
                title: "好友数",//标题friendsnum
                field: "friendsnum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.friendsnum==''||row.friendsnum=='null'||row.friendsnum=='unknown'||!row.friendsnum){
                        return '未知';
                    }else {
                        return row.friendsnum;
                    }
                }
            },
            {
                title: "粉丝数",//标题
                field: "fansnum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.fansnum=='null'||row.fansnum=='unknown'||row.fansnum==''|| !row.fansnum){
                        return '未知';
                    }else {
                        return row.fansnum;
                    }
                }
            },
        ],
    });
};
function basic(data){
    var wordData=[];
    $.each(data,function (index,item) {
        wordData.push({name:item[0], value: item[1]})
    });
    var myChart = echarts.init(document.getElementById('keyword'),'chalk');
    var option = {
        backgroundColor:'transparent',
        tooltip: {
            show: true
        },
        series: [{
            name: '',
            type: 'wordCloud',
            size: ['80%', '80%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            textStyle : {
                normal : {
                    fontFamily:'sans-serif',
                    color : function() {
                        return 'rgb('
                            + [ Math.round(Math.random() * 128+127),
                                Math.round(Math.random() * 128+127),
                                Math.round(Math.random() * 128+127) ]
                                .join(',') + ')';
                    }
                },
                emphasis : {
                    shadowBlur : 5,  //阴影距离
                    shadowColor : '#333'  //阴影颜色
                }
            },
            data:wordData
        }]
    };
    myChart.setOption(option);
}

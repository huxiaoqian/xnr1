var relatedUrl='/facebook_xnr_operate/related_recommendation/?xnr_user_no='+ID_Num+'&sort_item=sensitive';
public_ajax.call_request('get',relatedUrl,related);
function related(data) {
    $.each(data,function (index,item) {
        detList[item.uid]=item;
    });
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
                title: "用户UID",//标题
                field: "uid",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "敏感度",//标题
                field: "sensitive",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // visible:false
            },
            {
                title: "粉丝数",//标题
                field: "fansnum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直

            },
            {
                title: "好友数",//标题
                field: "friendsnum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直

            },
            {
                title: "帖子数",//标题
                field: "statusnum",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: '操作',//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var fol='';
                    if (row.weibo_type=='follow'){
                        fol='已关注';
                    }else if (row.weibo_type=='friends'){
                        fol='相互关注';
                    }else {//if (row.weibo_type=='stranger'||row.weibo_type=='followed')
                        fol='未关注';
                    }
                    return '<span style="cursor: pointer;" onclick="lookDetails(\''+row.uid+'\')" title="查看详情"><i class="icon icon-file-alt"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<span style="cursor: pointer;" onclick="driectFocus(\''+row.uid+'\',this)" title="'+fol+'"><i class="icon icon-star-empty"></i></span>';
                },
            },
        ],
    });
    $('.influence .search .form-control').attr('placeholder','输入关键词快速搜索（回车搜索）');
    $('#influe p').slideUp(700);
    $('.influence').show();
}
$('#influence').bootstrapTable('hideColumn', 'sensitive');
function showHide(_tp$) {
    if (_tp$=='sensitive'){
        $('#influence').bootstrapTable('showColumn', 'sensitive');
    }else {
        $('#influence').bootstrapTable('hideColumn', 'sensitive');
    }
}
$('#container .suggestion #myTabs li').on('click',function () {
    var ty=$(this).attr('tp');
    //idNAME=ty;
    $('.influence').hide();
    $('#influe p').show();
    var relatedUrl='/facebook_xnr_operate/related_recommendation/?xnr_user_no='+ID_Num+'&sort_item='+ty;
    public_ajax.call_request('get',relatedUrl,related);
    showHide(ty);
})
//直接搜索
$('.findSure').on('click',function () {
    var ids=$('.active-1-find').val();
    if (ids==''){
        $('#pormpt p').text('搜索内容不能为空。');
        $('#pormpt').modal('show');
    }else {
        ids=ids.replace(/,/g,'，');
        idNAME='searchResult';
        $('.influence').hide();
        $('#influe p').show();
        var searchUrl='/facebook_xnr_operate/direct_search/?xnr_user_no='+ID_Num+'&sort_item=sensitive&uids='+ids;
        public_ajax.call_request('get',searchUrl,related);
        $('.searchResult').slideDown(30);
    }
});
//查看详情
var detList={};
function lookDetails(puid) {
    var person=detList[puid];
    if (person.portrait_status== true){
        var name,img,gender,domain,location,topic_string,weibo_type;
        if (person.uname==''||person.uname=='unknown'||person.uname=='null'){
            name='未知';
        }else {
            name=person.uname;
        }
        if (person.photo_url==''||person.photo_url=='unknown'||person.photo_url=='null'){
            img='/static/images/unknown.png';
        }else {
            img=person.photo_url;
        }
        if (person.domain==''||person.domain=='unknown'||person.domain=='null'){
            domain='未知';
        }else {
            domain=person.domain;
        }
        if (person.location==''||person.location=='unknown'||person.location=='null'){
            location='未知';
        }else {
            location=person.location;
        }
        if (person.topic_string==''||person.topic_string=='unknown'||person.topic_string=='null'){
            topic_string='未知';
        }else {
            topic_string=person.topic_string.replace(/&/g,'-');
        }
        if (person.gender==1){gender='男'}else if (person.gender==2){gender='女'}else{gender='未知'}
        if (person.weibo_type=='follow'){
            weibo_type='已关注';
        }else if (person.weibo_type=='friends'){
            weibo_type='相互关注';
        }else {//if (person.weibo_type=='stranger'||person.weibo_type=='followed')
            weibo_type='未关注';
        }
        $('#details .uid').text(person.uid);
        $('#details .details-name').text(name);
        $('#details .det11').text(name).attr('title',name);
        $('#details .det22').text(domain).attr('title',domain);
        $('#details .det33').text(location).attr('title',location);
        $('#details .det44').text(gender).attr('title',gender);
        $('#details .addFOCUS b').text(weibo_type);
        $('#details .det55').text(topic_string).attr('title',topic_string);
        $('#details .det-2-num').text(Math.ceil(person.influence));
        $('#details .headImg').attr('src',img);

    };
    if (person.portrait_status== false){
        $('#details .details-name').html('该人物未入库，暂无画像信息');
        $('#details .details-1').hide();
        $('#details .details-2').hide();
        $('#details .addFOCUS').hide();
    }
    var str='';
    if (person.weibo_list.length==0){
        str='暂无代表微博';
    }else {
        $.each(person.weibo_list,function (index,item) {
            str+=
                '<div><i class="icon icon-tint"></i>&nbsp;<b class="det-3-content">'+item.text+'</b></div>'
        })
    };

    $('#details .det-3-info').html(str);
    $('#details').modal('show');
}
//直接关注
function driectFocus(uid,_this) {
    var foc_url,mid='';
    if (!uid){uid=$(_this).prev().text()}
    var f=$(_this).attr('title');
    if (f=='未关注'){
        mid='follow_operate';
    }else {
        mid='unfollow_operate';
    }
    foc_url='/facebook_xnr_operate/'+mid+'/?xnr_user_no='+ID_Num+'&uid='+uid;
    public_ajax.call_request('get',foc_url,sucFai)
}
//提示
function sucFai(data) {
    var m='';
    if (data[0]||data){
        m='操作成功';
    }else {
        m='操作失败';
    }
    $('#pormpt p').text(m);
    $('#pormpt').modal('show');
}





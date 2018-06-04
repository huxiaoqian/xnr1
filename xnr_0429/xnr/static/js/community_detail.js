// 社区成员列表  member-change-1，社区成员变化列表 member-change-2
var community_user_url='/weibo_xnr_community/get_community_detail/?model=user&community_id='+communityId;
public_ajax.call_request('GET',community_user_url,community_user);
$('#myTabs li').on('click',function () {
    var modal=$(this).attr('thisModal');
    var task=$(this).attr('task');
    var mid='';
    if (task=='socialContent'){var a=$('.orderType input:checked').val();mid='&order_by='+a;}
    var task_url='/weibo_xnr_community/get_community_detail/?model='+modal+'&community_id='+communityId+mid;
    public_ajax.call_request('GET',task_url,window[task]);
});
// 新发现社区列表
function newChangeUser() {
    setTimeout(function () {
        var community_userNew_url='/weibo_xnr_community/show_new_community/?xnr_user_no='+ID_Num;
        public_ajax.call_request('GET',community_userNew_url,community_user);
    },500);
};
var idBOX='#member-change-1',_visable=false;
function community_user(data) {
    var thisData=data['community_user_list'];
    if (idBOX=='#member-change-2'){thisData=data['community_user_change']};
    $(idBOX).bootstrapTable('load', thisData);
    $(idBOX).bootstrapTable({
        data:thisData,
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
                    var img;
                    if(row.photo_url == '' || row.photo_url == 'null' || row.photo_url == 'unknown'||!row.photo_url){
                        img='<img style="width: 32px;height: 32x;" src="/static/images/unknown.png"/>  ';
                    }else {
                        img='<img style="width: 32px;height: 32x;" src="'+row.photo_url+'"/>   ';
                    };
                    //重点用户
                    var zd='';
                    if (row.core_user==1){zd='  <i class="icon icon-ok-sign" title="核心用户" style="color:salmon;"></i>'};
                    //----
                    if (row.nick_name == '' || row.nick_name == 'null' || row.nick_name == 'unknown'||!row.nick_name) {
                        return img+row.uid+zd;
                    } else {
                        return img+row.nick_name+zd;
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
            {
                title: "变化类型",//标题
                field: "change",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                visible:_visable,
                formatter: function (value, row, index) {
                    if (row.change==1){
                        return '新增成员';
                    }else if (row.change==-1){
                        return '删减人员';
                    }else if (row.change==0){
                        return '无变化';
                    }else {
                        return '未知';
                    }
                }
            },
        ],
    });
    $(idBOX+' p').slideUp(30);
    if(idBOX=='#member-change-1'){idBOX='#member-change-2',_visable=true;newChangeUser()};
}
// 社区内容
// var community_content_url='/weibo_xnr_community/get_community_detail/?model=content&order_by=sensitive&community_id='+communityId;
// public_ajax.call_request('GET',community_content_url,socialContent);
function socialContent(data) {
    basicWORD(data['sensitive_wordcloud'],'basic-1','敏感词关键词云');
    setTimeout(function () {
        basicWORD(data['topic_wordcloud'],'basic-2','微话题关键词云');
    },500);
    basicPOST(data['content_post']);
}
function basicWORD(data,id,_title){
    if (isEmptyObject(data)){
        $('#'+id).css({textAlign:'center',lineHeight:'300px'}).text(_title+'暂无数据');
        return false;
    }
    var wordData=[];
    for(var k in data){
        wordData.push({name:k, value: data[k]})
    };
    var myChart = echarts.init(document.getElementById(id),'chalk');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: _title,
            textStyle:{
                color:'#fff'
            }
        },
        tooltip: {
            show: true
        },
        toolbox:{
            show:false,
            feature:{
                saveAsImage:{
                    show:false
                }
            },
            color:'#fff',
            effectiveColor:'#2a556f'
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
    // 为echarts对象加载数据
    myChart.setOption(option);
};
// 典型帖子
$('.orderType input').on('click',function () {
    $('.basic-3-content').children().hide();
    $('.basic-3-content p').show();
    var _val=$(this).val();
    var community_content_url='/weibo_xnr_community/get_community_detail/?model=content&order_by='+_val+'&community_id='+communityId;
    public_ajax.call_request('GET',community_content_url,socialContent);
});
function basicPOST(data){
    $('#basic-3-content').bootstrapTable('load', data);
    $('#basic-3-content').bootstrapTable({
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var item=row;
                    var name,text,text2,time,all='',img;
                    if (item.nick_name==''||item.nick_name=='null'||item.nick_name=='unknown'||!item.nick_name){
                        name=item.uid;
                    }else {
                        name=item.nick_name;
                    };
                    if (item.photo_url==''||item.photo_url=='null'||item.photo_url=='unknown'||!item.photo_url){
                        img='/static/images/unknown.png';
                    }else {
                        img=item.photo_url;
                    };
                    if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text){
                        text='暂无内容';
                    }else {
                        if (item.sensitive_words_string||!isEmptyObject(item.sensitive_words_string)){
                            var s=item.text;
                            var keywords=item.sensitive_words_string.split('&');
                            for (var f=0;f<keywords.length;f++){
                                s=s.toString().replace(new RegExp(keywords[f],'g'),'<b style="color:#ef3e3e;">'+keywords[f]+'</b>');
                            }
                            text=s;

                            var rrr=item.text;
                            if (rrr.length>=160){
                                rrr=rrr.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                rrr=item.text;
                                all='none';
                            }
                            for (var f of keywords){
                                rrr=rrr.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                            text2=rrr;
                        }else {
                            text=item.text;
                            if (text.length>=160){
                                text2=text.substring(0,160)+'...';
                                all='inline-block';
                            }else {
                                text2=text;
                                all='none';
                            }
                        };
                    };
                    if (item.timestamp==''||item.timestamp=='null'||item.timestamp=='unknown'||!item.timestamp){
                        time='未知';
                    }else {
                        time=getLocalTime(item.timestamp);
                    };
                    var rel_str=
                        '<div class="everySpeak everyUser" style="margin:0 auto;width: 100%;text-align: left;">'+
                        '        <div class="speak_center">'+
                        '            <div class="center_rel">'+
                        '                <img src="'+img+'" alt="" class="center_icon">'+
                        '                <a class="center_1 centerNAME" style="color:#f98077;">'+name+'</a>'+
                        '                <a class="mid" style="display: none;">'+item.mid+'</a>'+
                        '                <a class="uid" style="display: none;">'+item.uid+'</a>'+
                        '                <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                        '                <a class="_id" style="display: none;">'+item._id+'</a>'+
                        '                <span class="time" style="font-weight: 900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                        '                <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                        '                <p class="allall1" style="display:none;">'+text+'</p>'+
                        '                <p class="allall2" style="display:none;">'+text2+'</p>'+
                        '                <span class="center_2">'+text2+
                        '                </span>'+
                        '                <div class="center_3">'+
                        '                    <span class="cen3-1" onclick="retweet(this,\'预警\')"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                        '                    <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                        '                    <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '                    <span class="cen3-5" onclick="joinPolice(this,\'言论\')"><i class="icon icon-plus-sign"></i>&nbsp;&nbsp;加入预警库</span>'+
                        '                    <span class="cen3-9" onclick="robot(this)"><i class="icon icon-github-alt"></i>&nbsp;&nbsp;机器人回复</span>'+
                        '                    <span class="cen3-6" onclick="oneUP(this,\'言论\')"><i class="icon icon-upload-alt"></i>&nbsp;&nbsp;上报</span>'+
                        '                </div>'+
                        '               <div class="forwardingDown" style="width: 100%;display: none;">'+
                        '                   <input type="text" class="forwardingIput" placeholder="转发内容"/>'+
                        '                   <span class="sureFor" onclick="forwardingBtn()">转发</span>'+
                        '               </div>'+
                        '               <div class="commentDown" style="width: 100%;display: none;">'+
                        '                   <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '                   <span class="sureCom" onclick="comMent(this,\'预警\')">评论</span>'+
                        '               </div>'+
                        '            </div>'+
                        '        </div>';
                    return rel_str;
                }
            }

        ],
    });
    $('.basic-3-content').children().show();
    $('.basic-3-content p').slideUp(30);
}
// 社交特征
var divBox_1='social-content-1',divBox_2='social-content-2';
var socialData;
function social(data){
    socialData=data;
    var thisData=data;
    if (divBox_1=='social-content-1'&&divBox_2=='social-content-2'){
        thisData=data['core_user_socail'];
    };
    var allNode=[];
    var nodeList=[],linkList=[],categoriesList=[];
    $.each(thisData,function (index,item) {
        if(!(isInArray(allNode,item[0]))){
            nodeList.push({
                "name": item[0],//'用户id:'+item[0]+'<br/>用户名:'+item[1]
                "value": 10,
                "symbolSize": 10,
                "category": item[0],
                "draggable": "true"
            });
            categoriesList.push(item[0]);
            allNode.push(item[0]);
        }
        if(!(isInArray(allNode,item[2]))){
            nodeList.push({
                "name": item[2],
                "value": 10,
                "symbolSize": 10,
                "category": item[2],
                "draggable": "true"
            });
            categoriesList.push(item[2]);
            allNode.push(item[2]);
        }
        linkList.push({
            "source": item[0],
            "target": item[2]
        });
    });
    var myChart = echarts.init(document.getElementById(divBox_1),'chalk');
    myChart.showLoading();
    var option = {
        backgroundColor:'transparent',
        title:{
            text: "",
        },
        tooltip: {
            show:true,
            confine: true,
        },
        animationDuration: 3000,
        animationEasingUpdate: 'quinticInOut',
        series: [{
            name: '',
            type: 'graph',
            layout: 'force',
            force: {
                repulsion: 50
            },
            data: nodeList,
            links:linkList,
            categories:categoriesList,
            focusNodeAdjacency: true,
            roam: true,
            force: {
                repulsion: 70,
                gravity: 0.1,
                edgeLength: [150, 45]
                // layoutAnimation: true,
            },
            label: {
                normal: {
                    show: true,
                    position: 'top',
                }
            },
            lineStyle: {
                normal: {
                    color:'#fff',
                    width: 2,
                    type: "solid"
                }
            }
        }]
    };
    myChart.setOption(option);
    myChart.hideLoading();
    chartTable(thisData);
};
//表格
function chartTable(dataVal){
    var data=[];
    $.each(dataVal,function (index,item) {
        data.push({
            'id1':item[0],'name1':item[1],
            'id2':item[2],'name2':item[3],'count':item[4]
        })
    });
    $('#'+divBox_2).bootstrapTable('load', data);
    $('#'+divBox_2).bootstrapTable({
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
                title: "用户ID",//标题
                field: "id1",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.id1=='null'||row.id1=='unknown'||row.id1==''){
                        return '未知';
                    }else {
                        return row.id1;
                    }
                }
            },
            {
                title: "用户名",//标题
                field: "name1",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.name1=='null'||row.name1=='unknown'||row.name1==''){
                        return row.id1;
                    }else {
                        return row.name1;
                    }
                }
            },
            {
                title: "",//标题
                field: "",//键名
                sortable: false,//是否可排序
                order: "",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<img src="/static/images/arrow.png"/>'
                }
            },
            {
                title: "用户ID",//标题
                field: "id2",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.id2=='null'||row.id2=='unknown'||row.id2==''){
                        return '未知';
                    }else {
                        return row.id2;
                    }
                }
            },
            {
                title: "用户名",//标题
                field: "name2",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.name2=='null'||row.name2=='unknown'||row.name2==''){
                        return row.id2;
                    }else {
                        return row.name2;
                    }
                }
            },
            {
                title: "交互次数",//标题
                field: "count",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.count=='null'||row.count=='unknown'||row.count==''){
                        return '未知';
                    }else {
                        return row.count;
                    }
                }
            },
        ],
    });
    if (divBox_1=='social-content-1'&&divBox_2=='social-content-2'){
        setTimeout(function () {
            divBox_1='social-content-3',divBox_2='social-content-4';
            social(socialData['core_outer_socail']);
        },800)
    }
}


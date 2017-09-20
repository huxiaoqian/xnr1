var flag='',idbox='comment-1';
var xnrUser=ID_Num;
$('.copyFinish').on('click',function () {
    flag=$('#myTabs li.active').attr('flag');
    var _name=$(this).parent().prev().prev().find('b').text();
    var _dataType=$(this).attr('datatype');
    $(this).parents('.commentEvery').find('.'+_dataType+' .clone-1').attr('placeholder','回复'+_name);
    $(this).parent().next().show(40);
})
//type按键
$('#container .type_page #myTabs a').on('click',function () {
    var mmarrow=$(this).parent().attr('tp');
    idbox=$(this).parent().attr('idbox');
    var comURL='/weibo_xnr_operate/'+mmarrow+'/?xnr_user_no='+xnrUser+'&sort_item=timestamp';
    public_ajax.call_request('get',comURL,com);
})
//排序选择
$('#container .desc_index .demo-label input').on('click',function () {
    var tp1=$(this).val();
    var tp2=$('#myTabs li.active').attr('tp');
    var comURL='/weibo_xnr_operate/'+tp2+'/?xnr_user_no='+xnrUser+'&sort_item='+tp1;
    public_ajax.call_request('get',comURL,com);
})
//评论回复----转发回复
var comURL='/weibo_xnr_operate/show_comment/?xnr_user_no='+xnrUser+'&sort_item=timestamp';
public_ajax.call_request('get',comURL,com);
function com(data) {
    if (idbox=='comment-1'||idbox=='forwarding-1'){
        var mid;
        if (idbox=='comment-1'){mid='reply_comment'}else {mid='reply_retweet'}
        $('#'+idbox).bootstrapTable('load', data);
        $('#'+idbox).bootstrapTable({
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
                    title: "",//标题
                    field: "",//键名
                    sortable: true,//是否可排序
                    order: "desc",//默认排序方式
                    align: "center",//水平
                    valign: "middle",//垂直
                    formatter: function (value, row, index) {
                        var name,txt,img;
                        if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                            name='未命名';
                        }else {
                            name=row.nick_name;
                        };
                        if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                            img='/static/images/unknown.png';
                        }else {
                            img=row.photo_url;
                        };
                        if (row.text==''||row.text=='null'||row.text=='unknown'){
                            txt='暂无内容';
                        }else {
                            txt=row.text;
                        };
                        var star1='<img src="/static/images/level.png" alt="">',
                            star2='<img src="/static/images/level-e.png" alt="">',str='',user='';
                        if (row.sensitive_info==''||row.sensitive_info=='null'||row.sensitive_info=='unknown'||row.sensitive_info<=0){
                            star=star2.repeat(5);
                        }else if (row.sensitive_info>0&&row.sensitive_info<=3){
                            star+=star1;
                            star+=star2.repeat(4);
                        }else if (row.sensitive_info>3&&row.sensitive_info<=5){
                            star+=star1.repeat(2);
                            star+=star2.repeat(3);
                        }else if (row.sensitive_info>5&&row.sensitive_info<=7){
                            star+=star1.repeat(3);
                            star+=star2.repeat(2);
                        }else if (row.sensitive_info>7&&row.sensitive_info<=10){
                            star+=star1.repeat(4);
                            star+=star2.repeat(1);
                        }else if (row.sensitive_info>10){
                            star+=star1.repeat(5);
                        };
                        if (row.weibo_type=='follow'){
                            user='已关注用户';
                        }else if (row.weibo_type=='friend'){
                            user='相互关注用户';
                        }else if (row.weibo_type=='stranger'||row.weibo_type=='followed'){
                            user='未关注用户';
                        }
                        var str=
                            '<div class="commentAll">'+
                            '    <div class="commentEvery">'+
                            '        <img src="'+img+'" alt="" class="com-head">'+
                            '        <div class="com com-1">'+
                            '            <b class="com-1-name">来自 '+user+'</b>&nbsp;&nbsp;&nbsp;'+
                            '            <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;'+getLocalTime(row.timestamp)+'</span>&nbsp;&nbsp;'+
                            '            <i class="mid" style="display: none;">'+row.mid+'</i>'+
                            '            <i class="uid" style="display: none;">'+row.uid+'</i>'+
                            '            <div class="com-level">'+
                            '                <span style="display: inline-block;">敏感度：</span>'+
                            '                <div class="com-img" style="display: inline-block;">'+star+
                            '                </div>'+
                            '            </div>'+
                            '        </div>'+
                            '        <div class="com com-2">'+
                            '            <b class="com-2-name" style="color: #fa7d3c;cursor: pointer;">'+name+'</b>的回复：'+
                            '            <span class="com-2-tent">'+txt+'</span>'+
                            '        </div>'+
                            '        <div class="com com-3" style="overflow: hidden;">'+
                            // '            <span class="com-3-time">2017-11-11 11:11</span>'+
                            // '            <span>来自<span class="com-3-source">'+user+'</span></span>'+
                            '            <a class="com-3-reply copyFinish" datatype="commentClone" onclick="showInput(this)">回复</a>'+
                            '        </div>'+
                            '        <div class="commentClone">'+
                            '            <input type="text" class="clone-1" placeholder=""/>'+
                            '            <div class="clone-2">'+
                            '                <img src="/static/images/post-1.png" class="clone-2-1">'+
                            // '                <img src="/static/images/post-2.png" class="clone-2-2">'+
                            '                <label class="demo-label">'+
                            '                    <input class="demo-radio clone-2-3" type="checkbox" name="desc2">'+
                            '                    <span class="demo-checkbox demo-radioInput"></span> 同时转发到我的微博'+
                            '                </label>'+
                            '                <a href="###" class="clone-2-4" midurl="'+mid+'" onclick="comMent(this)">回复</a>'+
                            '            </div>'+
                            '        </div>'+
                            '    </div>'+
                            '</div>';
                        return str;
                    }
                },
            ],
        });
        $('#'+idbox+' p').hide();
        $('.'+idbox+' .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
    }else if (idbox=='letter-1'){
        letter(data);
    }else if (idbox=='reply-1'){
        reply(data);
    }else if (idbox=='focus-1'){
        focus(data);
    }
}
//====私信回复====
function letter(data) {
    $('#'+idbox).bootstrapTable('load', data);
    $('#'+idbox).bootstrapTable({
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name,txt,img;
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.nick_name;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                        // console.log(row.text.split('\n'))
                    };
                    var star1='<img src="/static/images/level.png" alt="">',
                        star2='<img src="/static/images/level-e.png" alt="">',str='',user='';
                    if (row.sensitive_info==''||row.sensitive_info=='null'||row.sensitive_info=='unknown'||row.sensitive_info<=0){
                        star=star2.repeat(5);
                    }else if (row.sensitive_info>0&&row.sensitive_info<=3){
                        star+=star1;
                        star+=star2.repeat(4);
                    }else if (row.sensitive_info>3&&row.sensitive_info<=5){
                        star+=star1.repeat(2);
                        star+=star2.repeat(3);
                    }else if (row.sensitive_info>5&&row.sensitive_info<=7){
                        star+=star1.repeat(3);
                        star+=star2.repeat(2);
                    }else if (row.sensitive_info>7&&row.sensitive_info<=10){
                        star+=star1.repeat(4);
                        star+=star2.repeat(1);
                    }else if (row.sensitive_info>10){
                        star+=star1.repeat(5);
                    };
                    if (row.weibo_type=='follow'){
                        user='已关注用户';
                    }else if (row.weibo_type=='friend'){
                        user='相互关注用户';
                    }else if (row.weibo_type=='stranger'||row.weibo_type=='followed'){
                        user='未关注用户';
                    }
                    var str=
                        '<div class="letterAll" style="background:rgba(8,23,44,0.35);">'+
                        '    <div class="letterEvery">'+
                        '        <img src="'+img+'" alt="" class="let-head">'+
                        '        <div class="let let-1">'+
                        '            <b class="let-1-name">来自 '+user+'&nbsp;'+name+'</b>&nbsp;&nbsp;&nbsp;'+
                        '            <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;'+getLocalTime(row.timestamp)+'</span>&nbsp;'+
                        '            <i class="mid" style="display: none;">'+row.mid+'</i>'+
                        '            <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        '            <div class="let-level">'+
                        '                <span style="display: inline-block;">敏感度：</span>'+
                        '                <div class="let-img" style="display: inline-block;">'+star+'</div>'+
                        '            </div>'+
                        '        </div>'+
                        '        <div class="let let-2">'+
                        '            <span class="let-2-content">'+txt+'</span>'+
                        '            <a class="let-2-reply copyFinish" datatype="letterClone" onclick="showInput(this)">回复</a>'+
                        '        </div>'+
                        '    </div>'+
                        '    <div class="letterClone" style="text-align: center;">'+
                        '        <input type="text" class="clone-1" style="width:79%;"/>'+
                        '        <div class="clone-2">'+
                        '            <img src="/static/images/post-1.png" class="clone-2-1">'+
                        // '            <img src="/static/images/post-2.png" class="clone-2-2">'+
                        // '            <img src="/static/images/post-11.png" class="clone-2-3">'+
                        '            <a href="###" class="clone-2-4" midurl="reply_private" onclick="comMent(this)">发送</a>'+
                        '        </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#'+idbox+' p').hide();
    $('.'+idbox+' .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
};
//=====@回复======
function reply(data) {
    console.log(data)
    $('#'+idbox).bootstrapTable('load', data);
    $('#'+idbox).bootstrapTable({
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name,txt,img,time;
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.nick_name;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.timestamp==''||row.timestamp=='null'||row.timestamp=='unknown'){
                        time='暂无内容';
                    }else {
                        time=getLocalTime(row.timestamp);
                    };
                    if (row.text==''||row.text=='null'||row.text=='unknown'){
                        txt='暂无内容';
                    }else {
                        txt=row.text;
                    };

                    var star1='<img src="/static/images/level.png" alt="">',
                        star2='<img src="/static/images/level-e.png" alt="">',str='',user='';
                    if (row.sensitive_info==''||row.sensitive_info=='null'||row.sensitive_info=='unknown'||row.sensitive_info<=0){
                        star=star2.repeat(5);
                    }else if (row.sensitive_info>0&&row.sensitive_info<=3){
                        star+=star1;
                        star+=star2.repeat(4);
                    }else if (row.sensitive_info>3&&row.sensitive_info<=5){
                        star+=star1.repeat(2);
                        star+=star2.repeat(3);
                    }else if (row.sensitive_info>5&&row.sensitive_info<=7){
                        star+=star1.repeat(3);
                        star+=star2.repeat(2);
                    }else if (row.sensitive_info>7&&row.sensitive_info<=10){
                        star+=star1.repeat(4);
                        star+=star2.repeat(1);
                    }else if (row.sensitive_info>10){
                        star+=star1.repeat(5);
                    };
                    if (row.weibo_type=='follow'){
                        user='已关注用户';
                    }else if (row.weibo_type=='friend'){
                        user='相互关注用户';
                    }else if (row.weibo_type=='stranger'||row.weibo_type=='followed'){
                        user='未关注用户';
                    }

                    var str=
                        '<div class="replyAll">'+
                        '    <div class="replyEvery">'+
                        '        <img src="'+img+'" alt="" class="rep-head">'+
                        '        <span style="display: none;" class="mid">'+row.mid+'</span>'+
                        '        <div class="rep rep-1">'+
                        '            <b class="rep-1-name">来自 '+user+'</b>&nbsp;&nbsp;'+
                        '            <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;'+time+'</span>&nbsp;'+
                        '            <div class="rep-level">'+
                        '                <span style="display: inline-block;">敏感度：</span>'+
                        '                <div class="rep-img" style="display: inline-block;">'+star+'</div>'+
                        '            </div>'+
                        // '            <div class="rep-1-time">'+time+'</div>'+
                        '        </div>'+
                        '        <div class="rep rep-2">'+
                        '            <b style="color: #fa7d3c;cursor: pointer;">'+name+'</b>的回复：'+
                        '            <span class="rep-2-tent">'+txt+'</span>'+
                        '        </div>'+
                        '        <div class="rep rep-3">'+
                        // '            <img src="/static/images/demo.jpg" alt="" class="rep-3-img">'+
                        '            <a class="rep-3-reply copyFinish" datatype="replyClone" onclick="showInput(this)">回复</a>'+
                        '        </div>'+
                        '    </div>'+
                        '    <div class="replyClone">'+
                        '        <input type="text" class="clone-1"/>'+
                        '        <div class="clone-2">'+
                        '            <img src="/static/images/post-1.png" class="clone-2-1">'+
                        // '            <img src="/static/images/post-2.png" class="clone-2-2">'+
                        '            <label class="demo-label">'+
                        '                <input class="demo-radio clone-2-3" type="checkbox" name="desc4">'+
                        '                <span class="demo-checkbox demo-radioInput"></span> 同时转发到我的微博'+
                        '            </label>'+
                        '            <a href="###" class="clone-2-4" midurl="reply_at" onclick="comMent(this)">发送</a>'+
                        '        </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#'+idbox+' p').hide();
    $('.'+idbox+' .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
};
//=====关注回粉--回复======
function focus(data) {
    console.log(data)
    $('#'+idbox).bootstrapTable('load', data);
    $('#'+idbox).bootstrapTable({
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
                title: "",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    var name,img,fan_source,geo,description,fol='',mark='',sent='';
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.nick_name;
                    };
                    if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=row.photo_url;
                    };
                    if (row.description==''||row.description=='null'||row.description=='unknown'){
                        description='未知';
                    }else {
                        description=row.description.trim();
                    };
                    if (row.fan_source==''||row.fan_source=='null'||row.fan_source=='unknown'){
                        fan_source='未知';
                    }else {
                        fan_source=row.fan_source;
                    };
                    if (row.geo==''||row.geo=='null'||row.geo=='unknown'){
                        geo='未知';
                    }else {
                        geo=row.geo;
                    };
                    var star1='<img src="/static/images/level.png" alt="">',
                        star2='<img src="/static/images/level-e.png" alt="">',str='',user='';
                    if (row.sensitive_info==''||row.sensitive_info=='null'||row.sensitive_info=='unknown'||row.sensitive_info<=0){
                        star=star2.repeat(5);
                    }else if (row.sensitive_info>0&&row.sensitive_info<=3){
                        star+=star1;
                        star+=star2.repeat(4);
                    }else if (row.sensitive_info>3&&row.sensitive_info<=5){
                        star+=star1.repeat(2);
                        star+=star2.repeat(3);
                    }else if (row.sensitive_info>5&&row.sensitive_info<=7){
                        star+=star1.repeat(3);
                        star+=star2.repeat(2);
                    }else if (row.sensitive_info>7&&row.sensitive_info<=10){
                        star+=star1.repeat(4);
                        star+=star2.repeat(1);
                    }else if (row.sensitive_info>10){
                        star+=star1.repeat(5);
                    };
                    if (row.weibo_type=='follow'){
                        fol='已关注';user='已关注用户';
                    }else if (row.weibo_type=='friends'){
                        fol='相互关注';user='相互关注用户';
                    }else if (row.weibo_type=='stranger'||row.weibo_type=='followed'){
                        fol='未关注';user='未关注用户';
                    }
                    if (row.trace_follow_mark){
                        mark='重点关注';
                    }else {
                        mark='普通关注';
                    }
                    if (row.sensor_mark){
                        sent='敏感用户';
                    }else {
                        sent='普通用户';
                    }
                    var str=
                        '<div class="focusAll">'+
                        '    <div class="focusEvery">'+
                        '        <img src="'+img+'" alt="" class="foc-head">'+
                        '        <div class="foc foc-1">'+
                        '            <b class="foc-1-name">'+name+'</b>&nbsp;&nbsp;'+
                        '            <b class="foc-1-sent">'+sent+'</b>&nbsp;&nbsp;'+
                        '            <b class="foc-1-mark">'+mark+'</b>'+
                        '            <b class="uid" style="display: none;">'+row.uid+'</b>'+
                        '            <div class="foc-level">'+
                        '                <span style="display: inline-block;">敏感度：</span>'+
                        '                <div class="foc-img" style="display: inline-block;">'+star+
                        '                </div>'+
                        '            </div>'+
                        '            <div class="foc-fm" style="float: right;margin-left:10px;">'+
                        '              <span class="foc-join" onclick="addfocus(this)">'+
                        '                     <i class="icon icon-ok"></i>&nbsp;|&nbsp;<span><i class="icon icon-plus" style="color:#f77911;"></i>&nbsp;<b>'+fol+'</b></span>'+
                        '              </span>'+
                        '            </div>'+
                        // '            <div class="foc-fm-2" style="float: right;">'+
                        // '              <span class="heavy-join" onclick="addheavy(this)">'+
                        // '                     <i class="icon icon-ok"></i>&nbsp;|&nbsp;<span><i class="icon icon-plus" style="color:#f77911;"></i>&nbsp;<b>'+mark+'</b></span>'+
                        // '              </span>'+
                        // '            </div>'+
                        '            <div class="foc-1-option">'+
                        '                <span>关注</span>&nbsp;<b class="foc-opt-1">'+row.follower+'</b>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '                <span>粉丝</span>&nbsp;<b class="foc-opt-2">'+row.fans+'</b>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '                <span>微博</span>&nbsp;<b class="foc-opt-3">'+row.weibos+'</b>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '            </div>'+
                        '        </div>'+
                        '        <div class="foc foc-2">'+
                        '            <div><span>地址</span>&nbsp;&nbsp;&nbsp;&nbsp;<b class="foc-2-1">'+geo+'</b></div>'+
                        '            <div><b class="foc-2-2">'+description+'</b></div>'+
                        '            <div>通过<b class="foc-2-3" style="color:#ec7a7a;">'+fan_source+'</b>关注</div>'+
                        '        </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
    $('#'+idbox+' p').hide();
    $('.'+idbox+' .search .form-control').attr('placeholder','输入关键词快速搜索相关微博（回车搜索）');
}

//============================
function postYES(data) {
    var f='';
    if (data[0]){
        f='操作成功';
    }else {
        f='操作失败，'+data[1];
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
//评论
function showInput(_this) {
    $(_this).hide();
    var _name=$(_this).parent().parent().find('b').text();
    var _dataType=$(_this).attr('datatype');
    $(_this).parent().parent().parent().find('.'+_dataType+' .clone-1').attr('placeholder','回复'+_name);
    $(_this).parent().parent().parent().find('.'+_dataType).show(40);
};
function comMent(_this){
    var txt = $(_this).parent().prev().val();
    var middle=$(_this).attr('midurl');
    var mid = $(_this).parent().parent().parent().find('.mid').text();
    if (txt!=''){
        var comurl;
        if (middle!='reply_at'){
            comurl='/weibo_xnr_operate/'+middle+'/?text='+txt+'&xnr_user_no='+xnrUser;
            if (middle=='reply_private'){
                var uid = $(_this).parent().parent().parent().find('.uid').text();
                comurl+='&uid='+uid;
            }else {
                comurl+='&mid='+mid;
            }
        }else {
            comurl='/weibo_xnr_operate/'+middle+'/?text='+txt+'&mid='+mid;
        }
        public_ajax.call_request('get',comurl,postYES);
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}

//关注回粉
// 关注
var ff_uid,f_txt;
function addfocus(_this) {
    ff_uid=$(_this).parents('.focusEvery').find('.uid').text();
    f_txt=$(_this).find('b').text();
    if (f_txt!='未关注'){
        $('#del_focus_modal').modal('show');
    }else {
        $('#focus_modal').modal('show');
    }
}
function delFocus() {
    var f1_url='/weibo_xnr_operate/unfollow_operate/?xnr_user_no='+xnrUser+'&uid='+ff_uid;
    public_ajax.call_request('get',f1_url,focusYES)
}
function focusUserSure() {
    var f2_url,trace_type;
    trace_type=$('#focus_modal input:radio[name="fcs"]:checked').val();
    f2_url='/weibo_xnr_operate/follow_operate/?xnr_user_no='+xnrUser+'&uid='+ff_uid+'&trace_type='+trace_type;
    public_ajax.call_request('get',f2_url,focusYES)
}
function focusYES(data) {
    var f='';
    if (data[0]){
        f='操作成功';
        var si=$('input:radio[name="fcs"]:checked').val();
        var ssr='/weibo_xnr_operate/show_fans/?xnr_user_no='+ID_Num+'&sort_item='+si;
        setTimeout(function () {
            public_ajax.call_request('get',ssr,focus);
        },500)
    }else {
        f='操作失败，'+data[1];
    }
    $('#focusSure p').text(f);
    $('#focusSure').modal('show');
}
//==========================================================


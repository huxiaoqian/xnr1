var timeUrl='/weibo_xnr_warming/show_date_warming/'//?xnr_user_no='+ID_Num;
public_ajax.call_request('get',timeUrl,calendar);
function calendar(data) {
    $('#remind .load').show();
    $('#remind').bootstrapTable('load', data);
    $('#remind').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
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
                    //时间节点名称、日期、距今、关键词、预警微博
                    var name,txt='',agoDay,time,time_2,keywords;
                    if (row.date_name==''||row.date_name=='null'||row.date_name=='unknown'||!row.date_name){
                        name='未命名';
                    }else {
                        name=row.date_name;
                    };
                    if (row.keywords==''||row.keywords=='null'||row.keywords=='unknown'||!row.keywords){
                        keywords = '暂无描述';
                    }else {
                        keywords = row.keywords.join('，');
                    };
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'||!row.create_time){
                        time='未知';
                    }else {
                        time=getLocalTime(row.create_time);
                    };
                    if (row.date_time==''||row.date_time=='null'||row.date_time=='unknown'||!row.date_time){
                        time_2='未知';
                    }else {
                        time_2=row.date_time;
                    };
                    if (row.countdown_days==''||row.countdown_days=='null'||row.countdown_days=='unknown'||!row.countdown_days){
                        agoDay = '暂无统计';
                    }else {
                        if (row.countdown_days.toString().indexOf('-')==-1){
                            agoDay = '距离下一次该日期还有 '+row.countdown_days+' 天';
                        }else {
                            agoDay = row.countdown_days.toString().replace(/-/g,'距离今天已经过去 ')+' 天';
                        }
                    };
                    if (row.weibo_date_warming_content==''||row.weibo_date_warming_content=='null'||row.weibo_date_warming_content.length==0||
                        row.weibo_date_warming_content=='unknown'||!row.weibo_date_warming_content){
                        txt = '暂无内容';
                    }else {
                        var artical=row.weibo_date_warming_content,str_2='';
                        if (artical.length==0||!artical){
                            str_2='暂无微博内容';
                        }else {
                            str_2=weibo(index,artical);
                        }
                        var str=
                            '<div class="post_perfect" style="margin:10px auto;">'+
                            '   <div class="post_center-hot">'+
                            '       <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                            '       <div class="center_rel">'+
                            '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>&nbsp;'+
                            '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="日期"><i class="icon icon-lightbulb"></i>&nbsp;&nbsp;'+time_2+'</span>  '+
                            '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="创建日期"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                            '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="距离今天过去多久"><i class="icon icon-bullhorn"></i>&nbsp;&nbsp;'+agoDay+'</span>  '+
                            '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="关键词"><i class="icon icon-bell-alt"></i>&nbsp;&nbsp;'+keywords+'</span>  '+
                            '           <div class="center_2 DsAuto"'+index+'><span style="color:#f98077;">敏感微博内容：</span>'+str_2+'</div>'+
                            '       </div>'+
                            '    </div>'+
                            '</div>';
                        return str;
                    };

                }
            },
        ],
    });
    $('#remind .load').hide();
};

// 转发===评论===点赞
function retComLike(_this) {
    var mid=$(_this).parents('.center_rel_weibo').find('.mid').text();
    var middle=$(_this).attr('type');
    var opreat_url;
    if (middle=='get_weibohistory_like'){
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid;
        public_ajax.call_request('get',opreat_url,postYES);
    }else if (middle=='get_weibohistory_comment'){
        $(_this).parents('.center_rel_weibo').find('.commentDown').show();
    }else {
        var txt=$(_this).parents('.center_rel_weibo').find('.center_2').text();
        if (txt=='暂无内容'){txt=''};
        opreat_url='/weibo_xnr_report_manage/'+middle+'/?xnr_user_no='+ID_Num+'&r_mid='+mid+'&text='+txt;
        public_ajax.call_request('get',opreat_url,postYES);
    }
}

function comMent(_this){
    var txt = $(_this).prev().val();
    var mid = $(_this).parents('.center_rel_weibo').find('.mid').text();
    if (txt!=''){
        var post_url='/weibo_xnr_report_manage/get_weibohistory_comment/?text='+txt+'&xnr_user_no='+ID_Num+'&mid='+mid;
        public_ajax.call_request('get',post_url,postYES)
    }else {
        $('#pormpt p').text('评论内容不能为空。');
        $('#pormpt').modal('show');
    }
}

//上报
function oneUP(_this) {
// #user_dict=[uid,nick_name,fansnum,friendsnum]
// #weibo_dict=[mid,text,timestamp,retweeted,like,comment]
    var info=[];
    var uid = $(_this).parents('.center_rel_weibo').find('.uid').text();info.push(uid);
    var mid = $(_this).parents('.center_rel_weibo').find('.mid').text();info.push(mid);
    var txt=$(_this).parents('.center_rel_weibo').find('.center_2').text();info.push(txt);
    var timestamp = $(_this).parents('.center_rel_weibo').find('.timestamp').text();info.push(timestamp);
    var forwarding = $(_this).parents('.center_rel_weibo').find('.forwarding').text();info.push(forwarding);
    var comment = $(_this).parents('.center_rel_weibo').find('.comment').text();info.push(comment);
    //=======URL======
    var allMent=[];
    allMent.push(info[1]);
    var txt=info[2].toString().replace(/#/g,'%23');allMent.push(txt);
    allMent.push(info[3]);allMent.push(info[4]);allMent.push(0);allMent.push(info[5]);
    var once_url='/weibo_xnr_warming/report_warming_content/?report_type=言论&xnr_user_no='+ID_Num+
        '&uid='+info[0]+'&weibo_info='+allMent.join(',');
    public_ajax.call_request('get',once_url,postYES);
}

//操作返回结果
function postYES(data) {
    var f='';
    if (data[0]||data){
        f='操作成功';
    }else {
        f='操作失败';
    }
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}

function weibo(idx,weibodata) {
    var ele_1=document.createElement('div');
    ele_1.className='weibo_'+idx;
    var ele=document.createElement('div');
    ele.id='weibo_'+idx;
    ele_1.appendChild(ele);
    document.body.appendChild(ele_1);
    $('#weibo_'+idx).bootstrapTable('load', weibodata);
    $('#weibo_'+idx).bootstrapTable({
        data:weibodata,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 3,//单页记录数
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
                    var item=row;
                    var str_new='';
                    var geo,txt,img,time;
                    if (item.geo==''||item.geo=='null'||item.geo=='unknown'){
                        geo='未知';
                    }else {
                        geo=item.geo.toString().replace(/&/g,' ');
                    };
                    if (item.photo_url==''||item.photo_url=='null'||item.photo_url=='unknown'){
                        img='/static/images/unknown.png';
                    }else {
                        img=item.photo_url;
                    };
                    if (item.timestamp==''||item.timestamp=='null'||item.timestamp=='unknown'){
                        time='未知';
                    }else {
                        time=getLocalTime(item.timestamp);
                    };
                    if (item.text==''||item.text=='null'||item.text=='unknown'||!item.text){
                        txt='暂无内容';
                    }else {
                        if (item.sensitive_words_string){
                            var keywords=item.sensitive_words_string.split('，');
                            for (var f of keywords){
                                txt=item.text.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                            }
                        }else {
                            txt=item.text;
                        };
                    };
                    str_new+=
                        '<div class="everySpeak" style="margin: 0 auto;">'+
                        '        <div class="speak_center">'+
                        '            <div class="center_rel center_rel_weibo">'+
                        // '                <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                        '                <a class="center_1" title="地理位置"><i class="icon icon-screenshot"></i> '+geo+'</a>'+
                        '                <a class="mid" style="display: none;">'+item.mid+'</a>'+
                        '                <a class="uid" style="display: none;">'+item.uid+'</a>'+
                        '                <a class="timestamp" style="display: none;">'+item.timestamp+'</a>'+
                        '                <span class="time" style="font-weight: 900;color:blanchedalmond;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                        '                <div class="center_2">'+txt+'</div>'+
                        '                <div class="center_3">'+
                        '                    <span class="cen3-2" onclick="retComLike(this)" type="get_weibohistory_retweet"><i class="icon icon-share"></i>&nbsp;&nbsp;转发（<b class="forwarding">'+item.retweeted+'</b>）</span>'+
                        '                    <span class="cen3-3" onclick="retComLike(this)" type="get_weibohistory_comment"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论（<b class="comment">'+item.comment+'</b>）</span>'+
                        '                    <span class="cen3-4" onclick="retComLike(this)" type="get_weibohistory_like"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        '                    <span class="cen3-6" onclick="oneUP(this)"><i class="icon icon-upload-alt"></i>&nbsp;&nbsp;上报</span>'+
                        '                </div>'+
                        '               <div class="commentDown" style="width: 100%;display: none;">'+
                        '                   <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        '                   <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        '               </div>'+
                        '            </div>'+
                        '        </div>';
                    return str_new;
                }
            },
        ],
    });
}
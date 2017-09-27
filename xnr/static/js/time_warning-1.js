var timeUrl='/weibo_xnr_warming/show_date_warming/'//?xnr_user_no='+ID_Num;
public_ajax.call_request('get',timeUrl,calendar);
function calendar(data) {
    console.log(data)
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
                    if (row.date_name==''||row.date_name=='null'||row.date_name=='unknown'){
                        name='未命名';
                    }else {
                        name=row.date_name;
                    };
                    if (row.keywords==''||row.keywords=='null'||row.keywords=='unknown'||!row.keywords){
                        keywords = '暂无描述';
                    }else {
                        keywords = row.keywords.join('，');
                    };
                    if (row.create_time==''||row.create_time=='null'||row.create_time=='unknown'){
                        time='未知';
                    }else {
                        time=getLocalTime(row.create_time);
                    };
                    if (row.date_time==''||row.date_time=='null'||row.date_time=='unknown'){
                        time_2='未知';
                    }else {
                        time_2=row.date_time;
                    };
                    if (row.countdown_days==''||row.countdown_days=='null'||row.countdown_days=='unknown'||!row.countdown_days){
                        agoDay = '暂无统计';
                    }else {
                        if (row.countdown_days.toString().indexOf('-')==-1){
                            agoDay = '还有 '+row.countdown_days+' 天';
                        }else {
                            agoDay = row.countdown_days.toString().replace(/-/g,'距离今天已经 ');
                        }
                    };
                    if (row.weibo_date_warming_content==''||row.weibo_date_warming_content=='null'||row.weibo_date_warming_content.length==0||
                        row.weibo_date_warming_content=='unknown'||!row.weibo_date_warming_content){
                        txt = '暂无内容';
                    }else {
                        $.each(row.weibo_date_warming_content,function (index,item) {
                            var xnr,type,txt2;
                            if (!item.text){txt2='无数据'}else {txt2=item.text};
                            if (!item.tweet_type){type='未知'}else {type=item.tweet_type};
                            if (!item.xnr_user_no){xnr='未知'}else {xnr=item.xnr_user_no};
                            txt +=
                                '<div class="post_short">'+
                                '    <img src="/static/images/post-11.png" alt="">'+
                                '    <span class="short_1">虚拟人：'+xnr+'</span>'+
                                '    <span class="short_2">类型：'+type+'</span>'+
                                '    <div class="center_rel" style="margin: 10px 0;padding-left: 25px;">'+
                                '        内容：'+txt2+
                                '    </div>'+
                                '</div>';
                        });
                    };
                    var str=
                        '<div class="post_perfect" style="margin:10px auto;width:920px;">'+
                        '   <div class="post_center-hot">'+
                        '       <img src="/static/images/post-6.png" alt="" class="center_icon">'+
                        '       <div class="center_rel">'+
                        '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>&nbsp;'+
                        // '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
                        // '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                        // '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="日期"><i class="icon icon-lightbulb"></i>&nbsp;&nbsp;'+time_2+'</span>  '+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="创建日期"><i class="icon icon-time"></i>&nbsp;&nbsp;'+time+'</span>  '+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="距离今天过去多久"><i class="icon icon-bullhorn"></i>&nbsp;&nbsp;'+agoDay+'</span>  '+
                        '           <span class="time" style="font-weight: 900;color:blanchedalmond;" title="关键词"><i class="icon icon-bell-alt"></i>&nbsp;&nbsp;'+keywords+'</span>  '+
                        '           <div class="center_2"><p style="color:#f98077;">敏感微博内容：</p>'+txt+'</div>'+
                        // '           <div class="center_3">'+
                        // '               <span class="cen3-1" onclick="retweet(this)"><i class="icon icon-share"></i>&nbsp;&nbsp;转发</span>'+
                        // '               <span class="cen3-2" onclick="showInput(this)"><i class="icon icon-comments-alt"></i>&nbsp;&nbsp;评论</span>'+
                        // '               <span class="cen3-3" onclick="thumbs(this)"><i class="icon icon-thumbs-up"></i>&nbsp;&nbsp;赞</span>'+
                        // '               <span class="cen3-4" onclick="focusThis(this)"><i class="icon icon-heart-empty"></i>&nbsp;&nbsp;关注该用户</span>'+
                        // '               <span class="cen3-5" onclick="joinlab(this)"><i class="icon icon-signin"></i>&nbsp;&nbsp;加入语料库</span>'+
                        // '           </div>'+
                        // '           <div class="commentDown" style="width: 100%;display: none;">'+
                        // '               <input type="text" class="comtnt" placeholder="评论内容"/>'+
                        // '               <span class="sureCom" onclick="comMent(this)">评论</span>'+
                        // '           </div>'+
                        '       </div>'+
                        '    </div>'+
                        '</div>';
                    return str;
                }
            },
        ],
    });
};
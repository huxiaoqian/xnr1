// 预警详情 页js
var communityDetails_url='/weibo_xnr_community/get_community_warning/?xnr_user_no='+ID_Num+
    '&community_id='+communityId+'&start_time=1521728241&end_time=1522333041';
public_ajax.call_request('GET',communityDetails_url,communityDetailsFun);
var time;
function communityDetailsFun(data) {
    $('.det1').text(data.community_name);
    var a=data.trace_time?getLocalTime(data.trace_time):'无数据';
    $('.det2').text(a);
    var b=data.num?data.num[data.num.length-1]:'无数据';
    $('.det3').text(b);
    time=data.trace_date;
    //人数===
    chartNum('人数变化图','people-num',data.num,'');//折线图
    descript('thisDEC_1',data.num_warning_descrp)//描述
    tablePic('table-1',data.num_warning_content)//表格
    //敏感度
    setTimeout(function () {
        chartNum('敏感度变化折线图','sensitivity',data.mean_sensitive,data.max_sensitive);//折线图
        descript('thisDEC_2',data.sensitive_warning_descrp)//描述
        tablePic('table-2',data.sensitive_warning_content)//文字
    },300);
    //影响力
    setTimeout(function () {
        chartNum('影响力变化折线图','influence',data.mean_influence,data.max_influence);//折线图
        descript('thisDEC_3',data.influence_warning_descrp)//描述
        tablePic('table-3',data.influence_warning_content)//文字
    },600);
    //聚集系数
    setTimeout(function () {
        chartNum('聚集系数变化折线图','convergence',data.density,'');//折线图
        descript('thisDEC_4',data.density_warning_descrp)//描述
        tablePic('table-4',data.density_warning_content)//表格
    },800);
}
// 人数变化图
function chartNum(tit,ID,peopleData,flag){
    if(!peopleData){
        $('#'+ID).html('<h4 style="width:100%;text-align:center;margin-top:140px;">人数变化图暂无数据</h4>');
        return false;
    }
    var myChart = echarts.init(document.getElementById(ID),'dark');
    var option = {
        backgroundColor:'transparent',
        title: {
            text: tit,
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: false,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis:  {
            type: 'category',
            boundaryGap: false,
            data: time
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                // formatter: '{value} °C'
                formatter: '{value}'
            }
        },
        series: [
            {
                name:'',
                type:'line',
                data:peopleData,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            },
        ]
    };
    if(flag){
        var ld=['平均敏感度','最大敏感度'];
        if(ID=='influence'){ld=['平均影响力','最大影响力']};
        option['legend']={
            data:ld
        };
        option.series[0].name=ld[0];
        option.series.push({
            name:ld[1],
            type:'line',
            data:flag,
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        });
    };
    myChart.setOption(option);
}
//描述
function descript(id,descrp) {
    var str='';
    for(var i=0;i<descrp.length;i++){
        var t;
        try{t=time[i]}catch(e){t='未知'}
        if(descrp[i]!=''){
            str+='<p style="margin:5px 10px;font-size: 14px;">● '+t+'：'+descrp[i]+'</p>';
        }
    }
    if (str==''){$('.'+id).html('<p style="margin-left:25px;font-size: 14px;">此时间段内无任何预警。</p>')}else {
        $('.'+id).html(str);
    }
};
//表格
function tablePic(id,_data) {
    var data=_data;
    if(id=='table-4'){
        data=[];
        $.each(_data,function (index,item) {
            data.push({
                'id1':item[0],'name1':item[1],
                'id2':item[2],'name2':item[3],'count':item[4]
            })
        });
    }
    $('#'+id).bootstrapTable('load', data);
    var tableColumns=[
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
    ];
    if(id=='table-2'||id=='table-3'){
        tableColumns=[{
            title: "",//标题
            field: "",//键名
            sortable: true,//是否可排序
            order: "desc",//默认排序方式
            align: "center",//水平
            valign: "middle",//垂直
            formatter: function (value, row, index) {
                var name,txt,txt2,img;
                if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'||!row.nick_name){
                    name=row.uid;
                }else {
                    name=row.nick_name;
                };
                if (row.photo_url==''||row.photo_url=='null'||row.photo_url=='unknown'||!row.photo_url){
                    img='/static/images/unknown.png';
                }else {
                    img=row.photo_url;
                };
                var all='';
                if (row.text==''||row.text=='null'||row.text=='unknown'){
                    txt='暂无内容';
                }else {
                    if (row.sensitive_words_string||!isEmptyObject(row.sensitive_words_string)){
                        var keyword_d=row.sensitive_words_string.split('&');
                        for (var f of keyword_d){
                            txt=row.text.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                        }
                        var rrr=row.text;
                        if (rrr.length>=160){
                            rrr=rrr.substring(0,160)+'...';
                            all='inline-block';
                        }else {
                            rrr=row.text;
                            all='none';
                        }
                        for (var f of keyword_d){
                            txt2=rrr.toString().replace(new RegExp(f,'g'),'<b style="color:#ef3e3e;">'+f+'</b>');
                        }
                    }else {
                        txt=row.text;
                        if (txt.length>=160){
                            txt2=txt.substring(0,160)+'...';
                            all='inline-block';
                        }else {
                            txt2=txt;
                            all='none';
                        }
                    };
                };
                var str=
                    '<div class="post_perfect" style="margin-bottom:10px;">'+
                    '   <div class="post_center-hot">'+
                    '       <img src="'+img+'" alt="" class="center_icon">'+
                    '       <div class="center_rel" style="text-align:left">'+
                    '           <a class="center_1" href="###" style="color: #f98077;">'+name+'</a>&nbsp;'+
                    '           <i class="mid" style="display: none;">'+row.mid+'</i>'+
                    '           <i class="uid" style="display: none;">'+row.uid+'</i>'+
                    '           <i class="timestamp" style="display: none;">'+row.timestamp+'</i>'+
                    '           <span class="time" style="font-weight: 900;color:#f6a38e;"><i class="icon icon-time"></i>&nbsp;&nbsp;'+getLocalTime(row.timestamp)+'</span>  '+
                    '           <button data-all="0" style="display:'+all+'" type="button" class="btn btn-primary btn-xs allWord" onclick="allWord(this)">查看全文</button>'+
                    '           <p class="allall1" style="display:none;">'+txt+'</p>'+
                    '           <p class="allall2" style="display:none;">'+txt2+'</p>'+
                    '           <span class="center_2">'+txt2+'</span>'+
                    '       </div>'+
                    '    </div>'+
                    '</div>';
                return str;
            }
        }]
    }else if(id=='table-4'){
        tableColumns=[
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
                title: "转发数",//标题
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
        ]
    }
    $('#'+id).bootstrapTable({
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
        columns:tableColumns,
    });
};
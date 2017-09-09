// var from_ts=Date.parse(new Date(new Date().setHours(0,0,0,0)))/1000;
// var to_ts=Date.parse(new Date())/1000;
var from_ts=1479513600,to_ts=1479981600;
//选择时间范围
$('.timeSure').on('click',function () {
    from_ts = $('.start').val();
    to_ts = $('.end').val();
    if (from_ts==''||to_ts==''){
        $('#pormpt p').text('请检查选择的时间（不能为空）');
        $('#pormpt').modal('show');
    }else {
        public_ajax.call_request('get',word_url,wordCloud);
        public_ajax.call_request('get',hotPost_url,hotPost);
        public_ajax.call_request('get',activePost_url,activeUser);
    }
});
$('.perTime .demo-label .demo-radio').on('click',function () {
    var day=$(this).val();
});
//----关键词云
var word_url='/weibo_xnr_monitor/lookup_weibo_keywordstring/?weiboxnr_id='+ID_Num+'&from_ts='+from_ts+'&to_ts='+to_ts;
public_ajax.call_request('get',word_url,wordCloud);
require.config({
    paths: {
        echarts: '/static/js/echarts-2/build/dist',
    }
});
function wordCloud(data) {
    console.log(data)
    var wordSeries=[];
    $.each(data,function (index,item) {
        wordSeries.push(
            {
                name: item['key'],
                value: item['doc_count'],
                itemStyle: createRandomItemStyle()
            }
        )
    });
    require(
        [
            'echarts',
            'echarts/chart/wordCloud'
        ],
        //关键词
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('content-1-word'));
            option = {
                title: {
                    text: '',
                },
                tooltip: {
                    show: true
                },
                series: [{
                    type: 'wordCloud',
                    size: ['100%', '100%'],
                    textRotation : [0, 0, 0, 0],
                    textPadding: 0,
                    autoSize: {
                        enable: true,
                        minSize: 14
                    },
                    data: wordSeries
                }]
            };
            myChart.setOption(option);
        }
    );
}
//热门帖子
$('#theme-2 .demo-radio').on('click',function () {
    var classify_id=$(this).val();
    var order_id=$('#theme-3 input:radio[name="demo"]:checked').val();
    var NEWhotPost_url='/weibo_xnr_monitor/lookup_hot_posts/?from_ts='+from_ts+'&to_ts='+to_ts+
        '&weiboxnr_id='+ID_Num+'&classify_id='+classify_id+'&order_id='+order_id;
    public_ajax.call_request('get',NEWhotPost_url,hotPost);
});
$('#theme-3 .demo-radio').on('click',function () {
    var classify_id=$('#theme-2 input:radio[name="demo-radio"]:checked').val();
    var order_id=$(this).val();
    var NEWhotPost_url='/weibo_xnr_monitor/lookup_hot_posts/?from_ts='+from_ts+'&to_ts='+to_ts+
        '&weiboxnr_id='+ID_Num+'&classify_id='+classify_id+'&order_id='+order_id;
    public_ajax.call_request('get',NEWhotPost_url,hotPost);
});
var hotPost_url='/weibo_xnr_monitor/lookup_hot_posts/?from_ts='+from_ts+'&to_ts='+to_ts+
    '&weiboxnr_id='+ID_Num+'&classify_id=0&order_id=1';
public_ajax.call_request('get',hotPost_url,hotPost);
function hotPost(data) {
    console.log(data)
}
//活跃用户
$('#user-1 .demo-radio').on('click',function () {
    var classify_id=$('#user-1 input:radio[name="deadio"]:checked').val();
    var NEWactivePost_url='/weibo_xnr_monitor/lookup_active_weibouser/?weiboxnr_id='+ID_Num+'&classify_id='+classify_id;
    public_ajax.call_request('get',NEWactivePost_url,activeUser);
});
var activePost_url='/weibo_xnr_monitor/lookup_active_weibouser/?weiboxnr_id='+ID_Num+
    '&from_ts='+from_ts+'&to_ts='+to_ts+'&classify_id=1';
public_ajax.call_request('get',activePost_url,activeUser);
function activeUser(persondata) {
    console.log(persondata)
    $('.userList #userList').bootstrapTable('load', persondata);
    $('.userList #userList').bootstrapTable({
        data:persondata,
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
                title: "添加关注",//标题
                field: "select",
                checkbox: true,
                align: "center",//水平
                valign: "middle"//垂直
            },
            {
                title: "用户ID",//标题
                field: "id",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                // formatter: function (value, row, index) {
                //     return row[1];
                // }
            },
            {
                title: "昵称",//标题
                field: "nick_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.nick_name==''||row.nick_name=='null'||row.nick_name=='unknown'){
                        return '无昵称';
                    }else {
                        return row.nick_name;
                    };
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
                    if (row.user_location==''||row.user_location=='null'||row.user_location=='unknown'){
                        return '未知';
                    }else {
                        return row.user_location;
                    };
                }
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
                title: "微博数",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "影响力",//标题
                field: "influence",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
            },
            {
                title: "网民详情",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor: pointer;" onclick="networkPeo(\''+row.id+'\')" ' +
                        'title="查看详情"><i class="icon icon-link"></i></span>'
                },
            },
        ],
    });
}
//-------------------颜色----------------------
function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 260),
                Math.round(Math.random() * 260),
                Math.round(Math.random() * 260)
            ].join(',') + ')'
        }
    };
}
//加入语料库  data-toggle="modal" data-target="#wordcloud"
function joinWord() {
    var create_type=$('#wordcloud input:radio[name="xnr"]:checked').val();
    var corpus_type=$('#wordcloud input:radio[name="theday"]:checked').val();
    var theme_daily_name=[],tt='';
    if (corpus_type=='主题语料'){tt=2};
    $("#wordcloud input:checkbox[name='theme"+tt+"']:checked").each(function (index,item) {
        theme_daily_name.push($(this).val());
    });
    var corpus_url='/weibo_xnr_monitor/addto_weibo_corpus/?corpus_type='+corpus_type+'&theme_daily_name='+theme_daily_name.join(',')+'&text='+text+
        '&uid='+uid+'&mid='+mid+'&retweeted='+retweeted+'&comment='+comment+'&like=0&create_type='+create_type;
}
//查看网民详情
function networkPeo(_id) {
    console.log(_id)
}
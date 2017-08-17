//渗透领域
var field_url='/weibo_xnr_create/show_domain/';
public_ajax.call_request('get',field_url,field);
function field(data) {
    console.log(data)
    var str='';
    for (var k in data){
        str+=
            '<label class="demo-label" title="'+data[k]+'">'+
            '   <input class="demo-radio" type="radio" name="demo1" id="'+k+'" value="'+data[k]+'">'+
            '   <span class="demo-checkbox demo-radioInput"></span> '+data[k]+
            '</label>';
    }
    $('#container .tit-2 .field').html(str);
    $('input[name=demo1]').on('click',function () {
        domainName=$(this).parent().attr('title');
        var nameLEN=$(this).attr('name').toString();
        var creat_url='/weibo_xnr_create/domain2role/?domain_name='+domainName;
        public_ajax.call_request('get',creat_url,creat_1)
    });
}

var domainName='',roleName='';

function creat_1(data) {
    addLabel(data,'opt-1','demo2');
}
function creat_2(data) {
    addLabel(data,'opt-2&opt-3','demo3&demo4');
}
var m;
function addLabel(data,className,name) {
    m=Number(name.charAt(name.length-1));
    var _string;
    if (m>3){
        var c=className.split('&'),n=name.split('&'),f=0;
        for (var k = 0;k<2;k++){
            var ary=[];
            if (k==0){
                $.each(data['political_side'],function (index,item) {
                    if (item[0]=='mid'){item[0]='中立'}else if (item[0]=='left'){item[0]='左倾'}else
                    if (item[0]=='right'){item[0]='右倾'}
                    ary.push(item[0].toString());
                });
                _string=labelSTR(ary,n[k]);
            }else if(k==1){
                $.each(data['psy_feature'],function (index,item) {
                    ary.push(item[0].toString());
                });
                _string=labelSTR(ary,n[k],'checkbox');
            }
            $('#container .buildOption .'+c[k]).empty().html(_string);
            f++;
        };
    }else {
        _string=labelSTR(data,name);
        $('#container .buildOption .'+className).empty().html(_string);
        $('input[name='+name+']').on('click',function () {
            roleName=$(this).parent().attr('title');
            var creat_url_2='/weibo_xnr_create/role2feature_info/?domain_name='+domainName+'&role_name='+roleName;
            public_ajax.call_request('get',creat_url_2,creat_2)
        });
    }
};
function labelSTR(data,name,radioCheckbox='radio') {
    var str='';
    if (data.length==0){
        //str='暂无数据';
        if (name=='demo3'){
            data=['左倾','中立','右倾'];
        }else if (name='demo4'){
            data=['中立','积极','悲伤','焦虑','生气','厌恶','消极其他'];
        }
    }
    for(var i=0;i<data.length;i++){
        str+= '<label class="demo-label" title="'+data[i]+'">'+
            '   <input class="demo-radio" value="'+data[i]+'" type="'+radioCheckbox+'" name="'+name+'">'+
            '   <span class="demo-checkbox demo-radioInput"></span> '+data[i]+
            '</label>';
    }
    return str;
}

//保存结果
//http://219.224.134.213:9090/weibo_xnr_create/save_step_one/?domain_name=维权群体&role_name=政府机构及人士
// &psy_feature=积极，中立，悲伤&political_side=中立&business_goal=扩大影响，渗透&monitor_keywords=维权，律师&daily_interests=旅游，美食
var daily='';
$('.nextButton').on('click',function () {
    var psyFeature=[],dailyInterests=[],politicalSide='',business=[];
    $(".opt-3 input[type=checkbox]:checkbox:checked").each(function (index,item) {
        psyFeature.push($(this).val());
    });
    $(".opt-2 input[type=radio]:radio:checked").each(function (index,item) {
        politicalSide=$(this).val().toString();
    });
    $(".opt-5 input[type=checkbox]:checkbox:checked").each(function (index,item) {
        dailyInterests.push($(this).val());
    });
    $(".opt-4 input[type=checkbox]:checkbox:checked").each(function (index,item) {
        business.push($(this).val());
    });
    var businessGoal= business.join(',');
    var monitorKeywords= $('.opt-6 .keywords').val().toString().replace(/，/g,',');
    if (!(domainName||roleName||psyFeature.length==0||dailyInterests.length==0||politicalSide||businessGoal||monitorKeywords)){
        $('#prompt p').text('请检查您选择和添加的信息。（不能为空）');
        $('#prompt').modal('show');
    }else {
        daily=dailyInterests.join(',');
        var saveFirst_url='/weibo_xnr_create/save_step_one/?domain_name='+domainName+'&role_name='+roleName+
        '&psy_feature='+psyFeature.join(',')+'&political_side='+politicalSide+'&business_goal='+businessGoal+
        '&monitor_keywords='+monitorKeywords+'&daily_interests='+daily;
        // window.open('/registered/virtualCreated/?domainName='+domainName+'&roleName='+roleName+'&daily='+daily+
        // '&psyFeature='+psyFeature.join(',')+'&politicalSide='+politicalSide+'&businessGoal='+businessGoal+
        // '&monitorKeywords='+monitorKeywords);
        window.open('/registered/virtualCreated/');
        var first={
            'domainName':domainName,
            'roleName':roleName,
            'daily':daily,
            'psyFeature':psyFeature.join(','),
            'politicalSide':politicalSide,
            'businessGoal':businessGoal,
            'monitorKeywords':monitorKeywords}
        localStorage.setItem('firstStep',JSON.stringify(first));
        //public_ajax.call_request('get',saveFirst_url,in_second);
    }
});
function in_second(data) {
    if (data){
        window.open('/registered/virtualCreated/');
    }else {
        $('#prompt p').text('您输入的内容有误，请刷新页面重新输入。');
        $('#prompt').modal('show');
    }
}
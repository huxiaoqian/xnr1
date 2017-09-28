setTimeout(function () {
    var chara_url='/weibo_xnr_create/recommend_step_two/?domain_name='+basicData.domain_name+
        '&role_name='+basicData.role_name+'&daily_interests='+basicData.daily_interests;
    public_ajax.call_request('get',chara_url,character);
},500)
//查看推荐
var recommendData;
function character(data) {
    recommendData=data;
    publicRecommend('role_example','#role_example .role_example_list');
    //其他信息推荐
    $('#container .other_basic .others a').on('click',function () {
        let _classname=$(this).parent().attr('class'),word='',tit='';
        if (_classname.includes('time')){
            //$('.other-3-example span').text('活跃时间推荐');
            //publicRecommend('active_time','.other_basic .other-3-list');
            word='active_time';tit='活跃时间推荐';_classname='other-1';
        }else if (_classname.includes('choose')){
            //$('.other-3-example span').text('发帖量推荐');
            //publicRecommend('day_post_num_average','.other_basic .other-3-list');
            word='day_post_num_average';tit='发帖量推荐';_classname='other-2';
        }
        _classname+='&other-3&other-3-example&other-3-list';
        publicRecommend(word,_classname,tit);
        $('.other-3').css({display:'block'});
    });
    //账户创建信息
    $('#container .account .account-1 a').on('click',function () {
        let _classname=$(this).parent().attr('class'),word='',tit='';
        if (_classname.includes('name')){
            //$('.account-2-example span').text('昵称推荐');
            word='nick_name';tit='昵称推荐';_classname='name';
        }else if (_classname.includes('age')){
            //$('.account-2-example span').text('年龄推荐');
            word='age';tit='年龄推荐';_classname='age';
        }else if (_classname.includes('gender')){
            //$('.account-2-example span').text('性别推荐');
            word='sex';tit='性别推荐';_classname='gender';
        }else if (_classname.includes('place')){
            //$('.account-2-example span').text('所在地推荐');
            word='user_location';tit='所在地推荐';_classname='place';
        }else if (_classname.includes('career')){
            //$('.account-2-example span').text('职业推荐');
            word='career';tit='职业推荐';_classname='career';
        }else if (_classname.includes('description')){
            //$('.account-2-example span').text('个人描述推荐');
            word='description';tit='个人描述推荐';_classname='description';
        }
        _classname+='&account-2&account-2-example&account-2-list';
        publicRecommend(word,_classname,tit);
    });

    var addRR=[
        {'word':'nick_name','_classname':'name'},
        {'word':'age','_classname':'age'},
        {'word':'sex','_classname':'gender'},
        {'word':'user_location','_classname':'place'},
        {'word':'career','_classname':'career'},
        {'word':'description','_classname':'description'},
    ];
    $.each(addRR,function (index,item) {
        var field=item.word;
        var className=item._classname;
        if (field=='sex'){
            var s = '';
            if (recommendData[field]==1){s='男'}else if(recommendData[field]==2){s='女'}else{s='未知'};
            $("#gender input[type='radio'][value='"+s+"']").attr("checked",true);
        }else {
            if (!recommendData[field]||recommendData[field]==''||recommendData==0||isEmptyObject(recommendData[field])){
                $('#container #'+className).val('暂无推荐');
            }else {
                var r=recommendData[field].toString().replace(/&/g,'，');
                $('#container #'+className).val(r);
            }
        }

    })
}

function publicRecommend(field,className,tit) {
    var str='';
    if (!recommendData[field]||recommendData[field]==''||recommendData.length==0||recommendData[field].length==0||
        isEmptyObject(recommendData[field])){
        str='<p style="text-align: center;">抱歉，暂无数据。</p>';
    }else {
        if (field=='day_post_num_average'){
            str+='<li><a href="###">'+parseInt(recommendData[field])+'条</a></li>';
        }else {
            var rd=[];
            if (typeof recommendData[field]=='string'){
                rd=recommendData[field].split('&');
            }else if (typeof recommendData[field]=='object'){
                for (var k in recommendData[field]){
                    if (recommendData[field][k]){
                        rd.push(recommendData[field][k])
                    }else {
                        rd.push(k);
                    }
                }
            }
            for(var a=0;a<rd.length;a++){
                var at=rd[a],time;
                if (field=='active_time'){
                    //time=at+':00-'+at+':59';
                    time='<label class="demo-label">'+
                    '        <input class="demo-radio" type="checkbox" name="timetampe">'+
                    '        <span class="demo-checkbox demo-radioInput"></span> '+at+':00-'+at+':59'+
                    '    </label>';
                    str+='<li>'+time+'</li>';
                }else {
                    time=at;
                    str+='<li><a href="###" title="'+time+'">'+time+'</a></li>';
                }
                //str+='<li><a href="###" title="'+time+'">'+time+'</a></li>';
            };
        }
    };

    if (tit){
        var big=className.split('&');
        var afterStr=
            '<div class="'+big[1]+'" style="margin:15px 0;">'+
            '   <p class="'+big[2]+'" style="text-align: center;padding: 5px;border-bottom: 1px solid #656e7b;">'+
            '       <span style="padding: 3px 6px;color: white;">'+tit+'</span>'+
            '       <b class="close icon icon-remove" style="float: right;font-size: 16px;color: white;opacity: 1;"></b>'+
            '   </p>'+
            '   <ul class="'+big[3]+'" style="padding: 10px 20px;">'+str+
            '   </ul>'+
            '</div>';
        $('.'+big[1]).remove();
        $('#container .'+big[0]).after(afterStr);
        $('.'+big[1]).css({display:'block'});
        $('.close').on('click',function () {
            $('.'+big[1]).remove();
        });
    }else {
        $('#container '+className).empty().html(str);
    }
};


//上一步，下一步，保存返回
var second;
//  /weibo_xnr_create/save_step_two/?task_id=WXNR0001&nick_name=大大DE律师
// &age=29&location=北京&career=律师&description=这是简介&active_time=9,10,11,19,20&day_post_average=9-12
$('.previous').on('click',function () {
    n=0;
    nameJudgment();
});
var n=0;
$('.next').on('click',function () {
    n=1;
    nameJudgment();
    //values();
});
$('.save_return').on('click',function () {
    n=0;
    nameJudgment();
    //values();
});
function nameJudgment() {
    //判断昵称是否重复
    var nickName=$('#name').val();
    public_ajax.call_request('GET','/weibo_xnr_create/nick_name_unique/?nick_name='+nickName,repeatNot);
}
function repeatNot(data) {
    if (data){
        values();
        //save();
    }else {
        $('#prompt p').text('您输入的昵称与系统数据重复，请重新输入。');
        $('#prompt').modal('show');
    }
};
$('.other-2 .choose input').on('click',function () {
    var s=$(this).attr('name');
    if (s=='pos'){
        $('.postNUM').show();
        $('.customize').hide();
    }else {
        $('.postNUM').hide();
        $('.postNUM').val('');
        $('.customize').show();
    }
})
function values() {
    var nickName=$('#name').val();
    var age=$('#age').val();
    var sex='';
    $(".gender input[type=radio]:radio:checked").each(function (index,item) {
        sex=$(this).val().toString();
    });
    var location=$('#place').val();
    var career=$('#career').val();
    var description=$('#description').val();

    var timelist=[];
    $(".other_basic input[type=checkbox]:checkbox:checked").each(function (index,item) {
        timelist.push($(this).val());
    });
    var active_time=Array.from(new Set(timelist)).join(',');

    var day_post_average='';//"abc 123 def".replace(/\s/g, "")
    if ($('.postNUM').val()){
        //patch('-',$('.postNUM').val().toString())==1
        if($('.postNUM').val().toString().indexOf('-')!=-1){
            day_post_average=$('.postNUM').val().toString().replace(/\s/g, "");
        }else {
            $('#prompt p').text('您输入的自定义发帖数有误，请重新输入（格式：6-8）。');
            $('#prompt').modal('show');
            return false;
        }
    }else {
        $(".other_basic .other-2 input[type=radio]:radio:checked").each(function (index,item) {
            day_post_average = $(this).val().toString();
        });
    }
    if (active_time||day_post_average){
        var saveSecond_url='/weibo_xnr_create/save_step_two/?submitter='+admin+'&task_id='+
            '&domain_name='+basicData.domain_name+'&role_name='+basicData.role_name+
            '&psy_feature='+basicData.psy_feature+'&political_side='+basicData.political_side+'&business_goal='+basicData.business_goal+
            '&monitor_keywords='+basicData.monitor_keywords+'&daily_interests='+basicData.daily_interests+
            '&active_time='+active_time+'&day_post_average='+day_post_average;
    }else {
        $('#prompt p').text('请检查您的活跃时间和日发帖量。');
        $('#prompt').modal('show');
        return false;
    }
    // var saveSecond_url='/weibo_xnr_create/save_step_two/?submitter='+admin+'&domain_name='+basicData.domain_name+'&role_name='+basicData.role_name+
    //     '&psy_feature='+basicData.psy_feature+'&political_side='+basicData.political_side+'&business_goal='+basicData.business_goal+
    //     '&monitor_keywords='+basicData.monitor_keywords+'&daily_interests='+basicData.daily_interests+'&nick_name='+nickName+'&age='+age+'&sex='+sex+
    //     '&location='+location+'&career='+career+'&description='+description+'&active_time='+active_time+'&day_post_average='+day_post_average;
    public_ajax.call_request('get',saveSecond_url,in_three);
    if (n == 1||n == 0){
        second={
            'nick_name':nickName,
            'age':age,
            'location':location,
            'career':career,
            'sex':sex,
            'active_time':active_time,
            'day_post_average':day_post_average,
            'description':description
        }
    };
}
function in_three(data) {
    if (data||data[0]){
        localStorage.setItem('secondStep',JSON.stringify(second));
        if (n==0){
            window.open('/personalCenter/individual/');
        }else {
            window.open('/registered/socialAccounts/');
        }
        localStorage.setItem('buildNewXnr',JSON.stringify(data[1]));
    }else {
        $('#prompt p').text('您输入的内容有误，请刷新页面重新输入。');
        $('#prompt').modal('show');
    }
}


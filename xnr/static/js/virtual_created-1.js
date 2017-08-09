var chara_url='/weibo_xnr_create/recommend_step_two/?domain_name='+basicData.domainName+
    '&role_name='+basicData.roleName+'&daily_interests='+basicData.daily;
public_ajax.call_request('get',chara_url,character);
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
}

function publicRecommend(field,className,tit) {
    var str='';
    if (recommendData[field].length==0||recommendData[field]==''){
        str='<p style="text-align: center;">抱歉，暂无数据。</p>';
    }else {
        if (field=='day_post_num_average'){
            str+='<li><a href="###">'+parseInt(recommendData[field])+'条</a></li>';
        }else {
            for(var a=0;a<recommendData[field].length;a++){
                var at=recommendData[field][a],time;
                if (field=='active_time'){
                    time=at+':00-'+at+':59';
                }else {
                    time=at;
                }
                str+='<li><a href="###" title="'+time+'">'+time+'</a></li>';
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
    window.location.href='/registered/targetCustom/';
});
var n=0;
$('.next').on('click',function () {
    n=1;
    values();
    localStorage.setItem('secondStep',JSON.stringify(second));
    window.open('/registered/socialAccounts/');
});
$('.save_return').on('click',function () {
    n=0;
    values();
    window.open('/personalCenter/individual/');
});

var task_id='WXNR0001';
function values() {
    var nickName=$('#name').val();
    var age=$('#age').val();
    var location=$('#place').val();
    var career=$('#career').val();
    var description=$('#description').val();
    var active_time=$('.timeRange').find('span').find('span').text().toString();
    var sex;
    $(".gender input[type=radio]:radio:checked").each(function (index,item) {
        sex=$(this).val().toString();
    });
    var day_post_average=$('#description').val();
    var saveSecond_url='/weibo_xnr_create/save_step_two/?task_id='+task_id='&nick_name='+nickName+'&age='+age+
        '&location='+location+'&career='+career+'&description='+description+'&active_time=9,10,11,19,20&day_post_average=9-12';
    public_ajax.call_request('get',saveSecond_url,in_three);
    if (n == 1){
        second={
            'nick_name':nickName,
            'age':age,
            'location':location,
            'career':career,
            'sex':sex,
            //'active_time':,
            //'day_post_average':,
            'description':description
        }
    };
}
function in_three(data) {
    if (data){
        window.open('/registered/socialAccounts/');
    }else {
        $('#prompt p').text('您输入的内容有误，请刷新页面重新输入。');
        $('#prompt').modal('show');
    }
}


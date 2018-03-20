//查看推荐
setTimeout(function () {
    // if (!$two||(go_on=='2')){
    var recommendURL=WFT_url+'/recommend_step_two/?domain_name='+$('#character1').text()+'&role_name='+
        $('#character2').text();
    if (flag==1){recommendURL+='&daily_interests='+$('#character6').text().toString().replace(/,/g,'，')};
    public_ajax.call_request('GET',recommendURL,recommendTwo);
},3000);
function recommendTwo(data) {
    if (isEmptyObject(data.role_example)){
        $('#role_example .role_example_list').html('<p style="text-align: center;">抱歉，暂无数据。</p>')
    }else {
        var peo='';
        for (var k in data.role_example){
            var a=data.role_example[k][0];
            var b=data.role_example[k][1];
            if (!a){a=k}
            if (!b){b='###'}
            peo+='<li><a pid="'+k+'" href="'+b+'" title="'+a+'">'+a+'</a></li>';
        }
        $('#role_example .role_example_list').html(peo);
    }
    var name,age,sex,location,career,description;
    if (data.nick_name){name=data.nick_name.toString().replace(/&/g,'，')}else {name='无昵称推荐'}
    if (data.age){age=data.age}else {age='无年龄推荐'}
    if (data.sex==1){sex='男'}else if (data.sex==2) {sex='女'}else {sex='未知'}
    if (data.user_location){location=data.user_location}else {location='无地理位置推荐'}
    if (data.career){career=data.career}else {career='无职业推荐'}
    if (data.description){description=data.description}else {description='无描述推荐'}
    $('#name').val(name);
    $('#age').val(age);
    $(".gender input[type='radio'][value='"+sex+"']").attr("checked",true);
    $('#place').val(location);
    $('#career').val(career);
    $('#description').val(description);
    for (var t of data.active_time){
        $(".task_time input[name='timetampe'][type='checkbox'][value='"+parseInt(t)+"']").attr("checked",true);
    }

    var posyNum = parseInt(data.day_post_num_average);
    if (posyNum>5){
        $('.other-2 .customize').hide();
        $('.other-2 .postNUM').show().val('0-'+parseInt(Number(posyNum)));
    }else if (posyNum==0){
        $(".other-2 input[name='Posting'][type='radio'][value='0-0']").attr("checked",true);
    }else if (posyNum>0&&posyNum<3){
        $(".other-2 input[name='Posting'][type='radio'][value='1-2']").attr("checked",true);
    }else if (posyNum>=3&&posyNum<=5){
        $(".other-2 input[name='Posting'][type='radio'][value='3-5']").attr("checked",true);
    }
}

//上一步，下一步，保存返回
var second,n=0;
$('.previous').on('click',function () {
    // n=0;
    // nameJudgment();
    if (go_on=='2'){
        var goUSER={
            'domain_name':$('#character1').text(),
            'role_name':$('#character2').text(),
        }
        localStorage.setItem('goONuser',JSON.stringify(goUSER));
    }
    window.open('/registered/targetCustom/');
});
$('.next').on('click',function () {
    n=1;
    nameJudgment();
});
$('.save_return').on('click',function () {
    n=2;
    nameJudgment();
});
function nameJudgment() {
    //判断昵称是否重复
    var nickName=$('#name').val();
    public_ajax.call_request('GET',WFT_url+'/nick_name_unique/?nick_name='+nickName,repeatNot);
    // if (go_on==2){
    //     var timelist=[];
    //     $(".other_basic input[type=checkbox]:checkbox:checked").each(function (index,item) {
    //         timelist.push($(this).val());
    //     });
    //     var actTime=Array.from(new Set(timelist)).join(',');
    //     var postNum;
    //     if ($('.postNUM').val()){
    //         //patch('-',$('.postNUM').val().toString())==1
    //         if($('.postNUM').val().toString().indexOf('-')!=-1){
    //             postNum=$('.postNUM').val().toString().replace(/\s/g, "");
    //         }else {
    //             $('#prompt p').text('您输入的自定义发帖数有误，请重新输入（格式：6-8）。');
    //             $('#prompt').modal('show');
    //             return false;
    //         }
    //     }else {
    //         $(".other_basic .other-2 input[type=radio]:radio:checked").each(function (index,item) {
    //             postNum = $(this).val().toString();
    //         });
    //     };
    //     var daily=$('#character6').text()
    //     var keywords=$('#character7').text();
    //     if (actTime&&postNum&&daily&&keywords){
    //         var modXNR_url='/weibo_xnr_create/modify_base_info/?xnr_user_no='+$id+'&active_time'+actTime+'&day_post_average='+
    //             postNum+'&daily_interests'+daily+'&monitor_keywords='+keywords;
    //         public_ajax.call_request('get',modXNR_url,success);
    //     }else {
    //         $('#prompt p').text('请检查您输入的内容（不能为空）');
    //         $('#prompt').modal('show');
    //     }
    // }
}
// function success(data) {
//     if (!data){
//         $('#prompt p').text('修改失败。');
//         $('#prompt').modal('show');
//     }else {
//         if (n==0){
//             window.open('/registered/targetCustom/');
//         }else if (n==1){
//             window.open('/registered/socialAccounts/');
//         }else if (n==2){
//             window.open('/personalCenter/individual/');
//         }
//     }
// }
function repeatNot(data) {
    if (data){
        values();
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
    var saveSecond_url;
    if (active_time||day_post_average){
        if(!taskID){taskID=''};
        saveSecond_url=WFT_url+'/save_step_two/?submitter='+admin+'&task_id='+taskID+
            '&domain_name='+basicData.domain_name+'&role_name='+basicData.role_name+
            '&psy_feature='+basicData.psy_feature+'&political_side='+basicData.political_side+'&business_goal='+basicData.business_goal+
            '&monitor_keywords='+basicData.monitor_keywords+'&daily_interests='+basicData.daily_interests;
    }else {
        $('#prompt p').text('请检查您的活跃时间和日发帖量。');
        $('#prompt').modal('show');
        return false;
    }
    // var saveSecond_url='/weibo_xnr_create/save_step_two/?submitter='+admin+'&domain_name='+basicData.domain_name+'&role_name='+basicData.role_name+
    //     '&psy_feature='+basicData.psy_feature+'&political_side='+basicData.political_side+'&business_goal='+basicData.business_goal+
    //     '&monitor_keywords='+basicData.monitor_keywords+'&daily_interests='+basicData.daily_interests+'&nick_name='+nickName+'&age='+age+'&sex='+sex+
    //     '&location='+location+'&career='+career+'&description='+description+'&active_time='+active_time+'&day_post_average='+day_post_average;
    if (n==1){
        public_ajax.call_request('get',saveSecond_url,in_three);
    }
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
    if (go_on==2){
        var first={
            'domain_name':$('#character1').text(),
            'role_name':$('#character2').text(),
            'daily_interests':$('#character6').text(),
            'psy_feature':$('#character3').text(),
            'political_side':$('#character4').text(),
            'business_goal':$('#character5').text(),
            'monitor_keywords':$('#character7').text(),
        };
        localStorage.setItem(firstStep,JSON.stringify(first));
        public_ajax.call_request('get',saveSecond_url,modSecondSuccess);
    }else if (go_on==1){
        var a=$('#name').val();
        var b=$('#age').val();
        var c=$('.gender input:radio[name="demo"]:checked').val();
        var d=$('#place').val().toString().replace(/,/g,'，');
        var ee=$('#career').val();
        var f=$('#description').val();
        var modSecond_ur=WFT_url+'/modify_userinfo/?nick_name='+a+'&age='+b+'&gender='+c+
            '&location='+d+'&career='+ee+'&description='+f;
        public_ajax.call_request('get',modSecond_ur,modSecondSuccess);
    }
}
function in_three(data) {
    if (data||data[0]){
        localStorage.setItem(secondStep,JSON.stringify(second));
        localStorage.setItem('buildNewXnr',JSON.stringify(data[1]));
        window.location.href='/registered/socialAccounts/?flag='+flag;
    }else {
        $('#prompt p').text('您输入的内容有误，请刷新页面重新输入。');
        $('#prompt').modal('show');
    }
}
function modSecondSuccess(data) {
    if (data){
        window.location.href='/personalCenter/individual/';
    }else {
        $('#prompt p').text('修改内容失败，请稍后再试。');
        $('#prompt').modal('show');
    }
}


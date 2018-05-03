var name1,name2,name3,password;
$('#go_bind').on('click',function () {
    name1=$('#username1').val();
    name2=$('#username2').val();
    name3=$('#username3').val();
    password=$('#passwords').val();
    if ((name1==''||name2=='')&&password==''&&name3==''){
        $('#_bind_per #information').text('账号名密码不能为空。');
    }else {
        $('#_bind_per #information').text('是否将该微博用户绑定为虚拟人？');
    }
    $('#_bind_per').modal('show');
});
function bindSF(data) {
    var txt='';
    if (data){
        if (data=='nick_name error'){
            txt='昵称输入错误，请检查昵称。';
        }else {
            txt='绑定成功';
            var listURL=WFT_url+'/recommend_follows/?monitor_keywords='+basicData_1.monitorKeywords;
            if (flag==1){listURL+='&daily_interests='+basicData_1.daily}
            public_ajax.call_request('get',listURL,list);
        }
    }else {
        txt='抱歉，系统网络原因，绑定失败';
        $('.backTWO').show();
        $('.notBind').hide();
        $('.sureBind').hide();
    }
    $('#success_fail #fs').text(txt);
    $('#success_fail').modal('show');
}
function userLIST() {
   // var taskID=JSON.parse(localStorage.getItem('buildNewXnr'));
    if (!taskID){
        taskID=JSON.parse(localStorage.getItem('buildNewXnr'));
    };
    var url1='weibo_mail_account',url2='weibo_phone_account'
    if(flag==4){
        url1='fb_mail_account',url2='fb_phone_account';
    }else if (flag==5){
        url1='tw_mail_account',url2='tw_phone_account';
    }
    var bind_url=WFT_url+'/save_step_three_1/?task_id='+taskID+'&'+url1+'='+name1 +
        '&'+url2+'='+name2+'&nick_name='+name3+'&password='+password;
    public_ajax.call_request('get',bind_url,bindSF);
}
function list(person) {
    var str1='',str2='';
    if (isEmptyObject(person.daily_interests)){
        str1='暂无数据';
        $('#success_fail .personlist1').css({textAlign:'center'});
    }else {
        for (var y in person.daily_interests){
            str1+=
                '<label class="demo-label" title="'+person.daily_interests[y]+'">'+
                '   <input class="demo-radio" type="checkbox" name="someone" value="'+y+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+person.daily_interests[y]+
                ' </label>';
        }
    };

    if (isEmptyObject(person.monitor_keywords)){
        str2='暂无数据';
        $('#success_fail .personlist2').css({textAlign:'center'});
    }else {
        for (var p in person.monitor_keywords){
            str2+=
                '<label class="demo-label" title="'+person.monitor_keywords[p]+'">'+
                '   <input class="demo-radio" type="checkbox" name="someone" value="'+p+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+person.monitor_keywords[p]+
                ' </label>';
        }
    };
    $('#success_fail .personlist1').html(str1);
    $('#success_fail .personlist2').html(str2);
}
$('#back').on('click',function () {
    window.open('/personalCenter/individual/');
});
$('.backTWO').on('click',function () {
    window.location.href='/registered/virtualCreated/?flag='+flag;
})
$('#release').on('click',function () {
    var t='';
    if (flag==1){t='posting'}else if (flag==4){t='postingTwitter'}
    else if(flag==5){t='postingFaceBook'};
    window.open('/control/'+t+'/');
});
function surefocus() {
    let people=[];
    $("[name=someone]:checkbox:checked").each(function (index,item) {
        people.push($(this).val());
    });
    let focus_url=WFT_url+'/save_step_three_2/?nick_name='+basicData_2.nick_name+'&followers_uids='+people.join(',');
    public_ajax.call_request('get',focus_url,focusSF);
}
function focusSF(data) {
    var txt='';
    if (data){
        txt='关注人物成功';
        $('.lastGO').show();
    }else {
        txt='抱歉，系统网络原因，关注人物失败';
    }
    $('#letGo p').text(txt);
    $('#letGo').modal('show');
}

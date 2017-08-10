var task_id='WXNR0001',phone='13192883429',uid='1897879843';
$('#go_bind').on('click',function () {
    let name=$('#username').val();
    let password=$('#passwords').val();
    if (name==''&&password==''){
        $('#_bind_per #information').text('账号名密码不能为空。');
    }else {
        name = '892312398@qq.com';password='111111';
        var bind_url='/weibo_xnr_create/save_step_three_1/?task_id='+task_id+'&weibo_mail_count='+name +
            '&weibo_phone_count='+phone+'&password='+password+'&uid='+uid;
        public_ajax.call_request('get',bind_url,bindSF);
        $('#_bind_per #information').text('是否将该微博用户绑定为虚拟人？');
    }
    $('#_bind_per').modal('show');
});
function bindSF(data) {
    var txt='';
    if (data){
        txt='绑定成功';
    }else {
        txt='抱歉，系统网络原因，绑定失败';
        $('.backTWO').show();
        $('.notBind').hide();
        $('.sureBind').hide();
    }
    $('#_bind_per #information').text(txt);
    $('#_bind_per').modal('show');
}
function userLIST() {
    var listURL='/weibo_xnr_create/recommend_follows/?monitor_keywords='+basicData_1.monitorKeywords+
        '&daily_interests='+basicData_1.daily;
    public_ajax.call_request('get',listURL,list);
}
function list(person) {
    var str='';
    for (var p of person.monitor_keywords){
        str+=
            '<label class="demo-label" title="'+p+'">'+
            '   <input class="demo-radio" type="checkbox" name="someone" value="'+p+'">'+
            '   <span class="demo-checkbox demo-radioInput"></span> '+p+
            ' </label>';
    }
    $('#success_fail .personlist').html(str);
}
$('#back').on('click',function () {
    readyGO();
    window.open('/personalCenter/individual/');
});
$('.backTWO').on('click',function () {
    window.location.href='/registered/virtualCreated/';
})
$('#release').on('click',function () {
    readyGO();
    window.open('/registered/posting/');
});
function readyGO() {
    let people=[];
    $("[name=someone]:checkbox:checked").each(function (index,item) {
        people.push($(this).val());
    });
    let focus_url='/weibo_xnr_create/save_step_three_2/?task_id='+task_id+
    '&followers_nickname='+people.join(',');
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
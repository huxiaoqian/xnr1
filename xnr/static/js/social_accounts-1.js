$('#go_bind').on('click',function () {
    let name=$('#username').val();
    let password=$('#passwords').val();
    if (name!=''&&password!=''){
        $('#_bind_per #information').text('账号名密码不能为空。');
    }else {
        $('#_bind_per #information').text('是否将该微博用户绑定为虚拟人？');
    }
    $('#_bind_per').modal('show');
});
$('#back').on('click',function () {
    window.open('/personalCenter/individual/');
});
$('#release').on('click',function () {
    window.open('/registered/posting/');
});
//登录虚拟人后取出ID或者名字
var ID_Num,REL_name,ID_name,userQQnum,nowUser;
function weiboORqq(type) {
    if (type=='weibo'){
        ID_Num=localStorage.getItem('user');
        REL_name=localStorage.getItem('userRelName');
        ID_name=localStorage.getItem('userName');
        if (ID_name){
            nowUser=decodeURI(ID_name);
        }
    }else if(type=="QQ") {
        ID_Num=localStorage.getItem('userQQ');
        REL_name=localStorage.getItem('userQQRelName');
        ID_name=localStorage.getItem('userQQName');
        userQQnum=localStorage.getItem('userQQnum');
        if (ID_name){
            nowUser=decodeURI(ID_name)+'（'+userQQnum+')';
        }
    }else if(type=="WX") {
        ID_Num=localStorage.getItem('userWX');
        REL_name=localStorage.getItem('userWXRelName');
        ID_name=localStorage.getItem('userWXName');
        if (ID_name){
            nowUser=decodeURI(ID_name);
        }
    }else if(type=="faceBook") {
        // ID_Num='FXNR0001';
        // REL_name='FXNR0001';
        // ID_name='FXNR0001';
        // nowUser=decodeURI('FXNR0001');
        ID_Num=localStorage.getItem('userFB');
        REL_name=localStorage.getItem('userFBRelName');
        ID_name=localStorage.getItem('userFBName');
        if (ID_name){
            nowUser=decodeURI(ID_name);
        }
    }else if(type=="twitter") {
        // ID_Num='TXNR0001';
        // REL_name='TXNR0001';
        // ID_name='TXNR0001';
        // nowUser=decodeURI('TXNR0001');
        ID_Num=localStorage.getItem('userTW');
        REL_name=localStorage.getItem('userTWRelName');
        ID_name=localStorage.getItem('userTWName');
        if (ID_name){
            nowUser=decodeURI(ID_name);
        }
    }
}

setTimeout(function(){
    if(loadingType=='QQ'){
        InloginName('QQ群虚拟人');
        // ---------10-12 LL向下展开盒子js--QQ
        var L_nav = $('.nav_top');
        $('#LL').empty();
        var LL_html = '<ul><li id="control"><i class="icon icon-cogs"></i>操作控制</li>';
        LL_html += '<li id="warning"><i class="icon icon-eye-open"></i>预警监控</li>';
        LL_html += '<li id="evaluation"><i class="icon icon-sitemap"></i></i>行为评估</li>';
        LL_html += '<li id="reportedmange"><i class="icon icon-share"></i>上报管理</li>';
        LL_html += '<li id="knowledgebase"><i class="icon icon-key"></i>知识库管理</li>';
        LL_html += '<li id="system"><i class="icon icon-inbox"></i>系统管理</li></ul>';
        $('#LL').append(LL_html);

        L_nav.mouseover(function () {
            $(this).find("#LL").stop().slideDown(200);
        });
        L_nav.mouseleave(function(){
            $(this).find("#LL").stop().slideUp(200);
        });
        //页面跳转
        var htmlUrl='';
        $('#control').on('click',function () {
            window.open('/personalCenter/individualQQ/');
        });
        $('#warning').on('click',function () {
            window.open('/inforDetection/inforCheckingQQ/');
        });
        $('#evaluation').on('click',function () {
            window.open('/behavioGauge/behaviorQQ/')
        });
        $('#reportedmange').on('click',function () {
            window.open('/reportManage/management/?flag=2');
        });
        $('#knowledgebase').on('click',function () {
            window.open('/knowledge/domainLibrary/?flag=2');
        });
        $('#system').on('click',function () {
            window.open('/systemManage/daily?flag=2');
        });
    }else if (loadingType=='weibo'){
        InloginName('微博虚拟人');
        // ---------10-12 LL向下展开盒子js--微博
        var L_nav = $('.nav_top');
        L_nav.mouseover(function () {
            $(this).find("#LL").stop().slideDown(200);
        })
        L_nav.mouseleave(function(){
            $(this).find("#LL").stop().slideUp(200);
        });
        //页面跳转
        $('#personal').on('click',function () {
            window.open('/personalCenter/individual/');
        });
        $('#control').on('click',function () {
            window.open('/control/operationControl/');
        });
        $('#info').on('click',function () {
            window.open('/inforDetection/inforChecking/');
        });
        $('#monitor').on('click',function () {
            window.open('/monitor/characterBehavior/');
        });
        $('#reported').on('click',function () {
            window.open('/behavioGauge/influeAssess/');
        });
        $('#knowledge').on('click',function () {
            window.open('/registered/targetCustom/?flag=1')
        });
        $('#reportedmange').on('click',function () {
            window.open('/reportManage/management/?flag=1');
        });
        $('#knowledgebase').on('click',function () {
            window.open('/knowledge/domainLibrary/?flag=1');
        });
        $('#system').on('click',function () {
            window.open('/systemManage/daily/?flag=1');
        });
    }else if (loadingType=='WX'){
        InloginName('微信虚拟人');
        // ---------10-30 LL向下展开盒子js--WX
        var L_nav = $('.nav_top');
        $('#LL').empty();
        var LL_html = '<ul><li id="control"><i class="icon icon-cogs"></i>操作控制</li>';
        LL_html += '<li id="warning"><i class="icon icon-eye-open"></i>预警监控</li>';
        LL_html += '<li id="evaluation"><i class="icon icon-sitemap"></i></i>行为评估</li>';
        LL_html += '<li id="reportedmange"><i class="icon icon-share"></i>上报管理</li>';
        LL_html += '<li id="knowledgebase"><i class="icon icon-key"></i>知识库管理</li>';
        LL_html += '<li id="system"><i class="icon icon-inbox"></i>系统管理</li></ul>';
        $('#LL').append(LL_html);

        L_nav.mouseover(function () {
            $(this).find("#LL").stop().slideDown(200);
        });
        L_nav.mouseleave(function(){
            $(this).find("#LL").stop().slideUp(200);
        });
        //页面跳转
        var htmlUrl='';
        // 操作控制
        $('#control').on('click',function () {
            window.open('/personalCenter/individualWX/');
        });
        // 预警监控
        $('#warning').on('click',function () {
            window.open('/inforDetection/inforCheckingWX/');
        });
        // 行为评估
        $('#evaluation').on('click',function () {
            window.open('/behavioGauge/behaviorWX/');
        });

        $('#reportedmange').on('click',function () {
            window.open('/reportManage/management/?flag=3');
        });
        $('#knowledgebase').on('click',function () {
            window.open('/knowledge/domainLibrary/?flag=3');
        });
        $('#system').on('click',function () {
            window.open('/systemManage/daily/?flag=3');
        });
    }else if(loadingType=='twitter'){
        InloginName('Twitter虚拟人');
        var L_nav = $('.nav_top');
        $('#LL').empty();
        var LL_html =
            '<ul><li id="personal"><i class="icon icon-github-alt"></i>我的虚拟人</li>'+
            '<li id="control"><i class="icon icon-cogs"></i>操作控制</li>'+
            '<li id="info"><i class="icon icon-eye-open"></i>信息监测</li>'+
            '<li id="monitor"><i class="icon icon-warning-sign"></i>预警监控</li>'+
            '<li id="knowledge"><i class="icon icon-user-md"></i>虚拟人定制</li>'+
            '<li id="reported"><i class="icon icon-sitemap"></i>行为评估</li>'+
            '<li id="reportedmange"><i class="icon icon-share"></i>上报管理</li>'+
            '<li id="knowledgebase"><i class="icon icon-key"></i>知识库管理</li>'+
            '<li id="system"><i class="icon icon-inbox"></i>系统管理</li></ul>'
        $('#LL').append(LL_html);
        L_nav.mouseover(function () {
            $(this).find("#LL").stop().slideDown(200);
        });
        L_nav.mouseleave(function(){
            $(this).find("#LL").stop().slideUp(200);
        });
        $('#personal').on('click',function () {
            window.open('/personalCenter/individualTwitter/');
        });
        $('#control').on('click',function () {
            window.open('/control/operationTwitter/');
        });
        $('#info').on('click',function () {
            window.open('/inforDetection/inforCheckingTwitter/');
        });
        $('#monitor').on('click',function () {
            window.open('/monitor/characterBehaviorTwitter/');
        });
        $('#reported').on('click',function () {
            window.open('/behavioGauge/influeAssessTwitter/');
        });
        $('#knowledge').on('click',function () {
            window.open('/registered/targetCustom/?flag=5')
        });
        $('#reportedmange').on('click',function () {
            window.open('/reportManage/management/?flag=5');
        });
        $('#knowledgebase').on('click',function () {
            window.open('/knowledge/domainLibrary/?flag=5');
        });
        $('#system').on('click',function () {
            window.open('/systemManage/daily/?flag=5');
        });
    }else if(loadingType=='faceBook') {
        InloginName('FaceBook虚拟人');
        var L_nav = $('.nav_top');
        $('#LL').empty();
        var LL_html =
            '<ul><li id="personal"><i class="icon icon-github-alt"></i>我的虚拟人</li>'+
            '<li id="control"><i class="icon icon-cogs"></i>操作控制</li>'+
            '<li id="info"><i class="icon icon-eye-open"></i>信息监测</li>'+
            '<li id="monitor"><i class="icon icon-warning-sign"></i>预警监控</li>'+
            '<li id="knowledge"><i class="icon icon-user-md"></i>虚拟人定制</li>'+
            '<li id="reported"><i class="icon icon-sitemap"></i>行为评估</li>'+
            '<li id="reportedmange"><i class="icon icon-share"></i>上报管理</li>'+
            '<li id="knowledgebase"><i class="icon icon-key"></i>知识库管理</li>'+
            '<li id="system"><i class="icon icon-inbox"></i>系统管理</li></ul>'
        $('#LL').append(LL_html);
        L_nav.mouseover(function () {
            $(this).find("#LL").stop().slideDown(200);
        });
        L_nav.mouseleave(function(){
            $(this).find("#LL").stop().slideUp(200);
        });
        $('#personal').on('click',function () {
            window.open('/personalCenter/individualFaceBook/');
        });
        $('#control').on('click',function () {
            window.open('/control/operationFaceBook/');
        });
        $('#info').on('click',function () {
            window.open('/inforDetection/inforCheckingFaceBook/');
        });
        $('#monitor').on('click',function () {
            window.open('/monitor/characterBehaviorFaceBook/');
        });
        $('#reported').on('click',function () {
            window.open('/behavioGauge/influeAssessFaceBook/');
        });
        $('#knowledge').on('click',function () {
            window.open('/registered/targetCustom/?flag=4')
        });
        $('#reportedmange').on('click',function () {
            window.open('/reportManage/management/?flag=4');
        });
        $('#knowledgebase').on('click',function () {
            window.open('/knowledge/domainLibrary/?flag=4');
        });
        $('#system').on('click',function () {
            window.open('/systemManage/daily/?flag=4');
        });
    }
},500);

$(document).ready(function() {
    $(document).on('show.bs.modal', '.modal', function() {
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    });
});
//切换虚拟人
$('.change').on('click',function () {
    var THEmid='/weibo_xnr_create/show_weibo_xnr/';
    // var THEmid;
    if (loadingType=='weibo'){
        THEmid='/weibo_xnr_create/show_weibo_xnr/';
    }else if (loadingType=='QQ'){
        THEmid='/qq_xnr_manage/show_qq_xnr/';
    }else if(loadingType=='WX'){
        THEmid='/wx_xnr_manage/show/';
    }else if(loadingType=='faceBook'){
        THEmid='/facebook_xnr_create/show_fb_xnr/';
    }else if(loadingType=='twitter'){
        THEmid='/twitter_xnr_create/show_tw_xnr/';
    }
    var THEurl=THEmid+"?submitter="+admin;
    public_ajax.call_request('GET',THEurl,addXnr)
    $('#choosePerson').modal('show');
});
function addXnr(data) {
    var str='';
    if (loadingType=='QQ'){
        $.each(data,function (index,item) {
            var name;
            if (item.nickname==''||item.nickname=='unknown'||!item.nickname){
                name='无昵称';
            }else {
                name=item.nickname;
            }
            str+=
                '<label class="demo-label" title="'+name+'">'+
                '   <input class="demo-radio" type="radio" name="ID" valueNum="'+item.qq_number+'" valueID='+item.xnr_user_no+' valueName='+name+'>'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+name+'（'+item.qq_number+'）'+
                '</label>';
        });
    }else if(loadingType=='weibo'){
        for (var k in data){
            if (data[k]==''||data[k]=='unknown'){
                data[k]='无昵称';
            }
            str+=
                '<label class="demo-label" title="'+data[k]+'">'+
                '   <input class="demo-radio" type="radio" name="ID" valueID='+k+' valueName='+data[k]+'>'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+data[k]+
                '</label>';
        }
    }else if(loadingType=='WX'){
        $.each(data,function (index,item) {
            var name;
            if (item.wx_id==''||item.wx_id=='unknown'||!item.wx_id){
                name='无昵称';
            }else {
                name=item.wx_id;
            }
            str+=
                '<label class="demo-label" title="'+name+'">'+
                '   <input class="demo-radio" type="radio" name="ID" valueNum="'+item.wxbot_id+'" valueID='+item.wxbot_id+' valueName='+name+'>'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+name+'（'+item.wxbot_id+'）'+
                '</label>';
        });
    }else if (loadingType=='faceBook'){
        for (var k in data){
            if (data[k]==''||data[k]=='unknown'){
                data[k]='无昵称';
            }
            str+=
                '<label class="demo-label" title="'+data[k]+'">'+
                '   <input class="demo-radio" type="radio" name="ID" valueID='+k+' valueName='+data[k]+'>'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+data[k]+
                '</label>';
        }
    }else if (loadingType=='twitter'){
        for (var k in data){
            if (data[k]==''||data[k]=='unknown'){
                data[k]='无昵称';
            }
            str+=
                '<label class="demo-label" title="'+data[k]+'">'+
                '   <input class="demo-radio" type="radio" name="ID" valueID='+k+' valueName='+data[k]+'>'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+data[k]+
                '</label>';
        }
    }
    $('#choosePerson .identity').html(str);
}
$('#choosePerson .sure_in').on('click',function () {
    if (loadingType=='QQ'){
        var userQQID=$('input:radio[name="ID"]:checked').attr('valueID');
        var userQQName=$('input:radio[name="ID"]:checked').attr('valueName');
        var userQQnum=$('input:radio[name="ID"]:checked').attr('valueNum');
        var userType=$('input:radio[name="choose"]:checked').val();
        if (!userQQID||!userQQName||!userType){
            $('#pormpt p').text('请检查选择登陆的QQ显示模式。');
            $('#pormpt').modal('show');
            return false;
        }else {
            var id_or_name='';
            if (userType=='隐身'){
                id_or_name=userQQID;
            }else {
                id_or_name=userQQName;
            }
            localStorage.setItem('userQQ',encodeURI(userQQID));
            localStorage.setItem('userQQRelName',encodeURI(userQQName));
            localStorage.setItem('userQQnum',encodeURI(userQQnum));
            localStorage.setItem('userQQName',encodeURI(id_or_name));
        }
    }else if (loadingType=='weibo'){
        var userID=$('input:radio[name="ID"]:checked').attr('valueID');
        var userName=$('input:radio[name="ID"]:checked').attr('valueName');
        var userType=$('input:radio[name="choose"]:checked').val();
        if (!userID||!userName||!userType){
            $('#pormpt p').text('请检查选择登陆的虚拟人显示模式。');
            $('#pormpt').modal('show');
            return false;
        }else {
            var id_or_name='';
            if (userType=='隐身'){
                id_or_name=userID;
            }else {
                id_or_name=userName;
            }
            localStorage.setItem('user',encodeURI(userID));
            localStorage.setItem('userRelName',encodeURI(userName));
            localStorage.setItem('userName',encodeURI(id_or_name));
        }
    }else if (loadingType=='WX'){
        var userWXID=$('input:radio[name="ID"]:checked').attr('valueID');
        var userWXName=$('input:radio[name="ID"]:checked').attr('valueName');
        var userType=$('input:radio[name="choose"]:checked').val();
        if (!userWXID||!userWXName||!userType){
            $('#pormpt p').text('请检查选择登陆的微信显示模式。');
            $('#pormpt').modal('show');
            return false;
        }else {
            var id_or_name='';
            if (userType=='隐身'){
                id_or_name=userWXID;
            }else {
                id_or_name=userWXName;
            }
            localStorage.setItem('userWX',encodeURI(userWXID));
            localStorage.setItem('userWXRelName',encodeURI(userWXName));
            // localStorage.setItem('userQQnum',encodeURI(userQQnum));
            localStorage.setItem('userWXName',encodeURI(id_or_name));
        }
    }else if (loadingType=='faceBook'){
        var userID=$('input:radio[name="ID"]:checked').attr('valueID');
        var userName=$('input:radio[name="ID"]:checked').attr('valueName');
        var userType=$('input:radio[name="choose"]:checked').val();
        if (!userID||!userName||!userType){
            $('#pormpt p').text('请检查选择登陆的虚拟人显示模式。');
            $('#pormpt').modal('show');
        }else {
            var id_or_name='';
            if (userType=='隐身'){
                id_or_name=userID;
            }else {
                id_or_name=userName;
            }
            localStorage.setItem('userFB',encodeURI(userID));
            localStorage.setItem('userFBRelName',encodeURI(userName));
            localStorage.setItem('userFBName',encodeURI(id_or_name));
            $('#xnrName').text(id_or_name+'（'+userID+'）').attr('title',id_or_name+'（'+userID+'）');
        }
    }
    location.reload();
});

$('.old').on('click',Change);
$('.old_2').on('click',Change);
$('.old_3').on('click',Change);
$('.old_4').on('click',Change);
var flagtxt='';
function Change(){
    var txt=$(this).find('span').text();
    flagtxt=txt;
    if (txt=='微博虚拟人'){
        same_xnr('weibo')
        setTimeout(function () {
            window.open('/index/navigation/');
        },1000);
    }else if(txt=='QQ群虚拟人') {
        same_xnr('qq');
        setTimeout(function () {
            window.open('/index/navigationQQ/');
        },1000)
    }
    /*else if(txt=='微信虚拟人'){
        same_xnr('weixin');
        setTimeout(function () {
            window.open('/index/navigationWX/');
        },1000);
    }else if(txt=='FaceBook虚拟人'){
        same_xnr('facebook');
        setTimeout(function () {
            window.open('/index/navigationFaceBook/');
        },1000);
    }else if(txt=='Twitter虚拟人'){
        same_xnr('twitter');
        setTimeout(function () {
            window.open('/index/navigationTwitter/');
        },1000);
    }*/
    $('#errorInfor h4').text('跳转提示');
    $('#errorInfor p').text('准备跳转中...请稍后...');
    $('#errorInfor').modal('show');
    setTimeout(function () {
        $('#errorInfor').modal('hide');
    },1000);
}
function same_xnr(mid2) {
    var txt=$('.nav_type').text(),mid1='',xnrNo='';
    if (txt=='(微博)'){
        mid1='weibo';xnrNo=localStorage.getItem('user');
    }else if (flagType=='2'){
        mid1='qq';xnrNo=localStorage.getItem('userQQ');
    }else if (flagType=='3'){
        mid1='weixin';xnrNo=localStorage.getItem('userWX');
    }else if (flagType=='4'){
        mid1='facebook';xnrNo=localStorage.getItem('userFB');
    }else if (flagType=='5'){
        mid1='twitter';xnrNo=localStorage.getItem('userTw');
    }
    var sameXnr_url='/system_manage/change_xnr_platform/?origin_platform='+mid1+'&origin_xnr_user_no='+xnrNo+'&new_platform='+mid2;
    // public_ajax.call_request('GET',sameXnr_url,sameXnrPoint)
}
function sameXnrPoint(data) {
    for (var k in data[0]){
        var sameID='';
        if (data[0][k]){sameID=data[0][k];localStorage.setItem('sameXnr',sameID);};
    }
}

//点击首页
$('#backHome').on('click',function () {
    var lf= $('.loadingUser .dropdown-menu .current').find('span').text();
    if (lf=='QQ群虚拟人'){
        $('#backHome .list_one.li_a').attr('href','/index/navigationQQ/');
    }else if(lf=='微博虚拟人') {
        $('#backHome .list_one.li_a').attr('href','/index/navigation/');
    }else if(lf=='微信虚拟人'){
        $('#backHome .list_one.li_a').attr('href','/index/navigationWX/');
    }else if(lf=='Twitter虚拟人') {
        $('#backHome .list_one.li_a').attr('href','/index/navigationTwitter/');
    }else if(lf=='FaceBook虚拟人') {
        $('#backHome .list_one.li_a').attr('href','/index/navigationFaceBook/');
    }
});
var _$xnrList=['微博虚拟人', 'QQ群虚拟人', '微信虚拟人', 'FaceBook虚拟人', 'Twitter虚拟人'];
function InloginName(nameType) {
    $('.current').find('span').text(nameType);
    _$xnrList.removeByValue(nameType);
    $('.old').find('span').text(_$xnrList[0]);
    $('.old_2').find('span').text(_$xnrList[1]);
    $('.old_3').find('span').text(_$xnrList[2]);
    $('.old_4').find('span').text(_$xnrList[3]);
    $('.loadingUser .nav_name').text(nowUser);
}
//存  localStorage.setItem('TYPE','1');
//取  localStorage.getItem('TYPE');
//删  localStorage.removeItem('TYPE');
function judgment(typeNum){
    var typeNum=Number(typeNum);
    var afterEle='';
    if (typeNum==1){
        $('.coorName').text('个人中心');
        $('.xnrShowHide').hide();
    }else if (typeNum==2){
        $('.coorName').text('操作控制');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/operationControl/">'+
            '        <i class="icon icon-user"></i>&nbsp;虚拟人中心' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/posting/">' +
            '        <i class="icon icon-pencil"></i>&nbsp;发帖操作' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/socialFeedback/">' +
            '        <i class="icon icon-random"></i>&nbsp;社交反馈' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/activeSocialization/">' +
            '        <i class="icon icon-headphones"></i>&nbsp;主动社交' +
            '    </a>'+
            '</li>';
    }else if (typeNum==3){
        $('.coorName').text('信息监测');
    }else if (typeNum==4){
        $('.coorName').text('预警监控');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/characterBehavior/">' +
            '        <i class="icon icon-user-md"></i>&nbsp;人物行为预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/speechContent/">' +
            '        <i class="icon icon-comment-alt"></i>&nbsp;言论内容预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/eventEmerges/">' +
            '        <i class="icon icon-bullhorn"></i>&nbsp;事件涌现预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/timeWarning/">' +
            '        <i class="icon icon-time"></i>&nbsp;时间预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/communityWarning/">' +
            '        <i class="icon icon-building"></i>&nbsp;社区预警' +
            '    </a>'+
            '</li>';
    }else if (typeNum==5){
        $('.coorName').text('行为评估');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/influeAssess/">' +
            '        <i class="icon icon-lightbulb"></i>&nbsp;影响力评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/penetration/">' +
            '        <i class="icon icon-tint"></i>&nbsp;渗透力评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/safe/">' +
            '        <i class="icon icon-glass"></i>&nbsp;安全性评估' +
            '    </a>'+
            '</li>';
            //'<li class="main_li">'+
            //'    <a class="li_a" href="/behavioGauge/evCompare/">' +
            //'        <i class="icon icon-paste"></i>&nbsp;对比评估' +
            //'    </a>'+
            //'</li>';
    }else if (typeNum==6){
        $('.coorName').text('虚拟人定制');
        $('.xnrShowHide').hide();
    }else if (typeNum==7){
        $('.coorName').text('上报管理');
        $('.xnrShowHide').hide();
    }else if (typeNum==8){
        $('.coorName').text('知识库管理');
        $('.xnrShowHide').hide();
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/domainLibrary/?flag=1">' +
            '        <i class="icon icon-globe"></i>&nbsp;领域知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/characterLibrary/?flag=1">' +
            '        <i class="icon icon-github"></i>&nbsp;角色知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/businessLibrary/?flag=1">' +
            '        <i class="icon icon-glass"></i>&nbsp;业务知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/speechLibrary/?flag=1">' +
            '        <i class="icon icon-comment"></i>&nbsp;言论知识库' +
            '    </a>'+
            '</li>';
    }else if (typeNum==9){
        $('.coorName').text('系统管理');
        $('.xnrShowHide').hide();
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/daily/?flag=1">' +
            '        <i class="icon icon-lightbulb"></i>&nbsp;日志管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/purview/?flag=1">' +
            '        <i class="icon icon-tint"></i>&nbsp;权限管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/virtual/?flag=1">' +
            '        <i class="icon icon-glass"></i>&nbsp;虚拟人管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/userMange/?flag=1">' +
            '        <i class="icon icon-user-md"></i>&nbsp;用户管理' +
            '    </a>'+
            '</li>';
    };
    $('.behind').html(afterEle);
};

function judgmentFaceBook(typeNum) {
    var typeNum=Number(typeNum);
    var afterEle='';
    if (typeNum==1){
        $('.coorName').text('个人中心');
        $('.xnrShowHide').hide();
    }else if (typeNum==2){
        $('.coorName').text('操作控制');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/operationFaceBook/">'+
            '        <i class="icon icon-user"></i>&nbsp;虚拟人中心' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/postingFaceBook/">' +
            '        <i class="icon icon-pencil"></i>&nbsp;发帖操作' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/socialFeedbackFaceBook/">' +
            '        <i class="icon icon-random"></i>&nbsp;社交反馈' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/activeSocializationFaceBook/">' +
            '        <i class="icon icon-headphones"></i>&nbsp;主动社交' +
            '    </a>'+
            '</li>';
    }else if (typeNum==3){
        $('.coorName').text('信息监测');
    }else if (typeNum==4){
        $('.coorName').text('预警监控');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/characterBehaviorFaceBook/">' +
            '        <i class="icon icon-user-md"></i>&nbsp;人物行为预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/speechContentFaceBook/">' +
            '        <i class="icon icon-comment-alt"></i>&nbsp;言论内容预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/eventEmergesFaceBook/">' +
            '        <i class="icon icon-bullhorn"></i>&nbsp;事件涌现预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/timeWarningFaceBook/">' +
            '        <i class="icon icon-time"></i>&nbsp;时间预警' +
            '    </a>'+
            '</li>';
    }else if (typeNum==5){
        $('.coorName').text('行为评估');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/influeAssessFaceBook/">' +
            '        <i class="icon icon-lightbulb"></i>&nbsp;影响力评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/penetrationFaceBook/">' +
            '        <i class="icon icon-tint"></i>&nbsp;渗透力评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/safeFaceBook/">' +
            '        <i class="icon icon-glass"></i>&nbsp;安全性评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/evCompare/">' +
            '        <i class="icon icon-paste"></i>&nbsp;对比评估' +
            '    </a>'+
            '</li>';;
    }else if (typeNum==6){
        $('.coorName').text('虚拟人定制');
        $('.xnrShowHide').hide();
    }else if (typeNum==7){
        $('.coorName').text('上报管理');
        $('.xnrShowHide').hide();
    }else if (typeNum==8){
        $('.coorName').text('知识库管理');
        $('.xnrShowHide').hide();
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/domainLibrary/?flag=4">' +
            '        <i class="icon icon-globe"></i>&nbsp;领域知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/characterLibrary/?flag=4">' +
            '        <i class="icon icon-github"></i>&nbsp;角色知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/businessLibrary/?flag=4">' +
            '        <i class="icon icon-glass"></i>&nbsp;业务知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/speechLibrary/?flag=4">' +
            '        <i class="icon icon-comment"></i>&nbsp;言论知识库' +
            '    </a>'+
            '</li>';
    }else if (typeNum==9){
        $('.coorName').text('系统管理');
        $('.xnrShowHide').hide();
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/daily/?flag=4">' +
            '        <i class="icon icon-lightbulb"></i>&nbsp;日志管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/purview/?flag=4">' +
            '        <i class="icon icon-tint"></i>&nbsp;权限管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/virtual/?flag=4">' +
            '        <i class="icon icon-glass"></i>&nbsp;虚拟人管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/userMange/?flag=4">' +
            '        <i class="icon icon-user-md"></i>&nbsp;用户管理' +
            '    </a>'+
            '</li>';
    };
    $('.behind').html(afterEle);
};

function judgmentTwitter(typeNum) {
    var typeNum=Number(typeNum);
    var afterEle='';
    if (typeNum==1){
        $('.coorName').text('个人中心');
        $('.xnrShowHide').hide();
    }else if (typeNum==2){
        $('.coorName').text('操作控制');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/operationTwitter/">'+
            '        <i class="icon icon-user"></i>&nbsp;虚拟人中心' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/postingTwitter/">' +
            '        <i class="icon icon-pencil"></i>&nbsp;发帖操作' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/socialFeedbackTwitter/">' +
            '        <i class="icon icon-random"></i>&nbsp;社交反馈' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/control/activeSocializationTwitter/">' +
            '        <i class="icon icon-headphones"></i>&nbsp;主动社交' +
            '    </a>'+
            '</li>';
    }else if (typeNum==3){
        $('.coorName').text('信息监测');
    }else if (typeNum==4){
        $('.coorName').text('预警监控');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/characterBehaviorTwitter/">' +
            '        <i class="icon icon-user-md"></i>&nbsp;人物行为预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/speechContentTwitter/">' +
            '        <i class="icon icon-comment-alt"></i>&nbsp;言论内容预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/eventEmergesTwitter/">' +
            '        <i class="icon icon-bullhorn"></i>&nbsp;事件涌现预警' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/monitor/timeWarningTwitter/">' +
            '        <i class="icon icon-time"></i>&nbsp;时间预警' +
            '    </a>'+
            '</li>';
    }else if (typeNum==5){
        $('.coorName').text('行为评估');
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/influeAssessTwitter/">' +
            '        <i class="icon icon-lightbulb"></i>&nbsp;影响力评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/penetrationTwitter/">' +
            '        <i class="icon icon-tint"></i>&nbsp;渗透力评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/safeTwitter/">' +
            '        <i class="icon icon-glass"></i>&nbsp;安全性评估' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/behavioGauge/evCompare/">' +
            '        <i class="icon icon-paste"></i>&nbsp;对比评估' +
            '    </a>'+
            '</li>';;
    }else if (typeNum==6){
        $('.coorName').text('虚拟人定制');
        $('.xnrShowHide').hide();
    }else if (typeNum==7){
        $('.coorName').text('上报管理');
        $('.xnrShowHide').hide();
    }else if (typeNum==8){
        $('.coorName').text('知识库管理');
        $('.xnrShowHide').hide();
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/domainLibrary/?flag=5">' +
            '        <i class="icon icon-globe"></i>&nbsp;领域知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/characterLibrary/?flag=5">' +
            '        <i class="icon icon-github"></i>&nbsp;角色知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/businessLibrary/?flag=5">' +
            '        <i class="icon icon-glass"></i>&nbsp;业务知识库' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/knowledge/speechLibrary/?flag=5">' +
            '        <i class="icon icon-comment"></i>&nbsp;言论知识库' +
            '    </a>'+
            '</li>';
    }else if (typeNum==9){
        $('.coorName').text('系统管理');
        $('.xnrShowHide').hide();
        afterEle=
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/daily/?flag=5">' +
            '        <i class="icon icon-lightbulb"></i>&nbsp;日志管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/purview/?flag=5">' +
            '        <i class="icon icon-tint"></i>&nbsp;权限管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/virtual/?flag=5">' +
            '        <i class="icon icon-glass"></i>&nbsp;虚拟人管理' +
            '    </a>'+
            '</li>'+
            '<li class="main_li">'+
            '    <a class="li_a" href="/systemManage/userMange/?flag=5">' +
            '        <i class="icon icon-user-md"></i>&nbsp;用户管理' +
            '    </a>'+
            '</li>';
    };
    $('.behind').html(afterEle);
};

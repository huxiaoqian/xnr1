var domainName,roleName;
$('input[name=demo1]').on('click',function () {
    domainName=$(this).parent().attr('title');
    var nameLEN=$(this).attr('name').toString();
    var creat_url='/weibo_xnr_create/domain2role/?domain_name='+domainName;
    public_ajax.call_request('get',creat_url,creat_1)
});
function creat_1(data) {
    addLabel(data,'opt-1','demo2');
}
function creat_2(data) {
    addLabel(data,'opt-2&opt-3','demo3&demo4');
}

function addLabel(data,className,name) {
    var m=Number(name.charAt(name.length-1));
    var _string;
    if (m>3){
        var c=className.split('&'),n=name.split('&'),f=0;
        console.log(data)
        for (var k = 0;k<2;k++){
            var ary=[];
            if (k==0){
                $.each(data['political_side'],function (index,item) {
                    ary.push(item[0].toString());
                });
            }else if(k==1){
                $.each(data['psy_feature'],function (index,item) {
                    ary.push(item[0].toString());
                });
            }
            _string=labelSTR(ary,n[k]);
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
function labelSTR(data,name) {
    var str='';
    if (data.length==0){
        str='暂无数据';
    }else {
        for(var i=0;i<data.length;i++){
            str+= '<label class="demo-label" title="'+data[i]+'">'+
                '   <input class="demo-radio" type="radio" name="'+name+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+data[i]+
                '</label>';
        }
    }

    return str;
}

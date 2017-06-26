function bindAdvanced(){
    $("#show_advanced").off("click").click(function(){
        if (($('#supersearch')).is(':hidden')){
            $(this).html('收起高级搜索');
            $("#supersearch").css('display', 'block');
        }
        else{
            $(this).html('高级搜索');
            $("#supersearch").css('display', 'none');
        }
    });
    $('#commit_search').click(function(){
        var current_user = $('#current_user').text();
        if ($('#supersearch').is(':hidden')){
            var url = '/attribute/portrait_search/?stype=1';
            url += get_simple_par();
        }
        else{
            var url = '/attribute/portrait_search/?stype=2';
            url += get_advanced_par();
        }
        url += '&submit_user=' + current_user;
        console.log(url);
        draw_conditions(url);
        //var url = '/attribute/portrait_search/?stype=1';
        base_call_ajax_request(url, draw_search_results);
        window.location.href = '#search_result';
    });
}


function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}
function draw_conditions(url){
    $("#search_result").css("margin-top", "40px");
    $('#conditions').empty();
    var html = '';
    var par_url = url.split('?')[1];
    var par_list = par_url.split('&');
    for (var i = 0;i < par_list.length;i++){
        var pair = par_list[i].split('=');
        var pre_name = pair[0];
        var pre_value;
        if (pair[1]){
            pre_value = pair[1];
        }
        else{
            pre_value = '';
        }
        var fix_result = process_par(pre_name, pre_value);
        //console.log(fix_result);
        var fix_name = fix_result[0];
        var fix_value = fix_result[1];
        // console.log(fix_name);
        // console.log(fix_value);
        if (fix_value){
            if (fix_value.indexOf(',') >= 0){
                var term_list = fix_value.split(',');
                for (var j = 0; j < term_list.length;j++){
                    html += '<span class="mouse" style="margin-left:10px">'+ fix_name + '：'+ term_list[j] + '</span>';
                }
            }
            else{
                html += '<span class="mouse" style="margin-left:10px">'+ fix_name + '：'+ fix_value + '</span>';
            }
        }
    }

    $('#conditions').html(html);
    return;
}
function process_par(name, value){
    var result = new Array();
    if(name=='term'){
        result[0] = '用户ID或昵称';
        result[1] = value;
    }
    else if(name=='activity_geo'){
        result[0] = '活跃地点';
        result[1] = value.split('/').join(' ');
    }
    else if(name=='keywords_string'){
        result[0] = '关键词';
        result[1] = value;
    }
    else if(name=='hashtag'){
        result[0] = '微话题';
        result[1] = value;
    }
    else if(name=='psycho_status_by_emotion'){
        result[0] = '语言特征';
        result[1] = value;
    }
    else if(name=='psycho_status_by_word'){
        result[0] = '性格特征';
        result[1] = value;
    }
    else if(name=='domain'){
        result[0] = '身份';
        result[1] = value;
    }
    else if(name=='topic_string'){
        result[0] = '领域';
        result[1] = value;
    }
    else if(name=='tag'){
        result[0] = '标签';
        result[1] = '';
        var term_list = value.split(',');
        for (var i = 0;i < term_list.length;i++){
            result[1] += (term_list[i].replace(':', '--') + ',');
        }
        result[1] = result[1].substring(0, result[1].length-1);
    }
    else{
        result[0] = '';
        result[1] = '';
    }
    return result;
}
function get_simple_par(){
    var str = '&term=' + $('#term').val();
    return str
}
function get_advanced_par(){
    var temp='';
    var input_value;
    var input_name;
    $('.ad-search').each(function(){
        input_name = '&' + $(this).attr('name');
        temp += input_name;
        input_value = '=' + $(this).val();
        if (input_name == '&activity_geo'){
            input_value = input_value.replace('省','');
            input_value = input_value.replace('市','');
            input_value = input_value.replace('市','');
        }
        temp += input_value;
    });
    /*
    var psycho_status_by_emotion = new Array();
    $("[name='psycho_status_by_emotion']:checked").each(function(){
        psycho_status_by_emotion.push($(this).val());
    });
    temp += '&psycho_status_by_emotion=' + psycho_status_by_emotion.join(',');
    
    var psycho_status_by_word = new Array();
    $("[name='psycho_status_by_word']:checked").each(function(){
        psycho_status_by_word.push($(this).val());
    });
    temp += '&psycho_status_by_word=' + psycho_status_by_word.join(',');
    */
    var domain = new Array();
    $("[name='domain']:checked").each(function(){
        domain.push($(this).val());
    });
    temp += '&domain=' + domain.join(',');

    var topic = new Array();
    $("[name='topic']:checked").each(function(){
        topic.push($(this).val());
    });
    temp += '&topic_string=' + topic.join(',');
    
    var tag_type = $('[name="tag_type"]').val();
    if (tag_type != ''){
        temp += '&tag=' + tag_type;
        var tag_value = $('[name="tag_name"]').val();
        temp += ':' + tag_value;
    }

    return temp;
}
function base_call_ajax_request(url, callback){
    $.ajax({
        url:url,
        type:"get",
        dataType: "json",
        async: false,
        success: callback
    })
}
function draw_value_option(data){
    //console.log(data);
    if (data == 'no attribute'){
        data = [];
    }
    $('[name=tag_name]').empty();
    var html = '';
    for (var i=0;i<data.length;i++){
        html += '<option value="' + data[i] + '">' + data[i] + '</option>';
    }
    $('[name=tag_name]').html(html);
}

function getAttributeName(){
    var attribute_name_url = '/tag/show_attribute_name/';
    base_call_ajax_request(attribute_name_url, draw_name_option);
    function draw_name_option(data){
        // console.log(data);
        $('[name=tag_type]').empty();
        var html = '';
        html += '<option value="" checked>不限</option>';
        for (var i=0;i<data.length;i++){
            html += '<option value="' + data[i] + '">' + data[i] + '</option>';
        }
        $('[name=tag_type]').html(html);
        /*
        var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
        attribute_value_url += data[0];
        base_call_ajax_request(attribute_value_url, draw_value_option);
        */
        $('[name=tag_type]').change(function(){
            if ($(this).val() == ''){
                $('[name=tag_name]').empty();
            }
            else{
                var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
                attribute_value_url += $(this).val();
                base_call_ajax_request(attribute_value_url, draw_value_option);
            }
        });
    }
}
$('[data-toggle="city-picker"]').citypicker({
    placeholder: '请选择省/市',
    level: 'city',
});
$('.city-picker-span').css('height','42px');
$('.city-picker-dropdown').css('left','932px');
$('.city-picker-dropdown').css('top','618px');
getAttributeName();
bindAdvanced();

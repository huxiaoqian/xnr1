getAttributeName();
attr_bind_click();

function getAttributeName(){
    var attribute_name_url = '/tag/show_attribute_name/';
    $.ajax({
        type:'GET',
        url: attribute_name_url,
        contentType:"application/json",
        dataType: "json",
        success: draw_name_option
    });
    function draw_name_option(data){
        // console.log(data);
        $('[name=tag_type]').empty();
        var html = '';
        html += '<option value="" checked>不限</option>';
        for (var i=0;i<data.length;i++){
            html += '<option value="' + data[i] + '">' + data[i] + '</option>';
        }
        $('[name=tag_type]').html(html);
        $('[name=tag_type]').change(function(){
            if ($(this).val() == ''){
                $('[name=tag_name]').empty();
            }
            else{
                var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
                attribute_value_url += $(this).val();
                $.ajax({
                    type:'GET',
                    url: attribute_value_url,
                    contentType:"application/json",
                    dataType: "json",
                    success: draw_value_option
                });
            }
        });
    }
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
function attr_bind_click(){
    $('#attribute_pattern #show_advanced').click(function(){
        if($('#attribute_pattern #advanced_condition').is(':hidden')){
            $(this).html('收起');
            $('#attribute_pattern #advanced_condition').css('display', 'block');
        }
        else{
            $(this).html('高级');
            $('#attribute_pattern #advanced_condition').css('display', 'none');
        }
    });
    $('#attribute_pattern #num-range').change(function(){
        var num = $('#attribute_pattern #num-range').val();
        $('#attribute_pattern #show_num').empty();
        $('#attribute_pattern #show_num').append(num);    
    });
}
function attribute_pattern_check(){             // check validation 
  //group_information check starts  
  var group_name = $('#first_name').val();
  var remark = $('#first_remarks').val();
  var num_range_count = $('#attribute_pattern #num-range').val();
  var influ_from_num = parseFloat($('#attribute_pattern #influ_from').val());
  var influ_to_num =parseFloat($('#attribute_pattern #influ_to').val());
  var impor_from_num = parseFloat($('#attribute_pattern #impor_from').val());
  var impor_to_num = parseFloat($('#attribute_pattern #impor_to').val());
  if (influ_from_num > influ_to_num){
    alert('影响力左侧输入值应小于右侧，请重新输入！')
    return false;
  }
  if (impor_from_num > impor_to_num){
    alert('重要度输入栏左侧输入值应小于右侧，请重新输入！')
    return false;
  }
  if(influ_from_num > 100 || influ_to_num > 100){
    alert('影响力输入值应在0到100之间，请重新输入！');
    return false;
  }
  if(impor_from_num>100 || impor_to_num>100){
    alert('重要度输入值应在0到100之间，请重新输入！');
    return false;
  }
  if(num_range_count ==0 ){
    alert('扩展规则中人数不能为0，请重新输入！');
    return false;
  }
  if (group_name.length == 0){
      alert('群体名称不能为空，请重新输入！');
      return false;
  }

  var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
  if (!group_name.match(reg)){
    alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
    return false;
  }
  if ((remark.length > 0) && (!remark.match(reg))){
    alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
    return false;
  }
  //other form check starts multi/single
  return true;

}


	function submit_attribute(){
    var flag = attribute_pattern_check();
    if(flag){
      var url_attribute = '/detect/attribute_pattern/?';
      var domain = new Array(); 
      var topic_string = new Array();
      var basic_url = '';
      var tag_string = new Array();
      var url_all = new Array();
      $('#attribute_pattern #basic .form-control').each(function(){
        var id = $(this).attr("id");
        var content = $(this).val();
        if(content != ''){
          basic_url = id +'='+ content;
          url_all.push(basic_url);
        }
      });
      
      $('#attribute_pattern #domain .inline-checkbox').each(function(){
        if($(this).is(':checked')){
          domain.push($(this).next().text());
        }
      });
      var domain_url = '';
      if(domain.length != 0 ){
        domain_url += 'domain=' + domain.join(',');
        url_all.push(domain_url);
      }
      
      var topic_url = '';
      $('#attribute_pattern #topic_string .inline-checkbox').each(function(){
        if($(this).is(':checked')){
          topic_string.push($(this).next().text());
        }
      });
      if(topic_string.length != 0){
        topic_url += 'topic_string=' + topic_string.join(',');
        url_all.push(topic_url);
      }  

      var tag_url = '';
      if ($('[name="tag_type"]').val() != ''){
          tag_url += 'tag_string=' + $('[name="tag_type"]').val() + '-' + $('[name="tag_name"]').val();
          url_all.push(tag_url);
      }
      
      var task_name_url = ''
      var task_name_id = 'task_name'
      var task_name_content = $('#first_name').val();
      if(task_name_content != ''){
        task_name_url =task_name_id +'='+ task_name_content;
        url_all.push(task_name_url);
      }

      var first_remarks_url = ''
      var first_remarks_id = 'state'
      var first_remarks_content = $('#first_remarks').val();
      if(first_remarks_content != ''){
        first_remarks_url = first_remarks_id +'='+ first_remarks_content;
        url_all.push(first_remarks_url);
      }

      var num_range_url = '';
      var num_range_count = $('#attribute_pattern #num-range').val();
      num_range_url = 'count=' + num_range_count;
      url_all.push(num_range_url);

      var influ_from_url ='';
      var influ_from_val = $('#attribute_pattern #influ_from').val();
      influ_from_url = 'influence_from=' + influ_from_val;
      url_all.push(influ_from_url);

      var influ_to_url ='';
      var influ_to_val = $('#attribute_pattern #influ_to').val();
      influ_to_url = 'influence_to=' + influ_to_val;
      url_all.push(influ_to_url);

      var important_from_url ='';
      var important_from_val = $('#attribute_pattern #impor_from').val();
      important_from_url = 'important_from=' + important_from_val;
      url_all.push(important_from_url);

      var important_to_url ='';
      var important_to_val = $('#attribute_pattern #impor_to').val();
      important_to_url = 'important_to=' + important_to_val;
      url_all.push(important_to_url);

      url_attribute += url_all.join('&') + '&submit_user=' + $('#useremail').text();
      console.log(url_attribute);

      $.ajax({
        type:'GET',
        url: url_attribute,
        contentType:"application/json",
        dataType: "json",
        success: attribute_callback
      });
      function attribute_callback(data){
        //console.log(data);
        seed_user_callback(data);
      }
      
    }	
}

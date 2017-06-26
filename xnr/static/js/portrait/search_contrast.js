function draw_search_results(data){
    //console.log(data);
    $('#search_result').empty();
    var user_url ;
    //console.log(user_url);
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th>';
    html += '<th>操作</th></tr></thead>';
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      item = replace_space(item);
      if (item[1] == '未知'){
          item[1] = item[0];
      } 
      for(var j=3;j<7;j++){
        if(item[j]!='未知')
          item[j] = item[j].toFixed(2);
      }
      user_url = '/index/personal/?uid=' + item[0];
      html += '<tr id=' + item[0] +'>';
      html += '<td class="center" name="uids"><a href='+ user_url+ '  target="_blank">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] +'</td>';
      html += '<td class="center">'+ item[2] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[3] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[4] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] +'</td>';
      html += '<td class="center" style="width:100px;">'+ item[6] +'</td>';
      html += '<td class="center" style="text-align:center;width:60px;"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item[0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#search_result').append(html);
    post_draw();
    $('.datatable').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "aaSorting":[[5, 'desc']],
        //"aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "每页&nbsp; _MENU_ 条"
        }
    });
}
var choose_contrast_uid = new Array();
function post_draw(){
    $('#contrast_block').css('display', 'block');
    $('input[name="search_result_option"]').change(function(){
        var uid = $(this).val();
        if ($(this).is(':checked')){
            var html = '';
	    html += '<span class="mouse" id=' + uid + ' style="margin-left:10px">'+ uid + '</span>';
            $('#contrast_chosen').append(html);
            if (choose_contrast_uid.length > 2){
                alert('选择对比的人数不能超过3人！');
                choose_contrast_uid.push(uid);
            }
            else{
                choose_contrast_uid.push(uid);
            }
        }
        else{
            for(var i = 0;i < choose_contrast_uid.length;i++){
                if (choose_contrast_uid[i] == uid){
                    choose_contrast_uid.splice(i,1);
                    break;
                }
            }
            $('#' + uid).remove();
        }
    });
    $('#commit_contrast').css('display', 'block');
    $('#commit_contrast').click(function(){
        if (choose_contrast_uid.length < 2){
          alert("请选择至少2个用户!");
        }
        else if (choose_contrast_uid.length > 3){
          alert("选择对比的人数不能超过3人!");
        }
        else{
            window.open('/index/contrast/?uid_list=' + choose_contrast_uid.join(','));
        }
    });
}

function create_user(){
	var data = [['arr11','vfkgvskjdhgkjvfkdj'],['arr12','vfkgvskjdhgkjvfkdj'],['arr13','vfkgvskjdhgkjvfkdj'],['arr14','vfkgvskjdhgkjvfkdj'],
			['arr15','vfkgvskjdhgkjvfkdj'],['arr16','vfkgvskjdhgkjvfkdj'],['arr17','vfkgvskjdhgkjvfkdj'],['arr18','vfkgvskjdhgkjvfkdj']]

	var email = $('#create_name').val();
	var password = $('#create_pw').val();
	var active = $('#create_user input[name="user_active"]:checked').val();
	var confirmed_at = $('#create_user #user_update').val();
	var role = [];
	$('#create_user input[name="choose_role"]:checked').each(function(){
		role.push($(this).val());
	})
        if(email==''){
                alert('用户名不能为空！')
                return false;
        }
        if(password == ''){
                alert('请输入密码！');
                return false;
        }
	var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
    	if (!email.match(reg)){
        	alert('用户名只能包含英文、汉字、数字和下划线,请重新输入!');
        	return false;
    	}
	if(role.length == 0){
		alert('请选择权限！')
                return false;
	}else{
		var html = '';
		html += '?email='+email + '&password=' + password + '&active=' + active + '&confirmed_at='+ confirmed_at + '&role' + role.join(',');
		console.log(html);
	}

	alert('修改成功！');
	
	$('#create_name').attr('value','');
	$('#create_pw').attr('value', '');
	$('#create_user #user_update').attr('value', '');
	$('#create_user input[name="user_active"]').attr('checked',false);
	$('#create_user input[name="choose_role"]').attr('checked',false);
	//draw_user_table(data);

}


function draw_role_table(data){
	$('#role_list').empty();
	var html = '';
	html += '<table id="role_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;">';
	html += '<thead><th style="text-align:center;">序号</th>';
	html += '<th style="text-align:center;">权限</th>';
	html += '<th style="text-align:center;">描述</th>';
	html += '<th style="text-align:center;">编辑</th></thead>';
	for(var i=0;i<data.length;i++){
		html += '<tr>';
		html += '<td style="text-align:center;">'+(i+1)+'</td>';
		html += '<td style="text-align:center;">'+data[i][0]+'</td>';
		html += '<td style="text-align:center;">'+data[i][1]+'</td>';
		html += '<td style="text-align:center;">';
		html += '<span class="edit_modal" style="cursor:pointer;" type="button" data-toggle="modal" data-target="#role_edit"><u>编辑</u></span>';
		html += '</td>';
		html += '</tr>';
	}
	html += '</table>';
	$('#role_list').append(html);
}

function draw_user_table(data){
	$('#user_list_table').empty();
	var html = '';
	html += '<table id="role_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;">';
	html += '<thead><th style="text-align:center;">序号</th>';
	html += '<th style="text-align:center;">用户名</th>';
	html += '<th style="text-align:center;">密码</th>';
	html += '<th style="text-align:center;">是否活跃</th>';
	html += '<th style="text-align:center;">更新时间</th>';
	html += '<th style="text-align:center;">权限</th>';
	html += '<th style="text-align:center;">编辑</th></thead>';
	for(var i=0;i<data.length;i++){
		html += '<tr>';
		html += '<td style="text-align:center;">'+(i+1)+'</td>';
		html += '<td style="text-align:center;">'+data[i][0]+'</td>';
		html += '<td style="text-align:center;">'+data[i][0]+'</td>';
		html += '<td style="text-align:center;">'+data[i][0]+'</td>';
		html += '<td style="text-align:center;">'+data[i][0]+'</td>';
		html += '<td style="text-align:center;">'+data[i][0]+'</td>';
		html += '<td style="text-align:center;">';
		html += '<span class="user_edit_modal" style="cursor:pointer;" type="button" data-toggle="modal" data-target="#user_edit"><u>编辑</u></span>';
		html += '<span style="margin-left:10px;cursor:pointer;" class="delete_user"><u>删除</u></span>';
		html += '</td>';
		html += '</tr>';
	}
	html += '</table>';
	$('#user_list_table').append(html);
}

var data = [['arr1','vfkgvskjdhgkjvfkdj'],['attribute','vfkgvskjdhgkjvfkdj'],['arr3','vfkgvskjdhgkjvfkdj'],['arr4','vfkgvskjdhgkjvfkdj'],
			['arr5','vfkgvskjdhgkjvfkdj'],['arr6','vfkgvskjdhgkjvfkdj'],['arr7','vfkgvskjdhgkjvfkdj'],['arr8','vfkgvskjdhgkjvfkdj']]
draw_role_table(data);
draw_user_table(data);

$('.delete_user').click(function(e){
	var a = confirm('确定要删除吗？');
	if (a == true){
		var url = '/detect/delete_task/?';
		var temp = $(this).parent().prev().prev().prev().prev().prev().text();
		url = url + 'task_name=' + temp;
		console.log(url);
		//window.location.href = url;
		//Group_identify_task.call_sync_ajax_request(url,Group_identify_task.ajax_method,del);
	}
});	

$('.edit_modal').click(function(){
	var name = $(this).parent().prev().prev().text();
	var role_description = $(this).parent().prev().text();
	$('#role_name').empty();
	$('#role_name').append(name);
	$('#role_description').empty();
	$('#role_description').append(role_description);
})


$('.user_edit_modal').click(function(){
	//$('input[name="choose_role"]').attr('checked', false);
	var name = $(this).parent().prev().prev().prev().prev().prev().text();
	var password = $(this).parent().prev().prev().prev().prev().text();
	var user_active = $(this).parent().prev().prev().prev().text();
	var update_time = $(this).parent().prev().prev().text();
	var user_role_edit = $(this).parent().prev().text();
	$('#user_name').attr('value', name);
	$('#user_pw').attr('value', password);
	if(user_active == 'arr1'){
		$('#user_edit #active_yes').attr('checked','checked');
	}else{
		$('#user_edit #active_no').attr('checked','checked');
	}
	$('#user_edit #user_update').attr('value', update_time);
	var array_role = user_role_edit.split(',');
	console.log(array_role[0]);
	for(var i=0;i<array_role.length;i++){
		$('#user_edit'+' #'+array_role[i]).attr('checked','checked'); 
	}
})

$('#submit_role_edit').click(function(){
var data = [['arr11','vfkgvskjdhgkjvfkdj'],['arr12','vfkgvskjdhgkjvfkdj'],['arr13','vfkgvskjdhgkjvfkdj'],['arr14','vfkgvskjdhgkjvfkdj'],
			['arr15','vfkgvskjdhgkjvfkdj'],['arr16','vfkgvskjdhgkjvfkdj'],['arr17','vfkgvskjdhgkjvfkdj'],['arr18','vfkgvskjdhgkjvfkdj']]

	var name = $('#role_name').text();
	var role_description = $('#role_description').val();
	var html = '';
	html += '?name=' + name + '&description=' + role_description;
	console.log(html);
	alert('修改成功！');
	draw_role_table(data);
});

$('#submit_user_edit').click(function(){
var data = [['arr11','vfkgvskjdhgkjvfkdj'],['arr12','vfkgvskjdhgkjvfkdj'],['arr13','vfkgvskjdhgkjvfkdj'],['arr14','vfkgvskjdhgkjvfkdj'],
			['arr15','vfkgvskjdhgkjvfkdj'],['arr16','vfkgvskjdhgkjvfkdj'],['arr17','vfkgvskjdhgkjvfkdj'],['arr18','vfkgvskjdhgkjvfkdj']]

	var email = $('#user_name').val();
	var password = $('#user_pw').val();
	var active = $('#user_edit input[name="user_active"]:checked').val();
	var confirmed_at = $('#user_edit #user_update').val();
	var role = [];
	$('#user_edit input[name="choose_role"]:checked').each(function(){
		role.push($(this).val());
	})
	if(email==''){
		alert('用户名不能为空！')
		return false;
	}
	if(password == ''){
		alert('请输入密码！');
		return false;
	}
        var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
        if (!email.match(reg)){
                alert('用户名只能包含英文、数汉和下、数字和下划线,请重新输入!'); 
                return false;
        }
	if(role.length == 0){
		alert('请选择权限！')
		return false;
	}else{
		var html = '';
		html += '?email='+email + '&password=' + password + '&active=' + active + '&confirmed_at='+ confirmed_at + '&role=' + role.join(',');
		console.log(html);
	}
	alert('修改成功！');
	draw_user_table(data);
});

var date = new Date();
date = date.format('yyyy/MM/dd hh:mm:ss');
$('#create_user #user_update').datetimepicker({value:date,step:1});

var role_list = ['attribute', 'detect', 'influence_application', 'group', 'profile', 'social_sensing', 'recommentation', 'overview'];

var role_html = '';
for(var i=0;i<role_list.length;i++){
	role_html += '<input type="checkbox" name="choose_role" id="'+ role_list[i] +'"';
	role_html += 'value="'+ role_list[i] +'" class="role_option">' + role_list[i];
}
$('#add_role1').empty();
$('#add_role2').empty();
$('#add_role1').append(role_html);
$('#add_role2').append(role_html);


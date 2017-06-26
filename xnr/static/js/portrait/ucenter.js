Date.prototype.format = function(format){
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}

function call_sync_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: true,
      success:callback
    });
}

function modal_work(){
	$('#Worktable').empty();
	var date = new Date();
	var to_date = new Date();
	to_date.setTime(date.getTime() - 60*60*24*7*1000);
	console.log(to_date);
	var from_date = date.format('yyyy/MM/dd hh:mm');
	to_date = to_date.format('yyyy/MM/dd hh:mm');
	var html = '';
	html += ' <table class="table table-bordered table-striped table-condensed datatable" >';
	html += ' <thead><tr style="text-align:center;">';
	html += '<th>任务ID</th><th>任务内容</th><th>提交时间</th><th>处理状态</th>';
	html += '</tr></thead>';
	html += '<tbody>';
	html += '<tr>'
	html += ' <td>'+'09XPX78'+'</td>';
	html += ' <td>'+'入库推荐'+'</td>';
	//html += ' <td>'+'2016/03/14-2016/03/21'+'</td>';
	html += ' <td>'+from_date+'-'+to_date+'</td>';
	// if(data[i][1] == '提交入库'){
	html += '<td style="cursor:pointer;" id="detail_button" type="button" data-toggle="modal" data-target="#detail_in_portrait"><u>查看详情</u></td>';
	// }
	html += '</tr>';
	html += '</tbody></table>';
	$('#Worktable').append(html);
}

function Draw_modal(data){
	$('#show_user_detail').empty();
	var html = '';
	html += ' <table class="table table-bordered table-striped table-condensed datatable" >';
	html += ' <thead><tr style="text-align:center;">';
	html += '<th>日期</th><th>uid</th><th>昵称</th><th>地理位置</th><th>粉丝数</th><th>微博数</th><th>影响力</th><th>是否入库</th>';
	html += '</tr></thead>';
	html += '<tbody>';
	for(var i=0;i<data[0].length;i++){
		html += '<tr>';
		html += '<td style="text-align;">'+data[0][i][0]+'</td>'
		html += '<td style="text-align;">'+data[0][i][1]+'</td>'
		html += '<td style="text-align;">'+data[0][i][2]+'</td>'
		html += '<td style="text-align;">'+data[0][i][3]+'</td>'
		html += '<td style="text-align;">'+data[0][i][4]+'</td>'
		html += '<td style="text-align;">'+data[0][i][5]+'</td>'
		html += '<td style="text-align;">'+data[0][i][6].toFixed(2)+'</td>';
		if(data[0][i][7] == '1'){
			html += '<td style="text-align;">'+'是'+'</td>';
		}else{
			html += '<td style="text-align;">'+'否'+'</td>';
		}
		html += '</tr>'
	}
	html += '</tbody></table>';
	$('#show_user_detail').append(html);

}

modal_work();
var admin=$('#tag_user').text();
$('#detail_button').click(function(){
	var url = '/ucenter/user_operation/?submit_user='+ admin;
		call_sync_ajax_request(url, Draw_modal);

});



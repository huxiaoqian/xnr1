var purview_Url='/system_manage/show_authority_list/';
public_ajax.call_request('get',purview_Url,purview);
function purview(data) {
    console.log(data);
    $('#purviewlist').bootstrapTable('load', data);
    $('#purviewlist').bootstrapTable({
        data:data,
        search: true,//是否搜索
        pagination: true,//是否分页
        pageSize: 8,//单页记录数
        pageList: [15,20,25],//分页步进值
        sidePagination: "client",//服务端分页
        searchAlign: "left",
        searchOnEnterKey: false,//回车搜索
        showRefresh: false,//刷新按钮
        showColumns: false,//列选择按钮
        buttonsAlign: "right",//按钮对齐方式
        locale: "zh-CN",//中文支持
        detailView: false,
        showToggle:false,
        sortName:'bci',
        sortOrder:"desc",
        columns: [
            // {
            //     title: "编号",//标题
            //     field: "",//键名
            //     sortable: true,//是否可排序
            //     order: "desc",//默认排序方式
            //     align: "center",//水平
            //     valign: "middle",//垂直
            //     formatter: function (value, row, index) {
            //         return index+1;
            //     }
            // },
            {
                title: "角色",//标题
                field: "role_name",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.role_name==''||row.role_name=='null'||row.role_name=='unknown'){
                        return '未知';
                    }else {
                        return row.role_name;
                    };
                }
            },
            {
                title: "权限描述",//标题
                field: "description",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    if (row.description==''||row.description=='null'||row.description=='unknown'){
                        return '无任何描述';
                    }else {
                        return row.description;
                    };
                }
            },
            {
                title: "操作",//标题
                field: "",//键名
                sortable: true,//是否可排序
                order: "desc",//默认排序方式
                align: "center",//水平
                valign: "middle",//垂直
                formatter: function (value, row, index) {
                    return '<span style="cursor:pointer;color:white;" onclick="modifyPur(\''+row.role_name+'\',\''+row.description+'\')" title="编辑"><i class="icon icon-edit"></i></span>&nbsp;&nbsp;&nbsp;&nbsp;'+
                        '<span style="cursor:pointer;color:white;" onclick="deletePur(\''+row.role_name+'\')" title="删除"><i class="icon icon-trash"></i></span>';
                }
            },
        ],
    });
}
//修改权限
var m_name='';
function modifyPur(name,description) {
    m_name=name;
    $('#editPur .character').val(name);
    $('#editPur .newDES').val(description);
    $('#editPur').modal('show');
}
function modifySure() {
    var newDes=$('#editPur .newDES').val();
    if (newDes){
        var modify_url='/system_manage/change_authority_list/?role_name='+m_name+'&description='+newDes;
        public_ajax.call_request('get',modify_url,successFail);
    }else {
        $('#pormpt p').text('请检查权限更改的内容，不能为空。');
        $('#pormpt').modal('show');
    }
}
//添加权限管理
function addPurSure() {
    var name=$('#addPurviewModal .purCC .purNAME').val();
    var description=$('#addPurviewModal .purCC .purDES').val();
    if (name||description){
        var addPur_url='/system_manage/create_role_authority/?role_name='+name+'&description='+description;
        public_ajax.call_request('get',addPur_url,successFail);
    }else {
        $('#pormpt p').text('请检查权限更改的内容，不能为空。');
        $('#pormpt').modal('show');
    }
}

//删除
var role_name='';
function deletePur(name) {
    $('#delAgain').modal('show');
    role_name=name;
}
function sureDelPur() {
    var delPur_Url='/system_manage/delete_authority_list/?role_name='+role_name;
    public_ajax.call_request('get',delPur_Url,successFail);
}
//=====
function successFail(data) {
    console.log(data)
    var f='';
    if (data[0]||data||data[0][0]){f='操作成功'}else {f='操作失败'}
    $('#pormpt p').text(f);
    $('#pormpt').modal('show');
}
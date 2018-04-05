
//添加项目组管理
$('#add_group').click(function(){
    var group = {};
    group['group'] = $("#group_name").val();
    group['passward'] = $("#group_passwd").val();
    group['authority'] = 0;
    group['action'] = "add_group";
    $.ajax({
        url : '/members_manage',
        data : group,
        type : 'POST',
        dataType : 'json',
        async: true,
        success : function(data) {
            alert(data.result);
            $('.modal').modal('hide')
            location.reload();
        }
     });
});

//删除项目组管理
$('#del_group').click(function(){
    var group = {};
    group['group'] = $("#del_group_name option:selected").val();
    group['authority'] = 0;
    group['action'] = "del_group";
    $.ajax({
        url : '/members_manage',
        data : group,
        type : 'POST',
        dataType : 'json',
        async: true,
        success : function(data) {
            alert(data.result);
            $('.modal').modal('hide')
            location.reload();
        }
     });
});

//添加项目组成员
$('#add_user').click(function(){
    var user = {};
    user['username'] = $("#user_name").val();
    user['passward'] = $("#user_passwd").val();
    user['authority'] = $("#user_authority option:selected").val();
    user['action'] = "add_user";
    user['group'] = "";
    $.ajax({
        url : '/members_manage',
        data : user,
        type : 'POST',
        dataType : 'json',
        async:true,
        success : function(data) {
            alert(data.result);
            $('.modal').modal('hide')
            location.reload();
        }
     });
});

//删除项目组成员
$('#del_user').click(function(){
    var user = {};
    user['username'] = $("#user_name").val();
    user['passward'] = $("#user_passwd").val();
    user['authority'] = $("#user_authority option:selected").val();
    user['action'] = "del_user";
    if(user['username'] && user['passward']){
        $.ajax({
            url : '/members_manage',
            data : user,
            type : 'POST',
            dataType : 'json',
            async:true,
            success : function(data) {
                alert(data.result);
                $('.modal').modal('hide')
                location.reload();
            }
         });
      }else{
        alert("删除失败");
      }
});




//$("#button").click(function(){
//    var newUrl = '/news/';    //设置新提交地址
//    $("#myform").attr('action',newUrl);    //通过jquery为action属性赋值
//    $("#myform").submit();    //提交ID为myform的表单
//   });
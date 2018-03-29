
//添加项目组管理
$('#add_group').click(function(){
    var group = {};
    group['group'] = $("#group_name").val();
    group['passward'] = $("#group_passwd").val();
    group['authority'] = 0;
    group['action'] = "add_group";
    console.log(group)
    $.ajax({
        url : '/members_manage',
        data : group,
        type : 'POST',
        dataType : 'json',
        async: false,
        success : function(data) {
            alert(data.result);
            $('.modal').modal('hide')
            location.reload();
        }
     });
});

//添加项目组成员
$('#add_user').click(function(){
    $.ajax({
        url : '${pageContext.request.contextPath}/stu/stu_upstudent.action',
        data : $("#addUserForm"),
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


//$("#button").click(function(){
//    var newUrl = '/news/';    //设置新提交地址
//    $("#myform").attr('action',newUrl);    //通过jquery为action属性赋值
//    $("#myform").submit();    //提交ID为myform的表单
//   });
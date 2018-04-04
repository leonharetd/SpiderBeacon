function get_deploy_progress(){
    $.ajax({
        url:"",

    })
}

//获取project_info的值
function get_ProInfo_value(){
    var projectValue = $('#projectValue option:selected').val();
    var spiderValue = $('#spiderValue option:selected').val();
    var datavalue = [];
    datavalue['project'] = projectValue;
    datavalue['spider'] = spiderValue;
    if(projectValue && spiderValue){
            $.ajax({
                url: "",
                data: datavalue,
                type: 'POST',
                dataType: 'json',
                async: true,
                success: function(data){
                    if(data.status == 'ok'){
                        $("#pro_info").val(data.message);
                    }
                }
            });
    }
}

$(".pro_select").change(function(){
    get_ProInfo_value();
})

$(".spider_select").change(function(){
    get_ProInfo_value();
})

$("#label1").click(function(){
    if ($(this).find("input").is(":checked")) {
        $("#dingshi").show();
    } else {
        $("#dingshi").hide();
    }
});

$("#label2").click(function(){
     $("#dingshi").hide();
})

$(".btn-info").click(function(){
    var projectValue = $('#projectValue option:selected').val();
    var spiderValue = $('#spiderValue option:selected').val();
    var dingValue = null;

    if(!projectValue){
//        form_error();
//        select1_error();
        alert("项目名不可以为空");
    }

    if(!spiderValue){
//        form_error();
//        select2_error();
        alert("爬虫项目名不可以为空");
    }

    if ($('#optionsRadios1').is(':checked')) {
        dingValue = $("#dingValue").val();
        if(!dingValue){
//            form_error();
            alert("定时任务不可以为空。");
        }
    }
    var server_value = [];
//    var options=$("#serversValue option:selected");
//    alert(options.text());
    $("#serversValue option:selected").each(function(){
        server_value.push($(this).text());
    });
    if(!Array.isArray(server_value) || server_value.length == 0){
//        form_error();
        alert("请选择要部署的服务器");
    }

    var datas = [];
    datas['project'] = projectValue;
    datas['spider'] = spiderValue;
    datas['dingValue'] = dingValue;
    datas['servers'] = server_value;

    $(".deploy_progress").show();

    $.ajax({
        url : '',
        data : datas,
        type : 'POST',
        dataType : 'json',
        async: true,
        success : function(data) {
            if(data.status == 'ok'){

            }

        }
    });
})


//function select1_error(){
//    $("#projectValue").css("border:1px solid #ff0000;");
//}
//function select1_success(){
//    $("#projectValue").css("border:1px solid #aaa;");
//}
//
//function select2_error(){
//    $("#spiderValue").css("border:1px solid #ff0000;");
//}
//function select2_success(){
//    $("#spiderValue").css("border:1px solid #aaa;");
//}
//
//function form_error(){
//    $('.form-group').addClass("has-error");
//}
//
//function form_success(){
//    $('.form-group').removeClass("has-error");
//}
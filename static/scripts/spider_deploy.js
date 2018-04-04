
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
        alert("项目名不可以为空");
    }

    if(!spiderValue){
        alert("爬虫项目名不可以为空");
    }

    if ($('#optionsRadios1').is(':checked')) {
        dingValue = $("#dingValue").val();
        if(!dingValue){
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
//        $('.form-group').addClass("has-error");
//        $('.help-block').show();
        alert("请选择要部署的服务器");
    }

    var datas = [];
    datas['project'] = projectValue;
    datas['spider'] = spiderValue;
    datas['dingValue'] = dingValue;
    datas['servers'] = server_value;
    $.ajax({
        url : '',
        data : datas,
        type : 'POST',
        dataType : 'json',
        async: true,
        success : function(data) {
            alert(data.result);
            $('.modal').modal('hide')
            location.reload();
        }
    });
})
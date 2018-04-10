//根据project，获取spider内容
function get_Spider_By_Pro(){
    var project_id = $('#projectValue option:selected').attr("project_id");
    if(project_id){
        $.ajax({
            url: "/spider_deploy",
            data: {"action": "get_spiders", "project_id": project_id},
            type: 'POST',
            dataType: 'json',
            async: true,
            success: function(data){
                if(data.status == 'ok'){
                    var html = '';
                    var spiList = data.message;

                    if (spiList.length > 0){
                        for (var i = 0; i < spiList.length; i++) {
                            html += '<option value="' + spiList[i] + '">' + spiList[i] + '</option>';
                        }
                    }
                    $('#spiderValue').html(html);
                }
            }
        });
    }
}

//获取project_info的值
function get_ProInfo_value(){
    var project_id = $('#projectValue option:selected').attr("project_id");
    if(projectValue && spiderValue){
            $.ajax({
                url: "/spider_deploy",
                data: {"action": "get_project_info", "project_id": project_id},
                type: 'POST',
                dataType: 'json',
                async: true,
                success: function(data){

                    if(data.status == 'ok'){
                        var html = '';
//                        alert(data.message);
                        var msgList = data.message;
//                        alert(msgList.username);
                        html += '<label>Project Info</label><div class="box-body"><table id="example1" class="table table-bordered table-striped">'+
                                 '<thead><tr><th>project</th><th>group</th><th>username</th><th>creator</th><th>version</th>'+
                                 '<th>create_time</th></tr></thead>'+
                                 '<tbody><tr>'+
                                 '<td>'+ msgList.project +'</td>'+
                                 '<td>'+ msgList.group +'</td>'+
                                 '<td>'+ msgList.username +'</td>'+
                                 '<td>'+ msgList.creator +'</td>'+
                                 '<td>'+ msgList.version +'</td>'+
                                 '<td>'+ msgList.create_time +'</td>'+
                                 '</tr></tbody></table></div>';
                        $("#project_Info").html(html);
                    }
                }
            });
    }
}

$(".pro_select").change(function(){
    get_Spider_By_Pro();
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


$("#label3").click(function(){
     $("#dingshi").hide();
})

//点击部署按钮
$(".btn-info").click(function(){
    var projectValue = $('#projectValue option:selected').val();
    var spiderValue = $('#spiderValue option:selected').val();
    var dingValue = "";

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

    dingValue = $('input:radio:checked').val();
    alert(dingValue);
    if(!dingValue){
//            form_error();
        alert("定时任务不可以为空。");
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

    var datas = {};
    datas['project'] = projectValue;
    datas['spider'] = spiderValue;
    datas['period'] = dingValue;
    datas['periodText'] = dingValue;
    datas['servers'] = server_value;
    datas['action'] = "deploy"
    $(".deploy_progress").show();
    var serverLength = server_value.length; //服务器数量

    var ws = new WebSocket("ws://localhost:8000/spider_flush");
    ws.onopen = function() {
        ws.send(JSON.stringify(datas));
    };
    ws.binaryType = "arraybuffer";
    var i = 1;
    var j = 1; //失败的次数
    var html = '';
    ws.onmessage = function(e) {
        //progress-bar
        $("#servers_progress").width(i/serverLength*100+'%');
        $("#p_progress").text(i+'/'+serverLength);
        $("#servers_progress").attr('aria-valuenow',i);
        $("#servers_progress").attr('aria-valuemax',serverLength);

        console.log(e.data);
        var datas = JSON.parse(e.data);

        if(datas.status == false){
            $("#error_table").show();
//            alert(html);

            html += '<tr><td>'+j+'</td><td>'+datas.ip +'</td><td><span class="label label-danger">False</span></td></tr>';
            $("#servers_false").html(html);
            j++;
        }
        i++;
    };
});


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
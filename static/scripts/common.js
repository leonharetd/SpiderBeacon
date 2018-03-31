
function reset( ) {
value = 0
  $("#prog").removeClass("progress-bar-success").css("width","0%").text("等待启动");
  //setTimeout(increment,5000);
}

(function () {

    //百分数增加，0-25时为蓝色，25-50为绿色，50-75为黄色，75-100为红色
//    function increment() {
//        var links = document.getElementsByClassName("progress-forcun");
//        for (var i = 0; i < links.length; i++) {
//            var value = links[i].getAttribute('aria-valuenow');
//            alert(value);
//            var time = 50;
//              $(".progress-bar").css("width",value + "%").text(value + "%");
//              if (value>=0 && value<=25) {
//                  $(".progress-bar").addClass("progress-bar-info");
//                  return;
//              }
//              else if (value>=25 && value <=50) {
//                  $(".progress-bar").removeClass("progress-bar-info").addClass("progress-bar-success");
//                  return;
//              }
//              else if (value>=50 && value <=75) {
//                  $(".progress-forcun").removeClass("progress-bar-success").addClass("progress-bar-warning");
//                   return;
//              }
//              else if(value >= 75 && value<100) {
//                  $(".progress-forcun").removeClass("progress-bar-warning").addClass("progress-bar-danger");
//                   return;
//              }
//              else{
//                  setTimeout(reset,3000);
//                  return;
//              }
//             st = setTimeout(increment,time);
//        }
//    };



    function increment() {
            var links = document.getElementsByClassName("progress-forcun");
            for (var i = 0; i < links.length; i++) {

                var value = links[i].getAttribute('aria-valuenow');
//                alert(value);
                var valuetext = "";
                if (value>=0 && value<=25) {
                  valuetext = "progress-bar-info";
                }
                else if (value>=25 && value <=50) {
                  valuetext = "progress-bar-success";
                }
                else if (value>=50 && value <=75) {
                   valuetext = "progress-bar-warning";
                }
                else if(value >= 75 && value<100) {
                   valuetext = "progress-bar-danger";
                }
                alert(valuetext);
//                (function () {
                $(".progress-bar").addClass(function() {
                    return valuetext;
                });

//                $(".progress-bar").css(("width",value + "%").text(value + "%"),function() {
//                    return value;
//                });

//             })();
             }
        }


    increment();


})();

//进度条停止与重新开始
$("#stop").click(function () {
  if ("stop" == $("#stop").val()) {
      //$("#prog").stop();
      clearTimeout(st);
      $("#prog").css("width","0%").text("等待启动");
      $("#stop").val("start").text("重新开始");
  } else if ("start" == $("#stop").val()) {
      increment();
      $("#stop").val("stop").text("停止");
  }
});

//进度条暂停与继续
$("#pause").click(function() {
  if ("pause" == $("#pause").val()) {
      //$("#prog").stop();
      clearTimeout(st);
      $("#pause").val("goon").text("继续");
  } else if ("goon" == $("#pause").val()) {
      increment();
      $("#pause").val("stop").text("暂停");
  }
});

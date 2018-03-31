
function reset( ) {
value = 0
  $("#prog").removeClass("progress-bar-success").css("width","0%").text("等待启动");
  //setTimeout(increment,5000);
}

(function () {
//    onload();

     function onload () {
        var links = document.getElementsByTagName("aria-valuenow");
        for (var i = 0; i < links.length; i++) {
            (function () {
                var res = i;
                var value = document.getElementById('prog').getAttribute('aria-valuenow');
                //因为闭包内要使用i，所以外层i还依旧存在内存中
                return function () {
                    alert(links[res].innerHTML);
                    alert(typeof this);
                    alert(value);
                }
            })();
        }
     };

//    increment();

    //百分数增加，0-25时为蓝色，25-50为绿色，50-75为黄色，75-100为红色
//    function increment() {
//        var links = document.getElementsByTagName("td")length;
        var links = $("td div div");
        alert(links);
        for (var i = 0; i < links.length; i++) {
            var value = links[i].getAttribute('aria-valuenow');
            alert(value);
            var time = 50;
            //  value += 1;
              $("#prog").css("width",value + "%").text(value + "%");
              if (value>=0 && value<=25) {
                  $("#prog").addClass("progress-bar-info");
              }
              else if (value>=25 && value <=50) {
                  $("#prog").removeClass("progress-bar-info");
                  $("#prog").addClass("progress-bar-success");
              }
              else if (value>=50 && value <=75) {
                  $("#prog").removeClass("progress-bar-success");
                  $("#prog").addClass("progress-bar-warning");
              }
              else if(value >= 75 && value<100) {
                  $("#prog").removeClass("progress-bar-warning");
                  $("#prog").addClass("progress-bar-danger");
              }
    //          else{
    //              setTimeout(reset,3000);
    //              return;
    //          }
    //          st = setTimeout(increment,time);
//        }
    }


//        var value = document.getElementById('prog').getAttribute('aria-valuenow');
//        alert(value);
//        var time = 50;
//        //  value += 1;
//          $("#prog").css("width",value + "%").text(value + "%");
//          if (value>=0 && value<=25) {
//              $("#prog").addClass("progress-bar-info");
//          }
//          else if (value>=25 && value <=50) {
//              $("#prog").removeClass("progress-bar-info");
//              $("#prog").addClass("progress-bar-success");
//          }
//          else if (value>=50 && value <=75) {
//              $("#prog").removeClass("progress-bar-success");
//              $("#prog").addClass("progress-bar-warning");
//          }
//          else if(value >= 75 && value<100) {
//              $("#prog").removeClass("progress-bar-warning");
//              $("#prog").addClass("progress-bar-danger");
//          }
//          else{
//              setTimeout(reset,3000);
//              return;
//          }
//          st = setTimeout(increment,time);

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

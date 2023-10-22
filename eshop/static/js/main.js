
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function checkMelliCode(input) {
    if (!/^\d{10}$/.test(input)) return false;
    const check = +input[9];
    const sum = input.split('').slice(0, 9).reduce((acc, x, i) => acc + +x * (10 - i), 0) % 11;
    return sum < 2 ? check === sum : check + sum === 11;
}

function ajax_call(url, data, success_function, success_function_args, typ="Post", data_type="json"){
    $.ajax({
        url: url,
        dataType: data_type,
        type: typ,
        async: true,
        headers: {'X-CSRFToken': csrftoken},
        data: data,
        success: function (data) {
            if (data["error"]){
                $.confirm({
                    type : 'red',
                    rtl: true,
                    theme : "modern",
                    title : "خطا",
                    content : data["error"],
                    animation : "scale",
                    closeAnimation : "scale",
                    buttons: {
                        ok :{
                            btnClass: 'btn-red',
                            action : function(){}
                        }
                    }
                    });
            }
            else if (data["success"]){
                eval(success_function).apply(this, success_function_args);
            }
        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status === 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status === 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }
            console.log(msg);

        }
    });
}

$(document).ready(function (){
    $("#login_mobile").keydown(function(event){
      if(event.keyCode === 13){
          $("#modal_login_submit").click();
      }
    });

    $("#login_confirm_code_4").keyup(function(event){
          // TODO send check code
        if($(this).val() !== ""){
            var code = $("#login_confirm_code_1").val() + $("#login_confirm_code_2").val() + $("#login_confirm_code_3").val() + $("#login_confirm_code_4").val();
            var username = $("#login_mobile").val();
            check_code("/check_code/", username, code);
        }
    });

    $(".code-input").keyup(function (event){
        $(this).next().focus();
    })
});
var csrftoken = getCookie('csrftoken');
function ajax_login(url, username){
    $.ajax({
        url: url,
        dataType: "json",
        type: "Post",
        async: true,
        headers: {'X-CSRFToken': csrftoken},
        data: {"username": username},
        success: function (data) {
            if (data["error"]){
                jconfirm({
                    type : 'red',
                    rtl: true,
                    theme : "modern",
                    title : "خطا",
                    content : data["error"],
                    animation : "scale",
                    closeAnimation : "scale",
                    buttons: {
                        ok :{
                            btnClass: 'btn-red',
                            action : function(){}
                        }
                    }
                    });
            }
            else if (data["success"]){
                $("#modal_login_step1").hide();
                $("#modal_login_step2").show("slow");
                setTimeout(function (){
                  $('#login_confirm_code_1').focus();
              }, 700);
            }
        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status === 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status === 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }
            console.log(msg);

        }
    });
}

function check_code(url, username, code){
    $.ajax({
        url: url,
        dataType: "json",
        type: "Post",
        async: true,
        headers: {'X-CSRFToken': csrftoken},
        data: {"username": username, "code": code},
        success: function (data) {
            if (data["error"]){
                jconfirm({
                    type : 'red',
                    rtl: true,
                    theme : "modern",
                    title : "خطا",
                    content : data["error"],
                    animation : "scale",
                    closeAnimation : "scale",
                    buttons: {
                        ok :{
                            btnClass: 'btn-red',
                            action : function(){
                                location.reload();
                            }
                        }
                    }
                    });
            }
            else if (data["success"]){
                $("#loginModal").modal("hide");
                callback();
            }
        },
        error: function (xhr, exception) {
            var msg = "";
            if (xhr.status === 0) {
                msg = "Not connect.\n Verify Network." + xhr.responseText;
            } else if (xhr.status === 404) {
                msg = "Requested page not found. [404]" + xhr.responseText;
            } else if (xhr.status === 500) {
                msg = "Internal Server Error [500]." +  xhr.responseText;
            } else if (exception === "parsererror") {
                msg = "Requested JSON parse failed.";
            } else if (exception === "timeout") {
                msg = "Time out error." + xhr.responseText;
            } else if (exception === "abort") {
                msg = "Ajax request aborted.";
            } else {
                msg = "Error:" + xhr.status + " " + xhr.responseText;
            }
            console.log(msg);
        }
    });
}
$(window).load(function () {
    var type = $('#type').attr("class");
    console.log(type);
    $("#get_token").click(function(){//发送邮箱地址 请求token
                var email = $('input[name="email"]').val();
                if (email.search("@nyu.edu") == -1){//输入的不是nyu邮箱
                    alert("请输入NYU邮箱")//弹窗报错
                } else {
                    $.ajax({
                        type:'post',
                        url:'/auth/token?'+type+'=1',
                        data:{"email":email},
                        success:function(data){
                            alert(data.message)//弹窗报错
                        }
                    })
                    //得到token
                }
    });


    $("#verify").click(function(){
            var input_token = $('input[name="token"]').val();
            console.log("here");
                $.ajax({
                type:'post',
                url:'/auth/email_verify?'+type+"=1",
                data:{"token":input_token},
                success:function(data){
                        if (data.status){
                            if (type == "registration"){
                                window.location.href="/auth/register";
                            }
                            else if (type == "exceeded_max_attempts"){
                                window.location.href="/auth/login";
                            }
                            else if (type == "reset_password"){
                                window.location.href="/auth/reset_password";
                            }
                        }
                        else{
                             alert(data.message);//弹窗报错
                        }
                    }
                })
             });



});

    $("#get_token").click(function(){//发送邮箱地址 请求token
            console.log("0");
			var email = $('input[name="email"]').val();
			console.log(email);
			if (email.search("@nyu.edu") == -1){//输入的不是nyu邮箱
			    alert("请输入NYU邮箱")//弹窗报错
			} else {
			    $.ajax({
			        type:'post',
			        url:'/auth/token',
			        data:{"email":email},
			        success:function(data){
			            alert(data.message)//弹窗报错
			        }
			    })
			    //得到token
			}
	  });

	$("#confirm").click(function(){
	    console.log("1");
	    var input_token = $('input[name="token"]').val();
        $.ajax({
		    type:'post',
		    url:'/auth/email_verify',
		    data:{"token":input_token},
	        success:function(data){
	            if (data.status){
	                window.location.href="/auth/register"
	                alert(data.message);//弹窗报错
	            }
	            else{
	                 alert(data.message);//弹窗报错
	            }

	        }
        })
	});

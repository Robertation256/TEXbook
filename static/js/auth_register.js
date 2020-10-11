

    $("#register").click(function(){
	    console.log("1");
	    var password = $('input[id="password"]').val();
	    var re_password = $('input[id="re_password"]').val();
	    if (password == re_password){
	        var username = $('input[name="username"]').val();
	        $.ajax({
		        type:'post',
		        url:'/auth/register',
		        data:{"username":username, "password":password}
            })
	    } else {
	        alert("请输入相同的密码");
	    }
	})


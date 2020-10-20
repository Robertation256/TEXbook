$(window).load(function () {

    $("#register").click(function(){
	    var password = $('input[id="password"]').val();
	    var re_password = $('input[id="re_password"]').val();
	    if (password == re_password){
	        $.ajax({
		        type:'post',
		        url:'/auth/register',
		        data:{"password":password},
		        success: function() {
		            window.location.href="/profile/profile"
		        }
            })
	    } else {
	        alert("请输入相同的密码");
	    }
	});

});


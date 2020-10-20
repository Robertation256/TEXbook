$(window).load(function () {

    $("#confirm").click(function(){
	    var password = $('input[id="password"]').val();
	    var re_password = $('input[id="re_password"]').val();
	    if (password == re_password){
	        $.ajax({
		        type:'post',
		        url:'/auth/reset_password',
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


$(window).load(function () {
    $("#login").click(function(){
	    var email = $('input[name="email"]').val();
		var password = $('input[name="password"]').val();
	    $.ajax({
		    type:'post',
		    url:'/auth/login',
		    data:{"email":email, "password":password},
	        success:function(data){
	            if (data.status) {
	                window.location.href="/home";
				}
				else if (data.chances_left == 0){
					window.location.href="/auth/email_verify?exceeded_max_attempts=1";
				}
	            else {
	                alert(data.message+", "+data.chances_left+" chances left");//弹窗报错
	            }
	        }
        })
	});
});


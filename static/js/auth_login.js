$(window).load(function () {
    $("#login").click(function(){
	    console.log("1");
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
	            else {
	                alert(data.message);//弹窗报错
	            }
	        }
        })
	});
});


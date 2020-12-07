$(window).load(function () {
    var avatar_selected = $("#avatar");
    $(".trigger_popup_fricc").click(function(){
       $('.hover_bkgr_fricc').show();
    });
//    $('.hover_bkgr_fricc').click(function(){
//        $('.hover_bkgr_fricc').hide();
//    });

    $(".avatar_option").click(function(){
        avatar_selected = $(this);
        $(".avatar_option_selected").removeClass("avatar_option_selected");
        $(this).addClass("avatar_option_selected");
    });

    $("#avatar_select").click(function(){
        $("#avatar").prop("src", avatar_selected.attr("src"));
        $("#avatar_id").val(avatar_selected.attr("value"));
        $('.hover_bkgr_fricc').hide();
    });

    $("#avatar_select_cancel").click(function(){
        $('.hover_bkgr_fricc').hide();
	});

    $("#update_profile").click(function(){
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var major = $("#major").val();
        var class_year = $("#class").val();
        var contact_information = $("#contact_information").val();
        var avatar_id = avatar_selected.attr("value");
        var data = {
			            "first_name":first_name,
			            "last_name": last_name,
			            "major": major,
			            "class": class_year,
			            "contact_information": contact_information,
			            "avatar_id": avatar_id
			        };
	    console.log(data);
        $.ajax({
			        type:'post',
			        url:'/profile/profile',
			        data:{
			            "first_name":first_name,
			            "last_name": last_name,
			            "major": major,
			            "class_year": class_year,
			            "contact_information": contact_information,
			            "avatar_id": avatar_id
			        },
			        success:function(data){
			            if (data.status){
			                alert("Update succeeded");
			                window.location.href="/profile/profile";
			            }
			            else{
			                alert("Update failed");
			            }
			        }
		})
	})

    $("#update_password").click(function(){
	    var password = $('input[id="password"]').val();
	    var re_password = $('input[id="re_password"]').val();
	    if (password == re_password){
	        $.ajax({
		        type:'post',
		        url:'/profile/profile_account',
		        data:{"password":password},
		        success: function() {
					alert("Password Sucessfully Update")
		        }
            })
	    } else {
			alert("Please enter matching passwords");
		}
		$("#settings")[0].reset();
    });
    
    $("#delete").on("click", function(){
		console.log('may work?')
        var confirmed = window.confirm("Are you sure you want to DELETE your account?");
        if (confirmed){ 
			$.ajax({
				type: "post",
				url: "/profile/delete_account"
			  }).done(function( o ) {
				alert("You have deleted your account")
				window.location.replace="\\"
			  });
        }
	});
	
    $("#update_notifications").click(function(){
		var email_notification = $('input[name="email_notification"]').val(); 
		var email_notification_freq = $("#frequency").val();
		var notificationA = $("#user_unlock").is(":checked");
		var notificationB = $("#book_listed").is(":checked");
        var data = {
			            "email_notification": email_notification,
			            "email_notification_freq": email_notification_freq,
			            "notificationA": notificationA,
			            "notificationB": notificationB,
					};
		$.ajax({
					type: 'post',
					url: '/profile/profile_notifications',
					data: {
			            "email_notification": email_notification,
			            "email_notification_freq": email_notification_freq,
			            "notificationA": notificationA,
			            "notificationB": notificationB,
					},
					success:function(data){
			            if (data.status){
			                alert("Update succeeded");
			            }
					}
		});
	});	
});


$(window).load(function() {
    $(".operation-icons").hide();
    $("body").on("mouseenter",".table_row", function(e) {
        var target = $(e.target);
        if (target.attr("class") == "table_row") {
            target.css("background-color","#F8F8F8");
            target.children(".operation-icons").show();
        }
        else if (target.attr("class") == "operation-icons"){
            var parent = $(target.closest(".table_row"));
            parent.css("background-color","#F8F8F8");
            target.show();
        }
        else {
            var parent = $(target.closest(".table_row"));
            parent.css("background-color","#F8F8F8");
            target.siblings(".operation-icons").show();
        }
    });

    $("body").on("mouseleave",".table_row", function(e) {
        var target = $(e.target);
        if (target.attr("class") == "table_row") {
            target.css("background-color","white")
            target.children(".operation-icons").hide();
        }
        else if (target.attr("class") == "operation-icons"){
            var parent = $(target.closest(".table_row"));
            parent.css("background-color","white");
            target.hide();
            }
        else {
            var parent = $(target.closest(".table_row"));
            parent.css("background-color","white");
            target.siblings(".operation-icons").hide()
        }
    });

    $(".off_shelf_btn").click(function(){
        var bool = confirm("Do you wish to put this listing off shelf?");
        if (bool){
            var parent = $(this).parent(".operation-icons");
            var listing_id = parent.siblings(".listing_id").text();
            $.ajax({
                url:"/listing/set?id="+listing_id+"&on_shelf=0",
                success: function(data){
                    if (data.status){
                        window.location.reload();
                    }
                    else{
                        alert(data.msg);
                    }
                }
            });
         }
     });


    $(".on_shelf_btn").click(function(){
        var bool = confirm("Do you wish to put this listing on shelf?");
        if (bool){
            var parent = $(this).parent(".operation-icons");
            var listing_id = parent.siblings(".listing_id").text();
            $.ajax({
                url:"/listing/set?id="+listing_id+"&on_shelf=1",
                success: function(data){
                    if (data.status){
                        window.location.reload();
                    }
                    else{
                        alert(data.msg);
                    }
                }
            });
        }
    });

    $(".delete_btn").click(function(){
        var bool = confirm("This listing or request will be permanently deleted. Do you wish to proceed?");
        if (bool){
            var parent = $(this).parent(".operation-icons");
            var listing_id = parent.siblings(".listing_id").text();
            $.ajax({
                url:"/listing/delete?id="+listing_id,
                success: function(data){
                    if (data.status){
                        window.location.reload();
                    }
                    else{
                        alert(data.msg);
                    }
                }
            });
        }
    });



    $(".lock_btn").click(function(){
        var bool = confirm("Do you wish to remove this listing from unlocked items?");
        if (bool){
            var parent = $(this).parent(".operation-icons");
            var listing_id = parent.siblings(".listing_id").text();
            $.ajax({
                url:"/listing/lock?id="+listing_id,
                success: function(data){
                    if (data.status){
                        window.location.reload();
                    }
                    else{
                        alert(data.msg);
                    }
                }
            });
        }
    });


});
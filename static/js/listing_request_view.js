$(window).load(function() {
    $(".hover_bkgr_fricc").hide();
    $(".seller-info").hide();
    var listing_id = -1;


    $(".listing-wrapper").click(function (e) {
        listing_id = $(this).attr("id");
        $(".carousel-inner").empty();
        $(".carousel-indicators").empty();
        $(".hidden_info").attr("id","closed");
        var option = $(this).find("#option-content").text();
        if (option == "Buy") {
            $(".pop_up_purchase_option").text("Demand to Purchase at");
        }
        else if (option == "Rent"){
            $(".pop_up_purchase_option").text("Demand to Rent at");
        }
        $(".pop_up_offered_price").text("￥"+$(this).find("#offered-price-content").text());
        $("#pop-up-condition").text($(this).find("#condition-content").text());
        $("#pop-up-defect").text($(this).find("#defect-content").text());
        $(".pop_up_checked_user").text($(this).find("#checked-user-num-content").text()+" user(s) have checked on seller contact information");
        $.ajax({
            url:"/listing/image_ids?id="+listing_id,
            type:"GET",
            success: function(data) {
                if (data.status) {
                    var image_ids = data.book_image_ids;
                    console.log(image_ids);
                    for (var i = 0; i < image_ids.length; i++){
                        if (i == 0){
                            var _ = $('<div class="carousel-item active"><img class="d-block w-100" src="/image/upload?id='+image_ids[i]+'" alt="First slide"></div>');
                            $(".carousel-inner").append(_);
                            var _ = $('<li data-target="#carousel-example-1z" class="active" data-slide-to="'+i+'"></li>');
                            $(".carousel-indicators").append(_);
                        }
                        else {
                            var _ = $('<div class="carousel-item"><img class="d-block w-100" src="/image/upload?id='+image_ids[i]+'" alt="First slide"></div>');
                            $(".carousel-inner").append(_);
                            var _ = $('<li data-target="#carousel-example-1z" data-slide-to="'+i+'"></li>');
                            $(".carousel-indicators").append(_);
                        }
                    }
                    $(".hover_bkgr_fricc").show();
                }
                else{
                    alert("Bad request for image_ids");
                }
            }
        });
    });

    $('.hover_bkgr_fricc').click(function(e){
        if ($(e.target).attr("class") == "hover_bkgr_fricc"){
            $('.hover_bkgr_fricc').hide();
        }
    });

    $("body").on("mouseenter",".listing-wrapper", function(e) {
        var target = $(e.target);
        if (target.attr("class") == "listing-wrapper") {
            target.css("background-color","#F8F8F8")
        }
        else {
            var parent = $(target.closest(".listing-wrapper"));
            parent.css("background-color","#F8F8F8");
        }
    });
    $("body").on("mouseleave",".listing-wrapper", function(e) {
        var target = $(e.target);
        if (target.attr("class") == "listing-wrapper") {
            target.css("background-color","white")
        }
        else {
            var parent = $(target.closest(".listing-wrapper"));
            parent.css("background-color","white");
        }
    });

    $(".hidden_info").click(function() {
        if ($(".hidden_info").attr("id") == "open"){
            $(".hidden_info").attr("id","closed");
            $(".seller-info").toggle("slide");
        }
        else{
            $.ajax({
                url:"/listing/unlock_contact_info?id="+listing_id,
                type:"GET",
                success:function(data){
                    console.log(data);
                    if (data.chance_left == 0){
                        alert("You have 0 unlock chance left for today. Get membership for unlimited access.");
                    }
                    else{
                        $(".name").text(data.contact_info.last_name + "," + data.contact_info.first_name);
                        $(".contact-info").text(data.contact_info.contact_info);
                        $(".hidden_info").attr("id","open");
                        $(".seller-info").toggle("slide");
                    }
                }
            });

        }



    });




});
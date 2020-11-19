$(window).load(function() {
    $(".hover_bkgr_fricc").hide();
    $(".listing-wrapper").click(function () {
        var listing_id = $(this).attr("value");
        $(".hover_bkgr_fricc").show();
        $.ajax({
            url:"/listing/get_image_ids",
            type:"GET",
            success: function(data) {
                if (data.status) {

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


});
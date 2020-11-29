$(window).load(function() {
    var form_data = new FormData();
    var reader = new FileReader();
    var img_num = 0;
    var img_id = 0;
    var previous_load = "";
    $("#book_info").hide();

    $("body").on("change","#textbook_select", function() {
        var current_val = $("#textbook_select option:selected").val();
        $.ajax({
            url:"/textbook/search?id="+current_val,
            type:"GET",
            success: function(data) {
                $("#title").text("Title:  "+data.title);
                $("#author").text("Author:  "+data.author);
                $("#publisher").text("Publisher:  "+data.publisher);
                $("#edition").text("Edition:  "+data.edition);
                $(".book_cover").attr("src","/image/bookcover?id="+data.cover_image_id);
                $("#book_info").show();
            }

        });
    });

    $("body").on("click","#publish", function() {
        form_data.append("textbook_id",$("#textbook_select").val());
        form_data.append("purchase_option",$("#purchase_option").val());
        form_data.append("offered_price",$("#offered_price").val());
        $.ajax({
            url:"/listing/request_publish",
            processData: false,
            contentType: false,
            type:"POST",
            data:form_data,
            success: function() {
                alert("Publish succeeds");
            }
        });
    });



})
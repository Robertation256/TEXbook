$(window).load(function() {
    var form_data = new FormData();
    var reader = new FileReader();
    var img_num = 0;
    var img_id = 0;
    var previous_load = "";
    $("#book_info").hide();

    reader.onloadend = function(e) {
        if (img_num < 4) {
            var preview_container = $('<div class="image_preview_container"></div>');
            var trash_image = $('<svg width="200px" display="none"; height="200px" viewBox="0 0 16 16" class="bi bi-trash" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>');
            var image_tag = $('<img class="preview_image">')
            preview_container.append(image_tag);
            preview_container.append(trash_image);
            preview_container.attr("img_id",img_id)
            $("#image_upload_container").prepend(preview_container);
            image_tag.attr("src",e.target.result);
            trash_image.hide();
            img_num += 1;
            img_id += 1;
        }
    };

    function readURL(input,image_tag) {
        if (input.files && input.files[0]) {
            reader.readAsDataURL(input.files[0]);
        }
    };

    $("body").on("mouseenter",".image_preview_container", function(event) {
        var current_node = $(event.target);
        current_node.hide();
        current_node.siblings("svg").show();
    });

    $("body").on("mouseleave",".bi", function(event){
        var current_node = $(event.target);
        current_node.hide();
        current_node.siblings(".preview_image").show();
    });

    $("#file-input").change(function() {
        form_data.append(img_id,this.files[0]);
        readURL(this);
        $('input[type="file"]').val(null);

    });

    $("body").on("click",".bi", function() {
        target_element = $(this).parent(".image_preview_container");
        var target_id = target_element.attr("img_id");
        target_element.remove();
        form_data.delete(target_id);
        img_num -= 1;
    });

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
        form_data.append("condition",$("#book_condition").val());
        form_data.append("defect",$("#defects").val());

        $.ajax({
            url:"/listing/publish",
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
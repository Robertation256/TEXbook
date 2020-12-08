$(window).load(function() {
    var display_mode = "display_unread_msg";
    var unread_notification_count = 0;

    $('.notification-dropdown-menu').on('click', function (event) {
        event.stopPropagation();
    });

    function make_notification_node(notification){
        if (notification.type == "listing_publish_event"){
            var msg = "Your requested textbook: \""+notification.book_title+"\" is now available";
        }
        else if (notification.type == "listing_unlock_event"){
            if (notification.listing_type == "seller_post"){
                var msg = "A user has checked your offer on \""+notification.book_title+"\"";
            }
            else{
                var msg = "A user has checked your request on \""+notification.book_title+"\"";
            }
        }
        var msg_node = $('<p style="font-size:15px;"></p>');
        msg_node.text(msg);

        var posted_date_node = $('<p class="text-warning" style="font-size:15px;"></p>');
        posted_date_node.text(notification.date_added);

        var notification_text_node = $('<div class="notification-text"></div>');
        notification_text_node.append(msg_node);
        notification_text_node.append(posted_date_node);

        if (notification.is_read == "false"){
            var notification_wrapper = $('<div class="notification-wrapper"><div class="notification-operation"><svg width="28px" height="28px" viewBox="0 0 16 16" class="bi bi-envelope-open mark-as-read" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8.47 1.318a1 1 0 0 0-.94 0l-6 3.2A1 1 0 0 0 1 5.4v.818l5.724 3.465L8 8.917l1.276.766L15 6.218V5.4a1 1 0 0 0-.53-.882l-6-3.2zM15 7.388l-4.754 2.877L15 13.117v-5.73zm-.035 6.874L8 10.083l-6.965 4.18A1 1 0 0 0 2 15h12a1 1 0 0 0 .965-.738zM1 13.117l4.754-2.852L1 7.387v5.73zM7.059.435a2 2 0 0 1 1.882 0l6 3.2A2 2 0 0 1 16 5.4V14a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V5.4a2 2 0 0 1 1.059-1.765l6-3.2z"/></svg><svg width="30px" height="30px" viewBox="0 0 16 16" class="bi bi-trash delete" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg></div>');
        }
        else{
            var notification_wrapper = $('<div class="notification-wrapper"><div class="notification-operation"><svg width="30px" height="30px" viewBox="0 0 16 16" class="bi bi-envelope mark-as-unread" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2zm13 2.383l-4.758 2.855L15 11.114v-5.73zm-.034 6.878L9.271 8.82 8 9.583 6.728 8.82l-5.694 3.44A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.739zM1 11.114l4.758-2.876L1 5.383v5.73z"/></svg><svg width="30px" height="30px" viewBox="0 0 16 16" class="bi bi-trash delete" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg></div>');
        }
        notification_wrapper.prepend(notification_text_node);
        notification_wrapper.attr("id",notification.id);

        if (notification.is_read == "true"){
            var status = "read";
        }
        else {
            var status = "unread";
        }
        notification_wrapper.addClass(status);

        return notification_wrapper
    }

    function refresh_all () {
        /*remove old notifications first*/
        unread_notification_count = 0;

        var old_notifications = $(".notification-wrapper");
        old_notifications.remove();

        /*request for notification data*/
        $.ajax({
            url:"/notification/get",
            type:"GET",
            success: function(data){
                var container = $(".notification-container");
                for (i=0; i < data.length; i++){
                    var node = make_notification_node(data[i]);
                    container.append(node);
                    if (node.hasClass("unread")){
                        unread_notification_count +=1;
                    }
                    if (display_mode=="display_unread_msg" & node.hasClass("read")){
                        node.hide();
                    }
                }
                if (unread_notification_count == 0){
                    $(".notification-count").hide();
                }
                else{
                    $(".notification-count").text(unread_notification_count);
                    $(".notification-count").show();
                }

                $(".notification-operation").hide();

                $(".mark-as-read").click(function() {
                    var notification_id = $(this).closest(".notification-wrapper").attr("id");
                    console.log(notification_id);
                    $.ajax({
                        url: "/notification/is_read?id="+notification_id+"&status=read",
                        type:"GET",
                        success: function(){
                            refresh_all();
                        }
                    });
                });

                $(".delete").click(function() {
                    var notification_id = $(this).closest(".notification-wrapper").attr("id");
                    console.log(notification_id);
                    $.ajax({
                        url: "/notification/notification_delete?id="+notification_id,
                        type:"GET",
                        success: function(){
                            refresh_all();
                        }
                 });
    });

                $(".mark-as-unread").click(function() {
                    var notification_id = $(this).closest(".notification-wrapper").attr("id");
                    console.log(notification_id);
                    $.ajax({
                        url: "/notification/is_read?id="+notification_id+"&status=unread",
                        type:"GET",
                        success: function(){
                            refresh_all();
                        }
                    });
                });


            }

        });

    }

    $("body").on("mouseenter",".notification-wrapper", function(e) {
        var target = $(e.target);
        if (target.attr("class") == "notification-wrapper") {
            target.css("background-color","#F8F8F8");
            target.find(".notification-operation").show();
        }
        else {
            var parent = $(target.closest(".notification-wrapper"));
            parent.css("background-color","#F8F8F8");
            parent.find(".notification-operation").show();
        }
    });


    $("body").on("mouseleave",".notification-wrapper", function(e) {
        var target = $(e.target);
        if (target.attr("class") == "notification-wrapper") {
            target.css("background-color","white")
            target.find(".notification-operation").hide();
        }
        else {
            var parent = $(target.closest(".notification-wrapper"));
            parent.css("background-color","white");
            parent.find(".notification-operation").hide()
        }
    });

    $("#bell").click(function(){
        refresh_all();
    })

    $(".delete").click(function() {
        var notification_id = $(this).closest(".notification-wrapper").attr("id");
        console.log(notification_id);
        $.ajax({
            url: "/notification/notification_delete?id="+notification_id,
            type:"GET",
            success: function(){
                refresh_all();
            }
        });
    });

    $(".display-mode-btn").click(function() {
        $(".notification-dropdown-menu").show();
        if (display_mode == "display_unread_msg"){
            display_mode = "display_all_msg";
            $(this).text("Show unread notifications");
            refresh_all();
        }
        else{
            display_mode = "display_unread_msg";
            $(this).text("Show all notifications");
            refresh_all();
        }

    })




    /*avatar dropdown control*/
    $(".avatar-dropdown").click(function(){
        $.ajax({
            url:"/profile/unlock_chances",
            type:"GET",
            success: function(unlock_chances){
                $("#unlock-chance").text(unlock_chances);
            }
        });

    })



});


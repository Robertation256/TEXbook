$(window).load(function() {
    $(".textbook_wrapper").click(function(e){
        var textbook_id = $(this).attr("id");
        console.log(textbook_id);
        window.location.href = "/listing/view_listing?id="+textbook_id
    });

});
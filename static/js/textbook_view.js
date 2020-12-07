$(window).load(function() {
    $(".textbook_wrapper").click(function(e){
        var textbook_id = $(this).attr("id");
        console.log(textbook_id);
        window.location.href = "/listing/view_listing?id="+textbook_id
    });

});
$(document).on('click','.switch',function(){
    $(this).toggleClass('switch-on');
    console.log('You just pushed me!')
    $(this).toggleClass('switch-off');
  });
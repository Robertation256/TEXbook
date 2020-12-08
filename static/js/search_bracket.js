$(window).load(function () {
    console.log("Here");
    var search_data = {};
    var field = $("#search_field option:selected").val();
    $.ajax({
        url:"/home/home_resource",
        type: "GET",
        success: function (res) {
            $.extend(search_data,res);
            if (field == "1" || field == undefined) {
            $("#search_input").typeahead({source: search_data.title});
            }
            else if (field == "2") {
                $("#search_input").typeahead("destroy");
                $("#search_input").typeahead({source: search_data.course_name});
            }
            else if (field == "3") {
                $("#search_input").typeahead("destroy");
                $("#search_input").typeahead({source: search_data.subject});
            }
            }
    });
    $("#search_field").on("change",function() {

        field = $("#search_field option:selected").val();
        if (field == "1") {
            $("#search_input").typeahead("destroy");
            $("#search_input").typeahead({source: search_data.title});
        }
        else if (field == "2") {
            $("#search_input").typeahead("destroy");
            $("#search_input").typeahead({source: search_data.course_name});
        }
        else if (field == "3") {
            $("#search_input").typeahead("destroy");
            $("#search_input").typeahead({source: search_data.subject});
        }
    });

    $("#search_btn").click(function () {
        if (field == undefined) {
            field = "1";
        };
        var keyword = $("#search_input").val();

        if (field == "1") {
            window.location.href="/textbook/search?book_name="+keyword;
        }
        else if (field == "2") {
            window.location.href="/textbook/search?course_name="+keyword;
        }
        else if (field == "3") {
            window.location.href="/textbook/search?subject="+keyword;
        }

    });



})
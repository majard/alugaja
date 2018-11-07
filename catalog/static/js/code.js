$(document).ready(function(){
    $("#filter-button").click(function(){
        $(".filter").toggle();
    });

    $(".navbar-toggler-btn").click(function(){
        $(".navbar-nav.list").toggle();
    });

    $(window).on('resize', function() {
        if($(window).width() > 768) {
            $(".navbar-nav.list").show();
        }
    })
});
$(document).ready(function(){
    // Tabs and table handler
    $('.content:first').show();
    $('.tabs:first').addClass('active');
    $('.tabs').click(function(event){
        index = $(this).index();
        $('.tabs').removeClass('active');
        $(this).addClass('active');
        $('.content').hide()
        $('.content').eq(index).show()
    })

    var rotation = 0;
    jQuery.fn.rotate = function(degrees) {
        $(this).css({'transform' : 'rotate('+ degrees +'deg)'});
        return $(this);
    };
    
    $('.show-form').click(function() {
        rotation += 180;
        $('.form-panel').slideToggle();
        $('.chevron-down').rotate(rotation);
    });
})
$(document).ready(function(){
    // Tabs and table handler
    $('.content:first').show();
    $('.tabs:first').addClass('active');
    
    // Formats number to currency
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'IDR',
    });

    // Keeps track of the active table, appends posted stuff into the table.
    var activeTable = 0;

    $('.tabs').click(function(event){
        activeTable = $(this).index();

        $('.tabs').removeClass('active');
        $(this).addClass('active');
        $('.content').hide();
        $('.content').eq(activeTable).show();
    });

    $('form').on("submit",function(e){
        // Serializes form data into string
        var serializedForm = $(this).serialize();
        
        var serializedArray = $(this).serializeArray();

        var currentPath = window.location.pathname;
        $.ajax({
            type : "POST",
            url : currentPath + "add",
            data : serializedForm,
            success : function(){
                var row = '';
                for(x in serializedArray){
                    if(x == 2){
                        row += '<td class="border-2 h-10">' +  formatter.format(serializedArray[x]['value']) + '</td>';
                    } else{
                        row += '<td class="border-2 h-10">' +  (serializedArray[x]['value']) + '</td>';
                    }
                }
                console.log(row)
                $('.content tbody').eq(activeTable).append('<tr>' + row + '</tr>');
                alert("Succesfully added record");
            }
        });
        
        e.preventDefault();
    });
    

    var rotation = 0;
    jQuery.fn.rotate180 = function(degrees) {
        $(this).css({'transform' : 'rotate('+ degrees +'deg)'});
        return $(this);
    };
    
    $('.show-form').click(function() {
        rotation += 180;
        $('.form-panel').slideToggle();
        $('.chevron-down').rotate180(rotation);
    });
});
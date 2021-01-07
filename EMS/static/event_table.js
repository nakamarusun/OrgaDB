$(document).ready(function(){
    // Tabs and table handler
    $('.content:first').show();
    $('.tabs:first').addClass('active');
    $('.form-wrapper').hide();
    $('.form-wrapper:first').show();
    // Formats number to currency
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'IDR',
    });

    // Keeps track of the active table, appends posted stuff into the table.
    activeTable = 0;
    $('.tabs').click(function(event){
        activeTable = $(this).index();

        $('.tabs').removeClass('active');
        $(this).addClass('active');
        $('.content').hide();
        $('.form-wrapper').hide();
        $('.content').eq(activeTable).show();
        $('.form-wrapper').eq(activeTable).show();
    });

    $('.form-panel').on("submit",function(e){
        // Serializes form data into string
        var serializedForm = $(this).serialize() + "&ActiveTable=" + activeTable;
        
        // Used to add a record on the front end
        var serializedArray = $(this).serializeArray();
        var currentPath = window.location.pathname;
        console.log(serializedArray)
        $.ajax({
            type : "POST",
            url : currentPath + "add",
            data : serializedForm,
            success : function(){
                $('.empty-message').hide()
                location.reload();
            }
        });
        
        // Prevents regular submit action on submit click
        e.preventDefault();
    });

    var rotation = 0;
    jQuery.fn.rotate180 = function(degrees) {
        $(this).css({'transform' : 'rotate('+ degrees +'deg)'});
        return $(this);
    };
    
    $('.show-form').click(function() {
        rotation += 180;
        $('.form-panel').eq(activeTable).slideToggle();
        console.log($('.chevron-down').eq(activeTable).cssText)
        $('.chevron-down').eq(activeTable).rotate180(rotation);
    }); 


    $(document).on('click','.edit', function(){
        $(this).parent().find('.delete').addClass('editing');
    })
    $(document).on('click','.edit-sponsor', function(){
        $(this).parent().find('.delete').addClass('editing');
    })
    $(document).on('click','.edit-position', function(){
        $(this).parent().find('.delete').addClass('editing');
    })
    $(document).on('click','.submit', function(){
        $(this).parent().find('.delete').removeClass('editing');
    })
    $(document).on('click','.submit-sponsor', function(){
        $(this).parent().find('.delete').removeClass('editing');
    })
    $(document).on('click','.submit-position', function(){
        $(this).parent().find('.delete').removeClass('editing');
    })

    $(document).on('click','.delete', function(){
        editRow = $(this).parent().parent();
        console.log(editRow)
        var columns = []
        tableColumns = $(this).parent().parent().parent().find('#table-header').children();
        for(i = 0;i < tableColumns.length; ++i){
            if(tableColumns[i].textContent !== 'Edit'){
                columns.push(tableColumns[i].textContent)
            }
        }
        console.log(columns)
        deletedData = "";
        if($(this).hasClass('editing')){
            for(i = 0; i < columns.length; ++i){
                if(i == 0){
                    deletedData += columns[i] + "=" + $(editRow).children('td').children().eq(i).text()
                } else{
                    deletedData += "&" + columns[i] + "=" + $(editRow).children('td').children().eq(i).text()
                }
            }
        } else{
            for(i = 0; i < columns.length; ++i){
                if(i == 0){
                    deletedData += columns[i] + "=" + $(editRow).children('td').eq(i).text()
                } else{
                    deletedData += "&" + columns[i] + "=" + $(editRow).children('td').eq(i).text()
                }
            }
        }
        deletedData += "&ActiveTable=" + activeTable
        console.log(deletedData)
        var currentPath = window.location.pathname;
        $.ajax({
            type : "POST",
            url : currentPath + "/delete",
            data : deletedData,
            success : function(){
                if(editRow.parent().children().length == 1){
                    editRow.parent().find('.empty-message').show()
                }
                
                alert("Succesfully deleted record");
            }
        });
        
        editRow.remove();
    });
});
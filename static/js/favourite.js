

// Load a login template if user is not signed in
const favouriteSymbol = function(button){

    symbol_id = $(button).attr('id');
    $.ajax({
        type:'POST',
        url: '/data/favourite/',
        data: {
        'symbol_id': symbol_id,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },

        success: function (response) {
            if(response.favourite){
                $(button).html('Remove');
                current_favourites = parseInt($('#' + symbol_id).html()) ;
                $('#' + symbol_id).html(current_favourites + 1);

            }
            else{
                $(button).html('Add');
                current_favourites = parseInt($('#' + symbol_id).html()) ;
                $('#' + symbol_id).html(current_favourites - 1);
            };
        },

        error: () =>{
            console.log("sorry something went wrong"); // Use alert or notify user
        }
    })
};
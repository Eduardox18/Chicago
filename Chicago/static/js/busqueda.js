$(function() {
    $("#buscar").submit(function( event ) {
        if($("#busqueda").val().trim()=== "") {
            event.preventDefault()
            $("#busqueda").addClass('is-invalid');
            $("#button-buscar").css('background-color','red');
      }   
      });
});




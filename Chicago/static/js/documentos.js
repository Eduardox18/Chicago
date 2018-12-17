$(document).ready(function() {
    $('#usuarios').multiselect();

    $('#btnCompartir').click(function (e) { 
        e.preventDefault(); 

        var lista_usuarios = $('#usuarios').val();
        var id_documento = $('#usuarios').attr("name");

        values = {
            "lista_usuarios": lista_usuarios,
            "id_documento": id_documento
        }
        $.ajax({
            type: "post",
            url: "/compartirDocumento/",
            data: {"values": JSON.stringify(values)},
            success: function (response) {
         
            }
        });
    });

    $('.clase-documento').click(function (e) {
        var button = $(this);
        $('#usuarios').attr("name", button.attr("name"));

        usuarios()
    });
});
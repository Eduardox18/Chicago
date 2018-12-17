$(document).ready(function() {
    $('#usuarios').multiselect();

    $('#btnCompartir').click(function (e) { 
        e.preventDefault(); 

        var lista_usuarios = $('#usuarios').val()
        var id_documento = $('#usuarios').attr("name")

        $.ajax({
            type: "post",
            url: "/compartirDocumento/",
            traditional: true,
            data: {
                "lista_usuarios": lista_usuarios,
                "id_documento": id_documento,
            },
            dataType: "json",
            success: function (response) {
                
            }
        });
    });

    $('.clase-documento').click(function (e) {
        var button = $(this);
        $('#usuarios').attr("name", button.attr("name"));
    });
});
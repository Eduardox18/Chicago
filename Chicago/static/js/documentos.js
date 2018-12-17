$(document).ready(function() {
    $('#usuarios').multiselect();

    $('#btnCompartir').click(function (e) { 
        e.preventDefault(); 

        var lista_usuarios = $('#usuarios').val()
        var id_documento = $('#usuarios').attr("name")

        var memes = {}
        memes["lista_usuarios"] = lista_usuarios
        memes["id_documento"] = id_documento

        $.post("/compartirDocumento/", {"lista": memes}, function(response){
            alert(response);
        });
    });

    $('.clase-documento').click(function (e) {
        var button = $(this);
        $('#usuarios').attr("name", button.attr("name"));

        usuarios()
    });
});

function usuarios() {
    $.ajax({
        type: "post",
        url: "/usuarios/",
        dataType: "json",
        success: function (response) {
            lista = JSON.parse(response.lista);
            $("#drop-usuarios").empty();
            lista.forEach(function (usuario) {
                nombre = usuario.fields.first_name + " " + usuario.fields.last_name.charAt(0) + ".";
                $("#drop-usuarios").append('<a class="dropdown-item" href="/chat/' + usuario.fields.username + '">' + nombre + '</a>');
            });
        }
    });
}
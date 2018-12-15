$(document).ready(function () {
    $("#enviarMensaje").click(function (e) { 
        e.preventDefault()
        if ($("#espacioMensaje").val() != "") {
            $.ajax({
                type: "post",
                url: "/enviarMensaje/",
                data: {
                    "destinatario": $("#titulo-pag").text().replace(/\s/g, ''),
                    "mensaje": $("#espacioMensaje").val(),
                    "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val(),
                },
                dataType: "json",
                success: function (response) {
                    $("#espacioMensaje").val("");
                    mensajes()
                }
            });
        }
    });
    mensajes();
    setInterval(mensajes, 3000);
    $.ajax({
        type: "post",
        url: "/usuarios/",
        dataType: "json",
        success: function (response) {
            lista = JSON.parse(response.lista);
            lista.forEach(function (usuario) {
                $("#drop-usuarios").append('<a class="dropdown-item" href="/chat/' + usuario.fields.username + '">' + usuario.fields.username + '</a>');
            });
        }
    });
    
    
});

function mensajes(){
    $.ajax({
        type: "post",
        url: "/recuperarMesajes/",
        data: {
            'destinatario': $("#mensajes").attr('name')
        },
        dataType: "json",
        success: function (response) {
            lista_mensajes = JSON.parse(response.mensajes);
            $("#mensajes").empty();
            lista_mensajes.forEach(function (mensaje) {
                if (mensaje.fields.idUsuarioDestinatario == $("#mensajes").attr('name')) {
                    console.log(mensaje)
                    $("#mensajes").append('<div class="container mensaje der"><p>' + mensaje.fields.mensaje + '</p></div >');
                } else {
                    $("#mensajes").append('<div class="container mensaje izq"><p>' + mensaje.fields.mensaje + '</p></div >');
                }
            })
            $('#mensajes').scrollTop($('#mensajes')[0].scrollHeight);

        }
    });
}
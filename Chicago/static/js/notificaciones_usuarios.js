$(document).ready(function () {
    usuarios();
    notificaciones();
    setInterval(usuarios, 3000);
    setInterval(notificaciones, 3000)
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

function notificaciones() {
    $.ajax({
        type: "post",
        url: "/notificaciones/",
        success: function (response) {
            var notificaciones = response.notificaciones;
            $("#notificaciones").empty();
            notificaciones.forEach(function(notificacion){
                if (notificacion.idDocumento == ""){
                    $("#notificaciones").append('<a class="dropdown-item notificacion" href="/verNotificacion/' + notificacion.id + '/mensaje/' + notificacion.userRemitente + '">');
                    $(".notificacion:last").append('<strong>Nuevo mensaje de ' + notificacion.remitente + ':</strong>');
                    if(notificacion.mensaje.length > 20){
                        $(".notificacion:last").append('<p>' + notificacion.mensaje.substring(0, 20) + '...</p>');
                    } else {
                        $(".notificacion:last").append('<p>' + notificacion.mensaje + '</p>');
                    }
                } else{
                    $("#notificaciones").append('<a class="dropdown-item notificacion" href="/verNotificacion/' + notificacion.id + '/doc/' + notificacion.idDocumento + '">');
                    $(".notificacion:last").append('<strong>' + notificacion.remitente + ' te ha invitado a un documeto:</strong>');
                    if (notificacion.nombreDoc.length > 20) {
                        $(".notificacion:last").append('<p>' + notificacion.nombreDoc.substring(0, 20) + '...</p>');
                    } else {
                        $(".notificacion:last").append('<p>' + notificacion.nombreDoc + '</p>');
                    }
                }
            });
            $("#numero_notificaciones").text(notificaciones.length);
        }
    });
}
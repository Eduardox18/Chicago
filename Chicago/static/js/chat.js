$(document).ready(function () {
    $("#enviarMensaje").click(function (e) { 
        $.ajax({
            type: "post",
            url: "url",
            data: "data",
            dataType: "json",
            success: function (response) {
                
            }
        });
    });
});

function recuperar_mensajes () {

}

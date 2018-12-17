$(document).ready(function () {
    $("#busqueda").on('input', function (e) {
        var busqueda = $("#busqueda").val().toLowerCase();
        if (busqueda != ""){
            $("#fila_docs").children().show();
            $("#fila_docs").children().each(function(){
                if (!this.innerText.replace(/\s/g, '').toLowerCase().startsWith(busqueda)){
                    if (this.id != "creador"){
                        $(this).hide();
                    }
                }
            })
        } else {
            $("#fila_docs").children().show();
        }
    });
});

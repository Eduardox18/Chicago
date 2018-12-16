$(document).ready(function () {
    $("#busqueda").on('input', function (e) {
        var prenda = $("#busqueda").val().toLowerCase();
        if (prenda != ""){
            $("#fila_docs").children().show();
            $("#fila_docs").children().each(function(){
                if (!this.innerText.replace(/\s/g, '').toLowerCase().includes(prenda)){
                    if (this.id != "creador"){
                        $(this).hide();
                    }
                }
            })
        }
    });
});

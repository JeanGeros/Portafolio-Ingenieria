function ValidacionNombreUsuario(e){
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key)
    teclas = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz1234567890-_";
    especiales = "8-37-39-46";

    tecla_especial = false
    for(var i in especiales){
        if(key == especiales[i]){
            tecla_especial = true;
            break;
        }
    }

    if(teclas.indexOf(tecla)==-1 && !tecla_especial){
        return false;
    }
}

function SinEspacios(e){
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key)
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúabcdefghijklmnñopqrstuvwxyz1234567890*-+{}[]!#$%&/()=¡<>,.@";
    especiales = "8-37-39-46";

    tecla_especial = false
    for(var i in especiales){
        if(key == especiales[i]){
            tecla_especial = true;
            break;
        }
    }

    if(letras.indexOf(tecla)==-1 && !tecla_especial){
        return false;
    }
}
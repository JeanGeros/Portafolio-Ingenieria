
let button = document.getElementById('boton_aceptar')
button.disabled = true

let contraseña = document.getElementsByName('password');
let conf_contraseña = document.getElementsByName('confirme_contraseña');

if (contraseña == conf_contraseña || contraseña != "" || conf_contraseña != ""){
    button.disabled = false
}

function ConfirmarBaja(){

    Swal.fire({
        icon: 'info',
        title: 'Estas seguro de querer dar de baja tu cuenta?',
        showCancelButton: true,
        confirmButtonText: '<form action="" method="post">{% csrf_token %}<button type="submit" name="BajarPerfil" value="{{request.user}}" class="btn btn-secondary" style="background-color: #705FFB!important;border-color: #705FFB!important;">Si, estoy seguro</button></form>',
        cancelButtonText: 'Cancelar',
    })
}


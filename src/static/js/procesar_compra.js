const listaCompra = document.querySelector('#procesar-carrito tbody');

cargarEventos();

function cargarEventos(){

    document.addEventListener('DOMContentLoaded', obtenerProductosLocalStorage());
    document.addEventListener('DOMContentLoaded', leerLocalStorageCompra());
    calcularTotal();
    
}

function obtenerProductosLocalStorage(){
    let productosLS;
    if(localStorage.getItem('productos') === null){
        productosLS = [];
    }else{
        productosLS = JSON.parse(localStorage.getItem('productos'));
    }
    return productosLS;
}

function leerLocalStorageCompra(){
    let productosLS;

    productosLS = obtenerProductosLocalStorage();
    let cont = 0;
    productosLS.forEach(function(producto) {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>
            <img src="${producto.imagen}" width=100>
        </td>
        <input type="hidden" name="producto_id${cont}" value="${producto.id}">
        <td>
            ${producto.nombre}
        </td>
        <input type="hidden" name="producto_nombre${cont}" value="${producto.nombre}">
        <td>
            $${producto.precio}
        </td>
        <input type="hidden" name="producto_precio${cont}" value="${producto.precio}">
        <td name="producto_cantidad" value="${producto.cantidad}">
            ${producto.cantidad}
        </td>
        <input type="hidden" name="producto_cantidad${cont}" value="${producto.cantidad}">
        <td>
        </td>
        `;
        listaCompra.appendChild(row);
        cont = cont + 1;
    });
}

function calcularTotal(){
    let productoLS;
    let total = 0;
    let totalDolar = 0;
    productoLS = obtenerProductosLocalStorage();
    console.log(productoLS);
    for(let i = 0; i < productoLS.length; i++){
       
        let num1 = Number(productoLS[i].precio);
        let num2 = Number(productoLS[i].cantidad);
        console.log(num1)
        console.log(num2)
        let element = (num1 * num2);
        total = total + element;
        function roundTo(value, places){
            var power = Math.pow(10, places);
            return Math.round(value * power) / power;
        }
        totalDolar = roundTo(total / 941.8, 2);
    }

    
    const total_dolar = totalDolar.toLocaleString('en-US');
    const total_peso = total.toLocaleString();

    document.getElementById('dolar').innerHTML = total_dolar;
    document.getElementById('totalCLP').innerHTML = total_peso;

    valores = document.createElement('tr')
    valores.innerHTML = `
        <td>
            <input type="hidden" name="total_dolar" value="${total_dolar}">
        </td>
        <td>
            <input type="hidden" name="total_peso" value="${total_peso}">
        </td>
    `
    listaCompra.appendChild(valores)
}

function vaciarLocalStorage(){
    localStorage.clear();
}


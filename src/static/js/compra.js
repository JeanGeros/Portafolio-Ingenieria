const carrito = document.getElementById('carrito');
const productos = document.getElementById('lista-productos');
const listaProductos = document.querySelector('#lista-carrito tbody');
const vaciarCarritoBtn = document.getElementById('vaciar-carrito');
const procesarPedidoBtn = document.getElementById('procesar-pedido');
const listaCompra = document.querySelector('#procesar-carrito tbody');



cargarEventos();

function cargarEventos(){
    productos.addEventListener('click', comprarProducto);

    carrito.addEventListener('click', eliminarProducto);

    vaciarCarritoBtn.addEventListener('click', vaciarCarrito);

    document.addEventListener('DOMContentLoaded', leerLocalStorage);

    procesarPedidoBtn.addEventListener('click', procesarPedido);  

     
}


function comprarProducto(e){
    e.preventDefault();
    if(e.target.classList.contains('agregar-carrito')){
        const producto = e.target.parentElement.parentElement;
        leerDatosProducto(producto);
    }
}

function leerDatosProducto(producto){
    let infoProducto = {
        imagen: producto.querySelector('img').src,
        nombre: producto.querySelector('h4').textContent.substr(7),
        precio: producto.querySelector('.precio').textContent.substr(7),
        id: producto.querySelector('a').getAttribute('data-id'),
        cantidad: 1
    }

    let existe;

    let productosLS;

    productosLS = obtenerProductosLocalStorage();
    
    
    productosLS.forEach(function(pro) {
        if(pro.id === infoProducto.id){
            existe = true;
            pro.cantidad++;
            cont = pro.cantidad++;
            
            
        }else{
            existe = false;
        }
    });

    if (existe){
        document.getElementById(infoProducto.id).remove();
        
        infoProducto = {
            imagen: producto.querySelector('img').src,
            nombre: producto.querySelector('h4').textContent.substr(7),
            precio: producto.querySelector('.precio').textContent.substr(7),
            id: producto.querySelector('a').getAttribute('data-id'),
            cantidad: cont
        }
        productosLS.forEach(function(productoLS, index){
            if(productoLS.id === infoProducto.id){
                productosLS.splice(index, 1);
            }
        });
        localStorage.setItem('productos', JSON.stringify(productosLS));
    }

    insertarCarrito(infoProducto);

}

function insertarCarrito(producto){
    const row = document.createElement('tr');
    row.id = producto.id
    row.innerHTML = `
        <td>
            <img src="${producto.imagen}" width=100>
        </td>
        <td>
            ${producto.nombre}
        </td>
        <td>
            $${producto.precio}
        </td>
        <td class="cantidad">
            ${producto.cantidad}
        </td>
        <td>
            <a href="#" class="borrar-producto" data-id="${producto.id}">X</a>
        </td>
    `;
    listaProductos.appendChild(row);

    guardarProductoLocalStorage(producto);
}

function eliminarProducto(e){
    e.preventDefault();

    let producto, productoId;

    if(e.target.classList.contains('borrar-producto')){
        e.target.parentElement.parentElement.remove();
        producto = e.target.parentElement.parentElement;
        productoId = producto.querySelector('a').getAttribute('data-id');
    }
    eliminarProductoLocalStorage(productoId)
}

function vaciarCarrito(){
    while(listaProductos.firstChild){
        listaProductos.removeChild(listaProductos.firstChild);
    }
    vaciarLocalStorage();

    return false;
}

function guardarProductoLocalStorage(producto){
    let productos;

    productos = obtenerProductosLocalStorage();
    productos.push(producto);

    localStorage.setItem('productos', JSON.stringify(productos));
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

function leerLocalStorage(){
    let productosLS;

    productosLS = obtenerProductosLocalStorage();

    productosLS.forEach(function(producto) {
        const row = document.createElement('tr');
        row.id = producto.id
        row.innerHTML = `
        <td>
            <img src="${producto.imagen}" width=100>
        </td>
        <td>
            ${producto.nombre}
        </td>
        <td>
        $${producto.precio}
        </td>
        <td class="cantidad">
            ${producto.cantidad}
        </td>
        <td>
            <a href="#" class="borrar-producto" data-id="${producto.id}">X</a>
        </td>
        `;
        listaProductos.appendChild(row);
    });
}

function leerLocalStorageCompra(){
    let productosLS;

    productosLS = obtenerProductosLocalStorage();
    productosLS.forEach(function(producto) {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>
            <img src="${producto.imagen}" width=100>
        </td>
        <td>
            ${producto.nombre}
        </td>
        <td>
            $${producto.precio}
        </td>
        <td>
            $${producto.cantidad}
        </td>
        `;
        listaCompra.appendChild(row);
    });
}

function eliminarProductoLocalStorage(producto){
    let productosLS;

    productosLS = obtenerProductosLocalStorage();

    productosLS.forEach(function(productoLS, index){
        if(productoLS.id === producto){
            productosLS.splice(index, 1);
        }
    });
    localStorage.setItem('productos', JSON.stringify(productosLS));
}

function vaciarLocalStorage(){
    localStorage.clear();
}

function procesarPedido(e){
    e.preventDefault();
    if(obtenerProductosLocalStorage().length === 0){
        Swal.fire({
            type: 'error',
            title: 'Oops...',
            text: 'El carrito esta vacio',
            timer: 2000,
            showConfirmButton: false
        })
    }
    else{
        location.href = "procesar_compra";
    }
    
}


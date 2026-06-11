let carrito = {}; 
let totalPrecio = 0;
let totalArticulos = 0;
let catalogoPerfumes = [];

function crearFondoMagico() {
    let contenedor = document.getElementById('contenedor-magico');
    let svgs = ["data:image/svg+xml,%3Csvg viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12 0 Q12 12 24 12 Q12 12 12 24 Q12 12 0 12 Q12 12 12 0 Z' fill='%23EFBF04'/%3E%3C/svg%3E"];
    for (let i = 0; i < 22; i++) {
        let estrella = document.createElement('div');
        estrella.className = 'estrella-js';
        estrella.style.top = Math.random() * 100 + '%'; 
        estrella.style.left = Math.random() * 100 + '%'; 
        let size = Math.random() * 100 + 40; 
        estrella.style.width = size + 'px'; estrella.style.height = size + 'px';
        estrella.style.backgroundImage = `url("${svgs[0]}")`;
        estrella.style.animationDelay = (Math.random() * 5) + 's'; 
        contenedor.appendChild(estrella);
    }
}
crearFondoMagico();

// Jalamos el inventario de la carpeta principal
fetch('../productos.json')
    .then(r => r.json())
    .then(datos => {
        // Filtramos para quedarnos estrictamente con perfumes
        catalogoPerfumes = datos.filter(p => p.categoria === 'perfumes');
        renderizarCatalogo(catalogoPerfumes);
    });

function renderizarCatalogo(productosArray) {
    let contenedor = document.getElementById("contenedor-catalogo");
    contenedor.innerHTML = ""; 
    
    if(productosArray.length === 0) {
        contenedor.innerHTML = "<p style='color: #2B0071; font-weight: 600;'>No hay fragancias registradas en esta sección por el momento.</p>";
        return;
    }

    productosArray.forEach(producto => {
        let esAgotado = producto.stock <= 0 ? "agotado" : "";
        let botonHTML = producto.stock > 0 
            ? `<button class="btn-comprar" onclick="agregarAlCarrito('${producto.nombre}', ${producto.precio})">Comprar ahora</button>`
            : `<button class="btn-comprar" disabled>No disponible</button>`;
        let textoStock = producto.stock > 0 ? `Disponibles: ${producto.stock}` : "Agotado";

        contenedor.innerHTML += `
            <div class="tarjeta ${esAgotado}">
                <p style="font-size:11px; color:#666; text-transform:uppercase; font-weight:bold; letter-spacing:1px; margin-bottom:5px;">Para: ${producto.subseccion}</p>
                <h2>${producto.nombre}</h2>
                <div class="imagen-placeholder">${producto.imagen}</div>
                <p class="desc">${producto.desc}</p>
                <p class="precio">$${producto.precio}</p>
                <p class="stock">${textoStock}</p>
                ${botonHTML}
            </div>
        `;
    });
}

function filtrarSeccion(subseccion) {
    document.querySelectorAll('.btn-cat').forEach(btn => btn.classList.remove('activo'));
    event.target.classList.add('activo');

    let titulos = {
        'todos': 'ALQIMIA LUMA',
        'mujeres': 'ESENCIAS PARA MUJER',
        'hombres': 'FRAGANCIAS PARA HOMBRE',
        'niños': 'ESENCIAS INFANTILES'
    };
    document.getElementById("titulo-tienda").innerText = titulos[subseccion];

    if (subseccion === 'todos') {
        renderizarCatalogo(catalogoPerfumes);
    } else {
        let filtrados = catalogoPerfumes.filter(p => p.subseccion === subseccion);
        renderizarCatalogo(filtrados);
    }
}

function agregarAlCarrito(nombre, precio) {
    if (carrito[nombre]) carrito[nombre].cantidad += 1;
    else carrito[nombre] = { precio: precio, cantidad: 1 };
    totalPrecio += precio; totalArticulos += 1;
    document.getElementById("contador").innerText = totalArticulos;
    alert("🌙 ¡Agregaste " + nombre + " a tu pedido!");
}

function abrirCarrito() {
    let divLista = document.getElementById("lista-carrito"); divLista.innerHTML = ""; 
    if (totalArticulos === 0) divLista.innerHTML = "<p>Aún no has agregado ninguna esencia mágica.</p>";
    else {
        for (let nombre in carrito) {
            let item = carrito[nombre];
            divLista.innerHTML += `<div class="item-carrito"><span>${item.cantidad}x ${nombre}</span><span>$${item.cantidad * item.precio}</span></div>`;
        }
    }
    document.getElementById("total-precio").innerText = totalPrecio;
    document.getElementById("modal-carrito").style.display = "block";
}
function cerrarCarrito() { document.getElementById("modal-carrito").style.display = "none"; }

function enviarPedido() {
    if (totalArticulos === 0) return alert("Agrega productos antes de enviar tu pedido.");
    let mensaje = "🛍️ *NUEVO PEDIDO DE ALQIMIA LUMA*%0A%0A";
    for (let nombre in carrito) {
        let item = carrito[nombre];
        mensaje += `✨ ${item.cantidad}x ${nombre} ($${item.precio * item.cantidad})%0A`;
    }
    mensaje += "%0A*Total a pagar: $" + totalPrecio + "*";
    window.open("https://wa.me/525649314239?text=" + mensaje, "_blank");
}
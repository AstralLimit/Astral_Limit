let catalogoRopa = [];
let ofertasRopa = {};

// 1. CARGAR DATOS Y OFERTAS SIMULTÁNEAMENTE
Promise.all([
    fetch('../ofertas.json').then(r => r.json()),
    fetch('../productos.json').then(r => r.json())
]).then(([datosOfertas, datosProductos]) => {
    ofertasRopa = datosOfertas["Solar Street"] || {};
    let sucursal = datosProductos["Solar Street"];
    
    if (sucursal.estado === "cerrado") {
        document.getElementById("contenedor-catalogo").innerHTML = `
            <div class="alerta-centro">
                <h2>TIENDA CERRADA</h2>
                <p>La división Solar Street se encuentra en mantenimiento.</p>
            </div>`;
        document.querySelector('.menu-btn').style.display = 'none';
    } else {
        catalogoRopa = sucursal.productos;
        filtrarSeccion('todos');
    }
}).catch(e => console.log("Error de sincronización con la base de datos central."));

// 2. CONTROL DEL MENÚ LATERAL
function abrirMenu() { 
    let anchoMenu = window.innerWidth <= 600 ? "85%" : "300px";
    document.getElementById("side-menu").style.width = anchoMenu; 
}
function cerrarMenu() { 
    document.getElementById("side-menu").style.width = "0"; 
}

// 3. RENDERIZAR EL CATÁLOGO CON BANNERS DINÁMICOS POR BLOQUE
function renderizarCatalogo(productos, seccionActual) {
    let contenedor = document.getElementById("contenedor-catalogo");
    contenedor.innerHTML = "";

    // LÓGICA DE DETECCIÓN DE BANNER INTELIGENTE
    let llaveOferta = "";
    if (seccionActual.startsWith("hombre")) llaveOferta = "hombre";
    else if (seccionActual.startsWith("mujer")) llaveOferta = "mujer";
    else if (seccionActual.startsWith("niños")) llaveOferta = "niños";
    else if (seccionActual === "oferta-mundial") llaveOferta = "oferta-mundial";
    else if (seccionActual === "oferta-verano") llaveOferta = "oferta-verano";

    // Si hay un banner activo para este bloque de ropa, se inyecta primero
    if (llaveOferta && ofertasRopa[llaveOferta] && ofertasRopa[llaveOferta].activa) {
        contenedor.innerHTML += `
            <div class="banner-oferta-contenedor">
                <div class="banner-oferta-texto">${ofertasRopa[llaveOferta].texto}</div>
            </div>`;
    }

    if (productos.length === 0) {
        contenedor.innerHTML += `
            <div class="alerta-centro">
                <h2>PRÓXIMAMENTE</h2>
                <p>Nuestros diseñadores están preparando las prendas para esta sección.</p>
            </div>`;
        return;
    }

    productos.forEach(prod => {
        contenedor.innerHTML += `
            <div class="tarjeta">
                <div class="tarjeta-img">${prod.imagen}</div>
                <h3 class="nombre-prod">${prod.nombre}</h3>
                <p class="desc-prod">${prod.desc}</p>
                <p class="precio-prod">$${prod.precio}</p>
                <button class="btn-proximamente" disabled>Próximamente</button>
            </div>
        `;
    });
}

// 4. FILTRAR POR SECCIÓN (DESDE EL DRAWER)
function filtrarSeccion(subseccion) {
    cerrarMenu();
    
    let nombresTitulos = {
        'todos': 'CATÁLOGO COMPLETO',
        'oferta-mundial': 'COLECCIÓN MUNDIAL',
        'oferta-verano': 'TEMPORADA DE VERANO',
        'hombre-playeras': 'PLAYERAS & SUDADERAS DE HOMBRE',
        'hombre-pantalones': 'PANTALONES DE HOMBRE',
        'hombre-zapatos': 'CALZADO DE HOMBRE',
        'hombre-accesorios': 'ACCESORIOS DE HOMBRE',
        'mujer-playeras': 'BLUSAS & PLAYERAS DE MUJER',
        'mujer-pantalones': 'PANTALONES DE MUJER',
        'mujer-zapatos': 'CALZADO DE MUJER',
        'mujer-accesorios': 'ACCESORIOS DE MUJER',
        'niños-playeras': 'PLAYERAS INFANTILES',
        'niños-pantalones': 'PANTALONES INFANTILES',
        'niños-zapatos': 'CALZADO INFANTIL',
        'niños-accesorios': 'ACCESORIOS INFANTILES'
    };

    document.getElementById("titulo-seccion-actual").innerText = nombresTitulos[subseccion] || 'CATÁLOGO';

    if (subseccion === 'todos') {
        renderizarCatalogo(catalogoRopa, subseccion);
    } else {
        let filtrados = catalogoRopa.filter(p => p.subseccion === subseccion);
        renderizarCatalogo(filtrados, subseccion);
    }
}
let catalogoRopa = [];

// 1. CARGAR DATOS AL INICIO
fetch('../productos.json')
    .then(r => r.json())
    .then(datos => {
        let sucursal = datos["Solar Street"];
        
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
    }).catch(e => console.log("Error cargando productos."));


// 2. CONTROL DEL MENÚ LATERAL
function abrirMenu() { 
    // En móviles ocupa más pantalla, en PC se queda en 300px
    let anchoMenu = window.innerWidth <= 600 ? "85%" : "300px";
    document.getElementById("side-menu").style.width = anchoMenu; 
}
function cerrarMenu() { 
    document.getElementById("side-menu").style.width = "0"; 
}

// 3. RENDERIZAR EL CATÁLOGO
function renderizarCatalogo(productos) {
    let contenedor = document.getElementById("contenedor-catalogo");
    contenedor.innerHTML = "";

    if (productos.length === 0) {
        contenedor.innerHTML = `
            <div class="alerta-centro">
                <h2>SIN STOCK</h2>
                <p>Aún no tenemos prendas disponibles en esta sección.</p>
            </div>`;
        return;
    }

    productos.forEach(prod => {
        // Como el carrito está pausado para ropa, el botón es informativo
        let botonHTML = `<button class="btn-proximamente" disabled>Próximamente</button>`;
        
        contenedor.innerHTML += `
            <div class="tarjeta">
                <div class="tarjeta-img">${prod.imagen}</div>
                <h3 class="nombre-prod">${prod.nombre}</h3>
                <p class="desc-prod">${prod.desc}</p>
                <p class="precio-prod">$${prod.precio}</p>
                ${botonHTML}
            </div>
        `;
    });
}

// 4. FILTRAR POR SECCIÓN (DESDE EL MENÚ LATERAL)
function filtrarSeccion(subseccion) {
    cerrarMenu(); // Cierra el menú al elegir
    
    // Nombres legibles para el título
    let nombresTitulos = {
        'todos': 'CATÁLOGO COMPLETO',
        'oferta-padre': 'ESPECIAL DÍA DEL PADRE',
        'oferta-mundial': 'COLECCIÓN MUNDIAL',
        'hombre-playeras': 'PLAYERAS DE HOMBRE',
        'hombre-pantalones': 'PANTALONES DE HOMBRE',
        'hombre-zapatos': 'CALZADO DE HOMBRE',
        'hombre-accesorios': 'ACCESORIOS DE HOMBRE',
        'mujer-playeras': 'PLAYERAS DE MUJER',
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
        renderizarCatalogo(catalogoRopa);
    } else {
        let filtrados = catalogoRopa.filter(p => p.subseccion === subseccion);
        renderizarCatalogo(filtrados);
    }
}
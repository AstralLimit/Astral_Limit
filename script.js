let divisionesMatriz = [];
let estadoTiendas = {};

// 1. Crear el cielo estrellado
function crearCieloEstrellado() {
    const cielo = document.getElementById("cielo-estrellado");
    const cantidadEstrellas = 100; 

    for (let i = 0; i < cantidadEstrellas; i++) {
        let estrella = document.createElement("div");
        estrella.classList.add("estrella-noche");
        estrella.style.top = Math.random() * 100 + "vh";
        estrella.style.left = Math.random() * 100 + "vw";
        let tamaño = Math.random() * 2 + 1; 
        estrella.style.width = tamaño + "px";
        estrella.style.height = tamaño + "px";
        estrella.style.animationDuration = (Math.random() * 3 + 1.5) + "s";
        estrella.style.animationDelay = (Math.random() * 5) + "s";
        cielo.appendChild(estrella);
    }
}
crearCieloEstrellado();

// 2. Solicitar empresas Y productos simultáneamente para saber quién está cerrado
Promise.all([
    fetch('empresas.json').then(r => r.json()),
    fetch('productos.json').then(r => r.json())
]).then(([empresasDatos, productosDatos]) => {
    divisionesMatriz = empresasDatos;
    estadoTiendas = productosDatos;
    construirMenuHub();
}).catch(e => console.log("Error de conexión al servidor central."));

// 3. Crear las tarjetas visuales (Aplicando estado CERRADO si es necesario)
function construirMenuHub() {
    const contenedor = document.getElementById("grid-marcas");
    contenedor.innerHTML = "";

    divisionesMatriz.forEach(division => {
        // Leemos el estado desde el JSON de productos, por defecto 'abierto'
        let estadoActual = "abierto";
        if (estadoTiendas[division.nombre] && estadoTiendas[division.nombre].estado) {
            estadoActual = estadoTiendas[division.nombre].estado;
        }

        // Si está cerrado, le añadimos la clase especial "tienda-cerrada"
        let claseCerrada = estadoActual === "cerrado" ? "tienda-cerrada" : "";

        contenedor.innerHTML += `
            <div class="tarjeta-marca ${claseCerrada}" onclick="abrirPantallaMarca(${division.id}, '${estadoActual}')">
                <div class="banner-categoria-tarjeta">${division.categoria}</div>
                <div class="contenedor-imagen-tarjeta">
                    <img src="${division.logo}" alt="" class="img-marca-hub" onerror="this.src='https://via.placeholder.com/200/ffffff/000?text=${division.nombre}'">
                </div>
            </div>
        `;
    });
}

function navegarA(pantallaDestino) {
    const hub = document.getElementById("pantalla-hub");
    const bienvenida = document.getElementById("pantalla-bienvenida");

    if (pantallaDestino === 'hub') {
        bienvenida.classList.add("web-oculta");
        hub.classList.remove("web-oculta");
    } else if (pantallaDestino === 'bienvenida') {
        hub.classList.add("web-oculta");
        bienvenida.classList.remove("web-oculta");
    }
}

function abrirPantallaMarca(id, estado) {
    // Si la tienda está cerrada, no deja abrir la tarjeta de bienvenida
    if(estado === "cerrado") {
        alert("🔒 Esta división se encuentra actualmente cerrada por mantenimiento o reestructuración.");
        return;
    }

    const marca = divisionesMatriz.find(m => m.id === id);
    
    document.getElementById("marca-logo").src = marca.logo;
    document.getElementById("marca-logo").onerror = function() { this.src = 'https://via.placeholder.com/150/ffffff/000?text=' + marca.nombre; };
    document.getElementById("marca-titulo").innerText = marca.nombre.toUpperCase();
    document.getElementById("marca-categoria").innerText = marca.categoria;
    document.getElementById("marca-mensaje").innerText = marca.mensaje;
    
    const btnIniciar = document.getElementById("btn-iniciar");
    
    if(marca.nombre === "Alqimia Luma") {
        btnIniciar.innerText = "¿LISTO PARA TU ESENCIA? ✨";
    } else if (marca.nombre === "Solar Street") {
        btnIniciar.innerText = "VER COLECCIÓN URBANA 🧥";
    } else {
        btnIniciar.innerText = "ACCEDER A LA TIENDA 🚀";
    }

    btnIniciar.onclick = function() {
        window.location.href = marca.enlace;
    };

    navegarA('bienvenida');
}
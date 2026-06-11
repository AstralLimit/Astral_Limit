let divisionesMatriz = [];

// 1. Solicitar las submarcas al servidor
fetch('empresas.json')
    .then(r => r.json())
    .then(datos => {
        divisionesMatriz = datos;
        construirMenuHub();
    });

// 2. Crear las tarjetas visuales de las divisiones
function construirMenuHub() {
    const contenedor = document.getElementById("grid-marcas");
    contenedor.innerHTML = "";

    divisionesMatriz.forEach(division => {
        contenedor.innerHTML += `
            <div class="tarjeta-marca" onclick="abrirPantallaMarca(${division.id})">
                <div class="logo-recuadro">
                    <img src="${division.logo}" alt="${division.nombre}" class="img-marca-hub" onerror="this.src='https://via.placeholder.com/130/0a0a0f/fff?text=${division.nombre.substring(0,2)}'">
                </div>
                <h3 class="nombre-marca-hub">${division.nombre}</h3>
                <p class="cat-marca-hub">${division.categoria}</p>
            </div>
        `;
    });
}

// 3. Sistema de ruteo interno (Cambio entre Hub y Bienvenida)
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

// 4. Montar la información de la marca seleccionada
function abrirPantallaMarca(id) {
    const marca = divisionesMatriz.find(m => m.id === id);
    
    // Inyectar los datos dinámicamente en las etiquetas de texto
    document.getElementById("marca-logo").src = marca.logo;
    document.getElementById("marca-logo").onerror = function() { this.src = 'https://via.placeholder.com/140/0a0a0f/fff?text=' + marca.nombre; };
    document.getElementById("marca-titulo").innerText = marca.nombre.toUpperCase();
    document.getElementById("marca-categoria").innerText = marca.categoria;
    document.getElementById("marca-mensaje").innerText = marca.mensaje;
    
    // Asignar la ruta de desvío al botón de Acción Principal
    const btnIniciar = document.getElementById("btn-iniciar");
    btnIniciar.onclick = function() {
        // Redirige al enlace registrado (puede ser otra web o ruta local)
        window.location.href = marca.enlace;
    };

    // Cambiar de pantalla con animación
    navegarA('bienvenida');
}
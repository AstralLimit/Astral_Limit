let divisionesMatriz = [];

// 1. Solicitar las submarcas al servidor
fetch('empresas.json')
    .then(r => r.json())
    .then(datos => {
        divisionesMatriz = datos;
        construirMenuHub();
    });

// 2. Crear las tarjetas visuales del Hub (Actualizado sin títulos abajo y con cintillo arriba)
function construirMenuHub() {
    const contenedor = document.getElementById("grid-marcas");
    contenedor.innerHTML = "";

    divisionesMatriz.forEach(division => {
        contenedor.innerHTML += `
            <div class="tarjeta-marca" onclick="abrirPantallaMarca(${division.id})">
                <div class="banner-categoria-tarjeta">${division.categoria}</div>
                
                <div class="contenedor-imagen-tarjeta">
                    <img src="${division.logo}" alt="" class="img-marca-hub" onerror="this.src='https://via.placeholder.com/200/0a0a0f/fff?text=${division.nombre}'">
                </div>
            </div>
        `;
    });
}

// 3. Sistema de ruteo interno
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
    
    document.getElementById("marca-logo").src = marca.logo;
    document.getElementById("marca-logo").onerror = function() { this.src = 'https://via.placeholder.com/140/0a0a0f/fff?text=' + marca.nombre; };
    document.getElementById("marca-titulo").innerText = marca.nombre.toUpperCase();
    document.getElementById("marca-categoria").innerText = marca.categoria;
    document.getElementById("marca-mensaje").innerText = marca.mensaje;
    
    const btnIniciar = document.getElementById("btn-iniciar");
    btnIniciar.onclick = function() {
        window.location.href = marca.enlace;
    };

    navegarA('bienvenida');
}
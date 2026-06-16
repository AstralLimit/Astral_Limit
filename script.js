let divisionesMatriz = [];

// 1. Crear el cielo estrellado
function crearCieloEstrellado() {
    const cielo = document.getElementById("cielo-estrellado");
    const cantidadEstrellas = 100; // Puedes subirlo a 150 si quieres más tupido

    for (let i = 0; i < cantidadEstrellas; i++) {
        let estrella = document.createElement("div");
        estrella.classList.add("estrella-noche");
        
        // Posición aleatoria
        estrella.style.top = Math.random() * 100 + "vh";
        estrella.style.left = Math.random() * 100 + "vw";
        
        // Tamaños muy pequeños, como estrellas reales (entre 1px y 3px)
        let tamaño = Math.random() * 2 + 1; 
        estrella.style.width = tamaño + "px";
        estrella.style.height = tamaño + "px";
        
        // Animación aleatoria para que titilen a destiempo
        estrella.style.animationDuration = (Math.random() * 3 + 1.5) + "s";
        estrella.style.animationDelay = (Math.random() * 5) + "s";
        
        cielo.appendChild(estrella);
    }
}
crearCieloEstrellado();

// 2. Solicitar las submarcas al servidor
fetch('empresas.json')
    .then(r => r.json())
    .then(datos => {
        divisionesMatriz = datos;
        construirMenuHub();
    });

// 3. Crear las tarjetas visuales luminosas
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

// 4. Sistema de ruteo interno
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

// 5. Montar la información con los nuevos textos
function abrirPantallaMarca(id) {
    const marca = divisionesMatriz.find(m => m.id === id);
    
    document.getElementById("marca-logo").src = marca.logo;
    document.getElementById("marca-logo").onerror = function() { this.src = 'https://via.placeholder.com/150/0a0a0f/fff?text=' + marca.nombre; };
    document.getElementById("marca-titulo").innerText = marca.nombre.toUpperCase();
    document.getElementById("marca-categoria").innerText = marca.categoria;
    document.getElementById("marca-mensaje").innerText = marca.mensaje;
    
    const btnIniciar = document.getElementById("btn-iniciar");
    
    // Si es Alqimia Luma, mostramos el botón especial, si son las otras, uno distinto
    if(marca.nombre === "Alqimia Luma") {
        btnIniciar.innerText = "¿LISTO PARA TU ESENCIA? ✨";
    } else {
        btnIniciar.innerText = "ACCEDER A LA TIENDA 🚀";
    }

    btnIniciar.onclick = function() {
        window.location.href = marca.enlace;
    };

    navegarA('bienvenida');
}
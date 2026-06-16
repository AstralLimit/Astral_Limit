function abrirMenu() { document.getElementById("side-menu").style.width = "250px"; }
function cerrarMenu() { document.getElementById("side-menu").style.width = "0"; }

function filtrar(categoria) {
    cerrarMenu();
    // Aquí filtrarías tu JSON de productos (en productos.json)
    console.log("Mostrando categoría: " + categoria);
}
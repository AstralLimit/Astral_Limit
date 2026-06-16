import json
import os

ARCHIVO_PROD = 'productos.json'
ARCHIVO_OFERTAS = 'ofertas.json'

ESTRUCTURA_BASE = {
    "Alqimia Luma": {"estado": "abierto", "productos": []},
    "Solar Street": {"estado": "abierto", "productos": []},
    "Iridio Tech": {"estado": "abierto", "productos": []}
}

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_json(ruta, default):
    try:
        with open(ruta, 'r', encoding='utf-8') as f: return json.load(f)
    except: return default

def guardar_json(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4, ensure_ascii=False)

def pedir_categoria(empresa):
    print("\n--- SELECCIÓN DE CATEGORÍA ---")
    if empresa == "Alqimia Luma":
        print("1. Mujeres\n2. Hombres\n3. Niños")
        op = input("Selecciona un número (1/2/3): ")
        return "mujeres" if op == '1' else "hombres" if op == '2' else "niños"
        
    elif empresa == "Solar Street":
        print("1. Hombre\n2. Mujer\n3. Niños\n4. Colección Mundial\n5. Temporada de Verano")
        op = input("Selecciona un número (1/2/3/4/5): ")
        
        if op == '1':
            print("\n-- Subcategoría HOMBRE --")
            print("1. Playeras | 2. Pantalones | 3. Zapatos | 4. Accesorios")
            s = input("Selecciona un número: ")
            return "hombre-playeras" if s=='1' else "hombre-pantalones" if s=='2' else "hombre-zapatos" if s=='3' else "hombre-accesorios"
        elif op == '2':
            print("\n-- Subcategoría MUJER --")
            print("1. Playeras | 2. Pantalones | 3. Zapatos | 4. Accesorios")
            s = input("Selecciona un número: ")
            return "mujer-playeras" if s=='1' else "mujer-pantalones" if s=='2' else "mujer-zapatos" if s=='3' else "mujer-accesorios"
        elif op == '3':
            print("\n-- Subcategoría NIÑOS --")
            print("1. Playeras | 2. Pantalones | 3. Zapatos | 4. Accesorios")
            s = input("Selecciona un número: ")
            return "niños-playeras" if s=='1' else "niños-pantalones" if s=='2' else "niños-zapatos" if s=='3' else "niños-accesorios"
        elif op == '4': return "oferta-mundial"
        elif op == '5': return "oferta-verano"
        return "general"
    return "tecnologia"

def gestionar_ofertas_empresa(nombre_empresa):
    ofertas_data = cargar_json(ARCHIVO_OFERTAS, {})
    if nombre_empresa not in ofertas_data: ofertas_data[nombre_empresa] = {}
    ofertas = ofertas_data[nombre_empresa]

    while True:
        limpiar_pantalla()
        print(f"\n--- 🏷️ GESTIÓN DE OFERTAS: {nombre_empresa.upper()} ---")
        for cat, data in ofertas.items():
            estado = "🟢 ACTIVA" if data.get('activa') else "🔴 INACTIVA"
            print(f"- [{cat.upper()}]: {estado} | Banner: '{data.get('texto', '')}'")

        print("\n1. Encender / Modificar Banner de Oferta")
        print("2. Apagar un Banner de Oferta")
        print("3. Volver al menú de la tienda")
        op = input("Elige una opción: ")

        if op == '1':
            if nombre_empresa == "Solar Street":
                print("\n¿A qué bloque afectará esta oferta?\n1. Sección Hombre\n2. Sección Mujer\n3. Sección Niños\n4. Colección Mundial\n5. Temporada de Verano")
                s = input("Elige: ")
                cat = "hombre" if s=='1' else "mujer" if s=='2' else "niños" if s=='3' else "oferta-mundial" if s=='4' else "oferta-verano"
            else:
                cat = pedir_categoria(nombre_empresa)
                
            texto = input("Escribe el texto publicitario que saldrá en la web: ")
            ofertas[cat] = {"activa": True, "texto": texto}
            ofertas_data[nombre_empresa] = ofertas
            guardar_json(ARCHIVO_OFERTAS, ofertas_data)
            input("\n✅ Banner publicitario activado. Enter...")
        elif op == '2':
            if nombre_empresa == "Solar Street":
                print("\n¿Qué bloque deseas apagar?\n1. Hombre | 2. Mujer | 3. Niños | 4. Mundial | 5. Verano")
                s = input("Elige: ")
                cat = "hombre" if s=='1' else "mujer" if s=='2' else "niños" if s=='3' else "oferta-mundial" if s=='4' else "oferta-verano"
            else:
                cat = pedir_categoria(nombre_empresa)
            if cat in ofertas:
                ofertas[cat]["activa"] = False
                ofertas_data[nombre_empresa] = ofertas
                guardar_json(ARCHIVO_OFERTAS, ofertas_data)
                input("\n✅ Banner de oferta desactivado. Enter...")
        elif op == '3': break

def menu_empresa(nombre_empresa, datos):
    while True:
        limpiar_pantalla()
        empresa_data = datos[nombre_empresa]
        estado_actual = empresa_data['estado'].upper()
        
        print(f"\n=== GESTIÓN: {nombre_empresa.upper()} ===")
        print(f"ESTADO ACTUAL: {estado_actual}")
        print("---------------------------------")
        print("1. Abrir / Cerrar Tienda (Bloquea el acceso)")
        print("2. Ver Inventario Completo")
        print("3. Añadir Nuevo Producto")
        print("4. Modificar Producto (Precio y Stock)")
        print("5. Eliminar Producto")
        print("6. 🏷️  Gestionar Banners de Ofertas")
        print("7. ← Volver a la Matriz Principal")
        
        op = input("\nElige una opción: ")
        
        if op == '1':
            nuevo_estado = "cerrado" if empresa_data['estado'] == "abierto" else "abierto"
            datos[nombre_empresa]['estado'] = nuevo_estado
            guardar_json(ARCHIVO_PROD, datos)
            input(f"\n✅ Tienda {nombre_empresa} ahora está {nuevo_estado.upper()}. Presiona Enter...")
            
        elif op == '2':
            limpiar_pantalla()
            print(f"\n--- CATÁLOGO DE {nombre_empresa.upper()} ---")
            prods = empresa_data['productos']
            if not prods: print("[ El catálogo está vacío ]")
            for i, p in enumerate(prods):
                print(f"ID: {i} | [{p['subseccion'].upper()}] {p['nombre']} | Precio: ${p['precio']} | Stock: {p['stock']} uds")
            input("\nPresiona Enter para regresar...")
                
        elif op == '3':
            limpiar_pantalla()
            print(f"\n--- AÑADIR PRODUCTO A {nombre_empresa.upper()} ---")
            sub = pedir_categoria(nombre_empresa)
            nombre = input("\nNombre del producto: ")
            try:
                precio = int(input("Precio: "))
                stock = int(input("Stock inicial: "))
            except:
                input("\n❌ Solo números enteros. Enter...")
                continue
            desc = input("Eslogan o descripción persuasiva: ")
            imagen_input = input("Emoji o icono [Enter para omitir]: ")
            imagen = imagen_input if imagen_input.strip() != "" else "📦"
            
            datos[nombre_empresa]['productos'].append({
                "subseccion": sub, "nombre": nombre, "precio": precio, 
                "stock": stock, "desc": desc, "imagen": imagen
            })
            guardar_json(ARCHIVO_PROD, datos)
            input(f"\n✅ {nombre} añadido con éxito. Enter...")
            
        elif op == '4':
            limpiar_pantalla()
            print(f"\n--- MODIFICAR PRODUCTO ---")
            prods = empresa_data['productos']
            if not prods: input("Catálogo vacío. Enter..."); continue
            for i, p in enumerate(prods):
                print(f"[{i}] {p['nombre']} | ${p['precio']} | Stock: {p['stock']}")
            try:
                idx = int(input("\nIngresa el ID a modificar: "))
                if 0 <= idx < len(prods):
                    p_nuevo = input(f"Nuevo precio (actual ${prods[idx]['precio']}) [Enter para saltar]: ")
                    s_nuevo = input(f"Nuevo stock (actual {prods[idx]['stock']}) [Enter para saltar]: ")
                    if p_nuevo: datos[nombre_empresa]['productos'][idx]['precio'] = int(p_nuevo)
                    if s_nuevo: datos[nombre_empresa]['productos'][idx]['stock'] = int(s_nuevo)
                    guardar_json(ARCHIVO_PROD, datos)
                    input("\n✅ Cambios guardados. Enter...")
            except: input("\n❌ Error. Enter...")
            
        elif op == '5':
            limpiar_pantalla()
            print(f"\n--- ELIMINAR PRODUCTO ---")
            prods = empresa_data['productos']
            if not prods: input("Catálogo vacío. Enter..."); continue
            for i, p in enumerate(prods):
                print(f"[{i}] {p['nombre']} | Sección: {p['subseccion']}")
            try:
                idx = int(input("\nIngresa el ID para eliminar definitivamente: "))
                if 0 <= idx < len(prods):
                    eliminado = datos[nombre_empresa]['productos'].pop(idx)
                    guardar_json(ARCHIVO_PROD, datos)
                    input(f"\n🗑️ {eliminado['nombre']} eliminado. Enter...")
            except: input("\n❌ Error. Enter...")
            
        elif op == '6': gestionar_ofertas_empresa(nombre_empresa)
        elif op == '7': break

def main():
    while True:
        limpiar_pantalla()
        datos = cargar_json(ARCHIVO_PROD, ESTRUCTURA_BASE)
        print("\n==================================")
        print("  ASTRAL LIMIT: PANEL DE CONTROL  ")
        print("==================================")
        print("1. Administrar Alqimia Luma (Perfumes)")
        print("2. Administrar Solar Street (Ropa)")
        print("3. Administrar Iridio Tech (Tecnología)")
        print("4. 🚀 GUARDAR Y SUBIR A INTERNET")
        print("5. ❌ Apagar Sistema")
        op = input("\nElige una opción: ")
        if op == '1': menu_empresa("Alqimia Luma", datos)
        elif op == '2': menu_empresa("Solar Street", datos)
        elif op == '3': menu_empresa("Iridio Tech", datos)
        elif op == '4':
            limpiar_pantalla()
            print("🚀 Sincronizando con el servidor central...")
            os.system('git add . && git commit -m "Actualizacion Inventario" && git push')
            input("\n✅ ¡Todo subido a internet! Enter...")
        elif op == '5': break

if __name__ == "__main__": main()
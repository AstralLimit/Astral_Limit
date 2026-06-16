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
        print("1. Hombre\n2. Mujer\n3. Niños\n4. Ofertas Especiales")
        op = input("Selecciona un número (1/2/3/4): ")
        
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
        elif op == '4':
            print("\n-- Subcategoría OFERTAS --")
            print("1. Día del Padre | 2. Colección Mundial")
            s = input("Selecciona un número: ")
            return "oferta-padre" if s=='1' else "oferta-mundial"
        return "general"
        
    else:
        return "tecnologia"

def gestionar_ofertas_empresa(nombre_empresa):
    ofertas_data = cargar_json(ARCHIVO_OFERTAS, {})
    if nombre_empresa not in ofertas_data: ofertas_data[nombre_empresa] = {}
    ofertas = ofertas_data[nombre_empresa]

    while True:
        limpiar_pantalla()
        print(f"\n--- 🏷️ GESTIÓN DE OFERTAS: {nombre_empresa.upper()} ---")
        if not ofertas:
            print("No hay ofertas configuradas para esta tienda.")
        else:
            for cat, data in ofertas.items():
                estado = "🟢 ACTIVA" if data.get('activa') else "🔴 INACTIVA"
                print(f"- [{cat.upper()}]: {estado} | Mensaje: '{data.get('texto', '')}'")

        print("\n1. Crear o Modificar Oferta en una sección")
        print("2. Apagar una oferta")
        print("3. Volver al menú de la tienda")
        op = input("Elige una opción: ")

        if op == '1':
            cat = pedir_categoria(nombre_empresa)
            texto = input("Texto persuasivo del banner: ")
            ofertas[cat] = {"activa": True, "texto": texto}
            ofertas_data[nombre_empresa] = ofertas
            guardar_json(ARCHIVO_OFERTAS, ofertas_data)
            input("\n✅ Oferta guardada y encendida. Presiona Enter...")
        elif op == '2':
            cat = pedir_categoria(nombre_empresa)
            if cat in ofertas:
                ofertas[cat]["activa"] = False
                ofertas_data[nombre_empresa] = ofertas
                guardar_json(ARCHIVO_OFERTAS, ofertas_data)
                input("\n✅ Oferta apagada. Presiona Enter...")
            else:
                input("\n❌ Esa sección no tiene oferta registrada. Presiona Enter...")
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
        print("6. 🏷️ Gestionar Ofertas de esta tienda")
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
                stk = f"{p['stock']} uds" if p['stock'] > 0 else "AGOTADO"
                print(f"ID: {i} | [{p['subseccion']}] {p['nombre']} | Precio: ${p['precio']} | Stock: {stk}")
            input("\nPresiona Enter para regresar...")
                
        elif op == '3':
            limpiar_pantalla()
            print(f"\n--- AÑADIR PRODUCTO A {nombre_empresa.upper()} ---")
            sub = pedir_categoria(nombre_empresa)
            nombre = input("\nNombre de la prenda/producto: ")
            
            try:
                precio = int(input("Precio (solo números): "))
                stock = int(input("Stock inicial (solo números): "))
            except:
                input("\n❌ Error: Solo debes ingresar números. Presiona Enter y reintenta.")
                continue
            
            desc = input("Eslogan o descripción persuasiva: ")
            
            # Imagen opcional
            imagen_input = input("Imagen/Emoji [Presiona Enter para omitir]: ")
            imagen = imagen_input if imagen_input.strip() != "" else "📦"
            
            datos[nombre_empresa]['productos'].append({
                "subseccion": sub, "nombre": nombre, "precio": precio, 
                "stock": stock, "desc": desc, "imagen": imagen
            })
            guardar_json(ARCHIVO_PROD, datos)
            input(f"\n✅ {nombre} añadido al catálogo de {sub}. Presiona Enter...")
            
        elif op == '4':
            limpiar_pantalla()
            print(f"\n--- MODIFICAR PRODUCTO ---")
            prods = empresa_data['productos']
            if not prods:
                input("No hay productos. Presiona Enter...")
                continue
            for i, p in enumerate(prods):
                print(f"[{i}] {p['nombre']} | ${p['precio']} | Stock: {p['stock']}")
            try:
                idx = int(input("\nIngresa el ID (número en corchetes) a modificar: "))
                if 0 <= idx < len(prods):
                    p_nuevo = input(f"Nuevo precio (actual ${prods[idx]['precio']}) [Enter para ignorar]: ")
                    s_nuevo = input(f"Nuevo stock (actual {prods[idx]['stock']}) [Enter para ignorar]: ")
                    if p_nuevo: datos[nombre_empresa]['productos'][idx]['precio'] = int(p_nuevo)
                    if s_nuevo: datos[nombre_empresa]['productos'][idx]['stock'] = int(s_nuevo)
                    guardar_json(ARCHIVO_PROD, datos)
                    input("\n✅ Producto actualizado exitosamente. Presiona Enter...")
                else: input("\n❌ ID no encontrado. Presiona Enter...")
            except: input("\n❌ Formato incorrecto. Presiona Enter...")
            
        elif op == '5':
            limpiar_pantalla()
            print(f"\n--- ELIMINAR PRODUCTO ---")
            prods = empresa_data['productos']
            if not prods:
                input("No hay productos. Presiona Enter...")
                continue
            for i, p in enumerate(prods):
                print(f"[{i}] {p['nombre']} | Sección: {p['subseccion']}")
            try:
                idx = int(input("\nIngresa el ID del producto que deseas eliminar definitivamente: "))
                if 0 <= idx < len(prods):
                    eliminado = datos[nombre_empresa]['productos'].pop(idx)
                    guardar_json(ARCHIVO_PROD, datos)
                    input(f"\n🗑️ {eliminado['nombre']} ha sido borrado del sistema. Presiona Enter...")
                else: input("\n❌ ID inválido. Presiona Enter...")
            except: input("\n❌ Debes ingresar un número. Presiona Enter...")
            
        elif op == '6': gestionar_ofertas_empresa(nombre_empresa)
        elif op == '7': break

def main():
    while True:
        limpiar_pantalla()
        datos = cargar_json(ARCHIVO_PROD, ESTRUCTURA_BASE)
        for key in ESTRUCTURA_BASE:
            if key not in datos: datos[key] = ESTRUCTURA_BASE[key]
            
        print("\n==================================")
        print("  ASTRAL LIMIT: PANEL DE CONTROL  ")
        print("==================================")
        print("1. Administrar Alqimia Luma (Perfumes)")
        print("2. Administrar Solar Street (Ropa)")
        print("3. Administrar Iridio Tech (Tecnología)")
        print("4. 🚀 GUARDAR Y SUBIR A INTERNET")
        print("5. ❌ Apagar Sistema")
        
        op = input("\nElige una división o acción: ")
        
        if op == '1': menu_empresa("Alqimia Luma", datos)
        elif op == '2': menu_empresa("Solar Street", datos)
        elif op == '3': menu_empresa("Iridio Tech", datos)
        elif op == '4':
            limpiar_pantalla()
            print("🚀 Sincronizando con el servidor en internet...")
            os.system('git add . && git commit -m "Actualizacion Inventario Astral Limit" && git push -u origin main')
            input("\n✅ ¡El ecosistema está en línea! Presiona Enter para volver...")
        elif op == '5':
            limpiar_pantalla()
            print("Sistema Astral Limit apagado. ¡Buen día!")
            break

if __name__ == "__main__": main()
import json
import os

ARCHIVO_PROD = 'productos.json'
ARCHIVO_OFERTAS = 'ofertas.json'

ESTRUCTURA_BASE = {
    "Alqimia Luma": {"estado": "abierto", "productos": []},
    "Astral Moda": {"estado": "abierto", "productos": []},
    "Astral Tech": {"estado": "abierto", "productos": []}
}

def cargar_json(ruta, default):
    try:
        with open(ruta, 'r', encoding='utf-8') as f: 
            datos = json.load(f)
            # Si el archivo viejo es una lista plana, lo reiniciamos a la nueva estructura
            if isinstance(datos, list): return default
            return datos
    except: return default

def guardar_json(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4, ensure_ascii=False)

def gestionar_ofertas():
    ofertas = cargar_json(ARCHIVO_OFERTAS, {"hombres": {"activa": False, "texto": ""}, "mujeres": {"activa": False, "texto": ""}, "niños": {"activa": False, "texto": ""}})
    while True:
        print("\n--- 🏷️ PANEL DE OFERTAS (ALQIMIA LUMA) ---")
        for cat, data in ofertas.items():
            estado = "🟢 ACTIVA" if data.get('activa') else "🔴 INACTIVA"
            print(f"- {cat.upper()}: {estado} | Mensaje: '{data.get('texto', '')}'")
        
        print("\n1. Activar o Modificar oferta")
        print("2. Apagar oferta")
        print("3. Volver al menú anterior")
        op = input("Elige: ")
        
        if op == '1':
            cat = input("Categoría (hombres / mujeres / niños): ").lower()
            texto = input("Texto del banner rojo gigante: ")
            if cat not in ofertas: ofertas[cat] = {}
            ofertas[cat] = {"activa": True, "texto": texto}
            guardar_json(ARCHIVO_OFERTAS, ofertas)
            print("✅ Oferta guardada y encendida.")
        elif op == '2':
            cat = input("Categoría a apagar: ").lower()
            if cat in ofertas:
                ofertas[cat]["activa"] = False
                guardar_json(ARCHIVO_OFERTAS, ofertas)
                print("✅ Oferta apagada.")
        elif op == '3': break

def menu_empresa(nombre_empresa, datos):
    while True:
        empresa_data = datos[nombre_empresa]
        estado_actual = empresa_data['estado'].upper()
        
        print(f"\n=== GESTIÓN: {nombre_empresa} ===")
        print(f"ESTADO DE SUCURSAL: {estado_actual}")
        print("1. Encender / Apagar Tienda")
        print("2. Ver Inventario Completo")
        print("3. Agregar Nuevo Producto")
        print("4. Modificar Producto (Precio y Stock)")
        print("5. Eliminar Producto")
        print("6. Volver a la Matriz")
        
        op = input("Elige una opción: ")
        
        if op == '1':
            nuevo_estado = "cerrado" if empresa_data['estado'] == "abierto" else "abierto"
            datos[nombre_empresa]['estado'] = nuevo_estado
            guardar_json(ARCHIVO_PROD, datos)
            print(f"✅ Tienda cambiada a {nuevo_estado.upper()}.")
            
        elif op == '2':
            print(f"\n--- INVENTARIO {nombre_empresa.upper()} ---")
            prods = empresa_data['productos']
            if not prods: print("[ Catálogo vacío ]")
            for i, p in enumerate(prods):
                sub = f"[{p.get('subseccion', 'general').upper()}]"
                stk = f"{p['stock']} uds" if p['stock'] > 0 else "AGOTADO"
                print(f"ID: {i} | {sub} {p['nombre']} | Precio: ${p['precio']} | Stock: {stk}")
                
        elif op == '3':
            print("\n-- NUEVO PRODUCTO --")
            sub = "general"
            if nombre_empresa == "Alqimia Luma":
                s_opc = input("Subsección (1: Mujeres | 2: Hombres | 3: Niños): ")
                sub = "mujeres" if s_opc == '1' else "hombres" if s_opc == '2' else "niños"
            
            nombre = input("Nombre: ")
            try:
                precio = int(input("Precio (solo números): "))
                stock = int(input("Stock (solo números): "))
            except:
                print("❌ Error: Usa solo números enteros para precio y stock.")
                continue
            desc = input("Descripción corporativa: ")
            
            datos[nombre_empresa]['productos'].append({
                "subseccion": sub, "nombre": nombre, "precio": precio, 
                "stock": stock, "desc": desc, "imagen": "📸 Foto"
            })
            guardar_json(ARCHIVO_PROD, datos)
            print(f"✅ {nombre} agregado exitosamente.")
            
        elif op == '4':
            prods = empresa_data['productos']
            if not prods:
                print("No hay productos para modificar.")
                continue
            for i, p in enumerate(prods):
                print(f"ID: {i} | {p['nombre']} | ${p['precio']} | Stock: {p['stock']}")
            try:
                idx = int(input("ID del producto a modificar: "))
                if 0 <= idx < len(prods):
                    p_nuevo = input(f"Nuevo precio (actual ${prods[idx]['precio']}) [Enter para saltar]: ")
                    s_nuevo = input(f"Nuevo stock (actual {prods[idx]['stock']}) [Enter para saltar]: ")
                    if p_nuevo: datos[nombre_empresa]['productos'][idx]['precio'] = int(p_nuevo)
                    if s_nuevo: datos[nombre_empresa]['productos'][idx]['stock'] = int(s_nuevo)
                    guardar_json(ARCHIVO_PROD, datos)
                    print("✅ Producto actualizado.")
                else: print("❌ ID inválido.")
            except: print("❌ Error de formato numérico.")
            
        elif op == '5':
            prods = empresa_data['productos']
            try:
                idx = int(input("ID del producto a eliminar: "))
                if 0 <= idx < len(prods):
                    eliminado = datos[nombre_empresa]['productos'].pop(idx)
                    guardar_json(ARCHIVO_PROD, datos)
                    print(f"🗑️ Eliminado: {eliminado['nombre']}")
            except: print("❌ Error.")
            
        elif op == '6': break

def main():
    while True:
        datos = cargar_json(ARCHIVO_PROD, ESTRUCTURA_BASE)
        # Aseguramos que la estructura base no se corrompa
        for key in ESTRUCTURA_BASE:
            if key not in datos: datos[key] = ESTRUCTURA_BASE[key]
            
        print("\n=== ASTRAL LIMIT: PANEL MATRIZ ===")
        print("1. Administrar Alqimia Luma (Perfumes)")
        print("2. Administrar Astral Moda (Ropa)")
        print("3. Administrar Astral Tech (Tecnología)")
        print("4. 🏷️ Gestionar Ofertas Globales")
        print("5. 🚀 SUBIR ACTUALIZACIONES A INTERNET")
        print("6. Salir del Sistema")
        
        op = input("Elige una división: ")
        
        if op == '1': menu_empresa("Alqimia Luma", datos)
        elif op == '2': menu_empresa("Astral Moda", datos)
        elif op == '3': menu_empresa("Astral Tech", datos)
        elif op == '4': gestionar_ofertas()
        elif op == '5':
            os.system('git add . && git commit -m "Actualizacion Matriz de Empresas" && git push -u origin main')
            print("🚀 ¡Todo el ecosistema ha sido subido a internet!")
        elif op == '6': break

if __name__ == "__main__": main()
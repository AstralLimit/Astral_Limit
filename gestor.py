import json
import os

ARCHIVO = 'productos.json'

def cargar_datos():
    try:
        with open(ARCHIVO, 'r', encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: return []

def guardar_datos(datos):
    with open(ARCHIVO, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4, ensure_ascii=False)

def mostrar_inventario(datos):
    print("\n--- CONTROL DE INVENTARIO CENTRAL ASTRAL LIMIT ---")
    if not datos:
        print("[ Catálogo vacío ]")
    for i, p in enumerate(datos):
        stock_str = f"{p['stock']} uds" if p['stock'] > 0 else "🚫 AGOTADO"
        sub = f" -> {p['subseccion'].upper()}" if 'subseccion' in p else ""
        print(f"ID: {i} | [{p['categoria'].upper()}{sub}] {p['nombre']} | ${p['precio']} | {stock_str}")
    print("--------------------------------------------------\n")

def main():
    while True:
        datos = cargar_datos()
        print("\n=== SISTEMA DE MANDO CENTRAL ===")
        print("1. Ver Inventario Completo")
        print("2. Agregar Nuevo Producto (Cualquier Marca)")
        print("3. Modificar Stock de Producto")
        print("4. Eliminar Producto")
        print("5. 🚀 SUBIR ACTUALIZACIONES A INTERNET")
        print("6. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1': mostrar_inventario(datos)
        elif opcion == '2':
            print("\n-- CLASIFICACIÓN DE LÍNEA --")
            print("1) Perfumes (Alqimia Luma) | 2) Ropa | 3) Tecnología")
            c_opc = input("Selecciona la división: ")
            
            if c_opc == '1':
                cat = "perfumes"
                print("\n-- CATEGORÍA DE FRAGANCIA --")
                print("1) Mujeres | 2) Hombres | 3) Niños")
                s_opc = input("Selecciona la subsección: ")
                sub = "mujeres" if s_opc == '1' else "hombres" if s_opc == '2' else "niños"
            elif c_opc == '2':
                cat = "ropa"
                sub = "general"
            else:
                cat = "tecnologia"
                sub = "general"
                
            nombre = input("Nombre del producto: ")
            try:
                precio = int(input("Precio de venta (solo números): "))
                stock = int(input("Unidades disponibles: "))
            except ValueError:
                print("❌ Error: Precio y stock deben ser numéricos.\n"); continue
                
            desc = input("Descripción comercial: ")
            
            datos.append({
                "id": len(datos) + 1,
                "categoria": cat,
                "subseccion": sub,
                "nombre": nombre,
                "precio": precio,
                "stock": stock,
                "desc": desc,
                "imagen": "📸 Foto"
            })
            guardar_datos(datos)
            print(f"✅ ¡{nombre} registrado con éxito en la matriz!")
            
        elif opcion == '3':
            mostrar_inventario(datos)
            try:
                idx = int(input("Escribe el ID del producto a modificar: "))
                if 0 <= idx < len(datos):
                    print(f"Modificando: {datos[idx]['nombre']}")
                    n_stock = input(f"Nuevo stock (actual: {datos[idx]['stock']}): ")
                    if n_stock: datos[idx]['stock'] = int(n_stock)
                    guardar_datos(datos)
                    print("✅ Inventario actualizado.")
                else: print("❌ ID no válido.")
            except ValueError: print("❌ Solo números enteros.")
            
        elif opcion == '4':
            mostrar_inventario(datos)
            try:
                idx = int(input("Escribe el ID del producto a eliminar: "))
                if 0 <= idx < len(datos):
                    eliminado = datos.pop(idx)
                    guardar_datos(datos)
                    print(f"🗑️ ¡{eliminado['nombre']} eliminado del catálogo!")
            except: print("❌ Error al eliminar.")
            
        elif opcion == '5':
            print("\nSincronizando servidores globales...")
            os.system('git add . && git commit -m "Actualizacion Inventario Astral Limit" && git push -u origin main')
            print("🚀 ¡Todo el ecosistema ha sido actualizado en internet!")
            
        elif opcion == '6': break

if __name__ == "__main__": main()
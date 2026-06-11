import json
import os

ARCHIVO_PROD = 'productos.json'
ARCHIVO_OFERTAS = 'ofertas.json'

def cargar_json(ruta, default):
    try:
        with open(ruta, 'r', encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: return default

def guardar_json(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4, ensure_ascii=False)

def mostrar_inventario(datos):
    print("\n--- CONTROL DE INVENTARIO CENTRAL ASTRAL LIMIT ---")
    if not datos: print("[ Catálogo vacío ]")
    for i, p in enumerate(datos):
        stock_str = f"{p['stock']} uds" if p['stock'] > 0 else "🚫 AGOTADO"
        sub = f" -> {p['subseccion'].upper()}" if 'subseccion' in p else ""
        print(f"ID: {i} | [{p['categoria'].upper()}{sub}] {p['nombre']} | ${p['precio']} | {stock_str}")
    print("--------------------------------------------------\n")

def gestionar_ofertas():
    ofertas = cargar_json(ARCHIVO_OFERTAS, {})
    while True:
        print("\n--- 🏷️ PANEL DE OFERTAS Y PROMOCIONES ---")
        for cat, data in ofertas.items():
            estado = "🟢 ACTIVA" if data.get('activa') else "🔴 INACTIVA"
            print(f"- {cat.upper()}: {estado} | Mensaje: '{data.get('texto', '')}'")
        
        print("\nOpciones:")
        print("1. Activar/Modificar oferta en una categoría")
        print("2. Apagar oferta en una categoría")
        print("3. Volver al menú principal")
        op = input("Elige: ")
        
        if op == '1':
            cat = input("¿En qué categoría? (hombres, mujeres, niños, todos): ").lower()
            texto = input("Escribe el texto del banner rojo gigante: ")
            if cat not in ofertas: ofertas[cat] = {}
            ofertas[cat] = {"activa": True, "texto": texto}
            guardar_json(ARCHIVO_OFERTAS, ofertas)
            print("✅ Oferta encendida.")
        elif op == '2':
            cat = input("¿Qué categoría quieres apagar?: ").lower()
            if cat in ofertas:
                ofertas[cat]["activa"] = False
                guardar_json(ARCHIVO_OFERTAS, ofertas)
                print("✅ Oferta apagada.")
        elif op == '3': break

def main():
    while True:
        datos = cargar_json(ARCHIVO_PROD, [])
        print("\n=== SISTEMA DE MANDO CENTRAL ===")
        print("1. Ver Inventario Completo")
        print("2. Agregar Nuevo Producto")
        print("3. Modificar Stock")
        print("4. Eliminar Producto")
        print("5. 🏷️ GESTIONAR OFERTAS")
        print("6. 🚀 SUBIR ACTUALIZACIONES A INTERNET")
        print("7. Salir")
        opcion = input("Elige una opción: ")

        if opcion == '1': mostrar_inventario(datos)
        elif opcion == '2':
            print("1) Perfumes | 2) Ropa | 3) Tecnología")
            c_opc = input("División: ")
            if c_opc == '1':
                cat = "perfumes"
                s_opc = input("1) Mujeres | 2) Hombres | 3) Niños : ")
                sub = "mujeres" if s_opc == '1' else "hombres" if s_opc == '2' else "niños"
            else:
                cat = "ropa" if c_opc == '2' else "tecnologia"
                sub = "general"
                
            nombre = input("Nombre del producto: ")
            try:
                precio = int(input("Precio: "))
                stock = int(input("Stock: "))
            except ValueError:
                print("❌ Error: Usa solo números."); continue
                
            datos.append({"id": len(datos) + 1, "categoria": cat, "subseccion": sub, "nombre": nombre, "precio": precio, "stock": stock, "desc": input("Descripción: "), "imagen": "📸 Foto"})
            guardar_json(ARCHIVO_PROD, datos)
            print("✅ Producto registrado.")
            
        elif opcion == '3':
            mostrar_inventario(datos)
            try:
                idx = int(input("ID a modificar: "))
                n_stock = input("Nuevo stock: ")
                if n_stock: datos[idx]['stock'] = int(n_stock)
                guardar_json(ARCHIVO_PROD, datos)
            except: print("❌ Error.")
        elif opcion == '4':
            mostrar_inventario(datos)
            try: idx = int(input("ID a eliminar: ")); datos.pop(idx); guardar_json(ARCHIVO_PROD, datos)
            except: print("❌ Error.")
        elif opcion == '5': gestionar_ofertas()
        elif opcion == '6':
            os.system('git add . && git commit -m "Actualizacion Inventario y Ofertas" && git push -u origin main')
            print("🚀 ¡Todo el ecosistema subido a internet!")
        elif opcion == '7': break

if __name__ == "__main__": main()
import json
import os

ARCHIVO = 'empresas.json'

def cargar_datos():
    with open(ARCHIVO, 'r', encoding='utf-8') as f: return json.load(f)

def guardar_datos(datos):
    with open(ARCHIVO, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4, ensure_ascii=False)

def mostrar_empresas(datos):
    print("\n--- DIVISIONES DE ASTRAL LIMIT ---")
    for i, emp in enumerate(datos):
        print(f"ID: {i} | Marca: {emp['nombre']} | Enlace: {emp['enlace']}")
    print("----------------------------------\n")

def main():
    while True:
        datos = cargar_datos()
        print("\n=== ASTRAL LIMIT: PANEL MATRIZ ===")
        print("1. Ver marcas | 2. Agregar nueva marca | 3. Eliminar marca | 5. 🚀 SUBIR | 6. Salir")
        opcion = input("Elige: ")

        if opcion == '1': 
            mostrar_empresas(datos)
        elif opcion == '2':
            print("\n-- NUEVA MARCA / DIVISIÓN --")
            nombre = input("Nombre de la empresa: ")
            logo = input("Nombre del archivo de su logo (ej. marca.png): ")
            mensaje = input("Texto de bienvenida al seleccionarla: ")
            enlace = input("Enlace de la página a la que irá (ej. https://...): ")
            
            datos.append({
                "id": len(datos)+1, "nombre": nombre, "logo": logo, 
                "mensaje": mensaje, "enlace": enlace
            })
            guardar_datos(datos)
            print("✅ Marca agregada al Hub Central.")
            
        elif opcion == '3':
            mostrar_empresas(datos)
            try:
                idx = int(input("ID de la marca a borrar: "))
                if 0 <= idx < len(datos):
                    eliminado = datos.pop(idx)
                    guardar_datos(datos)
                    print(f"🗑️ {eliminado['nombre']} eliminada.")
            except: print("❌ Error.")
            
        elif opcion == '5':
            # AQUÍ ESTÁ LA CORRECCIÓN: Comillas dobles para que Windows no se confunda
            os.system('git add . && git commit -m "Actualizacion Astral Limit" && git push')
            print("🚀 ¡Enviado a internet!")
        elif opcion == '6': break

if __name__ == "__main__": main()
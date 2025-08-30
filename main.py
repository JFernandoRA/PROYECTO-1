from tkinter import Tk
import menu
import lector_xml
import estudiante
import procesador
import graficador
from graphviz import Digraph
from tkinter import messagebox, simpledialog
from tkinter import filedialog
import salida


campos = None

def main():
    Tk().withdraw()

    global campos

    while True:
        menu.mostrar_menu()
        opcion = input("Elija una opción: ").strip()

        if opcion == '1':
            ruta = lector_xml.cargar_xml()
            if ruta:
                campos = lector_xml.leerConElementTree(ruta)

        elif opcion == '2':
            if campos is None:
                print("Primero debe cargar un archivo.")
            else:
                print("\n--- PROCESANDO ARCHIVO ---")
                procesador.procesar_campos(campos)

        elif opcion == '3':
            print("Escribir Archivo de Salida")
            if campos is None:
                print("Primero debe procesar el archivo.")
            else:
                print("Procesando campos para salida...")
                campos_procesados = procesador.procesar_campos(campos)
                if campos_procesados is None:
                    continue
                ruta_salida = filedialog.asksaveasfilename(
                    title ="Guardar archivo de salida",
                    defaultextension=".xml",
                    filetypes=[("Archivos XML", "*.xml")]
                )
                
                if ruta_salida:
                    salida.generar_xml_salida(campos_procesados, ruta_salida)
                else:
                    print("No se seleccionó una ruta de salida.")

        elif opcion == '4':
            estudiante.DatosdelEstudiante()
            
        elif opcion == '5':
            if campos is None:
                print("Primero debe cargar un archivo.")
                continue

            lista_campos = list(campos.recorrer())
            if not lista_campos:
                print("No hay campos cargados.")
                continue

            print("\nCampos agrícolas disponibles:")
            for i, campo in enumerate(lista_campos, start=1):
                print(f"{i}. {campo.nombre} (ID: {campo.id})")

            try:
                idx = int(input("\nSeleccione un campo (número): ")) - 1
                if idx < 0 or idx >= len(lista_campos):
                    print("Número de campo no válido.")
                    continue
                campo_seleccionado = lista_campos[idx]
            except ValueError:
                print("Entrada no válida. Debe ingresar un número.")
                continue

            campos_procesados = None
            try:
                campos_procesados = procesador.procesar_campos(campos)
            except Exception as e:
                print(f"Error al procesar los campos: {e}")

            try:
                graficador.menu_generar_graficas_proyecto(
                    campo_seleccionado, campos_procesados
                )
            except Exception as e:
                print(f"Error al generar gráficas: {e}")

        elif opcion == '6':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
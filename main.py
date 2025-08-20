# main.py
from tkinter import Tk
import menu
import lector_xml
import estudiante
import procesador

# Variable global para guardar los datos
campos = None

def main():
    # Ocultar ventana de Tkinter
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
                print("Funcionalidad en desarrollo...")

        elif opcion == '4':
            estudiante.DatosdelEstudiante()

        elif opcion == '5':
            print("Generar Gráficas")
            print("Funcionalidad en desarrollo...")

        elif opcion == '6':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
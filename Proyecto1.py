from tkinter import filedialog, messagebox, Tk
from xml.etree import ElementTree as ET


def mostrar_menu():
    print("\nMenú de opciones:")
    print("1. Cargar Archivo")
    print("2. Procesar Archivo")
    print("3. Escribir Archivo de Salida")
    print("4. Mostrar datos del Estudiante")
    print("5. Generar Gráficas")
    print("6. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")

        if opcion == '1':
            ruta = cargar_xml()
            if ruta == '':
                messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
            else:
                messagebox.showinfo("Archivo Cargado", f"Archivo cargado correctamente: {ruta}")

        elif opcion == '2':
            print("Procesar Archivo")
            leerConElementTree(ruta)
            
        elif opcion == '3':
            print("Escribir Archivo de Salida")
            # Lógica para escribir archivo de salida
            
        elif opcion == '4':    
            print("Mostrar datos del Estudiante")
            DatosdelEstudiante()
            
        elif opcion == '5':
            print("Generar Gráficas")
            # Lógica para generar gráficas
            
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


def cargar_xml():
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo XML",
        filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
    )
    root.destroy()
    return ruta

#GUIA 
def leerConElementTree(ruta):
    try:
        # Parsear el archivo XML
        tree = ET.parse(ruta)
        root = tree.getroot()

        if root.tag == "camposAgricolas":
            print("\n--- Campos Agrícolas encontrados ---")
            for campo in root.findall("campo"):
                id_campo = campo.get("id")
                nombre_campo = campo.get("nombre")
                print(f"Campo {id_campo}: {nombre_campo}")

                # Leer estaciones base
                estaciones = campo.find("estacionesBase")
                if estaciones is not None:
                    print("Estaciones Base:")
                    for estacion in estaciones.findall("estacion"):
                        id_est = estacion.get("id")
                        nombre_est = estacion.get("nombre")
                        print(f"    - {id_est}: {nombre_est}")

                # Leer sensores de suelo
                sensores_suelo = campo.find("sensoresSuelo")
                if sensores_suelo is not None:
                    print("Sensores de Suelo:")
                    for sensor in sensores_suelo.findall("sensorS"):
                        id_sensor = sensor.get("id")
                        nombre_sensor = sensor.get("nombre")
                        print(f"    - {id_sensor}: {nombre_sensor}")
                        for freq in sensor.findall("frecuencia"):
                            id_estacion = freq.get("idEstacion")
                            valor = freq.text.strip()
                            print(f"        Frecuencia en {id_estacion}: {valor}")

                # Leer sensores de cultivo
                sensores_cultivo = campo.find("sensoresCultivo")
                if sensores_cultivo is not None:
                    print("  Sensores de Cultivo:")
                    for sensor in sensores_cultivo.findall("sensorT"):
                        id_sensor = sensor.get("id")
                        nombre_sensor = sensor.get("nombre")
                        print(f"    - {id_sensor}: {nombre_sensor}")
                        for freq in sensor.findall("frecuencia"):
                            id_estacion = freq.get("idEstacion")
                            valor = freq.text.strip()
                            print(f"Frecuencia en {id_estacion}: {valor}")

        else:
            print("El archivo no es válido para este proyecto.")

    except Exception as e:
        print(f"Error al leer el XML: {e}")

        
                


def DatosdelEstudiante():
    print("\n--- Datos del estudiante ---")
    print("Nombre: José Fernando Ramírez Ambrocio")
    print("Carné: 202400195")
    print("Curso: Introducción a la Programación y Computación 2")
    print("Carrera: Ingeniería en Sistemas")
    print("Semestre: 4to")
    print("Documentación: https://github.com/JFernandoRA/PROYECTO-1.git")



if __name__ == "__main__":
        main()
    

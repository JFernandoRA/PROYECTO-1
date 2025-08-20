from tkinter import filedialog, messagebox
from xml.etree import ElementTree as ET
from estructuras.lista_simple import ListaSimple  
from estructuras.campo import Campo, Estacion, SensorS, SensorT  

def cargar_xml():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo XML",
        filetypes=[("Archivos XML", "*.xml"), ("Todos los archivos", "*.*")]
    )
    if ruta == "":
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
    else:
        messagebox.showinfo("Archivo Cargado", f"Archivo cargado correctamente: {ruta}")
    return ruta

def leerConElementTree(ruta):
    try:
        tree = ET.parse(ruta)
        root = tree.getroot()

        if root.tag != "camposAgricolas":
            print("El archivo no es válido para este proyecto.")
            return None

        campos = ListaSimple()

        for campo_xml in root.findall("campo"):
            id_campo = campo_xml.get("id")
            nombre_campo = campo_xml.get("nombre")
            print(f"➢ Cargando campo agrícola {id_campo} ({nombre_campo})")
            campo = Campo(id_campo, nombre_campo)

            # Estaciones base
            estaciones_xml = campo_xml.find("estacionesBase")
            if estaciones_xml is not None:
                for estacion_xml in estaciones_xml.findall("estacion"):
                    id_est = estacion_xml.get("id")
                    nombre_est = estacion_xml.get("nombre")
                    print(f"  ➜ Creando estación base {id_est} ({nombre_est})")
                    campo.estaciones.insertar(Estacion(id_est, nombre_est))

            # Sensores de suelo
            sensores_s_xml = campo_xml.find("sensoresSuelo")
            if sensores_s_xml is not None:
                for sensor_xml in sensores_s_xml.findall("sensorS"):
                    id_s = sensor_xml.get("id")
                    nombre_s = sensor_xml.get("nombre")
                    print(f"  ➜ Creando sensor de suelo {id_s} ({nombre_s})")
                    sensor = SensorS(id_s, nombre_s)
                    for freq in sensor_xml.findall("frecuencia"):
                        id_estacion = freq.get("idEstacion")
                        valor = int(freq.text.strip())
                        sensor.frecuencias.insertar({"idEstacion": id_estacion, "valor": valor})
                    campo.sensores_suelo.insertar(sensor)

            # Sensores de cultivo
            sensores_t_xml = campo_xml.find("sensoresCultivo")
            if sensores_t_xml is not None:
                for sensor_xml in sensores_t_xml.findall("sensorT"):
                    id_t = sensor_xml.get("id")
                    nombre_t = sensor_xml.get("nombre")
                    print(f"  ➜ Creando sensor de cultivo {id_t} ({nombre_t})")
                    sensor = SensorT(id_t, nombre_t)
                    for freq in sensor_xml.findall("frecuencia"):
                        id_estacion = freq.get("idEstacion")
                        valor = int(freq.text.strip())
                        sensor.frecuencias.insertar({"idEstacion": id_estacion, "valor": valor})
                    campo.sensores_cultivo.insertar(sensor)

            campos.insertar(campo)

        return campos  # Devuelve la lista de campos

    except Exception as e:
        print(f"Error al leer el XML: {e}")
        return None
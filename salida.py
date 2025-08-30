# salida.py
import xml.etree.ElementTree as ET
from xml.dom import minidom


def generar_xml_salida(campos_procesados, ruta_salida):
    root = ET.Element("camposAgricolas")

    for campo in campos_procesados:
        campo_elem = ET.SubElement(root, "campo", {
            "id": campo["id"],
            "nombre": campo["nombre"]
        })

        # Estaciones base reducidas
        estaciones_reducidas = ET.SubElement(campo_elem, "estacionesBaseReducidas")
        for estacion in campo["estaciones_reducidas"]:
            ET.SubElement(estaciones_reducidas, "estacion", {
                "id": estacion["id"],
                "nombre": estacion["nombre"]
            })

        # Sensores de suelo
        sensores_suelo = ET.SubElement(campo_elem, "sensoresSuelo")
        for sensor in campo["sensores_suelo"]:
            sensor_elem = ET.SubElement(sensores_suelo, "sensorS", {
                "id": sensor["id"],
                "nombre": sensor["nombre"]
            })
            for freq in sensor["frecuencias"]:
                ET.SubElement(sensor_elem, "frecuencia", {
                    "idEstacion": freq["idEstacion"]
                }).text = str(freq["valor"])

        # Sensores de cultivo
        sensores_cultivo = ET.SubElement(campo_elem, "sensoresCultivo")
        for sensor in campo["sensores_cultivo"]:
            sensor_elem = ET.SubElement(sensores_cultivo, "sensorT", {
                "id": sensor["id"],
                "nombre": sensor["nombre"]
            })
            for freq in sensor["frecuencias"]:
                ET.SubElement(sensor_elem, "frecuencia", {
                    "idEstacion": freq["idEstacion"]
                }).text = str(freq["valor"])

    # Formatear XML bonito
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Guardar archivo
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"Archivo de salida guardado en: {ruta_salida}")
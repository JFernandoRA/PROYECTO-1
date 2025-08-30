# procesador.py
from estructuras.lista_simple import ListaSimple


def calcular_patron(estacion_id, sensores):
    patron = []
    for sensor in sensores.recorrer():
        encontrado = False
        for freq in sensor.frecuencias.recorrer():
            if freq["idEstacion"] == estacion_id:
                patron.append(1)
                encontrado = True
                break
        if not encontrado:
            patron.append(0)
    return tuple(patron)


def procesar_campos(campos):
 
    if campos is None or campos.esta_vacia():
        print("No hay datos para procesar. Cargue un archivo primero.")
        return None

    campos_procesados = []

    for campo in campos.recorrer():
        print(f"\n--- PROCESANDO CAMPO: {campo.nombre} ---")
        grupos_suelo = {}
        grupos_cultivo = {}

     
        for estacion in campo.estaciones.recorrer():
            patron = calcular_patron(estacion.id, campo.sensores_suelo)
            if patron not in grupos_suelo:
                grupos_suelo[patron] = ListaSimple()
            grupos_suelo[patron].insertar(estacion)

      
        for estacion in campo.estaciones.recorrer():
            patron = calcular_patron(estacion.id, campo.sensores_cultivo)
            if patron not in grupos_cultivo:
                grupos_cultivo[patron] = ListaSimple()
            grupos_cultivo[patron].insertar(estacion)

        
        print(f"\nMatriz de patrones (Suelo):")
        for estacion in campo.estaciones.recorrer():
            patron = calcular_patron(estacion.id, campo.sensores_suelo)
            print(f"  {estacion.id} ({estacion.nombre}): {list(patron)}")

        print(f"\nMatriz de patrones (Cultivo):")
        for estacion in campo.estaciones.recorrer():
            patron = calcular_patron(estacion.id, campo.sensores_cultivo)
            print(f"  {estacion.id} ({estacion.nombre}): {list(patron)}")

        print(f"\n Estaciones agrupadas por patrón (Suelo):")
        for patron, grupo in grupos_suelo.items():
            nombres = [est.nombre for est in grupo.recorrer()]
            print(f"  Patrón {list(patron)} → {', '.join(nombres)}")

        print(f"\nEstaciones agrupadas por patrón (Cultivo):")
        for patron, grupo in grupos_cultivo.items():
            nombres = [est.nombre for est in grupo.recorrer()]
            print(f"  Patrón {list(patron)} → {', '.join(nombres)}")

        campo_procesado = {
            "id": campo.id,
            "nombre": campo.nombre,
            "estaciones_reducidas": [],
            "sensores_suelo": [],
            "sensores_cultivo": []
        }

        for patron, grupo in grupos_suelo.items():
            estacion_repr = grupo.primero.dato
            nombres_concatenados = ", ".join([est.nombre for est in grupo.recorrer()])
            campo_procesado["estaciones_reducidas"].append({
                "id": estacion_repr.id,
                "nombre": nombres_concatenados
            })

        for sensor in campo.sensores_suelo.recorrer():
            sensor_proc = {
                "id": sensor.id,
                "nombre": sensor.nombre,
                "frecuencias": []
            }
            for patron, grupo in grupos_suelo.items():
                total = 0
                estacion_repr = grupo.primero.dato.id
                for est in grupo.recorrer():
                    for freq in sensor.frecuencias.recorrer():
                        if freq["idEstacion"] == est.id:
                            total += freq["valor"]
                if total > 0:
                    sensor_proc["frecuencias"].append({
                        "idEstacion": estacion_repr,
                        "valor": total
                    })
            campo_procesado["sensores_suelo"].append(sensor_proc)

        for sensor in campo.sensores_cultivo.recorrer():
            sensor_proc = {
                "id": sensor.id,
                "nombre": sensor.nombre,
                "frecuencias": []
            }
            for patron, grupo in grupos_cultivo.items():
                total = 0
                estacion_repr = grupo.primero.dato.id
                for est in grupo.recorrer():
                    for freq in sensor.frecuencias.recorrer():
                        if freq["idEstacion"] == est.id:
                            total += freq["valor"]
                if total > 0:
                    sensor_proc["frecuencias"].append({
                        "idEstacion": estacion_repr,
                        "valor": total
                    })
            campo_procesado["sensores_cultivo"].append(sensor_proc)

        campos_procesados.append(campo_procesado)
        print(f"\nProcesamiento completado para {campo.nombre}")

    return campos_procesados
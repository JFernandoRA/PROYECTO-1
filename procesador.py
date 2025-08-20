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
    return tuple(patron)  # tuple para usar como clave

def procesar_campos(campos):
    if campos is None or campos.esta_vacia():
        print("No hay datos para procesar. Cargue un archivo primero.")
        return

    for campo in campos.recorrer():
        print(f"\n--- PROCESANDO CAMPO: {campo.nombre} ---")

        # Diccionario de agrupación por patrón (usando listas enlazadas)
        grupos_suelo = {}
        grupos_cultivo = {}

        # Agrupar estaciones por patrón (sensores de suelo)
        for estacion in campo.estaciones.recorrer():
            patron = calcular_patron(estacion.id, campo.sensores_suelo)
            if patron not in grupos_suelo:
                grupos_suelo[patron] = ListaSimple()
            grupos_suelo[patron].insertar(estacion)

        # Agrupar estaciones por patrón (sensores de cultivo)
        for estacion in campo.estaciones.recorrer():
            patron = calcular_patron(estacion.id, campo.sensores_cultivo)
            if patron not in grupos_cultivo:
                grupos_cultivo[patron] = ListaSimple()
            grupos_cultivo[patron].insertar(estacion)

        # Mostrar resultados
        print(f"  Estaciones agrupadas por patrón (Suelo):")
        for patron, grupo in grupos_suelo.items():
            nombres = []
            for est in grupo.recorrer():
                nombres.append(est.nombre)
            print(f"    Patrón {list(patron)} → {', '.join(nombres)}")

        print(f"  Estaciones agrupadas por patrón (Cultivo):")
        for patron, grupo in grupos_cultivo.items():
            nombres = []
            for est in grupo.recorrer():
                nombres.append(est.nombre)
            print(f"    Patrón {list(patron)} → {', '.join(nombres)}")

        # Aquí ya tienes los grupos. Puedes sumar frecuencias después
        print(f"Procesamiento completado para {campo.nombre}")
# graficador.py - Adaptado para Proyecto IPC2
from graphviz import Digraph
import os


def generar_matriz_frecuencias(campo, tipo_sensor="suelo", nombre_archivo="matriz_frecuencias"):
    """
    Genera la matriz de frecuencias F[n,s] o F[n,t] según especificación del proyecto.
    - F[n,s]: matriz de frecuencias para n estaciones base y s sensores de suelo
    - F[n,t]: matriz de frecuencias para n estaciones base y t sensores de cultivo
    """
    try:
        # Obtener datos según tipo de sensor
        estaciones = list(campo.estaciones.recorrer())
        if tipo_sensor == "suelo":
            sensores = list(campo.sensores_suelo.recorrer())
            titulo_matriz = f"F[n,s] - MATRIZ DE FRECUENCIAS SUELO"
            simbolo = "s"
        else:
            sensores = list(campo.sensores_cultivo.recorrer())
            titulo_matriz = f"F[n,t] - MATRIZ DE FRECUENCIAS CULTIVO"
            simbolo = "t"
        
        if not estaciones or not sensores:
            print(f"No se encontraron datos suficientes para {tipo_sensor}")
            return

        print(f"Generando {titulo_matriz}")
        print(f"   Estaciones (n): {len(estaciones)} | Sensores ({simbolo}): {len(sensores)}")

        dot = Digraph(comment=titulo_matriz)
        dot.attr(rankdir='TB', size='14,10', dpi='300')

        table = f'''<<table border="2" cellborder="1" cellspacing="0" cellpadding="12" bgcolor="white">
        <tr bgcolor="#4A90E2">
            <td><b><font color="white">Estaciones\\Sensores</font></b></td>'''

        for sensor in sensores:
            table += f'<td><b><font color="white">{sensor.id}</font></b></td>'
        table += '</tr>'

        for i, estacion in enumerate(estaciones):
            bgcolor = "#F0F8FF" if i % 2 == 0 else "#FFFFFF"
            table += f'<tr bgcolor="{bgcolor}"><td><b>{estacion.id}</b></td>'
            
            for sensor in sensores:
                frecuencia_valor = 0
                for freq_dict in sensor.frecuencias.recorrer():
                    if freq_dict["idEstacion"] == estacion.id:
                        frecuencia_valor = freq_dict["valor"]
                        break
                
                if frecuencia_valor == 0:
                    cell_color = "#FFFFFF"
                    text_color = "#999999"
                elif frecuencia_valor < 1000:
                    cell_color = "#E8F5E8"
                    text_color = "#2E7D2E"
                elif frecuencia_valor < 5000:
                    cell_color = "#FFF3CD"
                    text_color = "#856404"
                else:
                    cell_color = "#F8D7DA"
                    text_color = "#721C24"
                
                table += f'<td bgcolor="{cell_color}"><font color="{text_color}"><b>{frecuencia_valor}</b></font></td>'
            table += '</tr>'

        table += '</table>>'

        dot.node('titulo', label=f'{titulo_matriz}\\nCampo: {campo.nombre}', 
                 shape='box', style='filled', fillcolor='#4A90E2', fontcolor='white', fontsize='16')
        dot.node('matriz', label=table, shape='plaintext')
        dot.node('info', label=f'Dimensión: {len(estaciones)} x {len(sensores)}', 
                 shape='box', style='filled', fillcolor='lightgray', fontsize='12')
        
        dot.edge('titulo', 'matriz', style='invis')
        dot.edge('matriz', 'info', style='invis')
        
        nombre_completo = f"{nombre_archivo}_{tipo_sensor}"
        dot.render(nombre_completo, format='png', cleanup=True, view=True)
        print(f"Matriz F[n,{simbolo}] guardada como '{nombre_completo}.png'")
        
    except Exception as e:
        print(f"Error generando matriz de frecuencias: {e}")
        import traceback
        traceback.print_exc()


def generar_matriz_patrones(campo, tipo_sensor="suelo", nombre_archivo="matriz_patrones"):
    """
    Genera la matriz de patrones Fp[n,s] o Fp[n,t] según especificación del proyecto.
    - Fp[n,s]: matriz de patrones para sensores de suelo (1 si hay frecuencia, 0 si no)
    - Fp[n,t]: matriz de patrones para sensores de cultivo (1 si hay frecuencia, 0 si no)
    """
    try:
        estaciones = list(campo.estaciones.recorrer())
        if tipo_sensor == "suelo":
            sensores = list(campo.sensores_suelo.recorrer())
            titulo_matriz = f"Fp[n,s] - MATRIZ DE PATRONES SUELO"
            simbolo = "s"
        else:
            sensores = list(campo.sensores_cultivo.recorrer())
            titulo_matriz = f"Fp[n,t] - MATRIZ DE PATRONES CULTIVO"
            simbolo = "t"

        if not estaciones or not sensores:
            print(f"No se encontraron datos suficientes para {tipo_sensor}")
            return

        print(f"Generando {titulo_matriz}")
        print(f"   Estaciones (n): {len(estaciones)} | Sensores ({simbolo}): {len(sensores)}")

        dot = Digraph(comment=titulo_matriz)
        dot.attr(rankdir='TB', size='14,10', dpi='300')

        table = f'''<<table border="2" cellborder="1" cellspacing="0" cellpadding="12" bgcolor="white">
        <tr bgcolor="#28A745">
            <td><b><font color="white">Estaciones\\Sensores</font></b></td>'''

        for sensor in sensores:
            table += f'<td><b><font color="white">{sensor.id}</font></b></td>'
        table += '</tr>'

        patrones_por_estacion = {}

        for i, estacion in enumerate(estaciones):
            bgcolor = "#F0FFF0" if i % 2 == 0 else "#FFFFFF"
            table += f'<tr bgcolor="{bgcolor}"><td><b>{estacion.id}</b></td>'
            
            patron = []  
            
            for sensor in sensores:
                tiene_frecuencia = False
                for freq_dict in sensor.frecuencias.recorrer():
                    if freq_dict["idEstacion"] == estacion.id and freq_dict["valor"] > 0:
                        tiene_frecuencia = True
                        break
                
                valor_patron = 1 if tiene_frecuencia else 0
                patron.append(valor_patron)
                
                if valor_patron == 1:
                    cell_color = "#28A745"
                    text_color = "white"
                else:
                    cell_color = "#FFFFFF"
                    text_color = "#999999"
                
                table += f'<td bgcolor="{cell_color}"><font color="{text_color}"><b>{valor_patron}</b></font></td>'
            
            patrones_por_estacion[estacion.id] = tuple(patron)
            table += '</tr>'

        table += '</table>>'

        patrones_unicos = {}
        for est_id, patron in patrones_por_estacion.items():
            if patron not in patrones_unicos:
                patrones_unicos[patron] = []
            patrones_unicos[patron].append(est_id)

        info_agrupamiento = f"Patrones únicos encontrados: {len(patrones_unicos)}\\n"
        for i, (patron, estaciones_grupo) in enumerate(patrones_unicos.items(), 1):
            info_agrupamiento += f"Grupo {i}: {list(patron)} → {', '.join(estaciones_grupo)}\\n"

        dot.node('titulo', label=f'{titulo_matriz}\\nCampo: {campo.nombre}', 
                 shape='box', style='filled', fillcolor='#28A745', fontcolor='white', fontsize='16')
        dot.node('matriz', label=table, shape='plaintext')
        dot.node('agrupamiento', label=info_agrupamiento.strip(), 
                 shape='box', style='filled', fillcolor='#E8F5E8', fontsize='10', fontname='monospace')
        
        dot.edge('titulo', 'matriz', style='invis')
        dot.edge('matriz', 'agrupamiento', style='invis')
        
        nombre_completo = f"{nombre_archivo}_{tipo_sensor}"
        dot.render(nombre_completo, format='png', cleanup=True, view=True)
        print(f"Matriz Fp[n,{simbolo}] guardada como '{nombre_completo}.png'")
        print(f"Se identificaron {len(patrones_unicos)} patrones únicos para optimización")
        
    except Exception as e:
        print(f"Error generando matriz de patrones: {e}")
        import traceback
        traceback.print_exc()


def generar_matriz_reducida(campo_procesado, tipo_sensor="suelo", nombre_archivo="matriz_reducida"):
    """
    Genera la matriz reducida Fr[n,s] o Fr[n,t] según especificación del proyecto.
    - Fr[n,s]: matriz reducida para sensores de suelo después del agrupamiento
    - Fr[n,t]: matriz reducida para sensores de cultivo después del agrupamiento
    """
    try:
        estaciones_reducidas = campo_procesado.get("estaciones_reducidas", [])
        if tipo_sensor == "suelo":
            sensores = campo_procesado.get("sensores_suelo", [])
            titulo_matriz = f"Fr[n,s] - MATRIZ REDUCIDA SUELO"
            simbolo = "s"
        else:
            sensores = campo_procesado.get("sensores_cultivo", [])
            titulo_matriz = f"Fr[n,t] - MATRIZ REDUCIDA CULTIVO"
            simbolo = "t"

        if not estaciones_reducidas or not sensores:
            print(f"No se encontraron datos procesados para {tipo_sensor}")
            return

        print(f"Generando {titulo_matriz}")
        print(f"   Estaciones reducidas: {len(estaciones_reducidas)} | Sensores ({simbolo}): {len(sensores)}")

        dot = Digraph(comment=titulo_matriz)
        dot.attr(rankdir='TB', size='14,10', dpi='300')

        table = f'''<<table border="2" cellborder="1" cellspacing="0" cellpadding="12" bgcolor="white">
        <tr bgcolor="#FFC107">
            <td><b><font color="black">Estaciones\\Sensores</font></b></td>'''

        for sensor in sensores:
            table += f'<td><b><font color="black">{sensor["id"]}</font></b></td>'
        table += '</tr>'

        for i, estacion_red in enumerate(estaciones_reducidas):
            bgcolor = "#FFFBF0" if i % 2 == 0 else "#FFFFFF"
            nombre_completo = estacion_red["nombre"]
            table += f'<tr bgcolor="{bgcolor}"><td><b>{estacion_red["id"]}</b><br/><font point-size="10">({nombre_completo})</font></td>'
            
            for sensor in sensores:
                total_frecuencia = 0
                for freq in sensor.get("frecuencias", []):
                    if freq["idEstacion"] == estacion_red["id"]:
                        total_frecuencia += freq["valor"]
                
                if total_frecuencia == 0:
                    cell_color = "#FFFFFF"
                    text_color = "#999999"
                elif total_frecuencia < 2000:
                    cell_color = "#D4EDDA"
                    text_color = "#155724"
                elif total_frecuencia < 8000:
                    cell_color = "#FFF3CD"
                    text_color = "#856404"
                else:
                    cell_color = "#F8D7DA"
                    text_color = "#721C24"
                
                table += f'<td bgcolor="{cell_color}"><font color="{text_color}"><b>{total_frecuencia}</b></font></td>'
            table += '</tr>'

        table += '</table>>'

        campo_original = campo_procesado.get("nombre", "Desconocido")
        
        dot.node('titulo', label=f'{titulo_matriz}\\nCampo: {campo_original}', 
                 shape='box', style='filled', fillcolor='#FFC107', fontcolor='black', fontsize='16')
        dot.node('matriz', label=table, shape='plaintext')
        dot.node('optimizacion', 
                 label=f'OPTIMIZACIÓN LOGRADA\\nEstaciones reducidas: {len(estaciones_reducidas)}\\n(Agrupamiento por patrones idénticos)', 
                 shape='box', style='filled', fillcolor='#D4EDDA', fontcolor='#155724', fontsize='12')
        
        dot.edge('titulo', 'matriz', style='invis')
        dot.edge('matriz', 'optimizacion', style='invis')
        
        nombre_completo = f"{nombre_archivo}_{tipo_sensor}"
        dot.render(nombre_completo, format='png', cleanup=True, view=True)
        print(f"Matriz Fr[n,{simbolo}] guardada como '{nombre_completo}.png'")
        print(f"Optimización: Se redujo el número de estaciones base requeridas")
        
    except Exception as e:
        print(f"Error generando matriz reducida: {e}")
        import traceback
        traceback.print_exc()


def menu_generar_graficas_proyecto(campo, campos_procesados=None):
    """
    Menú específico para el proyecto IPC2 - Generar gráficas según especificación
    """
    print(f"\n=== GENERAR GRÁFICA - PROYECTO IPC2 ===")
    print(f"Campo seleccionado: {campo.nombre} (ID: {campo.id})")
    
    estaciones = list(campo.estaciones.recorrer())
    sensores_suelo = list(campo.sensores_suelo.recorrer())
    sensores_cultivo = list(campo.sensores_cultivo.recorrer())
    
    print(f"\nInformación del campo:")
    print(f"   • Estaciones base (n): {len(estaciones)}")
    print(f"   • Sensores de suelo (s): {len(sensores_suelo)}")
    print(f"   • Sensores de cultivo (t): {len(sensores_cultivo)}")
    
    print(f"\n¿Qué tipo de sensores desea graficar?")
    if sensores_suelo:
        print("1. Sensores de Suelo (s)")
    else:
        print("1. Sensores de Suelo (s) - [NO DISPONIBLE]")
    
    if sensores_cultivo:
        print("2. Sensores de Cultivo (t)")
    else:
        print("2. Sensores de Cultivo (t) - [NO DISPONIBLE]")
    
    print("0. Cancelar")
    
    try:
        opcion_sensor = input("\nSeleccione una opción: ").strip()
        
        if opcion_sensor == "0":
            print("Operación cancelada.")
            return
        elif opcion_sensor == "1" and sensores_suelo:
            tipo_sensor = "suelo"
            simbolo = "s"
        elif opcion_sensor == "2" and sensores_cultivo:
            tipo_sensor = "cultivo"
            simbolo = "t"
        else:
            print("Opción no válida o no disponible.")
            return
            
        print(f"Seleccionado: Sensores de {tipo_sensor} ({simbolo})")
        
    except Exception as e:
        print(f"Error seleccionando tipo de sensor: {e}")
        return
    
    print(f"\n¿Qué matriz desea generar?")
    print(f"1. Matriz de Frecuencias - F[n,{simbolo}]")
    print(f"2. Matriz de Patrones - Fp[n,{simbolo}]")
    print(f"3. Matriz Reducida - Fr[n,{simbolo}]")
    print("0. Cancelar")
    
    try:
        opcion_matriz = input("\nSeleccione una opción: ").strip()
        
        if opcion_matriz == "0":
            print("Operación cancelada.")
            return
        elif opcion_matriz == "1":
            print(f"\nGenerando matriz de frecuencias F[n,{simbolo}]...")
            generar_matriz_frecuencias(campo, tipo_sensor, "matriz_frecuencias")
        elif opcion_matriz == "2":
            print(f"\nGenerando matriz de patrones Fp[n,{simbolo}]...")
            generar_matriz_patrones(campo, tipo_sensor, "matriz_patrones")
        elif opcion_matriz == "3":
            if not campos_procesados:
                print("Para generar la matriz reducida necesita procesar los datos primero (Opción 2 del menú).")
                return
            
            campo_proc = None
            for cp in campos_procesados:
                if cp["id"] == campo.id:
                    campo_proc = cp
                    break
            
            if not campo_proc:
                print("No se encontraron datos procesados para este campo.")
                return
                
            print(f"\nGenerando matriz reducida Fr[n,{simbolo}]...")
            generar_matriz_reducida(campo_proc, tipo_sensor, "matriz_reducida")
        else:
            print("Opción no válida.")
            return
            
        print(f"\nGráfica generada exitosamente!")
        print("La imagen se ha guardado y abierto automáticamente")
            
    except Exception as e:
        print(f"Error generando matriz: {e}")
        import traceback
        traceback.print_exc()

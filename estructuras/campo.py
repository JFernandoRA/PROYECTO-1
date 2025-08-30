from .lista_simple import ListaSimple
from .Frecuencia import Frecuencia

class Estacion:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre


class SensorS:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaSimple()


class SensorT:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaSimple()


class Matriz:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = ListaSimple()  # Lista de filas

        for i in range(num_filas):
            fila = ListaSimple()
            for j in range(num_columnas):
                frecuencia = Frecuencia("", "0")
                fila.insertar(frecuencia)
            self.matriz.insertar(fila)

    def establecer(self, num_fila, num_columna, frecuencia):
        fila = self.obtener_fila(num_fila)
        if fila:
            nodo = fila.primero
            for _ in range(num_columna):
                if nodo:
                    nodo = nodo.siguiente
            if nodo:
                nodo.dato = frecuencia

    def obtener_fila(self, num_fila):
        actual = self.matriz.primero
        for _ in range(num_fila):
            if actual:
                actual = actual.siguiente
        return actual.dato if actual else None

    def obtener(self, num_fila, num_columna):
        fila = self.obtener_fila(num_fila)
        if fila:
            actual = fila.primero
            for _ in range(num_columna):
                if actual:
                    actual = actual.siguiente
            return actual.dato if actual else None
        return None

    def generar_graphviz_tabla(self, titulo, headers_fila, headers_columna, nombre_archivo="matriz"):
        try:
            from graphviz import Digraph
        except ImportError:
            print("Instala graphviz: pip install graphviz")
            return

        def esc(s):
            return str(s).replace('"', '\\"')

        # Encabezado de columnas
        th_cols = '<td border="1" bgcolor="#f5f7fa"></td>'
        for j in range(self.num_columnas):
            sensor = headers_columna.obtener(j)
            th_cols += f'<td border="1" bgcolor="#f5f7fa"><b>{esc(sensor.id)}</b></td>'

        # Filas
        filas_html = ""
        for i in range(self.num_filas):
            estacion = headers_fila.obtener(i)
            filas_html += f'<tr><td border="1" bgcolor="#f5f7fa"><b>{esc(estacion.id)}</b></td>'
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                valor = esc(frecuencia.valor)
                bg = "#ffffff" if valor == "0" else "#ffd6d6"
                filas_html += f'<td border="1" bgcolor="{bg}">{valor}</td>'
            filas_html += '</tr>'

        tabla = f'''
        <<table BORDER="0" CELLBORDER="0" CELLSPACING="0">
          <tr><td>
            <table BORDER="1" CELLBORDER="1" CELLSPACING="0">
              <tr>{th_cols}</tr>
              {filas_html}
            </table>
          </td></tr>
        </table>>
        '''

        dot = Digraph(comment=titulo)
        dot.attr(rankdir='LR')
        dot.node('matriz', label=tabla, shape='plain')
        dot.node('titulo', label=titulo, shape='box', style='filled', fillcolor='lightgreen')
        dot.edge('titulo', 'matriz', style='invis')

        try:
            dot.render(nombre_archivo, format='png', cleanup=True, view=True)
            print(f"✅ Gráfico generado: {nombre_archivo}.png")
        except Exception as e:
            print(f"❌ Error: {e}")
            dot.save(f"{nombre_archivo}.dot")
# estructuras/campo.py (dentro de la clase Campo)
class Campo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = ListaSimple()
        self.sensores_suelo = ListaSimple()
        self.sensores_cultivo = ListaSimple()

    def crear_matriz_frecuencias(self, tipo="suelo"):
        sensores = self.sensores_suelo if tipo == "suelo" else self.sensores_cultivo
        num_filas = len(self.estaciones)
        num_columnas = len(sensores)
        matriz = Matriz(num_filas, num_columnas)

        # Llenar matriz
        fila_idx = 0
        for estacion in self.estaciones.recorrer():
            col_idx = 0
            for sensor in sensores.recorrer():
                valor = "0"
                for freq in sensor.frecuencias.recorrer():
                    if freq["idEstacion"] == estacion.id:
                        valor = str(freq["valor"])
                        break
                frec = Frecuencia(estacion.id, valor)
                matriz.establecer(fila_idx, col_idx, frec)
                col_idx += 1
            fila_idx += 1

        return matriz
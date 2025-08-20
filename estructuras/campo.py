from .lista_simple import ListaSimple

class Estacion:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class SensorS:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaSimple()  # Lista de {idEstacion, valor}

class SensorT:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.frecuencias = ListaSimple()

class Campo:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.estaciones = ListaSimple()
        self.sensores_suelo = ListaSimple()
        self.sensores_cultivo = ListaSimple()
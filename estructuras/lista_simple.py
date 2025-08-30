from .nodo import Nodo

class ListaSimple:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._tamano = 0

    def insertar(self, dato):
        nuevo = Nodo(dato)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self._tamano += 1

    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self):
        return self._tamano

    def esta_vacia(self):
        return self.primero is None
    
    def obtener(self, indice):
        actual = self.primero
        for _ in range(indice):
            if actual:
                actual = actual.siguiente
            else:
                return None
        return actual.dato if actual else None
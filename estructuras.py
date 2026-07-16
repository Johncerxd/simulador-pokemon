class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if not self.cabeza: self.cabeza = nuevo
        else:
            temp = self.cabeza
            while temp.siguiente: temp = temp.siguiente
            temp.siguiente = nuevo
            
    def obtener_todos(self):
        elementos = []
        temp = self.cabeza
        while temp:
            elementos.append(temp.dato)
            temp = temp.siguiente
        return elementos

class Cola:
    def __init__(self):
        self.elementos = []
    
    def encolar(self, dato): self.elementos.append(dato)
    
    def desencolar(self): return self.elementos.pop(0) if self.elementos else None
    
    def esta_vacia(self): return len(self.elementos) == 0
    
    def obtener_cantidad(self): return len(self.elementos)
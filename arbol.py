class Nodo:
    def __init__(self, datos, padre=None, hijos=None):
        self.datos = datos  # Almacena el estado
        self.padre = padre  # Almacena el nodo padre
        self.costo = None
        self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos if hijos is not None else []
        for h in self.hijos:
            h.set_padre(self)  # Asegura que cada hijo tenga su padre

    def get_hijos(self):
        return self.hijos

    def get_datos(self):  
        return self.datos

    def set_datos(self, datos):
        self.datos = datos

    def get_padre(self):  
        return self.padre

    def set_padre(self, padre):  # ✅ Método agregado
        self.padre = padre

    def igual(self, nodo):
        return self.get_datos() == nodo.get_datos()

    def en_lista(self, lista_nodos):
        return any(self.igual(n) for n in lista_nodos)

    def __str__(self):
        return str(self.get_datos())

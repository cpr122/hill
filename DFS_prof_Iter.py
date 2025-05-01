from flask import Flask, request, jsonify, render_template

class Nodo:
    def __init__(self, datos, padre=None, hijos=None):
        self.datos = datos  
        self.padre = padre  
        self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos if hijos is not None else []
        for h in self.hijos:
            h.set_padre(self)  

    def get_hijos(self):
        return self.hijos

    def get_datos(self):  
        return self.datos

    def set_padre(self, padre):  
        self.padre = padre

    def get_padre(self):  
        return self.padre

def DFS_prof_iter(nodo, solucion, conexiones):
    for limite in range(0, 100):
        visitados = []
        sol = buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite, conexiones)
        if sol is not None:
            return sol
    return None

def buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite, conexiones):
    if limite > 0:
        visitados.append(nodo.get_datos())
        if nodo.get_datos() == solucion:
            return nodo
        else:
            lista_hijos = []
            for un_hijo in conexiones.get(nodo.get_datos(), []):
                hijo = Nodo(un_hijo)
                if hijo.get_datos() not in visitados:
                    hijo.set_padre(nodo)  
                    lista_hijos.append(hijo)
            nodo.set_hijos(lista_hijos)

            for nodo_hijo in nodo.get_hijos():
                sol = buscar_solucion_DFS_Rec(nodo_hijo, solucion, visitados, limite - 1, conexiones)
                if sol is not None:
                    return sol
    return None

app = Flask(__name__)

# Diccionario de conexiones (mapa de rutas)
conexiones = {
    'EDO.MEX': {'QRO', 'SLP', 'SONORA'},
    'PUEBLA': {'HIDALGO', 'SLP'},
    'CDMX': {'MICHOACAN'},
    'MICHOACAN': {'SONORA'},
    'SLP': {'QRO', 'PUEBLA', 'EDO.MEX', 'SONORA', 'GUADALAJARA'},
    'QRO': {'EDO.MEX', 'SLP'},
    'HIDALGO': {'PUEBLA', 'GUADALAJARA', 'SONORA'},
    'MONTERREY': {'HIDALGO', 'SLP'},
    'SONORA': {'MONTERREY', 'HIDALGO', 'SLP', 'EDO.MEX', 'MICHOACAN'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar_ruta', methods=['GET'])
def buscar_ruta():
    estado_inicial = request.args.get('inicio')
    solucion = request.args.get('destino')

    if estado_inicial not in conexiones or solucion not in conexiones:
        return jsonify({'error': 'Uno o ambos estados no están en nuestra info'}), 400

    nodo_inicial = Nodo(estado_inicial)
    nodo = DFS_prof_iter(nodo_inicial, solucion, conexiones)

    if nodo is not None:
        resultado = []
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
        return jsonify({'ruta': resultado})
    else:
        return jsonify({'mensaje': 'Solución no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)




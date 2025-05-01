from flask import Flask, render_template
import math
import random
import folium
import os
import uuid
import glob

app = Flask(__name__)

# Coordenadas de las ciudades

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754, -103.346253),
    'Monterrey': (25.691611, -100.321838),
    'QuintanaRoo': (21.163111, -86.802315),
    'Michohacan': (19.701400, -101.208296),
    'Aguascalientes': (21.876410, -102.264386),
    'CDMX': (19.432713, -99.133183),
    'QRO': (20.597194, -100.386670)
}

# Iconos para cada ciudad
iconos = {
    'Jiloyork': 'sun',
    'Toluca': 'city',
    'Atlacomulco': 'mountain',
    'Guadalajara': 'city',
    'Monterrey': 'city',
    'QuintanaRoo': 'umbrella-beach',
    'Michohacan': 'tree',
    'Aguascalientes': 'cloud',
    'CDMX': 'building',
    'QRO': 'city'
}

# Función para calcular la distancia entre dos puntos
def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# Evaluar la ruta (sumar las distancias)
def evalua_ruta(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(coord[ruta[i]], coord[ruta[i + 1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # Regresar al inicio (esto lo eliminamos luego)
    return total

# Algoritmo Hill Climbing para encontrar la mejor ruta
def i_hill_climbing():
    ciudades = list(coord.keys())
    mejor_ruta = ciudades[:]
    random.shuffle(mejor_ruta)
    mejor_dist = evalua_ruta(mejor_ruta)

    max_iteraciones = 10
    for _ in range(max_iteraciones):
        ruta = ciudades[:]
        random.shuffle(ruta)
        mejora = True

        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta)
            for i in range(len(ruta)):
                for j in range(i + 1, len(ruta)):
                    ruta_tmp = ruta[:]
                    ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                    dist = evalua_ruta(ruta_tmp)
                    if dist < dist_actual:
                        ruta = ruta_tmp[:]
                        mejora = True
                        break
                if mejora:
                    break

        if evalua_ruta(ruta) < mejor_dist:
            mejor_ruta = ruta[:]
            mejor_dist = evalua_ruta(ruta)

    return mejor_ruta, mejor_dist

# Función para crear el mapa usando Folium
def crear_mapa(ruta):
    puntos = [coord[ciudad] for ciudad in ruta]
    mapa = folium.Map(location=puntos[0], zoom_start=5)

    # Agregar marcadores numerados con iconos
    for i, ciudad in enumerate(ruta):
        folium.Marker(
            location=coord[ciudad],
            tooltip=f"{i+1}. {ciudad}",
            icon=folium.Icon(color="blue", icon=iconos[ciudad])
        ).add_to(mapa)

    # Trazo de la ruta (solo hasta el último punto sin regresar)
    camino = [coord[ciudad] for ciudad in ruta]  # No incluir el primer punto de regreso
    folium.PolyLine(locations=camino, color="blue", weight=3, opacity=0.8).add_to(mapa)

    # Guardar el archivo HTML del mapa
    mapa_id = uuid.uuid4().hex
    ruta_archivo = f'static/mapa_{mapa_id}.html'
    mapa.save(ruta_archivo)
    return ruta_archivo

@app.route('/')
def index():
    # Eliminar mapas anteriores (opcional)
    for archivo in glob.glob('static/mapa_*.html'):
        os.remove(archivo)

    # Obtener la mejor ruta y distancia total
    ruta, distancia_total = i_hill_climbing()

    # Crear el mapa de la ruta
    mapa_html = crear_mapa(ruta)

    # Renderizar la página con la ruta y el mapa
    return render_template(
        'index.html',
        ruta=ruta,
        distancia=round(distancia_total, 4),
        mapa=mapa_html,
        iconos=iconos
    )

if __name__ == '__main__':
    # Crear carpeta estática si no existe
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)

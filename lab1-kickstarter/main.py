from flask import Flask, jsonify, request
import random

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles
    for pelicula in peliculas:
        if pelicula['id'] == id:
            return jsonify(pelicula)
    return jsonify({'mensaje': 'Pelicula no encontrada'}), 404



def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    # Lógica para buscar la película por su ID y actualizar sus detalles
    nueva_peli = {
        'titulo' : request.json['titulo'],
        'genero' : request.json['genero']
    }
    for pelicula_actualizada in peliculas:
        if pelicula_actualizada['id'] == id:
            pelicula_actualizada['titulo'] = nueva_peli['titulo']
            pelicula_actualizada['genero'] = nueva_peli['genero']
            print(peliculas)
            return jsonify(pelicula_actualizada), 200
    return jsonify({'mensaje': 'Pelicula no encontrada'}), 404


def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla
    for x in range(len(peliculas)):
        if peliculas[x]['id'] == id:
            peliculas.pop(x)
            return jsonify({'mensaje': 'Película eliminada correctamente'})
    return jsonify({'mensaje': 'Pelicula no encontrada'}), 404


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1
    
def lista_por_genero(genero):
    # Esta funcion filtra las peliculas por genero
    ## Si la url contiene espacios damos error
    genero_ok = genero.replace('-', ' ') # Reemplazo los guiones por espacios
    print(" Cambia :" , genero_ok)
    pelis_por_genero = [] 
    for pelicula in peliculas:
        # Comparo el genero de la pelicula con el genero que me pasan en el request
        if pelicula['genero'].strip().lower() == genero_ok.strip().lower(): 
            pelis_por_genero.append(pelicula)
    if len(pelis_por_genero) > 0:
        return jsonify(pelis_por_genero), 201
    else:
        return jsonify({'mensaje': 'No hay peliculas con ese genero'}), 404

def filtro_por_titulo(palabra):
    # Esta funcion filtra las peliculas por palabra en el titulo
    lista_peli = [] 
    for pelicula in peliculas:
        if palabra.lower() in pelicula['titulo'].lower(): #lo hacemos indiferente a minusculas y mayusculas 
            lista_peli.append(pelicula)
    if lista_peli:    
        return jsonify(lista_peli), 201
    else:
        return jsonify({'mensaje': 'No existe pelicula con esa palabra incluida'}), 404

def pelicula_random():
    # Esta funcion recomienda una pelicula random
    todas_peliculas = obtener_peliculas()  # Asume que obtener_peliculas() devuelve la lista de peliculas
    pelis_ok = todas_peliculas.get_json()
    pelicula = random.choice(pelis_ok)
    print("Su pelicula es: ", pelicula)
    return jsonify(pelicula), 200

def pelicula_random_genero(genero):
    # Esta funcion recomienda una pelicula random segun el genero dado
    # Primero filtro las peliculas por genero
    respuesta, _ = lista_por_genero(genero) # Desempaqueto la respuesta dada por la func
    # La linea de abajo da error 
    pelis_ok = respuesta.get_json()
    print("Peliculas filtradas correctamente")
    print("Peliculas por genero: ", pelis_ok)
    # Si hay peliculas con ese genero, devuelvo una random
    pelicula = random.choice(pelis_ok)
    print("Su pelicula es: ", pelicula)
    return jsonify(pelicula), 201

app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
# Agregar nuevas rutas para los endpoints faltantes
app.add_url_rule('/peliculas/genero/<string:genero>', 'lista_por_genero', lista_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/titulo/<string:palabra>', 'filtro_por_titulo', filtro_por_titulo, methods=['GET'])
app.add_url_rule('/peliculas/random', 'pelicula_random', pelicula_random, methods=['GET'])
app.add_url_rule('/peliculas/random/<string:genero>', 'pelicula_random_genero', pelicula_random_genero, methods=['GET'])

if __name__ == '__main__':
    app.run()

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
    return jsonify(nueva_pelicula), 200


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
    pelis_por_genero = [] 
    for pelicula in peliculas:
        # Comparo el genero de la pelicula con el genero que me pasan en el request
        if pelicula['genero'] == request.json['genero']: 
            pelis_por_genero.append(pelicula)
        return jsonify(pelis_por_genero), 201
    return jsonify({'mensaje': 'No hay peliculas con ese genero'}), 404

def filtro_por_titulo(palabra):
    # Esta funcion filtra las peliculas por palabra en el titulo
    lista_peli = [] 
    for pelicula in peliculas:
        if palabra.lower() in pelicula['titulo'].lower(): #lo hacemos indiferente a minusculas y mayusculas 
            lista_peli.append(pelicula)
            return jsonify(lista_peli), 200
    return jsonify({'mensaje': 'No existe pelicula con esa palabra incluida'}), 404

def pelicula_random(peliculas):
    # Esta funcion recomienda una pelicula random
    pelicula = random.choice(peliculas)
    return jsonify(pelicula)

def pelicula_random_genero(genero):
    # Esta funcion recomienta una pelicula random segun el genero dado
    # Primero filtro las peliculas por genero
    pelis_por_genero = lista_por_genero(genero) 
    # Si hay peliculas con ese genero, devuelvo una random
    if len(pelis_por_genero) > 0:
        return jsonify(pelicula_random(pelis_por_genero)), 200
    return jsonify({'mensaje': 'No hay peliculas con ese genero'}), 404

app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])

if __name__ == '__main__':
    app.run()

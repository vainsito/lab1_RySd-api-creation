import random
from unidecode import unidecode
from flask import Flask, jsonify, request
from proximo_feriado import NextHoliday


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
            return jsonify(pelicula), 200
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
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
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
            return jsonify({'mensaje': 'Película eliminada correctamente'}), 200
    return jsonify({'mensaje': 'Pelicula no encontrada'}), 404


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


# Funcion Auxiliar para acomodar las palabras
def pretty_word(palabra):
    # Esta funcion parsea las palabras, eliminando espacios, guiones y mayusculas
    # Reemplazo los guiones por espacios
    palabra_ok = palabra.replace('-', ' ')
    palabra_ok = palabra_ok.strip().lower()  # Elimino espacios y paso a minusculas
    palabra_ok = unidecode(palabra_ok)  # Elimino tildes
    return palabra_ok


def lista_por_genero(genero):
    # Esta funcion filtra las peliculas por genero
    pelis_por_genero = []
    for pelicula in peliculas:
        # Comparo el genero de la pelicula con el genero que me pasan en el request
        if pretty_word(pelicula['genero']) == pretty_word(genero):
            pelis_por_genero.append(pelicula)
    if len(pelis_por_genero) > 0:
        return jsonify(pelis_por_genero), 200
    else:
        return jsonify({'mensaje': 'No hay peliculas con ese genero'}), 404


def filtro_por_titulo(palabra):
    # Esta funcion filtra las peliculas por palabra en el titulo
    lista_peli = []
    for pelicula in peliculas:
        if pretty_word(palabra) in pretty_word(pelicula['titulo']):
            lista_peli.append(pelicula)
    if len(lista_peli) > 0:
        return jsonify(lista_peli), 200
    else:
        return jsonify({'mensaje': 'No existe pelicula con esa palabra incluida'}), 404


def pelicula_random():
    # Esta funcion recomienda una pelicula random
    todas_peliculas = obtener_peliculas().get_json()  # Obtengo todas las peliculas
    if len(todas_peliculas) == 0:
        return jsonify({'mensaje': 'No hay peliculas disponibles'}), 404
    pelicula = random.choice(todas_peliculas)
    print("Su pelicula es: ", pelicula)
    return jsonify(pelicula), 200


def pelicula_random_genero(genero):
    # Esta funcion recomienda una pelicula random segun el genero dado
    # Primero filtro las peliculas por genero
    # Desempaqueto la respuesta dada por la func
    respuesta, _ = lista_por_genero(genero)
    pelis_ok = respuesta.get_json()
    if len(pelis_ok) == 0:
        return jsonify({'mensaje': 'No hay peliculas disponibles'}), 404
    print("Peliculas filtradas correctamente")
    print("Peliculas por genero: ", pelis_ok)
    # Si hay peliculas con ese genero, devuelvo una random
    pelicula = random.choice(pelis_ok)
    print("Su pelicula es: ", pelicula)
    return jsonify(pelicula), 200


def peli_random_feriado(genero):
    # Esta funcion recomienda una pelicula random segun el genero dado
    # Primero filtro las peliculas por genero
    feriado_obj = NextHoliday()
    feriados = feriado_obj.obtener_feriados()
    feriado_obj.set_next(feriados)
    print("Proximo feriado: ", feriado_obj.holiday)
    # Ahora uso pelicula random genero
    respuesta, _ = pelicula_random_genero(genero)
    resultado = {
        'pelicula': respuesta.get_json(),
        'proximo_feriado': feriado_obj.holiday
    }
    return jsonify(resultado), 200


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
# Agregar nuevas rutas para los endpoints faltantes
app.add_url_rule('/peliculas/genero/<string:genero>', 'lista_por_genero', lista_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/titulo/<string:palabra>', 'filtro_por_titulo', filtro_por_titulo, methods=['GET'])
app.add_url_rule('/peliculas/random/<string:genero>', 'pelicula_random_genero', pelicula_random_genero, methods =['GET'])
app.add_url_rule('/peliculas/random', 'pelicula_random', pelicula_random, methods=['GET'])
app.add_url_rule('/peliculas/feriado/<string:genero>', 'peli_random_feriado', peli_random_feriado, methods=['GET'])


if __name__ == '__main__':
    app.run()


from flask import Flask, jsonify, request

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


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])

if __name__ == '__main__':
    app.run()

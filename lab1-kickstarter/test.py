import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
    
# Filtrar películas por género
genero = 'Drama'  # Género por el que filtrar
response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
if response.status_code == 200:
    peliculas_filtradas = response.json()
    print(f"Películas de género '{genero}' son:")
    for pelicula in peliculas_filtradas:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener las películas por género.")
    
# Filtrar peliculas por palabra clave
palabra = 'El'
response = requests.get(f'http://localhost:5000/peliculas/titulo/{palabra}')
if response.status_code == 200:
    peliculas_filtradas = response.json()
    print(f"Películas con la palabra clave '{palabra}' son:")
    for pelicula in peliculas_filtradas:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener las películas por palabra clave.")

# Pelicula random
response = requests.get('http://localhost:5000/peliculas/random')
if response.status_code == 200:
    pelicula_random = response.json()
    print("Película aleatoria:")
    print(f"ID: {pelicula_random['id']}, Título: {pelicula_random['titulo']}, Género: {pelicula_random['genero']}")
else:
    print("Error al obtener la película aleatoria.")
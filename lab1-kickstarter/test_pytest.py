import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', status_code = 200, json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})
        m.get('http://localhost:5000/peliculas/50', status_code=404, json={'mensaje': 'Id no encontrado'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})
        m.put('http://localhost:5000/peliculas/50', status_code=404, json={'mensaje': 'Id no encontrado'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)
        m.delete('http://localhost:5000/peliculas/50', status_code=404, json={'mensaje': 'Id no encontrado'})

        # Simulamos la respuesta para obtener peliculas por su genero
        m.get('http://localhost:5000/peliculas/genero/Drama', status_code=200)
        m.get('http://localhost:5000/peliculas/genero/NoExiste', status_code=404, json={'mensaje': 'Género no encontrado'})

        # Simulamos la respuesta para obtener peliculas por una palabra clave
        m.get('http://localhost:5000/peliculas/titulo/Indi', status_code=200)
        m.get('http://localhost:5000/peliculas/titulo/NoExiste', status_code=404, json={'mensaje': 'Pelicula no encontrado'})

        # Simulamos la respuesta para obtener una pelicula aleatoria
        m.get('http://localhost:5000/peliculas/random', status_code=200)

        # Simulamos la respuesta para obtener una pelicula aleatoria de un genero particular
        m.get('http://localhost:5000/peliculas/random/Drama', status_code=200)
        m.get('http://localhost:5000/peliculas/random/NoExiste', status_code=404, json={'mensaje': 'Género no encontrado'})

        # Simulamos la respuesta para obtener una pelicula aleatoria de un genero particular en un dia feriado
        m.get('http://localhost:5000/peliculas/feriado/Drama', status_code=200)
        m.get('http://localhost:5000/peliculas/feriado/NoExiste', status_code=404, json={'mensaje': 'Género no encontrado'})

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_obetener_detalle_pelicula_error(mock_response):
    response = requests.get('http://localhost:5000/peliculas/50')
    assert response.status_code == 404

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_actualizar_detalle_pelicula_error(mock_response):
    response = requests.put('http://localhost:5000/peliculas/50', json={'titulo': 'Nuevo título', 'genero': 'Comedia'})
    assert response.status_code == 404

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200


def test_eliminar_pelicula_error(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/50')
    assert response.status_code == 404

def test_peliculas_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/genero/Drama')
    assert response.status_code == 200

def test_peliculas_genero_error(mock_response):
    response = requests.get('http://localhost:5000/peliculas/genero/NoExiste')
    assert response.status_code == 404

def test_filtro_por_titulo(mock_response):
    response = requests.get('http://localhost:5000/peliculas/titulo/Indi')
    assert response.status_code == 200
    assert "Indi".lower() in response.json()['titulo'].lower()

def test_filtro_por_titulo(mock_response):
    response = requests.get('http://localhost:5000/peliculas/titulo/NoExiste')
    assert response.status_code == 404

def test_pelicula_random(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random')
    assert response.status_code == 200

def test_pelicula_random_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/Drama')
    assert response.status_code == 200

def test_pelicula_random_genero_error(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/NoExiste')
    assert response.status_code == 404

def test_peli_random_feriado(mock_response):
    response = requests.get('http://localhost:5000/peliculas/feriado/Drama')
    assert response.status_code == 200

def test_peli_random_feriado_error(mock_response):
    response = requests.get('http://localhost:5000/peliculas/feriado/NoExiste')
    assert response.status_code == 404

# Run the test with the following command:
# pytest test_pytest.py
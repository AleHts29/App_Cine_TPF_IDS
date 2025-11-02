from flask import Flask, jsonify, request
from faker import Faker
from dotenv import load_dotenv
import os
import random


# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración general
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')
SERVER_PORT = int(os.getenv("SERVER_PORT", "9090"))

# Instancia de Faker
faker = Faker('es_ES')


# ==============================
#   DATOS FALSOS DE PELÍCULAS
# ==============================
# Lista de géneros base
GENEROS = [
    "Acción", "Comedia", "Drama", "Terror", "Aventura", "Romance",
    "Ciencia Ficción", "Fantasía", "Animación", "Documental"
]


def generar_pelicula_fake(id: int):
    """Genera una pelicula ficticia"""
    return {
        "id": id,
        "title": faker.catch_phrase(),
        "description": faker.text(max_nb_chars=150),
        "genrer": random.choice(GENEROS),
        "duration": random.randint(80, 180),
        "clasification": random.choice(["APT", "+13", "+16", "+18"]),
        "director": faker.name(),
        "imagen_url": faker.image_url(width=300, height=400)
    }

# Base de datos fake (memoria)
movies_fake = [generar_pelicula_fake(i) for i in range(1, 201)]

# ==============================
#   ENDPOINTS DE PELÍCULAS
# ==============================

@app.route('/')
def test():
    return jsonify({"status": "ok", "message": "API Cine IDS 2025 corriendo correctamente 🚀"})


@app.route('/api/movies', methods=['GET'])
def all_movies():
    return jsonify(movies_fake), 200


@app.route('/api/movies', methods=['POST'])
def create_movie():
    """Agrega una nueva película (fake)"""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    new_id = len(movies_fake) + 1
    new_movie = {
        "id": new_id,
        "title": data["title"],
        "description": data.get("description", faker.text(120)),
        "genrer": data.get("genrer", random.choice(GENEROS)),
        "duration": data.get("duration", random.randint(80, 180)),
        "clasification": data.get("clasification", random.choice(["ATP", "+13", "+16", "+18"])),
        "director": data.get("director", faker.name()),
        "imagen_url": data.get("imagen_url", faker.image_url(width=300, height=400))
    }

    movies_fake.append(new_movie)
    return jsonify({"message": "Película agregada exitosamente", "pelicula": new_movie}), 201


@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """Actualiza una película existente"""
    # Buscá dentro de movies_fake la primera película cuyo id sea igual a movie_id. Si no existe, devolvé None.
    movie = next((p for p in movies_fake if p['id'] == movie_id), None)
    if not movie:
        return jsonify({"error": "Película no encontrada"}), 404

    data = request.get_json()
    movie.update(data)
    return jsonify({"message": f"Película {movie_id} actualizada", "pelicula": movie}), 200



@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """Elimina una película"""
    global movies_fake
    # Recreá la lista movies_fake dejando fuera cualquier película cuyo id coincida con movie_id
    movies_fake = [p for p in movies_fake if p['id'] != movie_id]
    return jsonify({"message": f"Película {movie_id} eliminada"}), 200



# ==============================
#   ENDPOINTS DE CLIENTES
# ==============================


# ==============================
#   ENDPOINTS DE CONBOS
# ==============================


# ==============================
#   ENDPOINTS DE ENTRADAS
# ==============================




if __name__ == '__main__':
    app.run(host="localhost", port=SERVER_PORT, debug=True)
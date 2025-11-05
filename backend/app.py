from flask import Flask, jsonify, request
from flask_cors import CORS
from app_backend.routes.peliculas import peliculas_bp
from app_backend.routes.salas import salas_bp
from app_backend.routes.funciones import funciones_bp
from app_backend.routes.clientes import clientes_bp
from app_backend.routes.butacas import butacas_bp
from app_backend.routes.entradas import entradas_bp
from faker import Faker
from dotenv import load_dotenv
import os
import random
from db import get_connection


load_dotenv()

app = Flask(__name__)

app.register_blueprint(peliculas_bp,url_prefix="/peliculas")
app.register_blueprint(salas_bp,url_prefix="/salas")
app.register_blueprint(butacas_bp,url_prefix="/butacas")
app.register_blueprint(funciones_bp,url_prefix="/funciones")
app.register_blueprint(clientes_bp,url_prefix="/clientes")
app.register_blueprint(entradas_bp,url_prefix="/entradas")


# ==============================
#   DB CONNECTION SETUP
# ==============================
conn = get_connection()
if conn and conn.is_connected():
    print("✅ Conectado correctamente a MySQL!")
else:
    print("❌ No se pudo conectar.")

# Configuración general
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')
SERVER_PORT = int(os.getenv("SERVER_PORT", "9090"))


faker = Faker('es_ES')


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

movies_fake = [generar_pelicula_fake(i) for i in range(1, 201)]


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



from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route("/")
def get_peliculas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(peliculas)

@peliculas_bp.route("/[int:id_pelicula](int:id_pelicula)")
def get_pelicula(id_pelicula):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas WHERE id_pelicula = %s", (id_pelicula,))
    pelicula = cursor.fetchone()
    cursor.close()
    conn.close()
    if not pelicula:
        return ("Película no encontrada", 404)
    return jsonify(pelicula)

@peliculas_bp.route("/", methods=["POST"])
def create_pelicula():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    titulo = data.get("titulo")
    duracion = data.get("duracion")
    genero = data.get("genero")
    sinopsis = data.get("sinopsis")
    estado = data.get("estado", "Activa")


    cursor.execute("""
        INSERT INTO peliculas (titulo, duracion, genero, sinopsis, estado)
        VALUES (%s, %s, %s, %s, %s)
    """, (titulo, duracion, genero, sinopsis, estado))

    conn.commit()
    cursor.close()
    conn.close()
    return ("Película creada correctamente", 201)


@peliculas_bp.route("/[int:id_pelicula](int:id_pelicula)", methods=["PUT"])
def update_pelicula(id_pelicula):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    titulo = data.get("titulo")
    duracion = data.get("duracion")
    genero = data.get("genero")
    sinopsis = data.get("sinopsis")
    estado = data.get("estado")


    cursor.execute("""
        UPDATE peliculas
        SET titulo = %s, duracion = %s, genero = %s, sinopsis = %s, estado = %s
        WHERE id_pelicula = %s
    """, (titulo, duracion, genero, sinopsis, estado, id_pelicula))

    conn.commit()
    cursor.close()
    conn.close()
    return ("Película actualizada correctamente", 200)


@peliculas_bp.route("/[int:id_pelicula](int:id_pelicula)", methods=["DELETE"])
def delete_pelicula(id_pelicula):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM peliculas WHERE id_pelicula = %s", (id_pelicula,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Película eliminada correctamente", 200)
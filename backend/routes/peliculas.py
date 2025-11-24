from flask import Blueprint, jsonify, request
from flasgger import swag_from

from services.peliculas_service import (
    listar_peliculas,
    obtener_pelicula,
    agregar_pelicula,
    modificar_pelicula,
    eliminar_pelicula,
    crear_pelicula_completa_service
)


peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route("/", methods=["GET"])
# @swag_from("../swagger/peliculas.yml")
def get_peliculas():
    peliculas = listar_peliculas()   # obtenés la lista real
    print(f"data desde backend: {peliculas}")  # 🔹 ahora sí imprime el contenido
    return jsonify(peliculas)        # devolvés la respuesta JSON


@peliculas_bp.route("/<int:id_pelicula>", methods=["GET"])
# @swag_from("../swagger/peliculas.yml")
def get_pelicula(id_pelicula):
    pelicula = obtener_pelicula(id_pelicula)
    if not pelicula:
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify(pelicula)

@peliculas_bp.route("/", methods=["POST"])
# @swag_from("../swagger/peliculas.yml")
def post_pelicula():
    data = request.json
    try:
        agregar_pelicula(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Película creada correctamente"}), 201


@peliculas_bp.route("/pelicula-funcion", methods=["POST"])
# @swag_from("../swagger/peliculas.yml")
def crear_pelicula_completa():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    try:
        result = crear_pelicula_completa_service(data)
        return jsonify(result), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@peliculas_bp.route("/<int:id_pelicula>", methods=["PUT"])
# @swag_from("../swagger/peliculas.yml")
def put_pelicula(id_pelicula):
    if not modificar_pelicula(id_pelicula, request.json):
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify({"message": "Película actualizada correctamente"}), 200

@peliculas_bp.route("/<int:id_pelicula>", methods=["DELETE"])
# @swag_from("../swagger/peliculas.yml")
def delete_pelicula(id_pelicula):
    if not eliminar_pelicula(id_pelicula):
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify({"message": "Película eliminada correctamente"}), 200
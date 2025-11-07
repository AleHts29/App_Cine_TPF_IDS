from flask import Blueprint, jsonify, request

from services.peliculas_service import (
    listar_peliculas,
    obtener_pelicula,
    agregar_pelicula,
    modificar_pelicula,
    eliminar_pelicula
)

peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route("/", methods=["GET"])
def get_peliculas():
    return jsonify(listar_peliculas())

@peliculas_bp.route("/<int:id_pelicula>", methods=["GET"])
def get_pelicula(id_pelicula):
    pelicula = obtener_pelicula(id_pelicula)
    if not pelicula:
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify(pelicula)

@peliculas_bp.route("/", methods=["POST"])
def post_pelicula():
    data = request.json
    try:
        agregar_pelicula(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Película creada correctamente"}), 201

@peliculas_bp.route("/<int:id_pelicula>", methods=["PUT"])
def put_pelicula(id_pelicula):
    if not modificar_pelicula(id_pelicula, request.json):
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify({"message": "Película actualizada correctamente"}), 200

@peliculas_bp.route("/<int:id_pelicula>", methods=["DELETE"])
def eliminar_pelicula(id_pelicula):
    if not eliminar_pelicula(id_pelicula):
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify({"message": "Película eliminada correctamente"}), 200
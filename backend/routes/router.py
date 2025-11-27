from flask import Blueprint, jsonify, request
from services.services import (
    butacas_segun_pelicula
)

router_bp = Blueprint("router",__name__)
@router_bp.route("/funciones/<int:id_pelicula>", methods=["GET"])
def get_butacas_pelicula(id_pelicula):
    pelicula = butacas_segun_pelicula(id_pelicula)
    if not pelicula:
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify(pelicula)
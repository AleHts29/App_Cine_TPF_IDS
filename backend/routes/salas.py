from flask import Blueprint, jsonify, request
from services.salas_service import (
    listar_salas_service,
    obtener_sala_service,
    crear_sala_service,
    editar_sala_service,
    borrar_sala_service
)

salas_bp = Blueprint("salas", __name__)

# LISTAR TODAS LAS SALAS
@salas_bp.route("/salas", methods=["GET"])
def route_listar_salas():
    try:
        salas = listar_salas_service()
        return jsonify(salas), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# OBTENER UNA SALA POR ID
@salas_bp.route("/salas/<int:id_sala>", methods=["GET"])
def route_obtener_sala(id_sala):
    try:
        sala = obtener_sala_service(id_sala)
        return jsonify(sala), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# CREAR SALA
@salas_bp.route("/salas", methods=["POST"])
def route_crear_sala():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
    try:
        nuevo = crear_sala_service(data)
        return jsonify(nuevo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# EDITAR SALA
@salas_bp.route("/salas/<int:id_sala>", methods=["PUT"])
def route_editar_sala(id_sala):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
    try:
        resultado = editar_sala_service(id_sala, data)
        return jsonify({"success": resultado}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# BORRAR SALA
@salas_bp.route("/salas/<int:id_sala>", methods=["DELETE"])
def route_borrar_sala(id_sala):
    try:
        resultado = borrar_sala_service(id_sala)
        return jsonify({"success": resultado}), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500
from flask import Blueprint, jsonify, request

from services.butacas_service import (
    listar_butacas_service,
    obtener_butaca_service,
    crear_butaca_service,
    editar_butaca_service,
    borrar_butaca_service
)

butacas_bp = Blueprint("butacas", __name__)

# LISTAR TODAS LAS BUTACAS
@butacas_bp.route("/butacas", methods=["GET"])
def route_listar_butacas():
    try:
        butacas = listar_butacas_service()
        return jsonify(butacas), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# OBTENER UNA BUTACA POR ID
@butacas_bp.route("/butacas/<int:id_butaca>", methods=["GET"])
def route_obtener_butaca(id_butaca):
    try:
        butaca = obtener_butaca_service(id_butaca)
        return jsonify(butaca), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# CREAR BUTACA
@butacas_bp.route("/butacas", methods=["POST"])
def route_crear_butaca():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
    try:
        nuevo = crear_butaca_service(data)
        return jsonify(nuevo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# EDITAR BUTACA
@butacas_bp.route("/butacas/<int:id_butaca>", methods=["PUT"])
def route_editar_butaca(id_butaca):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
    try:
        resultado = editar_butaca_service(id_butaca, data)
        return jsonify({"success": resultado}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# BORRAR BUTACA
@butacas_bp.route("/butacas/<int:id_butaca>", methods=["DELETE"])
def route_borrar_butaca(id_butaca):
    try:
        resultado = borrar_butaca_service(id_butaca)
        return jsonify({"success": resultado}), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500
from flask import Blueprint, jsonify, request
from services.reservas_service import obtener_reserva_service, crear_reserva_pendiente_service, crear_reserva_pagada_service, completar_pago_service

reservas_bp = Blueprint("reservas", __name__)


# Crear reserva con estado pendiente
@reservas_bp.route("/pendiente", methods=["POST"])
def crear_reserva_pendiente():
    data = request.get_json(silent=True)
    try:
        result = crear_reserva_pendiente_service(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Error interno del servidor"}), 500


# Crear reserva con compra confirmada
@reservas_bp.route("/comprar", methods=["POST"])
def crear_reserva_pagada():
    data = request.get_json(silent=True)
    try:
        result = crear_reserva_pagada_service(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500
    


@reservas_bp.route("/<int:id_reserva>", methods=["GET"])
def route_obtener_reserva(id_reserva):    
    try:
        reserva = obtener_reserva_service(id_reserva)
        return jsonify(reserva), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Error interno del servidor"}), 500
    


@reservas_bp.route("/completar_pago", methods=["POST"])
def completar_pago():
    data = request.get_json()
    try:
        result = completar_pago_service(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
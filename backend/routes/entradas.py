from flask import Blueprint, request, jsonify

from services.entradas_service import (
    crear_entrada_service,
    editar_entrada_service,
    listar_entradas_service,
    obtener_entrada_service,
    borrar_entrada_service
)

entradas_bp = Blueprint("entradas", __name__)

# CREAR ENTRADA
@entradas_bp.route("/entradas", methods=["POST"])
def route_crear_entrada():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400

    try:
        nuevo = crear_entrada_service(data)
        return jsonify(nuevo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# EDITAR ENTRADA
@entradas_bp.route("/entradas/<int:id_entrada>", methods=["PUT"])
def route_editar_entrada(id_entrada):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400

    try:
        resultado = editar_entrada_service(id_entrada, data)
        return jsonify({"success": resultado}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# LISTAR ENTRADAS 
@entradas_bp.route("/entradas", methods=["GET"])
def route_listar_entradas():
    id_user = request.args.get("id_user")
    try:
        entradas = listar_entradas_service(id_user)
        return jsonify(entradas), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# OBTENER ENTRADA ESPECÍFICA
@entradas_bp.route("/entradas/<int:id_entrada>", methods=["GET"])
def route_obtener_entrada(id_entrada):
    try:
        entrada = obtener_entrada_service(id_entrada)
        return jsonify(entrada), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# BORRAR ENTRADA
@entradas_bp.route("/entradas/<int:id_entrada>", methods=["DELETE"])
def route_borrar_entrada(id_entrada):
    try:
        resultado = borrar_entrada_service(id_entrada)
        return jsonify({"success": resultado}), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500
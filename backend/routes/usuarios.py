from flask import Blueprint, request, jsonify
from services.usuarios_service import (
    crear_usuario_service,
    editar_usuario_service,
    listar_usuarios_service,
    borrar_usuario_service
)

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario_route():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400

    try:
        nuevo = crear_usuario_service(data)
        return jsonify(nuevo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def editar_usuario_route(id_usuario):
    data = request.get_json()
    actualizado = editar_usuario_service(id_usuario, data)
    return jsonify(actualizado), 200

@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios_route():
    email = request.args.get("email")

    usuarios = listar_usuarios_service(email=email)
    return jsonify(usuarios), 200


@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def borrar_usuario_route(id_usuario):
    borrar_usuario_service(id_usuario)
    return jsonify({"message": "Usuario eliminado"}), 200


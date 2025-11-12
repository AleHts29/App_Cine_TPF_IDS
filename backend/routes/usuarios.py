from flask import Blueprint, request, jsonify, render_template, session
from db import get_connection
from services.usuarios_service import (
    verificar_usuario_service,
    crear_usuario_service,
    editar_usuario_service,
    listar_usuarios_service,
    borrar_usuario_service
)

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/verify/<token>", methods=["GET"])
def verificar_usuario_route(token):
    try:
        user = verificar_usuario_service(token)

        session["user_id"] = user["id_user"]
        session["username"] = user["username"]

        return render_template("auth/verify.html", username=user["username"])
    except ValueError as e:
        return f"<h2>{str(e)}</h2>", 400


@usuarios_bp.route("/", methods=["POST"])
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

@usuarios_bp.route("/status/<int:id_usuario>", methods=["GET"])
def estado_usuario(id_usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT is_active FROM users WHERE id_user = %s", (id_usuario,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"is_active": bool(row["is_active"])})
    except Exception as e:
        return jsonify({"error": "Error interno"}), 500
    
@usuarios_bp.route("/me", methods=["GET"])
def usuario_actual():
    user_id = session.get("user_id")
    username = session.get("username")
    if user_id and username:
        return jsonify({"id": user_id, "username": username})
    return jsonify({}), 401

@usuarios_bp.route("/<int:id_usuario>", methods=["PUT"])
def editar_usuario_route(id_usuario):
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({"error": "Body vacío o formato inválido (debe ser JSON)"}), 400

    try:
        actualizado = editar_usuario_service(id_usuario, data)
        return jsonify(actualizado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios_route():
    busqueda = request.args.get("busqueda")

    usuarios = listar_usuarios_service(busqueda)
    return jsonify(usuarios), 200


@usuarios_bp.route("/<int:id_usuario>", methods=["DELETE"])
def borrar_usuario_route(id_usuario):
    borrar_usuario_service(id_usuario)
    return jsonify({"message": "Usuario eliminado"}), 200
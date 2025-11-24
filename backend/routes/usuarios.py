from flask import Blueprint, request, jsonify, render_template, session
from db import get_connection
from services.usuarios_service import (
    verificar_token_service,
    crear_usuario_service,
    editar_usuario_service,
    listar_usuarios_service,
    borrar_usuario_service
    contraseña_service
)
import bcrypt

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios", template_folder="../frontend/templates", static_folder="../frontend/static")


@usuarios_bp.route("/verify/<token>", methods=["GET"])
def verificar_usuario_route(token):
    try:
        user = verificar_token_service(token)
        token = str(user["id_user"])  

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
    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "No autorizado"}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_user, username, email, full_name, is_admin FROM users WHERE id_user = %s",
        (token,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Token inválido"}), 401

    return jsonify(user), 200

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

@usuarios_bp.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y password requeridos"}), 400

    user = verificar_usuario_service(email, password)  

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = str(user["id_user"])  

    return jsonify({
        "token": token,
        "username": user["username"]
    }), 200

def verificar_usuario_service(email, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_user, username, password_hash, is_active FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or user["is_active"] == 0:
        return None

    hashed_password = user["password_hash"].encode('utf-8')
    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return None

    return user

@usuarios_bp.route("/password", methods=["POST"])
def contraseña_route():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
from flask import Blueprint, jsonify, request
from services.funciones_service import (
    listar_funciones_service,
    obtener_funcion_service,
    crear_funcion_service,
    editar_funcion_service,
    borrar_funcion_service,
    listar_funciones_por_pelicula_service
)

funciones_bp = Blueprint("funciones", __name__)

# LISTAR TODAS LAS FUNCIONES
@funciones_bp.route("", methods=["GET"])
def route_listar_funciones():
    try:
        funciones = listar_funciones_service()
        return jsonify(funciones), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# OBTENER FUNCIÓN ESPECÍFICA
@funciones_bp.route("/<int:id_funcion>", methods=["GET"])
def route_obtener_funcion(id_funcion):
    try:
        funcion = obtener_funcion_service(id_funcion)
        return jsonify(funcion), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# CREAR FUNCIÓN
@funciones_bp.route("/", methods=["POST"])
def route_crear_funcion():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
    try:
        nuevo = crear_funcion_service(data)
        return jsonify(nuevo), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# EDITAR FUNCIÓN
@funciones_bp.route("/<int:id_funcion>", methods=["PUT"])
def route_editar_funcion(id_funcion):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido o body vacío"}), 400
    try:
        resultado = editar_funcion_service(id_funcion, data)
        return jsonify({"success": resultado}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500

# BORRAR FUNCIÓN
@funciones_bp.route("/<int:id_funcion>", methods=["DELETE"])
def route_borrar_funcion(id_funcion):
    try:
        resultado = borrar_funcion_service(id_funcion)
        return jsonify({"success": resultado}), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500
    

# OBTENER FUNCIONES POR ID DE PELÍCULA
@funciones_bp.route("/pelicula/<int:id_pelicula>", methods=["GET"])
def route_funciones_por_pelicula(id_pelicula):
    try:
        funciones = listar_funciones_por_pelicula_service(id_pelicula)
        return jsonify(funciones), 200
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500
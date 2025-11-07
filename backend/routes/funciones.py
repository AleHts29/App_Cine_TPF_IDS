from flask import Blueprint, jsonify, request
from db import get_connection

funciones_bp = Blueprint("funciones", __name__)

@funciones_bp.route("/")
def get_funciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT f.*, p.titulo AS pelicula, s.nombre AS sala
    FROM funciones f
    JOIN peliculas p ON p.id_pelicula = f.id_pelicula
    JOIN salas s ON s.id_sala = f.id_sala
    """)
    funciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(funciones)

@funciones_bp.route("/int:id_funcion")
def get_funcion(id_funcion):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT * FROM funciones WHERE id_funcion=%s
    """, (id_funcion,))
    funcion = cursor.fetchone()
    cursor.close()
    conn.close()
    if not funcion:
         return ("Función no encontrada", 404)
    return jsonify(funcion)

@funciones_bp.route("/", methods=["POST"])
def create_funcion():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO funciones (id_pelicula, id_sala, fecha, precio_base)
    VALUES (%s, %s, %s, %s)
    """, (data["id_pelicula"], data["id_sala"], data["fecha"], data["precio_base"]))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Función creada correctamente", 201)

@funciones_bp.route("/int:id_funcion", methods=["PUT"])
def update_funcion(id_funcion):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE funciones
    SET id_pelicula=%s, id_sala=%s, fecha=%s, precio_base=%s
    WHERE id_funcion=%s
    """, (data["id_pelicula"], data["id_sala"], data["fecha"], data["precio_base"], id_funcion))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Función actualizada correctamente", 200)

@funciones_bp.route("/int:id_funcion", methods=["DELETE"])
def delete_funcion(id_funcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funciones WHERE id_funcion=%s", (id_funcion,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Función eliminada correctamente", 200)
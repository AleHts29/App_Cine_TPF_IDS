from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

entradas_bp = Blueprint("entradas", __name__)

@entradas_bp.route("/")
def get_entradas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT e.*, c.nombre AS cliente, p.titulo AS pelicula, b.fila, b.numero
    FROM entradas e
    JOIN clientes c ON c.id_cliente = e.id_cliente
    JOIN funciones f ON f.id_funcion = e.id_funcion
    JOIN peliculas p ON p.id_pelicula = f.id_pelicula
    JOIN butacas b ON b.id_butaca = e.id_butaca
    """)
    entradas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(entradas)

@entradas_bp.route("/int:id_entrada")
def get_entrada(id_entrada):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM entradas WHERE id_entrada=%s", (id_entrada,))
    entrada = cursor.fetchone()
    cursor.close()
    conn.close()
    if not entrada:
            return ("Entrada no encontrada", 404)
    return jsonify(entrada)

@entradas_bp.route("/", methods=["POST"])
def create_entrada():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO entradas (id_funcion, id_cliente, id_butaca, precio_final, fecha, estado)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (data["id_funcion"], data["id_cliente"], data["id_butaca"], data["precio_final"], data["fecha"], data.get("estado", "Activa")))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Entrada creada correctamente", 201)

@entradas_bp.route("/int:id_entrada", methods=["PUT"])
def update_entrada(id_entrada):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE entradas
    SET id_funcion=%s, id_cliente=%s, id_butaca=%s, precio_final=%s, fecha=%s, estado=%s
    WHERE id_entrada=%s
    """, (data["id_funcion"], data["id_cliente"], data["id_butaca"], data["precio_final"], data["fecha"], data["estado"], id_entrada))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Entrada actualizada correctamente", 200)

@entradas_bp.route("/int:id_entrada", methods=["DELETE"])
def delete_entrada(id_entrada):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entradas WHERE id_entrada=%s", (id_entrada,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Entrada eliminada correctamente", 200)
from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

salas_bp = Blueprint("salas", __name__)

@salas_bp.route("/")
def get_salas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM salas")
    salas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(salas)

@salas_bp.route("/int:id_sala")
def get_sala(id_sala):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM salas WHERE id_sala=%s", (id_sala,))
    sala = cursor.fetchone()
    cursor.close()
    conn.close()
    if not sala:
            return ("Sala no encontrada", 404)
    return jsonify(sala)

@salas_bp.route("/", methods=["POST"])
def create_sala():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO salas (nombre, tipo_sala, capacidad)
    VALUES (%s, %s, %s)
    """, (data["nombre"], data["tipo_sala"], data["capacidad"]))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Sala creada correctamente", 201)

@salas_bp.route("/int:id_sala", methods=["PUT"])
def update_sala(id_sala):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE salas
    SET nombre=%s, tipo_sala=%s, capacidad=%s
    WHERE id_sala=%s
    """, (data["nombre"], data["tipo_sala"], data["capacidad"], id_sala))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Sala actualizada correctamente", 200)

@salas_bp.route("/int:id_sala", methods=["DELETE"])
def delete_sala(id_sala):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM salas WHERE id_sala=%s", (id_sala,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Sala eliminada correctamente", 200)
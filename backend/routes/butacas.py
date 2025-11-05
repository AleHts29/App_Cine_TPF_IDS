from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

butacas_bp = Blueprint("butacas", __name__)

@butacas_bp.route("/")
def get_butacas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM butacas")
    butacas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(butacas)

@butacas_bp.route("/int:id_butaca")
def get_butaca(id_butaca):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM butacas WHERE id_butaca=%s", (id_butaca,))
    butaca = cursor.fetchone()
    cursor.close()
    conn.close()
    if not butaca:
         return ("Butaca no encontrada", 404)
    return jsonify(butaca)

@butacas_bp.route("/", methods=["POST"])
def create_butaca():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO butacas (id_sala, fila, numero)
    VALUES (%s, %s, %s)
    """, (data["id_sala"], data["fila"], data["numero"]))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Butaca creada correctamente", 201)

@butacas_bp.route("/int:id_butaca", methods=["PUT"])
def update_butaca(id_butaca):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE butacas
    SET id_sala=%s, fila=%s, numero=%s
    WHERE id_butaca=%s
    """, (data["id_sala"], data["fila"], data["numero"], id_butaca))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Butaca actualizada correctamente", 200)

@butacas_bp.route("/int:id_butaca", methods=["DELETE"])
def delete_butaca(id_butaca):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM butacas WHERE id_butaca=%s", (id_butaca,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Butaca eliminada correctamente", 200)
from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/")
def get_clientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

@clientes_bp.route("/int:id_cliente")
def get_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente=%s", (id_cliente,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    if not cliente:
         return ("Cliente no encontrado", 404)
    return jsonify(cliente)

@clientes_bp.route("/", methods=["POST"])
def create_cliente():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO clientes (nombre, email, metodo_de_pago)
    VALUES (%s, %s, %s)
    """, (data["nombre"], data["email"], data["metodo_de_pago"]))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente creado correctamente", 201)

@clientes_bp.route("/int:id_cliente", methods=["PUT"])
def update_cliente(id_cliente):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE clientes
    SET nombre=%s, email=%s, metodo_de_pago=%s
    WHERE id_cliente=%s
    """, (data["nombre"], data["email"], data["metodo_de_pago"], id_cliente))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente actualizado correctamente", 200)

@clientes_bp.route("/int:id_cliente", methods=["DELETE"])
def delete_cliente(id_cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id_cliente,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente eliminado correctamente", 200)
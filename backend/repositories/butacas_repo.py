from db import get_connection

# obtener todas las butacas
def listar_butacas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM butacas")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# obtener butaca por id
def obtener_butaca(id_butaca):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM butacas WHERE id_butaca=%s", (id_butaca,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# crear nueva butaca
def crear_butaca(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO butacas (id_sala, fila, numero)
        VALUES (%s, %s, %s)
    """, (data["id_sala"], data["fila"], data["numero"]))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id

# actualizar butaca existente
def editar_butaca(id_butaca, data):
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
    return True

# borrar butaca
def borrar_butaca(id_butaca):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM butacas WHERE id_butaca=%s", (id_butaca,))
    conn.commit()
    cursor.close()
    conn.close()
    return True
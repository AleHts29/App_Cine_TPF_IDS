from db import get_connection

# LISTAR TODAS LAS SALAS
def listar_salas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM salas")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# OBTENER UNA SALA POR ID
def obtener_sala(id_sala):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM salas WHERE id_sala=%s", (id_sala,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# CREAR SALA
def crear_sala(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO salas (nombre, tipo_sala, capacidad)
        VALUES (%s, %s, %s)
    """, (data["nombre"], data["tipo_sala"], data["capacidad"]))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id

# EDITAR SALA
def editar_sala(id_sala, data):
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
    return True

# BORRAR SALA
def borrar_sala(id_sala):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM salas WHERE id_sala=%s", (id_sala,))
    conn.commit()
    cursor.close()
    conn.close()
    return True
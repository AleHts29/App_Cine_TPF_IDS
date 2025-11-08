from db import get_connection
import mysql.connector 

def crear_entrada(data):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO entradas (id_user, id_funcion, id_butaca, precio_final, estado, fecha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["id_user"],
            data["id_funcion"],
            data["id_butaca"],
            data["precio_final"],
            data.get("estado", "comprada"),  # por defecto "comprada"
            data.get("fecha")  # si no viene, podemos poner NOW() en SQL o datetime.now() en Python
        ))

        conn.commit()
        new_id = cursor.lastrowid
        return new_id

    except mysql.connector.IntegrityError as e:
        conn.rollback()
        raise
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def editar_entrada(id_entrada, data):
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if "estado" in data:
        fields.append("estado = %s")
        values.append(data["estado"])

    if "precio_final" in data:
        fields.append("precio_final = %s")
        values.append(data["precio_final"])

    if not fields:
        return False

    query = "UPDATE entradas SET " + ", ".join(fields) + " WHERE id_entrada = %s"
    values.append(id_entrada)

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return True

def listar_entradas(id_user=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if id_user:
        cursor.execute("""
            SELECT * FROM entradas WHERE id_user = %s
        """, (id_user,))
    else:
        cursor.execute("SELECT * FROM entradas")

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#obtener entrada
def obtener_entrada(id_entrada):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM entradas WHERE id_entrada = %s", (id_entrada,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise ValueError("Entrada no encontrada")
    return row

# BORRAR ENTRADA
def borrar_entrada(id_entrada):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entradas WHERE id_entrada = %s", (id_entrada,))
    conn.commit()
    cursor.close()
    conn.close()
    return True
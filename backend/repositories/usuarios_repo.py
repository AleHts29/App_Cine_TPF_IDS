from db import get_connection
import bcrypt
import mysql.connector 

def crear_usuario(data):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("""
            INSERT INTO users (email, full_name, username, password_hash, is_active, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["email"],
            data.get("full_name", None),
            data["username"],
            password_hash,
            1,
            0
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


#editar usuario

def editar_usuario(id, data):
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if "username" in data:
        fields.append("username = %s")
        values.append(data["username"])

    if "full_name" in data:
        fields.append("full_name = %s")
        values.append(data["full_name"])

    if "profile_image" in data:
        fields.append("profile_image = %s")
        values.append(data["profile_image"])

    if not fields:
        return False

    query = "UPDATE users SET " + ", ".join(fields) + " WHERE id_user = %s"
    values.append(id)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()
    return True

#mostrar usuarios (va a ser en una pagina de admins)
def listar_usuarios(busqueda=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if busqueda:
        cursor.execute("""
            SELECT id_user, email, full_name, username, profile_image, is_active, is_admin
            FROM users
            WHERE username LIKE %s OR email LIKE %s
         """, (f"%{busqueda}%", f"%{busqueda}%"))
    else:
        cursor.execute("""
            SELECT id_user, email, full_name, username, profile_image, is_active, is_admin
            FROM users
        """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

#borrar usuarios (exclusivo de admins)
def borrar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id_user = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return True

from db import get_connection
from repositories.butacas_repo import crear_butacas_funcion

def get_all_peliculas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def get_pelicula_by_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM peliculas WHERE id_pelicula=%s", (id,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res

def create_pelicula(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO peliculas (titulo, duracion, genero, sinopsis, director, imagen_url, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data["titulo"], data["duracion"], data["genero"], data["sinopsis"], data["director"], data["imagen_url"], data.get("estado", "en_cartelera")))
    conn.commit()
    cursor.close()
    conn.close()

def agregar_pelicula_completa_repo(data):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # --- 1) Crear película ---
        cursor.execute("""
            INSERT INTO peliculas (titulo, duracion, genero, sinopsis, director, imagen_url, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["titulo"],
            data["duracion"],
            data["genero"],
            data["sinopsis"],
            data["director"],
            data["imagen_url"],
            data["estado"]
        ))

        conn.commit()
        id_pelicula = cursor.lastrowid

        # --- 2) Crear funciones ---
        funciones_result = []

        for f in data["funciones"]:
            cursor.execute("""
                INSERT INTO funciones (id_pelicula, id_sala, fecha_hora, precio_base)
                VALUES (%s, %s, %s, %s)
            """, (
                id_pelicula,
                f["id_sala"],
                f["fecha"],
                f["precio_base"]
            ))

            conn.commit()
            id_funcion = cursor.lastrowid

            # --- 3) Crear butacas para la función ---
            crear_butacas_funcion(cursor, id_funcion, f["id_sala"])

            funciones_result.append({
                "id_funcion": id_funcion,
                "id_sala": f["id_sala"],
                "fecha": f["fecha"],
                "precio_base": f["precio_base"]
            })

        conn.commit()

        return {
            "id_pelicula": id_pelicula,
            "funciones_result": funciones_result
        }

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()



def update_pelicula(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE peliculas
        SET titulo=%s, duracion=%s, genero=%s, sinopsis=%s, director=%s, imagen_url=%s, estado=%s
        WHERE id_pelicula=%s
    """, (data["titulo"], data["duracion"], data["genero"], data["sinopsis"], data["director"], data["imagen_url"], data["estado"], id))
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return updated

def delete_pelicula(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM peliculas WHERE id_pelicula=%s", (id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted
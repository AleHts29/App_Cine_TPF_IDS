from db import get_connection

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
        INSERT INTO peliculas (titulo, duracion, genero, sinopsis, imagen_url, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data["titulo"], data["duracion"], data["genero"], data["sinopsis"], data["imagen_url"], data.get("estado", "en_cartelera")))
    conn.commit()
    cursor.close()
    conn.close()

def update_pelicula(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE peliculas
        SET titulo=%s, duracion=%s, genero=%s, sinopsis=%s, imagen_url=%s, estado=%s
        WHERE id_pelicula=%s
    """, (data["titulo"], data["duracion"], data["genero"], data["sinopsis"], data["imagen_url"], data["estado"], id))
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
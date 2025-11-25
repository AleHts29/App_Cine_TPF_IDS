from db import get_connection

# LISTAR TODAS LAS FUNCIONES
def listar_funciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*, p.titulo AS pelicula, s.nombre AS sala
        FROM funciones f
        JOIN peliculas p ON p.id_pelicula = f.id_pelicula
        JOIN salas s ON s.id_sala = f.id_sala
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# OBTENER UNA FUNCIÓN POR ID
def obtener_funcion(id_funcion):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM funciones WHERE id_funcion=%s", (id_funcion,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

# CREAR FUNCIÓN
def crear_funcion(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO funciones (id_pelicula, id_sala, fecha, precio_base)
        VALUES (%s, %s, %s, %s)
    """, (data["id_pelicula"], data["id_sala"], data["fecha"], data["precio_base"]))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id

# EDITAR FUNCIÓN
def editar_funcion(id_funcion, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE funciones
        SET id_pelicula=%s, id_sala=%s, fecha=%s, precio_base=%s
        WHERE id_funcion=%s
    """, (data["id_pelicula"], data["id_sala"], data["fecha"], data["precio_base"], id_funcion))
    conn.commit()
    cursor.close()
    conn.close()
    return True

# BORRAR FUNCIÓN
def borrar_funcion(id_funcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funciones WHERE id_funcion=%s", (id_funcion,))
    conn.commit()
    cursor.close()
    conn.close()
    return True

# LISTAR FUNCIONES POR ID DE PELÍCULA
def listar_funciones_por_pelicula_repo(id_pelicula):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            f.id_funcion,
            f.id_pelicula,
            f.id_sala,
            f.fecha_hora,
            f.precio_base,
            p.titulo,
            p.duracion,
            p.imagen_url
        FROM funciones f
        INNER JOIN peliculas p ON p.id_pelicula = f.id_pelicula
        WHERE f.id_pelicula = %s
        ORDER BY f.fecha_hora ASC
    """, (id_pelicula,))
    
    funciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return funciones
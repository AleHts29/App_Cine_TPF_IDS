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

def butacas_segun_idpelicula(idFuncion, idPelicula):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            p.id_pelicula, 
            f.id_funcion, 
            b.id_butaca, 
            b.fila, 
            b.numero, 
            bf.estado
        FROM peliculas p
        INNER JOIN funciones f
            ON f.id_pelicula = p.id_pelicula
        INNER JOIN butacas_funcion bf
            ON bf.id_funcion = f.id_funcion
        INNER JOIN butacas b 
            ON b.id_butaca = bf.id_butaca
        WHERE p.id_pelicula = %s
          AND f.id_funcion = %s
    """, (idPelicula, idFuncion))

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado


def verificar_butacas_libres(id_funcion, butacas):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    formato = ",".join(["%s"] * len(butacas))

    query = f"""
        SELECT id_butaca, estado
        FROM butacas_funcion
        WHERE id_funcion = %s
        AND id_butaca IN ({formato})
        AND estado = 'reservada'
    """

    cursor.execute(query, [id_funcion] + butacas)
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    # Si encontramos alguna en estado "reservada", NO están libres
    return len(resultados) == 0


def reservar_butacas(id_funcion, butacas):
    conn = get_connection()
    cursor = conn.cursor()

    for b in butacas:
        cursor.execute("""
            UPDATE butacas_funcion
            SET estado = 'reservada'
            WHERE id_funcion = %s AND id_butaca = %s
        """, (id_funcion, b))

    conn.commit()
    cursor.close()
    conn.close()

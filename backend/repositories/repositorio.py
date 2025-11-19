from db import get_connection
def butacas_segun_idpelicula(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.id_pelicula, f.id_funcion, b.id_butaca, b.fila, b.numero, bf.estado
        FROM peliculas p
        INNER JOIN funciones f
            ON f.id_pelicula = p.id_pelicula
        INNER JOIN butacas_funcion bf
            ON bf.id_funcion = f.id_funcion
        INNER JOIN butacas b 
            ON b.id_butaca = bf.id_butaca
        WHERE p.id_pelicula = %s
    """, (id,))

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado

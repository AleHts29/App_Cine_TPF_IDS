from db import get_connection


def insertar_reserva(id_funcion, id_pelicula, id_usuario, estado):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reservas (id_funcion, id_pelicula, id_usuario, estado)
        VALUES (%s, %s, %s, %s)
    """, (id_funcion, id_pelicula, id_usuario, estado))

    conn.commit()
    id_reserva = cursor.lastrowid

    cursor.close()
    conn.close()
    return id_reserva

def guardar_butacas_reserva(id_reserva, butacas):
    conn = get_connection()
    cursor = conn.cursor()

    for id_butaca in butacas:
        cursor.execute("""
            INSERT INTO reservas_butacas (id_reserva, id_butaca)
            VALUES (%s, %s)
        """, (id_reserva, id_butaca))

    conn.commit()
    cursor.close()
    conn.close()


def obtener_reserva_repo(id_reserva):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener datos generales
    cursor.execute("""
        SELECT r.id_reserva, r.fecha,
               p.titulo,
               f.fecha_hora,
               f.id_sala,
               f.precio_base
        FROM reservas r
        JOIN peliculas p ON p.id_pelicula = r.id_pelicula
        JOIN funciones f ON f.id_funcion = r.id_funcion
        WHERE r.id_reserva = %s
    """, (id_reserva,))

    reserva = cursor.fetchone()
    if not reserva:
        return None

    # Obtener butacas
    cursor.execute("""
        SELECT b.fila, b.numero
        FROM reservas_butacas rb
        JOIN butacas b ON b.id_butaca = rb.id_butaca
        WHERE rb.id_reserva = %s
        ORDER BY b.fila, b.numero
    """, (id_reserva,))

    butacas = cursor.fetchall()

    cursor.close()
    conn.close()

    # Formatear butacas ej: ["A1", "A2", "B4"]
    reserva["butacas"] = [f"{b['fila']}{b['numero']}" for b in butacas]

    return reserva


def actualizar_estado_reserva(id_reserva, nuevo_estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reservas SET estado = %s WHERE id_reserva = %s
    """, (nuevo_estado, id_reserva))
    conn.commit()
    cursor.close()
    conn.close()
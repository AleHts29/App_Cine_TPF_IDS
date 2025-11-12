from repositories.reservas_repo import insertar_reserva, obtener_reserva_repo, guardar_butacas_reserva, actualizar_estado_reserva
from repositories.butacas_repo import verificar_butacas_libres, reservar_butacas



# --- Reserva pendiente (paga en el cine)
def crear_reserva_pendiente_service(data):
    id_funcion = data.get("id_funcion")
    id_pelicula = data.get("id_pelicula")
    id_usuario = data.get("id_usuario")
    butacas = data.get("butacas")

    if not id_funcion or not id_pelicula or not butacas:
        raise ValueError("Faltan datos obligatorios")

    # Validar disponibilidad
    libres = verificar_butacas_libres(id_funcion, butacas)
    if not libres:
        raise ValueError("Una o más butacas ya está ocupada")

    # Guardar reserva con estado PENDIENTE
    id_reserva = insertar_reserva(id_funcion, id_pelicula, id_usuario, "pendiente")

    # Insertar la relación reserva - butacas
    guardar_butacas_reserva(id_reserva, butacas)

    # Cambiar estado a 'reservada' en butacas_funcion
    # marcar_reservadas_funcion(id_funcion, butacas)
    reservar_butacas(id_funcion, butacas)

    return {
        "message": "Reserva registrada (pendiente de pago)",
        "id_reserva": id_reserva
    }


# --- Compra completada
def crear_reserva_pagada_service(data):
    id_funcion = data.get("id_funcion")
    id_pelicula = data.get("id_pelicula")
    id_usuario = data.get("id_usuario")
    butacas = data.get("butacas")

    if not id_funcion or not id_pelicula or not butacas:
        raise ValueError("Faltan datos obligatorios")

    libres = verificar_butacas_libres(id_funcion, butacas)
    if not libres:
        raise ValueError("Una o más butacas ya está ocupada")

    id_reserva = insertar_reserva(id_funcion, id_pelicula, id_usuario, "pendiente")

    # Insertar la relación reserva - butacas
    guardar_butacas_reserva(id_reserva, butacas)


    # Cambiar estado a 'reservada' en butacas_funcion
    # marcar_reservadas_funcion(id_funcion, butacas)
    reservar_butacas(id_funcion, butacas)

    return {
        "message": "Reserva registrada (pendiente de pago)",
        "id_reserva": id_reserva
    }



def obtener_reserva_service(id_reserva):
    reserva = obtener_reserva_repo(id_reserva)
    if not reserva:
        raise ValueError("Reserva no encontrada")
    return reserva



def completar_pago_service(data):
    id_reserva = data.get("id_reserva")
    if not id_reserva:
        raise ValueError("id_reserva faltante")

    actualizar_estado_reserva(id_reserva, "pagada")

    return {
        "message": "Pago completado",
        "id_reserva": id_reserva
    }
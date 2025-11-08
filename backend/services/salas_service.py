from repositories.salas_repo import (
    listar_salas,
    obtener_sala,
    crear_sala,
    editar_sala,
    borrar_sala
)

# LISTAR SALAS
def listar_salas_service():
    return listar_salas()

# OBTENER SALA
def obtener_sala_service(id_sala):
    sala = obtener_sala(id_sala)
    if not sala:
        raise ValueError("Sala no encontrada")
    return sala

# CREAR SALA
def crear_sala_service(data):
    required = ["nombre", "tipo_sala", "capacidad"]
    for campo in required:
        if campo not in data:
            raise ValueError(f"{campo} es obligatorio")

    if not isinstance(data["capacidad"], int) or data["capacidad"] <= 0:
        raise ValueError("Capacidad debe ser un número mayor a 0")

    new_id = crear_sala(data)
    return {"id": new_id}

# EDITAR SALA
def editar_sala_service(id_sala, data):
    if not data:
        raise ValueError("No hay datos para actualizar")
    
    if "capacidad" in data:
        if not isinstance(data["capacidad"], int) or data["capacidad"] <= 0:
            raise ValueError("Capacidad debe ser un número mayor a 0")
    
    updated = editar_sala(id_sala, data)
    if not updated:
        raise ValueError("No se pudo actualizar la sala")
    
    return True

# BORRAR SALA
def borrar_sala_service(id_sala):
    return borrar_sala(id_sala)
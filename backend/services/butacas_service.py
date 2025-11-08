from repositories.butacas_repo import (
    listar_butacas,
    obtener_butaca,
    crear_butaca,
    editar_butaca,
    borrar_butaca
)

# LISTAR BUTACAS
def listar_butacas_service():
    return listar_butacas()

# OBTENER UNA BUTACA
def obtener_butaca_service(id_butaca):
    butaca = obtener_butaca(id_butaca)
    if not butaca:
        raise ValueError("Butaca no encontrada")
    return butaca

# CREAR BUTACA
def crear_butaca_service(data):
    required = ["id_sala", "fila", "numero"]
    for campo in required:
        if campo not in data:
            raise ValueError(f"{campo} es obligatorio")
    
    new_id = crear_butaca(data)
    return {"id": new_id}

# EDITAR BUTACA
def editar_butaca_service(id_butaca, data):
    if not data:
        raise ValueError("No hay datos para actualizar")
    
    if "fila" in data and not data["fila"]:
        raise ValueError("La fila no puede estar vacía")
    if "numero" in data and not data["numero"]:
        raise ValueError("El número no puede estar vacío")
    
    updated = editar_butaca(id_butaca, data)
    if not updated:
        raise ValueError("No se pudo actualizar la butaca")
    
    return True

# BORRAR BUTACA
def borrar_butaca_service(id_butaca):
    return borrar_butaca(id_butaca)
from repositories.entradas_repo import (
    crear_entrada,
    editar_entrada,
    listar_entradas,
    obtener_entrada,
    borrar_entrada
)

# crear entrada
def crear_entrada_service(data):
    required = ["id_user", "id_funcion", "id_butaca", "precio_final"]
    for campo in required:
        if campo not in data:
            raise ValueError(f"{campo} es obligatorio")

    if data["precio_final"] <= 0:
        raise ValueError("El precio debe ser mayor a 0")

    new_id = crear_entrada(data)
    return {"id": new_id}

# editar entrada
def editar_entrada_service(id_entrada, data):
    if not data:
        raise ValueError("No hay datos para actualizar")

    if "precio_final" in data and data["precio_final"] <= 0:
        raise ValueError("El precio debe ser mayor a 0")

    updated = editar_entrada(id_entrada, data)
    if not updated:
        raise ValueError("Nada para actualizar")

    return True

# listar entradas 
def listar_entradas_service(id_user=None):
    return listar_entradas(id_user)

# obtener entrada específica
def obtener_entrada_service(id_entrada):
    return obtener_entrada(id_entrada)

# borrar entrada
def borrar_entrada_service(id_entrada):
    return borrar_entrada(id_entrada)
from repositories.funciones_repo import (
    listar_funciones,
    obtener_funcion,
    crear_funcion,
    editar_funcion,
    borrar_funcion,
    listar_funciones_por_pelicula_repo
)

# LISTAR FUNCIONES
def listar_funciones_service():
    return listar_funciones()

# OBTENER FUNCIÓN ESPECÍFICA
def obtener_funcion_service(id_funcion):
    funcion = obtener_funcion(id_funcion)
    if not funcion:
        raise ValueError("Función no encontrada")
    return funcion

# CREAR FUNCIÓN
def crear_funcion_service(data):
    required = ["id_pelicula", "id_sala", "fecha", "precio_base"]
    for campo in required:
        if campo not in data:
            raise ValueError(f"{campo} es obligatorio")

    if data["precio_base"] <= 0:
        raise ValueError("El precio base debe ser mayor a 0")

    new_id = crear_funcion(data)
    return {"id": new_id}

# EDITAR FUNCIÓN
def editar_funcion_service(id_funcion, data):
    if not data:
        raise ValueError("No hay datos para actualizar")

    if "precio_base" in data and data["precio_base"] <= 0:
        raise ValueError("El precio base debe ser mayor a 0")

    updated = editar_funcion(id_funcion, data)
    if not updated:
        raise ValueError("No se pudo actualizar la función")

    return True

# BORRAR FUNCIÓN
def borrar_funcion_service(id_funcion):
    return borrar_funcion(id_funcion)

def listar_funciones_por_pelicula_service(id_pelicula):
    return listar_funciones_por_pelicula_repo(id_pelicula)
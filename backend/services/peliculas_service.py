from repositories.peliculas_repo import (
    get_all_peliculas,
    get_pelicula_by_id,
    create_pelicula,
    update_pelicula,
    delete_pelicula
)

def listar_peliculas():
    return get_all_peliculas()

def obtener_pelicula(id):
    return get_pelicula_by_id(id)

def agregar_pelicula(data):
    # Convertir tipos correctamente
    try:
        duracion = int(data.get("duracion"))
    except:
        raise ValueError("La duración debe ser un número entero")

    if duracion <= 0:
        raise ValueError("La duración debe ser mayor a 0")

    # titulo = data.get("titulo")
    # genero = data.get("genero")
    # sinopsis = data.get("sinopsis")
    # imagen_url = data.get("imagen_url")
    create_pelicula(data)

def modificar_pelicula(id, data):
    return update_pelicula(id, data)

def eliminar_pelicula(id):
    return delete_pelicula(id)
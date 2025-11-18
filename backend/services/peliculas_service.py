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
    # ejemplo de lógica extra:
    if data.get("duracion") <= 0:
        raise ValueError("Duración inválida")
    create_pelicula(data)

def modificar_pelicula(id, data):
    return update_pelicula(id, data)

def eliminar_pelicula(id):
    return delete_pelicula(id)


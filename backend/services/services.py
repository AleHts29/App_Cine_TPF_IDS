from repositories.repositorio import(
    butacas_segun_idpelicula
)


# TRAE LAS BUTACAS DE UNA PELICULA
def butacas_segun_pelicula(id):
    return butacas_segun_idpelicula(int(id))
    
    
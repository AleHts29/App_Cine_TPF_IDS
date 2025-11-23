from flask import Blueprint, jsonify, request

from services.peliculas_service import (
    listar_peliculas,
    obtener_pelicula,
    agregar_pelicula,
    modificar_pelicula,
    eliminar_pelicula,
    crear_pelicula_completa_service
)


peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route("/", methods=["GET"])
def get_peliculas():
    """
    Obtener todas las películas
    ---
    tags:
      - Películas
    responses:
      200:
        description: Lista de películas
        examples:
          application/json:
            - id: 1
              titulo: Matrix
              duracion: 120
              genero: Ciencia Ficción
              sinopsis: Viaje dentro de la simulación
              estado: en_cartelera
    """
    peliculas = listar_peliculas()   # obtenés la lista real
    print(f"data desde backend: {peliculas}")  # 🔹 ahora sí imprime el contenido
    return jsonify(peliculas)        # devolvés la respuesta JSON


@peliculas_bp.route("/<int:id_pelicula>", methods=["GET"])
def get_pelicula(id_pelicula):
    """
    Obtener una película por ID
    ---
    tags:
      - Películas
    parameters:
      - name: id_pelicula
        in: path
        required: true
        type: integer
        description: ID de la película
    responses:
      200:
        description: Película encontrada
      404:
        description: Película no encontrada
    """
    pelicula = obtener_pelicula(id_pelicula)
    if not pelicula:
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify(pelicula)

@peliculas_bp.route("/", methods=["POST"])
def post_pelicula():
    """
    Crear una nueva película
    ---
    tags:
      - Películas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: NuevaPelicula
          required:
            - titulo
            - duracion
          properties:
            titulo:
              type: string
            duracion:
              type: integer
            genero:
              type: string
            sinopsis:
              type: string
            estado:
              type: string
              enum: ['en_cartelera', 'proximamente', 'finalizada']
    responses:
      201:
        description: Película creada correctamente
      400:
        description: Datos inválidos
    """
    data = request.json
    try:
        agregar_pelicula(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Película creada correctamente"}), 201


@peliculas_bp.route("/pelicula-funcion", methods=["POST"])
def crear_pelicula_completa():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    try:
        result = crear_pelicula_completa_service(data)
        return jsonify(result), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@peliculas_bp.route("/<int:id_pelicula>", methods=["PUT"])
def put_pelicula(id_pelicula):
    """
    Modificar una película existente
    ---
    tags:
      - Películas
    parameters:
      - name: id_pelicula
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          id: ModificarPelicula
          properties:
            titulo:
              type: string
            duracion:
              type: integer
            genero:
              type: string
            sinopsis:
              type: string
            estado:
              type: string
              enum: ['en_cartelera', 'proximamente', 'finalizada']
    responses:
      200:
        description: Película actualizada correctamente
      404:
        description: Película no encontrada
    """
    if not modificar_pelicula(id_pelicula, request.json):
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify({"message": "Película actualizada correctamente"}), 200

@peliculas_bp.route("/<int:id_pelicula>", methods=["DELETE"])
def delete_pelicula(id_pelicula):
    """
    Eliminar una película por ID
    ---
    tags:
      - Películas
    parameters:
      - name: id_pelicula
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Película eliminada correctamente
      404:
        description: Película no encontrada
    """
    if not eliminar_pelicula(id_pelicula):
        return jsonify({"error": "Película no encontrada"}), 404
    return jsonify({"message": "Película eliminada correctamente"}), 200



from flask import Flask, render_template, request, jsonify
import requests
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = "static/img"




@app.route('/')
def home():
    return render_template('index.html')


"""*
*
* PELICULAS
*
"""
@app.route('/cartelera')
def cartelera():
    try:
        response = requests.get("http://localhost:9090/peliculas")
        response.raise_for_status()  

        peliculas = response.json()  
        print(f"data desde backend: {peliculas}")
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        peliculas = []  

    
    return render_template('cartelera.html', peliculas=peliculas, active_page='cartelera')


"""*
*
* MGMT USERs
*
"""
@app.route('/login')
def login():
    return render_template('auth/login.html', active_page='logueo')

@app.route('/register')
def register():
    return render_template('auth/register.html', active_page='registro')


"""*
*
* BUTACAS
*
"""
@app.route('/butacas')
def butacas():
    return render_template('butacas.html',active_page='butacas')


"""*
*
* ADMIN
*
"""
@app.route('/admin')
def admin():
    try:
        response = requests.get("http://localhost:6000/users")
        response.raise_for_status()  

        usuarios = response.json()  
        print(f"data desde backend: {usuarios}")
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        usuarios = []  

    
    return render_template('admin.html', usuarios=usuarios, active_page='admin')


@app.route("/admin/peliculas/nueva", methods=["POST"])
def nueva_pelicula():
    titulo = request.form.get("titulo")
    duracion = request.form.get("duracion")
    genero = request.form.get("genero")
    sinopsis = request.form.get("sinopsis")

    # === 1) GUARDAR IMAGEN EN FRONTEND ===
    file = request.files.get("imagen")
    image_url = None

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = f"/img/{filename}"

    # === 2) ARMAR PAYLOAD PARA EL BACKEND ===
    payload = {
        "titulo": titulo,
        "duracion": duracion,
        "genero": genero,
        "sinopsis": sinopsis,
        "imagen_url": image_url
    }

    # === 3) ENVIAR REQUEST AL BACKEND ===
    backend_url = "http://localhost:9090/peliculas"
    try:
        response = requests.post(backend_url, json=payload)
    except Exception as e:
        return jsonify({"error": "Backend no disponible", "details": str(e)}), 500

    # === 4) PROCESAR RESPUESTA ===
    if response.status_code >= 400:
        return jsonify({
            "error": "Error al crear película en backend",
            "details": safe_json(response)
        }), response.status_code

    # === 5) RESPUESTA CORRECTA ===
    return jsonify({
        "message": "Película creada correctamente desde frontend",
        "backend_response": response.json()
    }), 201

@app.route("/admin/peliculas/lista")
def admin_lista_peliculas():
    resp = requests.get("http://localhost:9090/peliculas")
    peliculas = resp.json()
    return jsonify(peliculas)


@app.route("/admin/peliculas/<int:id>")
def admin_get_pelicula(id):
    resp = requests.get(f"http://localhost:9090/peliculas/{id}")
    return jsonify(resp.json())

@app.route("/admin/peliculas/<int:id>", methods=["DELETE"])
def admin_delete_pelicula(id):
    resp = requests.delete(f"http://localhost:9090/peliculas/{id}")
    return jsonify(resp.json()), resp.status_code

@app.route("/admin/peliculas/<int:id>", methods=["PUT"])
def admin_update_pelicula(id):
    data = {}

    # Datos del formulario
    data["titulo"] = request.form.get("titulo")
    data["duracion"] = request.form.get("duracion")
    data["genero"] = request.form.get("genero")
    data["sinopsis"] = request.form.get("sinopsis")
    data["estado"] = request.form.get("estado")

    # Imagen actual enviada desde el front
    imagen_actual = request.form.get("imagen_actual")

    # Archivo enviado (si existe)
    file = request.files.get("imagen")

    if file and file.filename.strip() != "":
        # Se subió nueva imagen → reemplazar
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        imagen_url = f"img/{filename}"
    else:
        # NO se subió imagen → mantener la actual
        imagen_url = imagen_actual

   
    data["imagen_url"] = imagen_url

    # Enviar al backend real
    resp = requests.put(f"http://localhost:9090/peliculas/{id}", json=data)

    # Manejo respuesta
    return jsonify(resp.json()), resp.status_code



def safe_json(resp):
    try:
        return resp.json()
    except ValueError:
        return resp.text

if __name__ == '__main__':
    app.run(debug=True,port=8080)
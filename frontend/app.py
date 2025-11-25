from flask import Flask, render_template, request, jsonify, redirect
import requests
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = "static/img"

# =====================================
# HOME
# =====================================

@app.route('/')
def home():
    return render_template('index.html')

# =====================================
# PELICULAS
# =====================================

@app.route('/cartelera')
def cartelera():
    try:
        response = requests.get("http://localhost:9090/peliculas")
        response.raise_for_status()
        peliculas = response.json()
    except Exception:
        peliculas = []
    return render_template('cartelera.html', peliculas=peliculas, active_page='cartelera')


@app.route("/funciones")
def funciones():
    id_pelicula = request.args.get("pelicula")
    resp = requests.get(f"http://localhost:9090/funciones/pelicula/{id_pelicula}")
    return render_template("funciones.html", funciones=resp.json(), id_pelicula=id_pelicula)


@app.route("/reservas/nueva", methods=["POST"])
def nueva_reserva():
    resp = requests.post("http://localhost:9090/reservas", json=request.json)
    return jsonify(resp.json()), resp.status_code


@app.route("/reservas/pendiente", methods=["POST"])
def reservar_butacas():
    resp = requests.post("http://localhost:9090/reservas/pendiente", json=request.json)
    data = resp.json()
    if resp.status_code != 201:
        return f"Error creando reserva: {data.get('error')}", 400
    return jsonify(data), resp.status_code


@app.route("/reservas/comprar", methods=["POST"])
def comprar_butacas():
    resp = requests.post("http://localhost:9090/reservas/comprar", json=request.json)
    data_resp = resp.json()
    if resp.status_code != 201:
        return jsonify({"error": data_resp.get("error")}), resp.status_code
    return jsonify(data_resp), resp.status_code


@app.route("/confirmacion/<int:id_reserva>")
def confirmacion(id_reserva):
    try:
        reserva = requests.get(f"http://localhost:9090/reservas/{id_reserva}").json()
    except Exception:
        reserva = None
    return render_template("reserva.html", id_reserva=id_reserva, reserva=reserva)


@app.route("/pago/<int:id_reserva>")
def pago(id_reserva):
    try:
        reserva = requests.get(f"http://localhost:9090/reservas/{id_reserva}").json()
        precio = float(reserva["precio_base"])
        reserva["total"] = precio * len(reserva["butacas"])
    except Exception:
        reserva = None
    return render_template("pago.html", reserva=reserva, id_reserva=id_reserva)


@app.route("/reservas/completar_pago", methods=["POST"])
def completar_pago():
    resp = requests.post("http://localhost:9090/reservas/completar_pago", json=request.json)
    return jsonify(resp.json()), resp.status_code


# =====================================
# AUTH
# =====================================

@app.route('/login')
def login():
    return render_template('auth/login.html', active_page='logueo')


@app.route('/register')
def register():
    return render_template('auth/register.html', active_page='registro')


# =====================================
# ADMIN (UNIFICADO)
# =====================================

@app.route('/admin/<tipo>')
def admin(tipo='usuarios'):
    try:
        datos = requests.get(f"http://localhost:9090/{tipo}").json()
    except Exception:
        datos = []
    return render_template('admin.html', tipo=tipo, datos=datos)


@app.route('/admin/desactivar/<int:id_usuario>')
def desactivar_usuario(id_usuario):
    requests.patch(f"http://localhost:9090/usuarios/desactivar/{id_usuario}")
    usuarios = requests.get("http://localhost:9090/usuarios").json()
    return render_template('admin.html', tipo='usuarios', datos=usuarios)


@app.route('/admin/activar/<int:id_usuario>')
def activar_usuario(id_usuario):
    requests.patch(f"http://localhost:9090/usuarios/activar/{id_usuario}")
    usuarios = requests.get("http://localhost:9090/usuarios").json()
    return render_template('admin.html', tipo='usuarios', datos=usuarios)


@app.route('/admin/borrar/<int:id_usuario>')
def borrar_usuario(id_usuario):
    requests.patch(f"http://localhost:9090/usuarios/borrar/{id_usuario}")
    usuarios = requests.get("http://localhost:9090/usuarios").json()
    return render_template('admin.html', tipo='usuarios', datos=usuarios)


# =====================================
# BUTACAS
# =====================================

@app.route("/butacas/funciones/<int:id_funcion>/pelicula/<int:id_pelicula>")
def butacas_funcion(id_funcion, id_pelicula):
    resp = requests.get(f"http://localhost:9090/butacas/funciones/{id_funcion}/pelicula/{id_pelicula}")
    return jsonify(resp.json()), resp.status_code


@app.route('/butacas')
def butacas():
    return render_template(
        'butacas.html',
        id_pelicula=request.args.get("pelicula"),
        id_funcion=request.args.get("funcion"),
        active_page='butacas'
    )


# =======================================================
# PANEL ADMIN ALTERNATIVO (RENOMBRADO, PARA EVITAR CHOQUE)
# =======================================================

@app.route('/admin-panel')
def admin_panel():
    try:
        usuarios = requests.get("http://localhost:6000/users").json()
    except Exception:
        usuarios = []
    return render_template('admin.html', usuarios=usuarios, active_page='admin')


# =====================================
# PELICULAS ADMIN
# =====================================

@app.route("/admin/peliculas/nueva", methods=["POST"])
def nueva_pelicula():
    titulo = request.form.get("titulo")
    duracion = request.form.get("duracion")
    genero = request.form.get("genero")
    sinopsis = request.form.get("sinopsis")

    file = request.files.get("imagen")
    image_url = None

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = f"/img/{filename}"

    payload = {
        "titulo": titulo,
        "duracion": duracion,
        "genero": genero,
        "sinopsis": sinopsis,
        "imagen_url": image_url
    }

    response = requests.post("http://localhost:9090/peliculas", json=payload)

    if response.status_code >= 400:
        return jsonify({"error": "Error en backend", "details": safe_json(response)}), response.status_code

    return jsonify({"message": "Película creada", "backend": response.json()}), 201


@app.route("/admin/peliculas/lista")
def admin_lista_peliculas():
    return jsonify(requests.get("http://localhost:9090/peliculas").json())


@app.route("/admin/peliculas/<int:id>")
def admin_get_pelicula(id):
    return jsonify(requests.get(f"http://localhost:9090/peliculas/{id}").json())


@app.route("/admin/peliculas/<int:id>", methods=["DELETE"])
def admin_delete_pelicula(id):
    resp = requests.delete(f"http://localhost:9090/peliculas/{id}")
    return jsonify(resp.json()), resp.status_code


@app.route("/admin/peliculas/<int:id>", methods=["PUT"])
def admin_update_pelicula(id):
    data = {
        "titulo": request.form.get("titulo"),
        "duracion": request.form.get("duracion"),
        "genero": request.form.get("genero"),
        "sinopsis": request.form.get("sinopsis"),
        "estado": request.form.get("estado"),
    }

    imagen_actual = request.form.get("imagen_actual")
    file = request.files.get("imagen")

    if file and file.filename.strip():
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        data["imagen_url"] = f"img/{filename}"
    else:
        data["imagen_url"] = imagen_actual

    resp = requests.put(f"http://localhost:9090/peliculas/{id}", json=data)
    return jsonify(resp.json()), resp.status_code


def safe_json(resp):
    try:
        return resp.json()
    except:
        return resp.text


if __name__ == '__main__':
    app.run(debug=True, port=8080)

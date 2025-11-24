from flask import Flask, render_template, request, redirect, url_for, make_response, session, jsonify, redirect,current_app
import requests
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from zoneinfo import ZoneInfo
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "123456"
UPLOAD_FOLDER = "static/img"

@app.route("/")
def home():

    tz = ZoneInfo("America/Argentina/Buenos_Aires")
    ahora = datetime.now(tz)                
    hoy = datetime.now(tz).date()
    hoy_legible = datetime.now(tz).strftime("%d/%m/%Y")

    token = request.cookies.get("token")
    username = None
    email = None
    r_name = None
    admin = None
    
    if token:
        try:
            response = requests.get(
                "http://localhost:9090/usuarios/me",
                cookies={"token": token}
            )
            if response.ok:
                username = response.json().get("username")
                email = response.json().get("email")
                r_name = response.json().get("full_name")
                admin = response.json().get("is_admin")
        except:
            pass

    
    carpeta = os.path.join(current_app.root_path, "static", "images", "slider")

    imagenes = []

    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                imagenes.append("images/slider/" + archivo)
    

    response = requests.get("http://localhost:9090/peliculas").json()
    
    proximamente = [p for p in response if p["estado"] == "proximamente"]
    resp = requests.get("http://localhost:9090/funciones")
    funciones = resp.json()
    resp=requests.get("http://localhost:9090/peliculas")
    peliculas= resp.json()

    formato_backend = "%a, %d %b %Y %H:%M:%S %Z"

    funciones_hoy = []
    for f in funciones:
        fecha_hora = f.get("fecha_hora")
        if fecha_hora:
            f["fecha_hora"] = datetime.strptime(fecha_hora, formato_backend).date()
            if f["fecha_hora"] == hoy:
                funciones_hoy.append(f)
        else:
            f["fecha_hora"] = None
           
    peliculas_ids_hoy = {f["id_pelicula"] for f in funciones_hoy}  
  
    peliculas_hoy = [p for p in peliculas if p["id_pelicula"] in peliculas_ids_hoy]

    return render_template(
        "index.html",
        username=username,
        email=email,
        r_name=r_name,
        imagenes=imagenes,
        proximamente=proximamente,
        peliculas=peliculas_hoy, 
        hoy=hoy,
        hoy_legible=hoy_legible
    )


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

@app.route("/funciones")
def funciones():
    id_pelicula = request.args.get("pelicula")

    # pedir funciones al backend Java
    resp = requests.get(f"http://localhost:9090/funciones/pelicula/{id_pelicula}")

    funciones = resp.json()

    return render_template(
        "funciones.html",
        funciones=funciones,
        id_pelicula=id_pelicula
    )

@app.route("/reservas/nueva", methods=["POST"])
def nueva_reserva():
    data = request.json
    resp = requests.post("http://localhost:9090/reservas", json=data)
    return jsonify(resp.json()), resp.status_code


@app.route("/reservas/pendiente", methods=["POST"])
def reservar_butacas():
    data = request.json
    resp = requests.post("http://localhost:9090/reservas/pendiente", json=data)
    data = resp.json()

    if resp.status_code != 201:
        return f"Error creando reserva: {data.get('error')}", 400
    return jsonify(resp.json()), resp.status_code


@app.route("/reservas/comprar", methods=["POST"])
def comprar_butacas():
    data = request.json

    resp = requests.post("http://localhost:9090/reservas/comprar", json=data)
    data_resp = resp.json()

    if resp.status_code != 201:
        return jsonify({"error": data_resp.get("error")}), resp.status_code

    return jsonify(data_resp), resp.status_code


@app.route("/confirmacion/<int:id_reserva>")
def confirmacion(id_reserva):
    try:
        resp = requests.get(f"http://localhost:9090/reservas/{id_reserva}")
        resp.raise_for_status()
        reserva = resp.json()
    except Exception as e:
        print(f"Error consultando reserva: {e}")
        reserva = None

    return render_template(
        "reserva.html",
        id_reserva=id_reserva,
        reserva=reserva,
        active_page="reserva"
    )

@app.route("/pago/<int:id_reserva>")
def pago(id_reserva):
    try:
        resp = requests.get(f"http://localhost:9090/reservas/{id_reserva}")
        resp.raise_for_status()
        reserva = resp.json()
         # Convertir precio_base a número
        precio = float(reserva["precio_base"])

        # Calcular total
        reserva["total"] = precio * len(reserva["butacas"])
    
    except Exception:
        reserva = None

    return render_template(
        "pago.html",
        reserva=reserva,
        id_reserva=id_reserva
    )

@app.route("/reservas/completar_pago", methods=["POST"])
def completar_pago():
    data = request.get_json()
    resp = requests.post("http://localhost:9090/reservas/completar_pago", json=data)
    return jsonify(resp.json()), resp.status_code


"""*
*
* MGMT USERs
*
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            response = requests.post(
                "http://localhost:9090/usuarios/login",
                json={"email": email, "password": password}
            )

            if response.ok:
                data = response.json()
                token = data.get("token")

                resp = make_response(redirect(url_for("home")))
                resp.set_cookie("token", token)
                return resp
            else:
                error_msg = response.json().get("error", "Credenciales incorrectas")
                return render_template("auth/login.html", error=error_msg)

        except requests.exceptions.RequestException:
            return render_template("auth/login.html", error="Error de conexión con el backend")

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("home")))
    resp.set_cookie("token", "", expires=0)
    return resp


@app.route('/register')
def register():
    return render_template('auth/register.html', active_page='registro')

@app.route('/usuarios/', methods=['POST'])
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json(force=True)
    resp = requests.post("http://localhost:9090/usuarios", json=data)
    data = resp.json()

    if resp.status_code != 201:
        return f"Error creando usuario: {data.get('error')}", 400
    return jsonify(data), resp.status_code

@app.route('/usuarios/status/<int:user_id>', methods=['GET'])
def status_usuario(user_id):
    url = f"http://localhost:9090/usuarios/status/{user_id}"
    resp = requests.get(url)
    data = resp.json()

    if resp.status_code != 200:
        return f"Error en el polling en flask: {data.get('error')}", 400
    return jsonify(data), resp.status_code


"""*
*
* BUTACAS
*
"""
@app.route("/butacas/funciones/<int:id_funcion>/pelicula/<int:id_pelicula>")
def butacas_funcion(id_funcion, id_pelicula):
    resp = requests.get(f"http://localhost:9090/butacas/funciones/{id_funcion}/pelicula/{id_pelicula}")
    return jsonify(resp.json()), resp.status_code

@app.route('/butacas')
def butacas():
    id_pelicula = request.args.get("pelicula")
    id_funcion = request.args.get("funcion")

    return render_template(
        'butacas.html',
        id_pelicula=id_pelicula,
        id_funcion=id_funcion,
        active_page='butacas'
    )


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
    director = request.form.get("director")
    estado = request.form.get("estado")

    # === 1) GUARDAR IMAGEN EN FRONTEND ===
    file = request.files.get("imagen")
    image_url = None

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = f"/img/{filename}"

    # --- OBTENER FUNCIONES DEL FORM ---
    salas = request.form.getlist("funcion_sala[]")
    fechas = request.form.getlist("funcion_fecha[]")
    precios = request.form.getlist("funcion_precio[]")

    funciones = []
    for sala, fecha, precio in zip(salas, fechas, precios):
        funciones.append({
            "id_sala": int(sala),
            "fecha": fecha,
            "precio_base": float(precio)
    })

    # === 2) ARMAR PAYLOAD PARA EL BACKEND ===
    payload = {
        "titulo": titulo,
        "duracion": int(duracion),
        "genero": genero,
        "sinopsis": sinopsis,
        "director": director,
        "imagen_url": image_url,
        "estado": estado,
        "funciones": funciones
    }

    # === 3) ENVIAR REQUEST AL BACKEND ===
    backend_url = "http://localhost:9090/peliculas/pelicula-funcion"
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
    data["director"] = request.form.get("director")
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
    app.run(debug=True, port=8080)
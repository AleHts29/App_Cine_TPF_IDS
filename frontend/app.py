from flask import Flask, render_template, request, redirect, url_for, make_response, session, jsonify, current_app
import requests
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from zoneinfo import ZoneInfo
from auth_utils import get_current_user

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "123456"
UPLOAD_FOLDER = "static/img"





@app.context_processor
def inject_user():
    user = get_current_user(request)

    return dict(
        user=user,
        idUsuario=user.get("id_user") if user else None, 
        username=user.get("username") if user else None,
        email=user.get("email") if user else None,
        full_name=user.get("full_name") if user else None,
        admin=user.get("is_admin") if user else None,
        activo=user.get("is_active") if user else None,
        foto=user.get("profile_image") if user else None
    )





@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")




@app.route("/")
def home():
    tz = ZoneInfo("America/Argentina/Buenos_Aires")
    hoy = datetime.now(tz).date()
    hoy_legible = datetime.now(tz).strftime("%d/%m/%Y")

    carpeta = os.path.join(current_app.root_path, "static", "images", "slider")
    imagenes = [f"images/slider/{f}" for f in os.listdir(carpeta)
                if os.path.isfile(os.path.join(carpeta, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))] if os.path.exists(carpeta) else []

    peliculas = requests.get("http://localhost:9090/peliculas").json()
    proximamente = [p for p in peliculas if p["estado"] == "proximamente"]

    funciones = requests.get("http://localhost:9090/funciones").json()
    formato_backend = "%a, %d %b %Y %H:%M:%S %Z"

    funciones_hoy = []
    for f in funciones:
        fecha_hora = f.get("fecha_hora")
        if fecha_hora:
            f["fecha_hora"] = datetime.strptime(fecha_hora, formato_backend).date()
            if f["fecha_hora"] == hoy:
                funciones_hoy.append(f)

    peliculas_ids_hoy = {f["id_pelicula"] for f in funciones_hoy}
    peliculas_hoy = [p for p in peliculas if p["id_pelicula"] in peliculas_ids_hoy]

    return render_template(
        "index.html",
        imagenes=imagenes,
        proximamente=proximamente,
        peliculas=peliculas_hoy,
        hoy=hoy,
        hoy_legible=hoy_legible
    )


@app.route('/cartelera')
def cartelera():

    tz = ZoneInfo("America/Argentina/Buenos_Aires")
    hoy = datetime.now(tz)

    try:
        response = requests.get("http://localhost:9090/peliculas")
        response.raise_for_status()
        peliculas = response.json()
    except:
        peliculas = []

    peliculas_filtradas = []
    formato_backend = "%a, %d %b %Y %H:%M:%S %Z"

    for p in peliculas:
        resp = requests.get(f"http://localhost:9090/funciones/pelicula/{p['id_pelicula']}")
        funciones = resp.json()

        funciones_futuras = []

        for f in funciones:
            fecha_raw = f.get("fecha_hora")
            if not fecha_raw:
                continue
            
            try:
                fecha_dt = datetime.strptime(fecha_raw, formato_backend).replace(tzinfo=tz)
            except:
                continue
            
            if fecha_dt >= hoy:
                funciones_futuras.append(f)

        if funciones_futuras:
            peliculas_filtradas.append(p)

    return render_template('cartelera.html', peliculas=peliculas_filtradas, active_page='cartelera')


@app.route("/funciones")
def funciones():
    id_pelicula = request.args.get("pelicula")
    resp = requests.get(f"http://localhost:9090/funciones/pelicula/{id_pelicula}")
    return render_template("funciones.html", funciones=resp.json(), id_pelicula=id_pelicula)


@app.route("/api/funciones")
def api_funciones():
    id_pelicula = request.args.get("pelicula")
    if not id_pelicula:
        return jsonify({"error": "Falta parámetro 'pelicula'"}), 400

    resp = requests.get(f"http://localhost:9090/funciones/pelicula/{id_pelicula}")
    if resp.status_code != 200:
        return jsonify({"error": "Backend error"}), 500
    return jsonify(resp.json())

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
    except:
        reserva = None
    return render_template("reserva.html", id_reserva=id_reserva, reserva=reserva)

@app.route("/pago/<int:id_reserva>")
def pago(id_reserva):
    try:
        reserva = requests.get(f"http://localhost:9090/reservas/{id_reserva}").json()
        precio = float(reserva["precio_base"])
        reserva["total"] = precio * len(reserva["butacas"])
    except:
        reserva = None
    return render_template("pago.html", reserva=reserva, id_reserva=id_reserva)

@app.route("/reservas/completar_pago", methods=["POST"])
def completar_pago():
    resp = requests.post("http://localhost:9090/reservas/completar_pago", json=request.json)
    return jsonify(resp.json()), resp.status_code


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
                token = response.json().get("token")
                resp = make_response(redirect(url_for("home")))
                resp.set_cookie("token", token)
                return resp
            else:
                error_msg = response.json().get("error", "Credenciales incorrectas")
                return render_template("auth/login.html", error=error_msg)
        except:
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

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json(force=True)
    resp = requests.post("http://localhost:9090/usuarios", json=data)
    if resp.status_code != 201:
        return f"Error creando usuario: {resp.json().get('error')}", 400
    return jsonify(resp.json()), resp.status_code

@app.route('/usuarios/status/<int:user_id>', methods=['GET'])
def status_usuario(user_id):
    resp = requests.get(f"http://localhost:9090/usuarios/status/{user_id}")
    if resp.status_code != 200:
        return f"Error en el polling en flask: {resp.json().get('error')}", 400
    return jsonify(resp.json()), resp.status_code

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        email = request.form.get("email")
        try:
            response = requests.post("http://localhost:9090/usuarios/password", json={"email": email})
            data = response.json()
            if response.ok:
                return render_template('auth/password.html', message=data["message"])
            return render_template('auth/password.html', error=data.get("error"))
        except:
            return render_template('auth/password.html', error="Error conectando con backend")
    return render_template('auth/password.html', active_page='password')

@app.route("/password/new", methods=["GET", "POST"])
def new_password():
    if request.method == "GET":
        token = request.args.get("token")
        return render_template("auth/new_password.html", token=token, active_page='new_password')

    token = request.form.get("token")
    password = request.form.get("password")
    password_confirm = request.form.get("c-password")
    if not token:
        return render_template("auth/new_password.html", token=None, error="Token faltante")
    if password != password_confirm:
        return render_template("auth/new_password.html", token=token, error="Las contraseñas no coinciden")
    if len(password) < 6:
        return render_template("auth/new_password.html", token=token, error="La contraseña es muy corta")
    try:
        resp = requests.post("http://localhost:9090/usuarios/password/reset", json={"token": token, "password": password})
        if resp.ok:
            return render_template("auth/new_password.html", token=token, message=resp.json()["message"])
        return render_template("auth/new_password.html", token=token, error=resp.json().get("error"))
    except:
        return render_template("auth/new_password.html", token=token, error="Error conectando con backend")


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


@app.route('/admin')
def admin():
    tipo = request.args.get('tipo', 'usuarios')
    
    try:
        datos = requests.get(f"http://localhost:9090/{tipo}").json()
    except Exception:
        datos = []

    return render_template('admin.html', tipo=tipo, datos=datos, active_page='admin')



@app.route('/admin/desactivar/<int:id_usuario>')
def desactivar_usuario(id_usuario):
    requests.patch(f"http://localhost:9090/usuarios/desactivar/{id_usuario}")
    return redirect(url_for('admin', tipo='usuarios'))

@app.route('/admin/activar/<int:id_usuario>')
def activar_usuario(id_usuario):
    requests.patch(f"http://localhost:9090/usuarios/activar/{id_usuario}")
    return redirect(url_for('admin', tipo='usuarios'))

@app.route('/admin/borrar/<int:id_usuario>')
def borrar_usuario(id_usuario):
    requests.patch(f"http://localhost:9090/usuarios/borrar/{id_usuario}")
    return redirect(url_for('admin', tipo='usuarios'))

@app.route("/admin/peliculas/nueva", methods=["POST"])
def nueva_pelicula():
    titulo = request.form.get("titulo")
    duracion = request.form.get("duracion")
    genero = request.form.get("genero")
    sinopsis = request.form.get("sinopsis")
    director = request.form.get("director")
    estado = request.form.get("estado")
    file = request.files.get("imagen")
    image_url = None
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = f"/img/{filename}"

    salas = request.form.getlist("funcion_sala[]")
    fechas = request.form.getlist("funcion_fecha[]")
    precios = request.form.getlist("funcion_precio[]")
    funciones = [{"id_sala": int(s), "fecha": f, "precio_base": float(p)} for s, f, p in zip(salas, fechas, precios)]

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

    try:
        response = requests.post("http://localhost:9090/peliculas/pelicula-funcion", json=payload)
        if response.status_code >= 400:
            return jsonify({"error": "Error en backend"}), response.status_code
        return jsonify({"message": "Película creada", "backend": response.json()}), 201
    except Exception as e:
        return jsonify({"error": "Backend no disponible", "details": str(e)}), 500

@app.route("/admin/peliculas/lista")
def admin_lista_peliculas():
    return jsonify(requests.get("http://localhost:9090/peliculas").json())

@app.route("/admin/peliculas/<int:id>", methods=["GET", "DELETE", "PUT"])
def admin_pelicula(id):
    if request.method == "GET":
        return jsonify(requests.get(f"http://localhost:9090/peliculas/{id}").json())
    elif request.method == "DELETE":
        resp = requests.delete(f"http://localhost:9090/peliculas/{id}")
        return jsonify(resp.json()), resp.status_code
    elif request.method == "PUT":
        data = {
            "titulo": request.form.get("titulo"),
            "duracion": request.form.get("duracion"),
            "genero": request.form.get("genero"),
            "sinopsis": request.form.get("sinopsis"),
            "director": request.form.get("director"),
            "estado": request.form.get("estado"),
        }
        imagen_actual = request.form.get("imagen_actual")
        file = request.files.get("imagen")
        if file and file.filename.strip():
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            data["imagen_url"] = f"/img/{filename}"
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

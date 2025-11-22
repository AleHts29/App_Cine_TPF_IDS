from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "123456"


@app.route("/")
def home():
    token = request.cookies.get("token")
    username = None
    email = None
    r_name = None
    is_admin = None
    
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
                is_admin = response.json().get("is_admin")
        except:
            pass
    
    return render_template("index.html", username=username, email=email, r_name=r_name, admin=is_admin)


@app.route('/cartelera')
def cartelera():
    try:
        response = requests.get("http://localhost:9090/peliculas")
        response.raise_for_status()
        peliculas = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        peliculas = []

    return render_template('cartelera.html', peliculas=peliculas, active_page='cartelera')


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
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)
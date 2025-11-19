from flask import Flask, render_template, request, redirect, url_for, make_response
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "123456"


@app.route("/")
def home():
    token = request.cookies.get("token")
    username = None

    if token:
        try:
            response = requests.get(
                "http://localhost:9090/usuarios/me",
                cookies={"token": token}
            )
            if response.ok:
                username = response.json().get("username")
        except:
            pass
    
    return render_template("index.html", username=username)


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


if __name__ == '__main__':
    app.run(debug=True, port=8080)
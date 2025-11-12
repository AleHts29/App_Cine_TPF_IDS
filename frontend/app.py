from flask import Flask, render_template, session
import requests
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    username = None
    try:
        response = requests.get("http://localhost:9090/usuarios/me", cookies=request.cookies)
        if response.ok:
            data = response.json()
            username = data.get("username")
    except Exception as e:
        print("Error consultando backend:", e)
    
    return render_template("index.html", username=username)


@app.route('/cartelera')
def cartelera():
    try:
        response = requests.get("http://localhost:6000/peliculas")
        response.raise_for_status()  

        peliculas = response.json()  
        print(f"data desde backend: {peliculas}")
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        peliculas = []  

    
    return render_template('cartelera.html', peliculas=peliculas, active_page='cartelera')


@app.route('/login')
def login():
    return render_template('auth/login.html', active_page='logueo')

@app.route('/register')
def register():
    return render_template('auth/register.html', active_page='registro')


if __name__ == '__main__':
    app.run(debug=True,port=8080)
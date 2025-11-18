from flask import Flask, render_template
import requests
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

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


@app.route('/login')
def login():
    return render_template('auth/login.html', active_page='logueo')

@app.route('/register')
def register():
    return render_template('auth/register.html', active_page='registro')

@app.route('/butacas')
def butacas():
    return render_template('butacas.html',active_page='butacas')

@app.route('/admin')
@app.route('/admin/<tipo>')
def admin(tipo='usuarios'):
    try:
        response = requests.get(f"http://localhost:9090/{tipo}")
        response.raise_for_status()
        datos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        datos = []

    return render_template(
        'admin.html',
        tipo=tipo,
        datos=datos
    )



if __name__ == '__main__':
    app.run(debug=True,port=8080)
from flask import Flask, render_template
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cartelera')
def cartelera():
    return render_template('cartelera.html', active_page='cartelera')

@app.route('/login')
def login():
    return render_template('auth/login.html', active_page='logueo')


if __name__ == '__main__':
    app.run(debug=True)
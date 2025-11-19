from flask import Flask, jsonify
from flask_cors import CORS
from routes.peliculas import peliculas_bp
from routes.salas import salas_bp
from routes.funciones import funciones_bp
from routes.usuarios import usuarios_bp
from routes.butacas import butacas_bp
from routes.entradas import entradas_bp
from dotenv import load_dotenv
from flasgger import Swagger
import os
from db import get_connection

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app) 
CORS(app)


# Blueprints
app.register_blueprint(peliculas_bp, url_prefix="/peliculas")
app.register_blueprint(salas_bp, url_prefix="/salas")
app.register_blueprint(butacas_bp, url_prefix="/butacas")
app.register_blueprint(funciones_bp, url_prefix="/funciones")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(entradas_bp, url_prefix="/entradas")

# Test DB connection
conn = get_connection()
if conn and conn.is_connected():
    print("✅ Conectado correctamente a MySQL!")
    conn.close()
else:
    print("❌ No se pudo conectar.")

SERVER_PORT = int(os.getenv("SERVER_PORT", 9090))

@app.route("/")
def home():
    return jsonify({"api": "Cine IDS 2025", "status": "running 🚀"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
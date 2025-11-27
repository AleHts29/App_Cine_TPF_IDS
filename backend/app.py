from flask import Flask, jsonify
from flask_cors import CORS
from routes.peliculas import peliculas_bp
from routes.reservas import reservas_bp
from routes.salas import salas_bp
from routes.funciones import funciones_bp
from routes.usuarios import usuarios_bp
from routes.butacas import butacas_bp
from routes.entradas import entradas_bp
from routes.router import router_bp
from dotenv import load_dotenv
from flasgger import Swagger
import os
import yaml
from db import get_connection

load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.jinja_loader.searchpath.append('../frontend/templates')
CORS(app)
app.secret_key = "123456"

# ----------------------------
# ▶ Cargar todos los YAML del directorio ./swagger automáticamente
# ----------------------------
def load_all_yaml_specs(directory="./swagger"):
    combined_paths = {}
    combined_definitions = {}

    for filename in os.listdir(directory):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            filepath = os.path.join(directory, filename)

            with open(filepath, "r") as f:
                spec = yaml.safe_load(f)

                # MERGE paths
                if "paths" in spec:
                    combined_paths.update(spec["paths"])

                # MERGE definitions
                if "definitions" in spec:
                    combined_definitions.update(spec["definitions"])

    # Plantilla base
    return {
        "swagger": "2.0",
        "info": {
            "title": "API Cine IDS 2025",
            "version": "1.0.0",
            "description": "Documentación completa de API"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": combined_paths,
        "definitions": combined_definitions
    }


swagger_template = load_all_yaml_specs("./swagger")
swagger = Swagger(app, template=swagger_template)


# Blueprints
app.register_blueprint(peliculas_bp, url_prefix="/peliculas")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(salas_bp, url_prefix="/salas")
app.register_blueprint(butacas_bp, url_prefix="/butacas")
app.register_blueprint(funciones_bp, url_prefix="/funciones")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(entradas_bp, url_prefix="/entradas")
app.register_blueprint(router_bp, url_prefix="/router")

# Test DB connection
conn = get_connection()
if conn and conn.is_connected():
    print("✅ Conectado correctamente a MySQL!")
    conn.close()
else:
    print("❌ No se pudo conectar.")

# SERVER_PORT = int(os.getenv("PORT", 9090))

@app.route("/")
def home():
    return jsonify({"api": "Cine IDS 2025", "status": "running 🚀"})

if __name__ == "__main__":
    SERVER_PORT = int(os.environ.get("PORT", 9090))
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config
from flasgger import Swagger  # Agrega la importación de Flasgger
import os

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = config('SECRET_KEY')


swagger = Swagger(app)

db = SQLAlchemy(app)

# Importa las rutas de usuario
from routes.user import user_bp

# Importa la ruta de style
from routes.style import style_bp

# Importa la ruta de autor
from routes.author import author_bp

# Importa la ruta de técnica
from routes.tecnique import tecnique_bp

# Importa la ruta de material
from routes.material import material_bp

# Importa la ruta de attraction
from routes.attraction import attraction_bp

# Importa la ruta de category
from routes.category import category_bp

# Importa la ruta de mac_address
from routes.mac_address import mac_address_bp


# Registra las rutas de usuario
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(style_bp, url_prefix='/style')
app.register_blueprint(author_bp, url_prefix='/author')
app.register_blueprint(tecnique_bp, url_prefix='/tecnique')
app.register_blueprint(material_bp, url_prefix='/material')
app.register_blueprint(attraction_bp, url_prefix='/attraction')
app.register_blueprint(category_bp, url_prefix='/category')
app.register_blueprint(mac_address_bp, url_prefix='/mac_address')



# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
   return jsonify({"messenge": "Ruta no encontrada."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config
from flasgger import Swagger  # Agrega la importación de Flasgger
import os

app = Flask(__name__)
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


# Registra las rutas de usuario
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(style_bp, url_prefix='/style')
app.register_blueprint(author_bp, url_prefix='/author')
app.register_blueprint(tecnique_bp, url_prefix='/tecnique')
app.register_blueprint(material_bp, url_prefix='/material')
app.register_blueprint(attraction_bp, url_prefix='/attraction')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

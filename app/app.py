from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config 

app = Flask(__name__)

app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = config('SECRET_KEY')

db = SQLAlchemy(app)

# Importar las rutas de usuario
from routes.user import user_bp
#Importar la ruta de detalle 
from routes.detail_attraction import detail_attraction_bp
#Importar la ruta de coordenadas
from routes.coordinates import coordinate_bp
#Importar la ruta de style
from routes.style import style_bp

# Registrar las rutas de usuario
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(detail_attraction_bp, url_prefix='/detail_attraction')
app.register_blueprint(coordinate_bp, url_prefix='/coordinate')
app.register_blueprint(style_bp, url_prefix='/style')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
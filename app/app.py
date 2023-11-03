from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config 

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = config('SECRET_KEY')

db = SQLAlchemy(app)

# Importar las rutas de usuario
from routes.user import user_bp

# Registrar las rutas de usuario
app.register_blueprint(user_bp, url_prefix='/user')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
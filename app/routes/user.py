from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['POST'])
def registro():
    data = request.get_json()
    name = data['name']
    password = data['password']
    email = data['email']

    # Hashea la contraseña antes de almacenarla en la base de datos con el método 'pbkdf2:sha256'
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(name=name, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user.id, 'name': user.name, 'token': user.token})
    else:
        return jsonify({'message': 'Credenciales inválidas'})

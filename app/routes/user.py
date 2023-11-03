from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db
from decouple import config 
import jwt

user_bp = Blueprint('user', __name__)
SECRET_KEY = config('SECRET_KEY')

from middleware.middleware import jwt_required


@user_bp.route('/', methods=['POST'])
@jwt_required
def registro(data):
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

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user(data, user_id):
    new_data = request.get_json()

    # Verifica si el usuario existe
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Actualiza la información del usuario
    if 'name' in new_data:
        user.name = new_data['name']
    if 'password' in new_data:
        hashed_password = generate_password_hash(new_data['password'], method='pbkdf2:sha256')
        user.password = hashed_password
    if 'email' in new_data:
        user.email = new_data['email']

    db.session.commit()

    return jsonify({'message': 'Información del usuario actualizada exitosamente'})
    user_id = data['user_id']  # Obtiene el ID del usuario del token JWT
    new_data = request.get_json()

    # Verifica si el usuario existe
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    # Actualiza la información del usuario
    if 'name' in new_data:
        user.name = new_data['name']
    if 'password' in new_data:
        hashed_password = generate_password_hash(new_data['password'], method='pbkdf2:sha256')
        user.password = hashed_password
    if 'email' in new_data:
        user.email = new_data['email']

    db.session.commit()
    
    return jsonify({'message': 'Información del usuario actualizada exitosamente'})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # Genera un nuevo token JWT con el correo del usuario al iniciar sesión
        token = generate_token(email)
        return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user.id, 'name': user.name, 'token': token})
    else:
        return jsonify({'message': 'Credenciales inválidas'})

def generate_token(email):
    payload = {'email': email}
    token = jwt.encode(payload, SECRET_KEY , algorithm='HS256')  
    return token

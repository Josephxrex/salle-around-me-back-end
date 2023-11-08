from flask import Blueprint,  jsonify #request,
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db
from decouple import config 
import jwt


attraction_bp = Blueprint('attraction', __name__)
SECRET_KEY = config('SECRET_KEY')

from middleware.middleware import jwt_required
"""
    Autor: Daniel Ppérez Salgado
    Descripción: CRUD EndPoints de Attraction
    Fecha: 2023-11-01
    """
# Método para crear una atracción
@attraction_bp.route('/', methods=['POST'])
#@jwt_required
def create_attraction(data):
    try:
        data = data.get_json()
        name = data['name']
        img = data['img']
        id_detail = data['id_detail']
        id_category = data['id_category']
        id_author = data['id_author']
        id_coordinates = data['id_coordinates']
        id_mac_address = data['id_mac_address']
        id_user = data['id_user']

        new_attraction = Attraction(name=name, img=img, id_detail=id_detail, id_category=id_category,
                                    id_author=id_author, id_coordinates=id_coordinates,
                                    id_mac_address=id_mac_address, id_user=id_user)
        db.session.add(new_attraction)
        db.session.commit()
        return jsonify({'message': 'Atracción creada exitosamente'}), 200
    except:
        return jsonify({'message': 'Error al crear la atracción'}), 400

# Método para obtener todas las atracciones
@attraction_bp.route('/', methods=['GET'])
#@jwt_required
def get_attractions(data):
    try:
        attractions = Attraction.query.all()
        return jsonify([{'id': attraction.id, 'name': attraction.name, 'img': attraction.img,
                         'id_detail': attraction.id_detail, 'id_category': attraction.id_category,
                         'id_author': attraction.id_author, 'id_coordinates': attraction.id_coordinates,
                         'id_mac_address': attraction.id_mac_address, 'id_user': attraction.id_user}
                        for attraction in attractions]), 200
    except:
        return jsonify({'message': 'Atracciones no encontradas'}), 404

# Método para obtener una atracción por su id
@attraction_bp.route('/<int:id>', methods=['GET'])
#@jwt_required
def get_attraction(data,id):
    try:
        attraction = Attraction.query.get(id)
        if attraction:
            return jsonify({'id': attraction.id, 'name': attraction.name, 'img': attraction.img,
                            'id_detail': attraction.id_detail, 'id_category': attraction.id_category,
                            'id_author': attraction.id_author, 'id_coordinates': attraction.id_coordinates,
                            'id_mac_address': attraction.id_mac_address, 'id_user': attraction.id_user})
        else:
            return jsonify({'message': 'Atracción no encontrada'}), 404
    except:
        return jsonify({'message': 'Error al obtener la atracción'}), 500

# Método para actualizar una atracción por su id
@attraction_bp.route('/<int:id>', methods=['PUT'])
#@jwt_required
def update_attraction(data,id):
    try:
        attraction = Attraction.query.get(id)
        if attraction:
            data = data.get_json()
            attraction.name = data.get('name', attraction.name)
            attraction.img = data.get('img', attraction.img)
            attraction.id_detail = data.get('id_detail', attraction.id_detail)
            attraction.id_category = data.get('id_category', attraction.id_category)
            attraction.id_author = data.get('id_author', attraction.id_author)
            attraction.id_coordinates = data.get('id_coordinates', attraction.id_coordinates)
            attraction.id_mac_address = data.get('id_mac_address', attraction.id_mac_address)
            attraction.id_user = data.get('id_user', attraction.id_user)
            db.session.commit()
            return jsonify({'message': 'Atracción actualizada exitosamente'})
        else:
            return jsonify({'message': 'Atracción no encontrada'}), 404
    except:
        return jsonify({'message': 'Error al actualizar la atracción'}), 500

# Método para eliminar una atracción por su id
@attraction_bp.route('/<int:id>', methods=['DELETE'])
#@jwt_required
def delete_attraction(data,id):
    try:
        attraction = Attraction.query.get(id)
        if attraction:
            db.session.delete(attraction)
            db.session.commit()
            return jsonify({'message': 'Atracción eliminada exitosamente'})
        else:
            return jsonify({'message': 'Atracción no encontrada'}), 404
    except:
        return jsonify({'message': 'Error al eliminar la atracción'}), 500

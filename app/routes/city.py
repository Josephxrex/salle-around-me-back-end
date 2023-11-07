from flask import Blueprint, request, jsonify
from models.city import City
from app import db

city_bp = Blueprint('city', __name__)

from middleware.middleware import jwt_required

@city_bp.route('/', methods=['POST'])
@jwt_required
def create_city():
    try:
        data = request.get_json()
        name = data.get('name')

        new_city = City(name=name)

        db.session.add(new_city)
        db.session.commit()

        return jsonify({'message': 'City creada exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear city: ' + str(e)}), 500


@city_bp.route('/', methods=['GET'])
@jwt_required
def get_citys():
    try:
        citys = City.query.all()
        citys_list = []

        for city in citys:
            city_data = {
                'id': city.id,
                'name': city.name
            }
            citys_list.append(city_data)

        return jsonify(citys_list)

    except Exception as e:
        return jsonify({'error': 'Error al listar city: ' + str(e)}), 500


@city_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_city(id):
    try:
        city = City.query.get(id)

        if city:
            return jsonify({'name': city.name})
        else:
            return jsonify({'message': 'City no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener city: ' + str(e)}), 500


@city_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_city(id):
    try:
        city = City.query.get(id)

        if city:
            data = request.get_json()
            city.name = data.get('name')

            db.session.commit()

            return jsonify({'message': 'City actualizada exitosamente'}), 200
        else:
            return jsonify({'message': 'City no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al actualizar city: ' + str(e)}), 500


@city_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_city(id):
    try:
        city = City.query.get(id)

        if city:
            db.session.delete(city)
            db.session.commit()

            return jsonify({'message': 'City eliminada exitosamente'})
        else:
            return jsonify({'message': 'City no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar city: ' + str(e)}), 500

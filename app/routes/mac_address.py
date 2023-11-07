from flask import Blueprint, request, jsonify
from models.mac_address import Mac_address
from app import db

mac_address_bp = Blueprint('mac_address', __name__)

from middleware.middleware import jwt_required

@mac_address_bp.route('/', methods=['POST'])
@jwt_required
def create_mac_address():
    try:
        data = request.get_json()
        mac_address = data.get('mac_address')

        new_mac_address = Mac_address(mac_address=mac_address)

        db.session.add(new_mac_address)
        db.session.commit()

        return jsonify({'message': 'Mac_address creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear mac_address: ' + str(e)}), 500


@mac_address_bp.route('/', methods=['GET'])
@jwt_required
def get_mac_address():
    try:
        mac_address = Mac_address.query.all()
        mac_address_list = []

        for mac_address in mac_address:
            mac_address_data = {
                'id': mac_address.id,
                'mac_address': mac_address.mac_address
            }
            mac_address_list.append(mac_address_data)

        return jsonify(mac_address_list)

    except Exception as e:
        return jsonify({'error': 'Error al listar los mac_address: ' + str(e)}), 500


@mac_address_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_mac_address(id):
    try:
        mac_address = Mac_address.query.get(id)

        if mac_address:
            return jsonify({'mac_address': mac_address.mac_address})
        else:
            return jsonify({'message': 'mac_address no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener mac_address: ' + str(e)}), 500


@mac_address_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_mac_address(id):
    try:
        mac_address = Mac_address.query.get(id)

        if mac_address:
            data = request.get_json()
            mac_address.mac_address = data.get('mac_address')

            db.session.commit()

            return jsonify({'message': 'mac_address actualizado exitosamente'}), 200
        else:
            return jsonify({'message': 'mac_address no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al actualizar mac_address: ' + str(e)}), 500


@mac_address_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_mac_address(id):
    try:
        mac_address = Mac_address.query.get(id)

        if mac_address:
            db.session.delete(mac_address)
            db.session.commit()

            return jsonify({'message': 'mac_address eliminado exitosamente'})
        else:
            return jsonify({'message': 'mac_address no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar mac_address: ' + str(e)}), 500

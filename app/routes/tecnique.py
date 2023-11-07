from flask import Blueprint, request, jsonify
from models.tecnique import Tecnique
from app import db

tecnique_bp = Blueprint('tecnique', __name__)

from middleware.middleware import jwt_required

@tecnique_bp.route('/', methods=['POST'])
@jwt_required
def create_tecnique():
    try:
        data = request.get_json()
        name = data.get('name')

        new_tecnique = Tecnique(name=name)

        db.session.add(new_tecnique)
        db.session.commit()

        return jsonify({'message': 'Tecnique creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear tecnique: ' + str(e)}), 500


@tecnique_bp.route('/', methods=['GET'])
@jwt_required
def get_tecniques():
    try:
        tecniques = Tecnique.query.all()
        tecniques_list = []

        for tecnique in tecniques:
            tecnique_data = {
                'id': tecnique.id,
                'name': tecnique.name
            }
            tecniques_list.append(tecnique_data)

        return jsonify(tecniques_list)

    except Exception as e:
        return jsonify({'error': 'Error al listar los tecnique: ' + str(e)}), 500


@tecnique_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_tecnique(id):
    try:
        tecnique = Tecnique.query.get(id)

        if tecnique:
            return jsonify({'name': tecnique.name})
        else:
            return jsonify({'message': 'Tecnique no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener tecnique: ' + str(e)}), 500


@tecnique_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_tecnique(id):
    try:
        tecnique = Tecnique.query.get(id)

        if tecnique:
            data = request.get_json()
            tecnique.name = data.get('name')

            db.session.commit()

            return jsonify({'message': 'Tecnique actualizado exitosamente'}), 200
        else:
            return jsonify({'message': 'Tecnique no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al actualizar tecnique: ' + str(e)}), 500


@tecnique_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_tecnique(id):
    try:
        tecnique = Tecnique.query.get(id)

        if tecnique:
            db.session.delete(tecnique)
            db.session.commit()

            return jsonify({'message': 'Tecnique eliminado exitosamente'})
        else:
            return jsonify({'message': 'Tecnique no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar tecnique: ' + str(e)}), 500

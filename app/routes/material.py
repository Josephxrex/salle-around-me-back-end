from flask import Blueprint, request, jsonify
from models.material import Material
from app import db

material_bp = Blueprint('material', __name__)

from middleware.middleware import jwt_required

@material_bp.route('/', methods=['POST'])
@jwt_required
def create_material(data):
    try:
        data = request.get_json()
        name = data.get('name')

        new_material = Material(name=name)

        db.session.add(new_material)
        db.session.commit()

        return jsonify({'message': 'Material creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear material: ' + str(e)}), 500


@material_bp.route('/', methods=['GET'])
@jwt_required
def get_materials(data):
    try:
        materials = Material.query.all()
        materials_list = []

        for material in materials:
            material_data = {
                'id': material.id,
                'name': material.name
            }
            materials_list.append(material_data)

        return jsonify(materials_list)

    except Exception as e:
        return jsonify({'error': 'Error al listar los materiales: ' + str(e)}), 500


@material_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_material(data, id):
    try:
        material = Material.query.get(id)

        if material:
            return jsonify({'name': material.name})
        else:
            return jsonify({'message': 'Material no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener material: ' + str(e)}), 500


@material_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_material(data, id):
    try:
        material = Material.query.get(id)

        if material:
            data = request.get_json()
            material.name = data.get('name')

            db.session.commit()

            return jsonify({'message': 'Material actualizado exitosamente'}), 200
        else:
            return jsonify({'message': 'Material no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al actualizar material: ' + str(e)}), 500


@material_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_material(data, id):
    try:
        material = Material.query.get(id)

        if material:
            db.session.delete(material)
            db.session.commit()

            return jsonify({'message': 'Material eliminado exitosamente'})
        else:
            return jsonify({'message': 'Material no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar material: ' + str(e)}), 500

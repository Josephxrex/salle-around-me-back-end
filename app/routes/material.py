from flask import Blueprint, request, jsonify
from models.material import Material
from app import db

material_bp = Blueprint('material', __name__)

from middleware.middleware import jwt_required


@material_bp.route('/', methods=['POST'])
@jwt_required
def create_material(data):
    """
        Crear una nuevo Material
        ---
        parameters:
          - name: data
            in: body
            required: true
            description: Datos para crear una nuevo Material.
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Material.
        responses:
          200:
            description: Material creada exitosamente.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Mensaje de éxito.
          500:
            description: Error al crear el Material.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
    """
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
    """
            Obtener todas los Materials
            ---
            parameters:
              - name: data
                in: body
                required: true
                description: Datos necesarios para obtener todas los Materials.
            responses:
              200:
                description: Lista de Materials.
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: ID de la Material.
                      name:
                        type: string
                        description: Material.
              500:
                description: Error al obtener los Materials.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error.
    """
    try:
        # Consulta todas los materials donde id_delete es igual a 0
        materials = Material.query.filter(Material.is_delete == 0).all()

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
    """
        Obtener un Material por su ID
        ---
        parameters:
          - name: id_material
            in: path
            type: integer
            required: true
            description: ID del material que se desea obtener.
        responses:
          200:
            description: Información del material.
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: ID del material.
                name:
                  type: string
                  description: Material.
          404:
            description: Material no encontrada.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
          500:
            description: Error al obtener el Material.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error."""
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
    """
        Actualizar un Material por su ID
        ---
        parameters:
          - name: id_material
            in: path
            type: integer
            required: true
            description: ID del Material que se desea actualizar.
          - name: data
            in: body
            required: true
            description: Datos para actualizar el material.
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Material.
        responses:
          200:
            description: Material actualizado exitosamente.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Mensaje de éxito.
          404:
            description: Material no encontrada.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
          500:
            description: Error al actualizar el Material.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
    """
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
    """
        Eliminar un Material por su ID (Borrado lógico)
        ---
        parameters:
          - name: id_material
            in: path
            type: integer
            required: true
            description: ID del Material que se desea eliminar (marcar como eliminada).
        responses:
          200:
            description: Material eliminada exitosamente.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Mensaje de éxito.
          404:
            description: Material no encontrada.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
          500:
            description: Error al eliminar el Material.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
    """
    try:
        material = Material.query.get(id)

        if material:
            # Actualizar el campo is_delete a 1 (marcar como eliminado)
            material.is_delete = 1
            db.session.commit()

            return jsonify({'message': 'Material eliminado exitosamente'})
        else:
            return jsonify({'message': 'Material no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar material: ' + str(e)}), 500

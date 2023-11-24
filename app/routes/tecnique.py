from flask import Blueprint, request, jsonify
from models.tecnique import Tecnique
from app import db

tecnique_bp = Blueprint('tecnique', __name__)

from middleware.middleware import jwt_required

@tecnique_bp.route('/', methods=['POST'])
@jwt_required
def create_tecnique(data):
    """
            Crear una nuevo Tecnique
            ---
            parameters:
              - name: data
                in: body
                required: true
                description: Datos para crear una nuevo Tecnique.
                schema:
                  type: object
                  properties:
                    name:
                      type: string
                      description: Tecnique.
            responses:
              200:
                description: Tecnique creada exitosamente.
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      description: Mensaje de éxito.
              500:
                description: Error al crear Tecnique.
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

        new_tecnique = Tecnique(name=name)

        db.session.add(new_tecnique)
        db.session.commit()

        return jsonify({'message': 'Tecnique creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear tecnique: ' + str(e)}), 500


@tecnique_bp.route('/', methods=['GET'])
@jwt_required
def get_tecniques(data):
    """
        Obtener todas las Tecniques
        ---
        parameters:
          - name: data
            in: body
            required: true
            description: Datos necesarios para obtener todas las Tecniques.
        responses:
          200:
            description: Lista de Tecniques.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID de la Tecnique.
                  technique:
                    type: string
                    description: Tecnique.
          500:
            description: Error al obtener las Tecniques.
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensaje de error.
    """
    try:
        # Consulta todas las tecnique donde id_delete es igual a 0
        tecniques = Tecnique.query.filter(Tecnique.is_delete == 0).all()

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
def get_tecnique(data, id):
    """
            Obtener un Tecnique por su ID
            ---
            parameters:
              - name: Tecnique_id
                in: path
                type: integer
                required: true
                description: ID del Tecnique que se desea obtener.
            responses:
              200:
                description: Información del Tecnique.
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: ID del Tecnique.
                    name:
                      type: string
                      description: Tecnique.
              404:
                description: Tecnique no encontrada.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error.
              500:
                description: Error al obtener el Tecnique.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error."""
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
def update_tecnique(data, id):
    """
            Actualizar un Tecnique por su ID
            ---
            parameters:
              - name: Tecnique_id
                in: path
                type: integer
                required: true
                description: ID del Tecnique que se desea actualizar.
              - name: data
                in: body
                required: true
                description: Datos para actualizar el Tecnique.
                schema:
                  type: object
                  properties:
                    name:
                      type: string
                      description: Tecnique.
            responses:
              200:
                description: Tecnique actualizado exitosamente.
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      description: Mensaje de éxito.
              404:
                description: Tecnique no encontrada.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error.
              500:
                description: Error al actualizar el Tecnique.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error.
        """
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
def delete_tecnique(data, id):
    """
            Eliminar un Tecnique por su ID (Borrado lógico)
            ---
            parameters:
              - name: Tecnique_id
                in: path
                type: integer
                required: true
                description: ID del Tecnique que se desea eliminar (marcar como eliminada).
            responses:
              200:
                description: Tecnique eliminada exitosamente.
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      description: Mensaje de éxito.
              404:
                description: Tecnique no encontrada.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error.
              500:
                description: Error al eliminar el Tecnique.
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Mensaje de error.
        """
    try:
        tecnique = Tecnique.query.get(id)

        if tecnique:
            # Actualizar el campo is_delete a 1 (marcar como eliminado)
            tecnique.is_delete = 1
            db.session.commit()

            return jsonify({'message': 'Tecnique eliminado exitosamente'})
        else:
            return jsonify({'message': 'Tecnique no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar tecnique: ' + str(e)}), 500

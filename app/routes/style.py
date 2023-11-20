from datetime import datetime
from flask import Blueprint, request, jsonify
from models.style import Style
from app import db

style_bp = Blueprint('style', __name__)

from middleware.middleware import jwt_required

@style_bp.route('/', methods=['POST'])
@jwt_required
def create_style(data):
    """
    Crear un nuevo estilo
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos del estilo a crear.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre del estilo.
    responses:
        200:
            description: Estilo creado exitosamente.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de éxito.
        401:
            description: Acceso no autorizado.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de error.
    """
    try:
        data = request.get_json()
        name = data.get('name')
        new_style = Style(name=name, create_at=create_at)

        db.session.add(new_style)
        db.session.commit()

        return jsonify({'message': 'Estilo creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear el estilo: ' + str(e)}), 500

@style_bp.route('/', methods=['GET'])
@jwt_required
def get_styles(data):
    """
    Listar todos los estilos
    ---
    responses:
        200:
            description: Estilos listados exitosamente.
            schema:
            type: object
            properties:
                id:
                type: integer
                description: ID del estilo.
                name:
                type: string
                description: Nombre del estilo.
        401:
            description: Acceso no autorizado.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de error.
    """
    try:
        styles = Style.query.filter(Style.is_delete == 0).all()
        styles_list = []

        for style in styles:
            style_data = {
                'id': style.id,
                'name': style.name,
                'create_at': style.create_at,
                'update_at': style.update_at,
                'is_delete': style.is_delete
            }
            styles_list.append(style_data)

        return jsonify(styles_list), 200

    except Exception as e:
        return jsonify({'error': 'Error al listar los estilos: ' + str(e)}), 500

@style_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_style_by_id(data, id):
    """
    Obtener un estilo por su ID
    ---
    responses:
        200:
            description: Estilo obtenido exitosamente.
            schema:
            type: object
            properties:
                name:
                type: string
                description: Nombre del estilo.
        404:
            description: Estilo no encontrado.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de error.
        500:
            description: Error en el servidor.
            schema:
            type: object
            properties:
                error:
                type: string
                description: Mensaje de error.
    """
    try:
        style = Style.query.get(id)

        if style:
            style_data = {
                'id': style.id,
                'name': style.name,
                'create_at': style.create_at,
                'update_at': style.update_at,
                'is_delete': style.is_delete
            }
            return jsonify(style_data), 200
        else:
            return jsonify({'message': 'Estilo no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener el estilo: ' + str(e)}), 500

@style_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_style(data, id):
    """
    Actualizar un estilo por su ID
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos del estilo a actualizar.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre del estilo.
    responses:
        200:
            description: Estilo actualizado exitosamente.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de éxito.
        404:
            description: Estilo no encontrado.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de error.
        500:
            description: Error en el servidor.
            schema:
            type: object
            properties:
                error:
                type: string
                description: Mensaje de error.
    """
    try:
        #Obtener el style por su ID
        style = Style.query.get(id)

        if style:
            data = request.get_json()
            style.name = data.get('name')
            db.session.commit()

            return jsonify({'message': 'Estilo actualizado exitosamente'}), 200
        else:
            return jsonify({'message': 'Estilo no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al actualizar el estilo: ' + str(e)}), 500

@style_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_style(data, id):
    """
    Eliminar un estilo por su ID
    ---
    responses:
        200:
            description: Estilo eliminado exitosamente.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de éxito.
        404:
            description: Estilo no encontrado.
            schema:
            type: object
            properties:
                message:
                type: string
                description: Mensaje de error.
        500:
            description: Error en el servidor.
            schema:
            type: object
            properties:
                error:
                type: string
                description: Mensaje de error.
    """
    try:
        style = Style.query.get(id)

        if style is None:
            return jsonify({'error': 'Estilo no encontrado'}), 404
        
        # Actualizar el campo is_delete a 1 (marcar como eliminado)
        style.is_delete = 1
        db.session.commit()
        return jsonify({'message': 'Estilo eliminado exitosamente'}), 200

    except Exception as e:
        return jsonify({'error': 'Error al eliminar el estilo: ' + str(e)}), 500

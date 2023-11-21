from flask import Blueprint, request, jsonify
from models.category import Category
from app import db

category_bp = Blueprint('category', __name__)

from middleware.middleware import jwt_required
    
@category_bp.route('/', methods=['GET'])
@jwt_required
def get_categories(data):
    """
    Obtener todas las categorias
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos necesarios para obtener todas las categorias.
    responses:
      200:
        description: Lista de categorias.
        schema:
          type: array
          items:
            type: object
            properties:
            id:
              type: integer
              description: ID de la categoria.
            name:
              type: string
              description: Nombre de la categoria.
            description:
              type: string
              description: descripicion de la categoria.
      500:
        description: Error al obtener las categorias.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Consulta todas las Categorías donde id_delete es iguala a 0
        categories = Category.query.filter(Category.is_delete == 0).all()
        
        # Crea una lista para almacenar todos los datos de Category
        categories_list = []

        for category in categories:
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
            categories_list.append(category_data)

        return jsonify(categories_list), 200

    except Exception as e:
        return jsonify({'error': 'Error al listar las categorias: ' + str(e)}), 500
    
@category_bp.route('/', methods=['POST'])
@jwt_required
def create_category(data):
    """
    Crear una nueva categoria
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos para crear una nueva categoria.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre de la categoria.
            description:
              type: string
              description: descripicion de la categoria.
    responses:
      200:
        description: Categoria creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      500:
        description: Error al crear la categoria.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        data = request.get_json()
        
        name = data.get('name')
        description = data.get('description')
        
        new_category = Category(name=name, description=description)

        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'Categoría creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear la Categoría: ' + str(e)}), 500
    
@category_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_category(data,id):
    """
    Obtener una nueva categoria
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos para crear una nueva categoria.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre de la categoria.
            description:
              type: string
              description: descripicion de la categoria.
    responses:
      200:
        description: Categoria creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      500:
        description: Error al crear la categoria.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""

    try:
        category = Category.query.get(id)

        if category:
            return jsonify({'name': category.name, 'description': category.description}), 200
        else:
            return jsonify({'message': 'Categoría no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener la Categoría: ' + str(e)}), 500
    
@category_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_category(data, id):
    """
    Actualizar una categoria por su ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la categoria que se desea actualizar.
      - name: data
        in: body
        required: true
        description: Datos para actualizar la categoria.
        schema:
          type: object
          properties:
            name:
                type: string
                description: Nombre de la categoria.
            description:
                type: string
                description: descripicion de la categori.
    responses:
      200:
        description: categoria actualizada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      404:
        description: categoria no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al actualizar la categoria.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        category = Category.query.get(id)

        if category:
            data = request.get_json()
            category.name = data.get('name')
            category.description = data.get('description')

            db.session.commit()

            return jsonify({'message': 'Categoría actualizada exitosamente'}), 200
        else:
            return jsonify({'message': 'Categoría no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al actualizar la Categoría: ' + str(e)}), 500
    
@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_category(data, id):
    """
    Eliminar una categoria por su ID (Borrado lógico)
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de la categoria que se desea eliminar (marcar como eliminada).
    responses:
      200:
        description: categoria eliminada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      404:
        description: categoria no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al eliminar la categoria.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la categoria existente por su ID
        category = Category.query.get(id)

        if category is None:
          return jsonify({'message': 'Categoría no encontrada'}), 404

        # Actualizar el campo is_delete a 1 (marcar como eliminado)
        category.is_delete = 1
        db.session.commit()
        return jsonify({'message': 'Categoría eliminada exitosamente'}), 200

            

    except Exception as e:
        return jsonify({'error': 'Error al eliminar la Categoría: ' + str(e)}), 500
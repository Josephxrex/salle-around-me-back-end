from flask import Blueprint, request, jsonify
from models.category import Category
from app import db

category_bp = Blueprint('category', __name__)

    
@category_bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        categories_list = []

        for category in categories:
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
            categories_list.append(category_data)

        return jsonify(categories_list)

    except Exception as e:
        return jsonify({'error': 'Error al listar las categorias: ' + str(e)}), 500
    
@category_bp.route('/', methods=['POST'])
def create_category():
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
def get_category(id):
    try:
        category = Category.query.get(id)

        if category:
            return jsonify({'name': category.name, 'description': category.description})
        else:
            return jsonify({'message': 'Categoría no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener la Categoría: ' + str(e)}), 500
    
@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
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
def delete_category(id):
    try:
        category = Category.query.get(id)

        if category:
            db.session.delete(category)
            db.session.commit()

            return jsonify({'message': 'Categoría eliminada exitosamente'})
        else:
            return jsonify({'message': 'Categoría no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar la Categoría: ' + str(e)}), 500
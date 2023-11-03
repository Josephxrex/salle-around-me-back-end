from flask import Blueprint, request, jsonify
from models.style import Style
from app import db

style_bp = Blueprint('style', __name__)

@style_bp.route('/', methods=['POST'])
def create_style():
    try:
        data = request.get_json()
        name = data.get('name')

        new_style = Style(name=name)

        db.session.add(new_style)
        db.session.commit()

        return jsonify({'message': 'Estilo creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear el estilo: ' + str(e)}), 500

@style_bp.route('/', methods=['GET'])
def get_styles():
    try:
        styles = Style.query.all()
        styles_list = []

        for style in styles:
            style_data = {
                'id': style.id,
                'name': style.name
            }
            styles_list.append(style_data)

        return jsonify(styles_list)

    except Exception as e:
        return jsonify({'error': 'Error al listar los estilos: ' + str(e)}), 500

@style_bp.route('/<int:id>', methods=['GET'])
def get_style(id):
    try:
        style = Style.query.get(id)

        if style:
            return jsonify({'name': style.name})
        else:
            return jsonify({'message': 'Estilo no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener el estilo: ' + str(e)}), 500

@style_bp.route('/<int:id>', methods=['PUT'])
def update_style(id):
    try:
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
def delete_style(id):
    try:
        style = Style.query.get(id)

        if style:
            db.session.delete(style)
            db.session.commit()

            return jsonify({'message': 'Estilo eliminado exitosamente'})
        else:
            return jsonify({'message': 'Estilo no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al eliminar el estilo: ' + str(e)}), 500

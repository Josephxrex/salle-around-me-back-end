from flask import Blueprint, request, jsonify
from models.detail_attraction import detail_attraction
from app import db

detail_attraction_bp = Blueprint('detail_attraction', __name__)

from middleware.middleware import jwt_required

# Método para crear un datalle de atraccion 
"""
    Autor: Laura Pérez
    Descripción: Crea un nuevo detalle de atracción a partir de datos JSON proporcionados en la solicitud.
    Fecha: 2023-10-31

    Return:
    - 201 (Created) si el detalle se crea exitosamente.
    - 400 (Bad Request) si ocurre algún error durante la creación.
"""
@detail_attraction_bp.route('/', methods=['POST'])
@jwt_required
def create_detail_attraction(data):
    try:
        # Obtener los datos JSON de la solicitud
        data = request.get_json()

        # Extraer los campos del detalle de atracción desde los datos
        description = data.get('description')
        size = data.get('size')
        tecnique_id = data.get('tecnique_id')
        material_id = data.get('material_id')
        style_id = data.get('style_id')
        city_id = data.get('city_id')
        country_id = data.get('country_id')
        address_id = data.get('address_id')
        # Crear una nueva instancia de detail_attraction
        new_detail_attraction = detail_attraction(
            description=description,
            size=size,
            tecnique_id=tecnique_id,
            material_id=material_id,
            style_id=style_id,
            city_id=city_id,
            country_id=country_id,
            address_id=address_id
        )
        
        # Agregar el nuevo detalle de atracción a la base de datos y realizar la confirmación
        db.session.add(new_detail_attraction)
        db.session.commit()

        # Devolver un mensaje de éxito
        return jsonify({'message': 'Detalle de atracción creado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        # Devolver un mensaje de error en caso de excepción
        return jsonify({'error': 'Error al crear el detalle de atracción: ' + str(e)}), 400
    
  # Método para obtener todos los detalles de atraccion
"""
    Autor: Laura Pérez
    Descripción: Obtiene los detalles de un atracción.
    Fecha: 2023-10-31

    Return:
    - 200 (OK) y los datos del detalle si se encuentra.
    - 404 (Not Found) si el detalle no existe.
    - 400 (Bad Request) si ocurre algún error durante la obtención.
    """
@detail_attraction_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_detail_attractionbyid(data, id):
    try:
        detail = detail_attraction.query.get(id)
        
        if detail:
            # Convierte cada objeto detail_attraction a un diccionario y agrega a la lista
            detail_data = {
                'id': detail.id,
                'description': detail.description,
                'size': detail.size,
                'tecnique_id': detail.tecnique_id,
                'material_id': detail.material_id,
                'style_id': detail.style_id,
                'city_id': detail.city_id,
                'country_id': detail.country_id,
                'address_id': detail.address_id
            }
        
            return jsonify(detail_data)
            #Si no existe, se retorna un mensaje de error 404
        else:
            return jsonify({'message': 'Coordenada no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': 'Error al obtener el detalle de atraccion: ' + str(e)}), 400

  # Método para obtener todos los detalles de atraccion
"""
    Autor: Laura Pérez
    Descripción: Obtiene los detalles de un atracción.
    Fecha: 2023-10-31

    Return:
    - 200 (OK) y los datos del detalle si se encuentra.
    - 404 (Not Found) si el detalle no existe.
    - 400 (Bad Request) si ocurre algún error durante la obtención.
    """
@detail_attraction_bp.route('/', methods=['GET'])
@jwt_required
def get_detail_attraction(data):
    try:
        details = detail_attraction.query.all()
        detail_list = []
        
        for detail in details:
            # Convierte cada objeto detail_attraction a un diccionario y agrega a la lista
            detail_data = {
                'id': detail.id,
                'description': detail.description,
                'size': detail.size,
                'tecnique_id': detail.tecnique_id,
                'material_id': detail.material_id,
                'style_id': detail.style_id,
                'city_id': detail.city_id,
                'country_id': detail.country_id,
                'address_id': detail.address_id
            }
            detail_list.append(detail_data)
        
        return jsonify(detail_list)

    except Exception as e:
        return jsonify({'error': 'Error al obtener los detalles de atracción: ' + str(e)}), 400

# Método para editar el detalle de atraccion
"""
    Autor: Laura Pérez
    Descripción: Actualiza los detalles de un atracción por su ID con datos proporcionados en la solicitud JSON.
    Fecha: 2023-10-31

    Return:
    - 200 (OK) si el detalle se actualiza exitosamente.
    - 404 (Not Found) si el detalle no existe.
    - 400 (Bad Request) si ocurre algún error durante la actualización.
    """
@detail_attraction_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_detail_attraction(data, id):
    try:
        # Buscar el detalle de atracción por su ID
        detail = detail_attraction.query.get(id)
        data = request.get_json()

        if detail:
          # Convierte el objeto detail_attraction a un diccionario
          detail.description = data.get('description'),
          detail.size = data.get('size'),
          detail.tecnique_id = data.get('tecnique_id'),
          detail.material_id = data.get('material_id'),
          detail.style_id = data.get('style_id'),
          detail.city_id = data.get('city_id'),
          detail.country_id = data.get('country_id'),
          detail.address_id = data.get('address_id')

          # Agregar la actualizacion  detalle de atracción a la base de datos y realizar la confirmación
          db.session.commit()
          db.session.close()
          # Devolver los datos del detalle de atracción
          return  jsonify({'message': 'Actualizado correctamente'}), 404
        else:
            # Devolver un mensaje de detalle no encontrado
            return jsonify({'message': 'Detalle de atracción no encontrado'}), 404

    except Exception as e:
        # Devolver un mensaje de error en caso de excepción
        return jsonify({'error': 'Error al obtener el detalle de atracción: ' + str(e)}), 400



#Método para eliminar el detalle de atraccion
"""
    Autor: Laura Pérez
    Descripción: Elimina los detalles de un atracción por su ID.
    Fecha: 2023-10-31

    Return:
    - 200 (OK) si el detalle se elimina exitosamente.
    - 404 (Not Found) si el detalle no existe.
    - 400 (Bad Request) si ocurre algún error durante la eliminación.
    """
@detail_attraction_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_detail_attraction(data, id):
    try:
        # Buscar el detalle de atracción por su ID
        detail = detail_attraction.query.get(id)
        if not detail:
            # Devolver un mensaje de detalle no encontrado si no existe
            return jsonify({'message': 'Detalle de atracción no encontrado'}), 404
        # Eliminar el detalle de atracción de la base de datos
        db.session.delete(detail)
        db.session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'message': 'Detalle de atracción eliminado exitosamente'}), 200

    except Exception as e:
        db.session.rollback()
        # Devolver un mensaje de error en caso de excepción
        return jsonify({'error': 'Error al eliminar el detalle de atracción: ' + str(e)}), 400
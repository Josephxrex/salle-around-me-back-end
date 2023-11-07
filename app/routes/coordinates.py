from flask import Blueprint, request, jsonify
from models.coordinates import Coordinates
from app import db

coordinate_bp = Blueprint('coordinate', __name__)

from middleware.middleware import jwt_required
#Métodos para la API de coordenadas
"""
    Autor: Josue Meza Lozano
    Descripción: Se crea una coordenada.
    Fecha: 2023-10-31
    """
#Se crea una nueva coordenada
@coordinate_bp.route('/', methods=['POST'])
@jwt_required
def create_coordinate(data):
    try:
      #Se obtienen los datos de la petición
      data = request.get_json()
      lat = data.get('lat')
      lng = data.get('lng')

      #Se crea la nueva coordenada
      new_coordinate = Coordinates(
         lat=lat, 
         lng=lng
      )
      #Se agrega la nueva coordenada a la base de datos
      db.session.add(new_coordinate)
      #Se confirman los cambios
      db.session.commit()
      db.session.close()
      #Se retorna un mensaje de éxito
      return jsonify({'message': 'Coordenada creada exitosamente'}), 200
    except Exception as e:
      #Si ocurre un error, se retorna un mensaje de error 400
      db.session.rollback()
      return jsonify({'message': 'Error al crear la coordenada'+ str(e)}), 500

#Métodos para la API de coordenadas
"""
    Autor: Josue Meza Lozano
    Descripción: Se obtienen todas las coordenadas.
    Fecha: 2023-10-31
    """
#Se obtienen todas las coordenadas
@coordinate_bp.route('/', methods=['GET'])
@jwt_required
def get_coordinates(data):
    try:
      #Se obtienen todas las coordenadas de la base de datos
      coordinates = Coordinates.query.all()
      coordinates_list = []
      #Se recorren las coordenadas
      for coordinate in coordinates:
          coordinates_data={
              'id': coordinate.id,
              'lat': coordinate.lat,
              'lng': coordinate.lng
          }
          coordinates_list.append(coordinates_data)
      #Se retornan las coordenadas en formato JSON
      return jsonify(coordinates_list)
    except Exception as e:
      #Si ocurre un error, se retorna un mensaje de error 500
      return jsonify({'message': 'Error al listar las coordenadas'+str(e)}), 500

#Métodos para la API de coordenadas
"""
    Autor: Josue Meza Lozano
    Descripción: Se obtiene una coordenada por su id.
    Fecha: 2023-10-31
    """
#Se obtiene una coordenada por su id
@coordinate_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_coordinate(data, id):
    try:
      #Se obtiene la coordenada de la base de datos por su id
      coordinate = Coordinates.query.get(id)
      #Si la coordenada existe, se retorna en formato JSON
      if coordinate:
          return jsonify({
             'lat': coordinate.lat, 
             'lng': coordinate.lng
             })
      #Si no existe, se retorna un mensaje de error 404
      else:
          return jsonify({'message': 'Coordenada no encontrada'}), 404
    except Exception as e:
      #Si ocurre un error, se retorna un mensaje de error 404
      return jsonify({'message': 'Coordenada no encontrada'+ str(e)}), 500

#Métodos para la API de coordenadas
"""
    Autor: Josue Meza Lozano
    Descripción: Se modifica una coordenada por su id.
    Fecha: 2023-10-31
    """
#Se actualiza una coordenada por su id
@coordinate_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_coordinate(data, id):
    try:
      #se obtiene la coordenada de la base de datos por su id
      coordinate = Coordinates.query.get(id)
      #Si la coordenada existe, se actualiza
      if coordinate:
          #Se obtienen los datos de la petición
          data = request.get_json()
          coordinate.lat = data.get('lat')
          coordinate.lng = data.get('lng')
          #Se confirman los cambios
          db.session.commit()
          db.session.close()
          #Se retorna un mensaje de éxito
          return jsonify({'message': 'Coordenada actualizada exitosamente'}), 200
      #Si no existe, se retorna un mensaje de error 404
      else:
          return jsonify({'message': 'Coordenada no encontrada'}), 404
    except Exception as e:
      #Si ocurre un error, se retorna un mensaje de error 400
      return jsonify({'message': 'Error al actualizar la coordenada' + str(e)}), 400

#Métodos para la API de coordenadas
"""
    Autor: Josue Meza Lozano
    Descripción: Se elimina una coordenada por su id.
    Fecha: 2023-10-31
    """
#Se elimina una coordenada por su id
@coordinate_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_coordinate(data, id):
    try:
      #Se obtiene la coordenada de la base de datos por su id
      coordinate = Coordinates.query.get(id)
      #Si la coordenada existe, se elimina
      if coordinate:
          db.session.delete(coordinate)
          db.session.commit()
          return jsonify({'message': 'Coordenada eliminada exitosamente'})
      #Si no existe, se retorna un mensaje de error 404
      else:
          return jsonify({'message': 'Coordenada no encontrada'}), 404
    except:
      #Si ocurre un error, se retorna un mensaje de error 400
      return jsonify({'message': 'Error al eliminar la coordenada'}), 400
from flask import Blueprint, request, jsonify
from models.mac_address import MacAddress
from app import db

mac_address_bp = Blueprint('mac_address', __name__)

from middleware.middleware import jwt_required

@mac_address_bp.route("/", methods=["POST"])
@jwt_required
def create_mac_address(data):
    """
    Crear una nueva Mac Address
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos para crear una nueva Mac Address.
        schema:
          type: object
          properties:
            mac_address:
              type: string
              description: Mac Addres.
    responses:
      200:
        description: Mac Address creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      500:
        description: Error al crear la Mac Address.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        dataJson = request.get_json()

        address = dataJson.get("mac_address")

        new_mac_address = MacAddress(
            address=address
        )

        db.session.add(new_mac_address)
        db.session.commit()

        return jsonify({"message": "Mac Address creada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la Mac Address: " + str(e)}), 500

@mac_address_bp.route("/", methods=["GET"])
@jwt_required
def get_all_mac_address(data):
    """
    Obtener todas las Mac Address
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos necesarios para obtener todas las Mac Address.
    responses:
      200:
        description: Lista de Mac Address.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID de la Mac Address.
              mac_address:
                type: string
                description: Mac Address.
      500:
        description: Error al obtener las Mac Address.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Consulta todas las Mac Address donde id_delete es igual a 0
        mac_addresses = MacAddress.query.filter(MacAddress.is_delete == 0).all()

        # Crear una lista para almacenar los datos de Mac Address
        mac_address_data = []

        for mac_address in mac_addresses:
            # Crear un diccionario para almacenar los datos de la Mac Address
            mac_address_info = {
                "id": mac_address.id,
                "mac_address": mac_address.address,
            }

            mac_address_data.append(mac_address_info)

        return jsonify(mac_address_data), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener las Mac Address: " + str(e)}), 500

@mac_address_bp.route("/<int:mac_address_id>", methods=["PUT"])
@jwt_required
def update_mac_address(data, mac_address_id):
    """
    Actualizar una Mac Address por su ID
    ---
    parameters:
      - name: mac_address_id
        in: path
        type: integer
        required: true
        description: ID de la Mac Address que se desea actualizar.
      - name: data
        in: body
        required: true
        description: Datos para actualizar la Mac Address.
        schema:
          type: object
          properties:
            mac_address:
              type: string
              description: Mac Address.
    responses:
      200:
        description: Mac Address actualizada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      404:
        description: Mac Address no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al actualizar la Mac Address.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la Mac Address existente por su ID
        existing_mac_address = MacAddress.query.get(mac_address_id)

        if existing_mac_address is None:
            return jsonify({"error": "Mac Address no encontrada"}), 404

        dataJson = request.get_json()

        # Actualizar los campos de la Mac Address con los datos proporcionados en el JSON
        existing_mac_address.address = dataJson.get("mac_address")

        db.session.commit()

        return jsonify({"message": "Mac Address actualizada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar la Mac Address: " + str(e)}), 500

@mac_address_bp.route("/<int:mac_address_id>", methods=["GET"])
@jwt_required
def get_mac_address_by_id(data, mac_address_id):
    """
    Obtener una Mac Address por su ID
    ---
    parameters:
      - name: mac_address_id
        in: path
        type: integer
        required: true
        description: ID de la Mac Address que se desea obtener.
    responses:
      200:
        description: Información de la Mac Address.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID de la Mac Address.
            mac_address:
              type: string
              description: Mac Address.
      404:
        description: Mac Address no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al obtener la Mac Address.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la mac_address por su ID
        mac_address = MacAddress.query.get(mac_address_id)

        if mac_address is None:
            return jsonify({"error": "Mac Address no encontrada"}), 404

        # Crear un diccionario para almacenar los datos de la Mac Address
        mac_address_info = {
            "id": mac_address.id,
            "mac_address": mac_address.address,
        }

        return jsonify(mac_address_info), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener la Mac Address: " + str(e)}), 500

@mac_address_bp.route("/<int:mac_address_id>", methods=["DELETE"])
@jwt_required
def delete_mac_address(data, mac_address_id):
    """
    Eliminar una Mac Address por su ID (Borrado lógico)
    ---
    parameters:
      - name: mac_address_id
        in: path
        type: integer
        required: true
        description: ID de la Mac Address que se desea eliminar (marcar como eliminada).
    responses:
      200:
        description: Mac Address eliminada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      404:
        description: Mac Address no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al eliminar la Mac Address .
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la Mac Address existente por su ID
        existing_mac_address = MacAddress.query.get(mac_address_id)

        if existing_mac_address is None:
            return jsonify({"error": "Mac Address no encontrada"}), 404

        # Actualizar el campo is_delete a 1 (marcar como eliminado)
        existing_mac_address.is_delete = 1
        db.session.commit()

        return jsonify({"message": "Mac Address eliminada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar la Mac Address: " + str(e)}), 500

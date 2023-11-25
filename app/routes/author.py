from flask import Blueprint, jsonify, request
from models.author import Author
from middleware.middleware import jwt_required
from app import db

author_bp = Blueprint("author", __name__)


@author_bp.route("/", methods=["POST"])
@jwt_required
def create_author(data):
    """
    Crear un nuevo autor
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos para crear un nuevo autor.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre del autor.
            father_lastname:
              type: date
              description: Apellido paterno.
            mother_lastname:
              type: date
              description: Apellido materno.
            birthday:
              type: date
              description: Fecha de nacimiento con formato año-mes-dia (1990-12-31).
            death:
              type: date
              description: Fecha de defunción con formato año-mes-dia (1990-12-31).
    responses:
      200:
        description: Autor creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      500:
        description: Error al crear el autor.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        dataJson = request.get_json()

        name = dataJson.get("name")
        father_lastname = dataJson.get("father_lastname")
        mother_lastname = dataJson.get("mother_lastname")
        birthday = dataJson.get("birthday")
        death = dataJson.get("death")

        new_author = Author(
            name=name,
            father_lastname=father_lastname,
            mother_lastname=mother_lastname,
            birthday=birthday,
            death=death,
        )

        db.session.add(new_author)
        db.session.commit()

        return jsonify({"message": "Autor creado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear el autor: " + str(e)}), 500


@author_bp.route("/", methods=["GET"])
@jwt_required
def get_authors(data):
    """
    Obtener todos los autores
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos necesarios para obtener todas los autores.
    responses:
      200:
        description: Lista de autores.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID del autor.
              name:
                type: string
                description: Nombre del autor.
              father_lastname:
                type: date
                description: Apellido paterno.
              mother_lastname:
                type: date
                description: Apellido materno.
              birthday:
                type: date
                description: Fecha de nacimiento con formato año-mes-dia (1990-12-31).
              death:
                type: date
                description: Fecha de defunción con formato año-mes-dia (1990-12-31).
      500:
        description: Error al obtener los autores.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        authors = Author.query.filter(Author.is_delete == 0).all()
        authors_list = []

        for author in authors:
            author_data = {
                "id": author.id,
                "name": author.name,
                "father_lastname": author.father_lastname,
                "mother_lastname": author.mother_lastname,
                "birthday": author.birthday,
                "death": author.death,
            }
            authors_list.append(author_data)

        return jsonify(authors_list), 200

    except Exception as e:
        return jsonify({"error": "Error al listar los autores: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["GET"])
@jwt_required
def get_author_by_id(data, id):
    """
    Obtener un autor por su ID
    ---
    parameters:
      - name: id
        in: path
        type: integer 
        required: true
        description: ID del autor que se desea obtener.
    responses:
      200:
        description: Información del autor.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID del autor.
            name:
              type: string
              description: Nombre del autor.
            father_lastname:
              type: date
              description: Apellido paterno.
            mother_lastname:
              type: date
              description: Apellido materno.
            birthday:
              type: date
              description: Fecha de nacimiento con formato año-mes-dia (1990-12-31).
            death:
              type: date
              description: Fecha de defunción con formato año-mes-dia (1990-12-31).
      404:
        description: Autor no encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al obtener los autores.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la el author por su ID
        author = Author.query.get(id)

        if author:
            return jsonify(
                {
                    "name": author.name,
                    "father_lastname": author.father_lastname,
                    "mother_lastname": author.mother_lastname,
                    "birthday": author.birthday,
                    "death": author.death,
                }
            ), 200
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al obtener el autor: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["PUT"])
@jwt_required
def update_author(data, id):
    """
    Actualizar un autor por su ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del autor que se desea actualizar.
      - name: data
        in: body
        required: true
        description: Datos para actualizar el autor.
        schema:
          type: object
          properties:
            name:
                type: string
                description: Nombre del autor.
            father_lastname:
                type: date
                description: Apellido paterno.
            mother_lastname:
                type: date
                description: Apellido materno.
            birthday:
                type: date
                description: Fecha de nacimiento con formato año-mes-dia (1990-10-1).
            death:
                type: date
                description: Fecha de defunción con formato año-mes-dia (1990-10-1).
    responses:
      200:
        description: Atracción actualizada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      404:
        description: Atracción no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al actualizar la atracción.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        author = Author.query.get(id)

        if author:
            dataJson = request.get_json()

            author.name = dataJson.get("name")
            author.father_lastname = dataJson.get("father_lastname")
            author.mother_lastname = dataJson.get("mother_lastname")
            author.birthday = dataJson.get("birthday")
            author.death = dataJson.get("death")

            db.session.commit()

            return jsonify({"message": "Autor actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al actualizar el autor: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_author(data, id):
    """
    Eliminar un autor por su ID (Borrado lógico)
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del autor que se desea eliminar (marcar como eliminada).
    responses:
      200:
        description: Autor eliminado exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      404:
        description: Autor no encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al eliminar el Autor.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener el autor existente por su ID
        author = Author.query.get(id)

        if author:
            author.is_delete = 1
            db.session.commit()

            return jsonify({"message": "Autor eliminado exitosamente"}), 200
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al eliminar el autor: " + str(e)}), 500
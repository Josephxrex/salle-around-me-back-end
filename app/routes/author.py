from flask import Blueprint, jsonify, request
from models.author import Author
from middleware.middleware import jwt_required
from app import db

author_bp = Blueprint("author", __name__)


@author_bp.route("/", methods=["POST"])
@jwt_required
def create_author(data):
    try:
        dataJson = request.get_json()

        name = dataJson.get("name")
        lastname = dataJson.get("lastname")
        birthday = dataJson.get("birthday")
        death = dataJson.get("death")
        description = dataJson.get("description")
        img = dataJson.get("img")

        new_author = Author(
            name=name,
            lastname=lastname,
            birthday=birthday,
            death=death,
            description=description,
            img=img,
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
    try:
        authors = Author.query.all()
        authors_list = []

        for author in authors:
            author_data = {
                "id": author.id,
                "name": author.name,
                "lastname": author.lastname,
                "birthday": author.birthday,
                "death": author.death,
                "description": author.description,
                "img": author.img,
            }
            authors_list.append(author_data)

        return jsonify(authors_list)

    except Exception as e:
        return jsonify({"error": "Error al listar los autores: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["GET"])
@jwt_required
def get_author(data, id):
    try:
        author = Author.query.get(id)

        if author:
            return jsonify(
                {
                    "name": author.name,
                    "lastname": author.lastname,
                    "birthday": author.birthday,
                    "death": author.death,
                    "description": author.description,
                    "img": author.img,
                }
            )
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al obtener el autor: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["PUT"])
@jwt_required
def update_author(data, id):
    try:
        author = Author.query.get(id)

        if author:
            dataJson = request.get_json()

            author.name = dataJson.get("name")
            author.lastname = dataJson.get("lastname")
            author.birthday = dataJson.get("birthday")
            author.death = dataJson.get("death")
            author.description = dataJson.get("description")
            author.img = dataJson.get("img")

            db.session.commit()

            return jsonify({"message": "Autor actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al actualizar el autor: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required
def delete_author(data, id):
    try:
        author = Author.query.get(id)

        if author:
            db.session.delete(author)
            db.session.commit()

            return jsonify({"message": "Autor eliminado exitosamente"})
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al eliminar el autor: " + str(e)}), 500
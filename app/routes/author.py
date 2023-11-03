from flask import Blueprint, request, jsonify
from models.author import Author
from app import db

author_bp = Blueprint("author", __name__)


@author_bp.route("/", methods=["POST"])
def create_author():
    try:
        data = request.get_json()

        name = data.get("name")
        lastname = data.get("lastname")
        birthday = data.get("birthday")
        death = data.get("death")
        description = data.get("description")
        img = data.get("img")

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
def get_authors():
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
def get_author(id):
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
def update_author(id):
    try:
        author = Author.query.get(id)

        if author:
            data = request.get_json()

            author.name = data.get("name")
            author.lastname = data.get("lastname")
            author.birthday = data.get("birthday")
            author.death = data.get("death")
            author.description = data.get("description")
            author.img = data.get("img")

            db.session.commit()

            return jsonify({"message": "Autor actualizado exitosamente"}), 200
        else:
            return jsonify({"message": "Autor no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al actualizar el autor: " + str(e)}), 500


@author_bp.route("/<int:id>", methods=["DELETE"])
def delete_author(id):
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
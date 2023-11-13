from flask import Blueprint, request, jsonify
from models.attraction import Attraction
from models.detailMaterial import DetailMaterial
from models.detailTecnique import DetailTecnique
from models.tecnique import Tecnique
from models.material import Material
from models.category import Category
from models.author import Author
from models.style import Style
from models.user import User


from middleware.middleware import jwt_required
from app import db

attraction_bp = Blueprint("attraction", __name__)


@attraction_bp.route("/", methods=["POST"])
@jwt_required
def create_attraction(data):
    """
    Crear una nueva atracción
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos para crear una nueva atracción.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nombre de la atracción.
            lat:
              type: number
              description: Latitud de la atracción.
            lng:
              type: number
              description: Longitud de la atracción.
            description:
              type: string
              description: Descripción de la atracción.
            img:
              type: array
              description: Imágenes de la atracción.
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: URL de la imagen.
            size:
              type: integer
              description: Tamaño de la atracción.
            id_author:
              type: integer
              description: ID del autor de la atracción.
            id_style:
              type: integer
              description: ID del estilo de la atracción.
            id_user:
              type: integer
              description: ID del usuario de la atracción.
            id_mac_address:
              type: integer
              description: ID de la dirección MAC de la atracción.
            id_category:
              type: integer
              description: ID de la categoría de la atracción.
            material:
              type: array
              description: Lista de materiales de la atracción.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID del material.
            tecnica:
              type: array
              description: Lista de técnicas de la atracción.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID de la técnica.
    responses:
      200:
        description: Atracción creada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensaje de éxito.
      500:
        description: Error al crear la atracción.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        dataJson = request.get_json()

        name = dataJson.get("name")
        lat = dataJson.get("lat")
        lng = dataJson.get("lng")
        description = dataJson.get("description")
        img = dataJson.get("img")
        size = dataJson.get("size")
        id_author = dataJson.get("id_author")
        id_style = dataJson.get("id_style")
        id_user = dataJson.get("id_user")
        id_mac_address = dataJson.get("id_mac_address")
        id_category = dataJson.get("id_category")
        materials = dataJson.get("material")  # Lista de materiales
        tecnicas = dataJson.get("tecnica")  # Lista de técnicas

        new_attraction = Attraction(
            name=name,
            lat=lat,
            lng=lng,
            description=description,
            img=img,
            size=size,
            id_author=id_author,
            id_style=id_style,
            id_user=id_user,
            id_mac_address=id_mac_address,
            id_category=id_category,
        )

        db.session.add(new_attraction)
        db.session.commit()

        # Obtener el ID de la atracción recién creada
        attraction_id = new_attraction.id

        # Agregar materiales y técnicas asociados
        for material in materials:
            material_id = material.get("id")
            new_material = DetailMaterial(
                material_id=material_id, attraction_id=attraction_id
            )
            db.session.add(new_material)

        for tecnica in tecnicas:
            tecnique_id = tecnica.get("id")
            new_tecnica = DetailTecnique(
                tecnique_id=tecnique_id, attraction_id=attraction_id
            )
            db.session.add(new_tecnica)

        db.session.commit()

        return jsonify({"message": "Atracción creada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la atracción: " + str(e)}), 500


@attraction_bp.route("/", methods=["GET"])
@jwt_required
def get_all_attractions(data):
    """
    Obtener todas las atracciones
    ---
    parameters:
      - name: data
        in: body
        required: true
        description: Datos necesarios para obtener todas las atracciones.
    responses:
      200:
        description: Lista de atracciones.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID de la atracción.
              name:
                type: string
                description: Nombre de la atracción.
              lat:
                type: number
                description: Latitud de la atracción.
              lng:
                type: number
                description: Longitud de la atracción.
              description:
                type: string
                description: Descripción de la atracción.
              img:
                type: array
                description: Imágenes de la atracción.
                items:
                  type: object
                  properties:
                    url:
                      type: string
                      description: URL de la imagen.
              size:
                type: integer
                description: Tamaño de la atracción.
              authorName:
                type: string
                description: Nombre del autor de la atracción.
              styleName:
                type: string
                description: Nombre del estilo de la atracción.
              userName:
                type: string
                description: Nombre del usuario de la atracción.
              categoryname:
                type: string
                description: Nombre de la categoría de la atracción.
              materials:
                type: array
                description: Lista de materiales de la atracción.
                items:
                  type: object
                  properties:
                    material_name:
                      type: string
                      description: Nombre del material.
              tecnicas:
                type: array
                description: Lista de técnicas de la atracción.
                items:
                  type: object
                  properties:
                    tecnique_name:
                      type: string
                      description: Nombre de la técnica.
      500:
        description: Error al obtener las atracciones.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Consulta todas las atracciones donde id_delete es igual a 0
        attractions = Attraction.query.filter(Attraction.is_delete == 0).all()

        # Crear una lista para almacenar los datos de atracción
        attraction_data = []

        for attraction in attractions:
            # Crear un diccionario para almacenar los datos de la atracción
            attraction_info = {
                "id": attraction.id,
                "name": attraction.name,
                "lat": attraction.lat,
                "lng": attraction.lng,
                "description": attraction.description,
                "img": attraction.img,
                "size": attraction.size,
            }

            author = Author.query.get(attraction.id_author)
            if author:
                attraction_info["authorName"] = author.name

            style = Style.query.get(attraction.id_style)
            if style:
                attraction_info["styleName"] = style.name

            user = User.query.get(attraction.id_user)
            if user:
                attraction_info["userName"] = user.name

            category = Category.query.get(attraction.id_category)
            if category:
                attraction_info["categoryname"] = category.name

            materials = DetailMaterial.query.filter(
                DetailMaterial.attraction_id == attraction.id
            ).all()
            tecnicas = DetailTecnique.query.filter(
                DetailTecnique.attraction_id == attraction.id
            ).all()

            material_data = []
            tecnica_data = []

            for material in materials:
                # Obtener el nombre del material a partir de su ID
                material_name = Material.query.get(material.material_id).name
                material_info = {
                    "material_name": material_name,
                }
                material_data.append(material_info)

            for tecnica in tecnicas:
                # Obtener el nombre de la técnica a partir de su ID
                tecnica_name = Tecnique.query.get(tecnica.tecnique_id).name
                tecnica_info = {
                    "tecnique_name": tecnica_name,
                }
                tecnica_data.append(tecnica_info)

            attraction_info["materials"] = material_data
            attraction_info["tecnicas"] = tecnica_data

            attraction_data.append(attraction_info)

        return jsonify(attraction_data), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener las atracciones: " + str(e)}), 500


@attraction_bp.route("/<int:attraction_id>", methods=["PUT"])
@jwt_required
def update_attraction(data, attraction_id):
    """
    Actualizar una atracción por su ID
    ---
    parameters:
      - name: attraction_id
        in: path
        type: integer
        required: true
        description: ID de la atracción que se desea actualizar.
      - name: data
        in: body
        required: true
        description: Datos para actualizar la atracción.
        schema:
          type: object
          properties:
            name:
              type: string
              description: Nuevo nombre de la atracción.
            lat:
              type: number
              description: Nueva latitud de la atracción.
            lng:
              type: number
              description: Nueva longitud de la atracción.
            description:
              type: string
              description: Nueva descripción de la atracción.
            img:
              type: array
              description: Nuevas imágenes de la atracción.
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: URL de la nueva imagen.
            size:
              type: integer
              description: Nuevo tamaño de la atracción.
            id_author:
              type: integer
              description: Nuevo ID del autor de la atracción.
            id_style:
              type: integer
              description: Nuevo ID del estilo de la atracción.
            id_user:
              type: integer
              description: Nuevo ID del usuario de la atracción.
            id_mac_address:
              type: integer
              description: Nuevo ID de la dirección MAC de la atracción.
            id_category:
              type: integer
              description: Nuevo ID de la categoría de la atracción.
            material:
              type: array
              description: Nueva lista de materiales de la atracción.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID del nuevo material.
            tecnica:
              type: array
              description: Nueva lista de técnicas de la atracción.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID de la nueva técnica.
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
        # Obtener la atracción existente por su ID
        existing_attraction = Attraction.query.get(attraction_id)

        if existing_attraction is None:
            return jsonify({"error": "Atracción no encontrada"}), 404

        dataJson = request.get_json()

        # Actualizar los campos de la atracción con los datos proporcionados en el JSON
        existing_attraction.name = dataJson.get("name")
        existing_attraction.lat = dataJson.get("lat")
        existing_attraction.lng = dataJson.get("lng")
        existing_attraction.description = dataJson.get("description")
        existing_attraction.img = dataJson.get("img")
        existing_attraction.size = dataJson.get("size")
        existing_attraction.id_author = dataJson.get("id_author")
        existing_attraction.id_style = dataJson.get("id_style")
        existing_attraction.id_user = dataJson.get("id_user")
        existing_attraction.id_mac_address = dataJson.get("id_mac_address")
        existing_attraction.id_category = dataJson.get("id_category")

        # Borrar materiales y técnicas existentes asociados a la atracción
        DetailMaterial.query.filter(
            DetailMaterial.attraction_id == attraction_id
        ).delete()
        DetailTecnique.query.filter(
            DetailTecnique.attraction_id == attraction_id
        ).delete()

        # Agregar materiales y técnicas asociados a la atracción
        materials = dataJson.get("material")
        tecnicas = dataJson.get("tecnica")

        for material in materials:
            material_id = material.get("id")
            new_material = DetailMaterial(
                material_id=material_id, attraction_id=attraction_id
            )
            db.session.add(new_material)

        for tecnica in tecnicas:
            tecnique_id = tecnica.get("id")
            new_tecnica = DetailTecnique(
                tecnique_id=tecnique_id, attraction_id=attraction_id
            )
            db.session.add(new_tecnica)

        db.session.commit()

        return jsonify({"message": "Atracción actualizada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar la atracción: " + str(e)}), 500


@attraction_bp.route("/<int:attraction_id>", methods=["DELETE"])
@jwt_required
def delete_attraction(data, attraction_id):
    """
    Eliminar una atracción por su ID (Borrado lógico)
    ---
    parameters:
      - name: attraction_id
        in: path
        type: integer
        required: true
        description: ID de la atracción que se desea eliminar (marcar como eliminada).
    responses:
      200:
        description: Atracción eliminada exitosamente.
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
        description: Error al eliminar la atracción.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la atracción existente por su ID
        existing_attraction = Attraction.query.get(attraction_id)

        if existing_attraction is None:
            return jsonify({"error": "Atracción no encontrada"}), 404

        # Actualizar el campo is_delete a 1 (marcar como eliminado)
        existing_attraction.is_delete = 1
        db.session.commit()

        return jsonify({"message": "Atracción eliminada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar la atracción: " + str(e)}), 500


@attraction_bp.route("/<int:attraction_id>", methods=["GET"])
@jwt_required
def get_attraction_by_id(data, attraction_id):
    """
    Obtener una atracción por su ID
    ---
    parameters:
      - name: attraction_id
        in: path
        type: integer
        required: true
        description: ID de la atracción que se desea obtener.
    responses:
      200:
        description: Información de la atracción.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID de la atracción.
            name:
              type: string
              description: Nombre de la atracción.
            lat:
              type: number
              description: Latitud de la atracción.
            lng:
              type: number
              description: Longitud de la atracción.
            description:
              type: string
              description: Descripción de la atracción.
            img:
              type: object
              description: Información de la imagen de la atracción.
              properties:
                url:
                  type: string
                  description: URL de la imagen de la atracción.
            size:
              type: integer
              description: Tamaño de la atracción.
            authorName:
              type: string
              description: Nombre del autor de la atracción.
            styleName:
              type: string
              description: Nombre del estilo de la atracción.
            userName:
              type: string
              description: Nombre del usuario de la atracción.
            categoryName:
              type: string
              description: Nombre de la categoría de la atracción.
            materials:
              type: array
              description: Lista de materiales asociados a la atracción.
              items:
                type: object
                properties:
                  material_name:
                    type: string
                    description: Nombre del material.
            tecnicas:
              type: array
              description: Lista de técnicas asociadas a la atracción.
              items:
                type: object
                properties:
                  tecnique_name:
                    type: string
                    description: Nombre de la técnica.
      404:
        description: Atracción no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al obtener la atracción.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error."""
    try:
        # Obtener la atracción por su ID
        attraction = Attraction.query.get(attraction_id)

        if attraction is None:
            return jsonify({"error": "Atracción no encontrada"}), 404

        # Crear un diccionario para almacenar los datos de la atracción
        attraction_info = {
            "id": attraction.id,
            "name": attraction.name,
            "lat": attraction.lat,
            "lng": attraction.lng,
            "description": attraction.description,
            "img": attraction.img,
            "size": attraction.size,
        }

        # Obtener datos relacionados a través de consultas
        author = Author.query.get(attraction.id_author)
        if author:
            attraction_info["authorName"] = author.name

        style = Style.query.get(attraction.id_style)
        if style:
            attraction_info["styleName"] = style.name

        user = User.query.get(attraction.id_user)
        if user:
            attraction_info["userName"] = user.name

        category = Category.query.get(attraction.id_category)
        if category:
            attraction_info["categoryName"] = category.name

        # Consulta de materiales asociados a la atracción
        materials = DetailMaterial.query.filter(
            DetailMaterial.attraction_id == attraction.id
        ).all()

        # Consulta de técnicas asociadas a la atracción
        tecnicas = DetailTecnique.query.filter(
            DetailTecnique.attraction_id == attraction.id
        ).all()

        # Crear listas para almacenar nombres de materiales y técnicas
        material_data = []
        tecnica_data = []

        for material in materials:
            # Obtener el nombre del material a partir de su ID
            material_name = Material.query.get(material.material_id).name
            material_info = {"material_name": material_name}
            material_data.append(material_info)

        for tecnica in tecnicas:
            # Obtener el nombre de la técnica a partir de su ID
            tecnica_name = Tecnique.query.get(tecnica.tecnique_id).name
            tecnica_info = {"tecnique_name": tecnica_name}
            tecnica_data.append(tecnica_info)

        attraction_info["materials"] = material_data
        attraction_info["tecnicas"] = tecnica_data

        return jsonify(attraction_info), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener la atracción: " + str(e)}), 500

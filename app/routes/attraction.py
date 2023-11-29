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
from geopy.distance import geodesic


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
        id_attraction = new_attraction.id

        # Agregar materiales y técnicas asociados
        for material in materials:
            id_material = material.get("id")
            new_material = DetailMaterial(
                id_material=id_material, id_attraction=id_attraction
            )
            db.session.add(new_material)

        for tecnica in tecnicas:
            id_tecnique = tecnica.get("id")
            new_tecnica = DetailTecnique(
                id_tecnique=id_tecnique, id_attraction=id_attraction
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
              author:
                type: object
                properties:
                  id:
                    type: number
                    description: identificador.
                  name:
                    type: string
                    description: nombre del elemento.
              style:
                type: object
                properties:
                  id:
                    type: number
                    description: identificador.
                  name:
                    type: string
                    description: nombre del elemento.
              userName:
                type: string
                description: Nombre del usuario de la atracción.
              category:
                type: object
                properties:
                  id:
                    type: number
                    description: identificador.
                  name:
                    type: string
                    description: nombre del elemento.
              materials:
                type: array
                description: Lista de materiales de la atracción.
                items:
                  type: object
                  properties:
                    id:
                      type: number
                      description: identificador.
                    name:
                      type: string
                      description: nombre del elemento.
              tecnicas:
                type: array
                description: Lista de técnicas de la atracción.
                items:
                  type: object
                  properties:
                    id:
                      type: number
                      description: identificador.
                    name:
                      type: string
                      description: nombre del elemento.
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
                attraction_info["author"] = {
                  "id":author.id,
                  "name":author.name}

            style = Style.query.get(attraction.id_style)
            if style:
                attraction_info["style"] = {
                  "id":style.id,
                  "name":style.name
                  }

            user = User.query.get(attraction.id_user)
            if user:
                attraction_info["userName"] = user.name

            category = Category.query.get(attraction.id_category)
            if category:
                attraction_info["category"] = {
                  "id":category.id,
                  "name":category.name
                  }

            materials = DetailMaterial.query.filter(
                DetailMaterial.id_attraction == attraction.id
            ).all()
            tecnicas = DetailTecnique.query.filter(
                DetailTecnique.id_attraction == attraction.id
            ).all()

            material_data = []
            tecnica_data = []

            for material in materials:
                # Obtener el nombre del material a partir de su ID
                material = Material.query.get(material.id_material)
                material_info = {
                    "id": material.id,
                    "material_name": material.name,
                }
                material_data.append(material_info)

            for tecnica in tecnicas:
                # Obtener el nombre de la técnica a partir de su ID
                tecnica = Tecnique.query.get(tecnica.id_tecnique)
                tecnica_info = {
                    "id": tecnica.id,
                    "tecnique_name": tecnica.name,
                }
                tecnica_data.append(tecnica_info)

            attraction_info["materials"] = material_data
            attraction_info["tecnicas"] = tecnica_data

            attraction_data.append(attraction_info)

        return jsonify(attraction_data), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener las atracciones: " + str(e)}), 500


@attraction_bp.route("/<int:id_attraction>", methods=["PUT"])
@jwt_required
def update_attraction(data, id_attraction):
    """
    Actualizar una atracción por su ID
    ---
    parameters:
      - name: id_attraction
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
        existing_attraction = Attraction.query.get(id_attraction)

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
            DetailMaterial.id_attraction == id_attraction
        ).delete()
        DetailTecnique.query.filter(
            DetailTecnique.id_attraction == id_attraction
        ).delete()

        # Agregar materiales y técnicas asociados a la atracción
        materials = dataJson.get("material")
        tecnicas = dataJson.get("tecnica")

        for material in materials:
            id_material = material.get("id")
            new_material = DetailMaterial(
                id_material=id_material, id_attraction=id_attraction
            )
            db.session.add(new_material)

        for tecnica in tecnicas:
            id_tecnique = tecnica.get("id")
            new_tecnica = DetailTecnique(
                id_tecnique=id_tecnique, id_attraction=id_attraction
            )
            db.session.add(new_tecnica)

        db.session.commit()

        return jsonify({"message": "Atracción actualizada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar la atracción: " + str(e)}), 500


@attraction_bp.route("/<int:id_attraction>", methods=["DELETE"])
@jwt_required
def delete_attraction(data, id_attraction):
    """
    Eliminar una atracción por su ID (Borrado lógico)
    ---
    parameters:
      - name: id_attraction
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
        existing_attraction = Attraction.query.get(id_attraction)

        if existing_attraction is None:
            return jsonify({"error": "Atracción no encontrada"}), 404

        # Actualizar el campo is_delete a 1 (marcar como eliminado)
        existing_attraction.is_delete = 1
        db.session.commit()

        return jsonify({"message": "Atracción eliminada exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar la atracción: " + str(e)}), 500


@attraction_bp.route("/<int:id_attraction>", methods=["GET"])
@jwt_required
def get_attraction_by_id(data, id_attraction):
    """
    Obtener una atracción por su ID
    ---
    parameters:
      - name: id_attraction
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
        attraction = Attraction.query.get(id_attraction)

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
            DetailMaterial.id_attraction == attraction.id
        ).all()

        # Consulta de técnicas asociadas a la atracción
        tecnicas = DetailTecnique.query.filter(
            DetailTecnique.id_attraction == attraction.id
        ).all()

        # Crear listas para almacenar nombres de materiales y técnicas
        material_data = []
        tecnica_data = []

        for material in materials:
            # Obtener el nombre del material a partir de su ID
            material_name = Material.query.get(material.id_material).name
            material_info = {"material_name": material_name}
            material_data.append(material_info)

        for tecnica in tecnicas:
            # Obtener el nombre de la técnica a partir de su ID
            tecnica_name = Tecnique.query.get(tecnica.id_tecnique).name
            tecnica_info = {"tecnique_name": tecnica_name}
            tecnica_data.append(tecnica_info)

        attraction_info["materials"] = material_data
        attraction_info["tecnicas"] = tecnica_data

        return jsonify(attraction_info), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener la atracción: " + str(e)}), 500

@attraction_bp.route("/GetAllAttractions", methods=["GET"])
def getallattracctions():
    """
    Obtener categorías con sus atracciones
    ---
    responses:
      200:
        description: Información de categorías con sus atracciones.
        schema:
          type: object
          properties:
            categories:
              type: array
              description: Lista de categorías.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID de la categoría.
                  name:
                    type: string
                    description: Nombre de la categoría.
                  attractions:
                    type: array
                    description: Lista de atracciones para la categoría.
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
                          description: Latitud de la ubicacion.
                        lng:
                          type: number
                          description: Longitud de la ubicacion.
                        description:
                          type: string
                          description: Descripción de la atracción.
                        img:
                          type: string
                          description: URL de la imagen de la atracción.
      500:
        description: Error al obtener la información.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
    """
    try:
        categories = Category.query.filter(Category.is_delete == 0).all()

        categories_info = []
        for category in categories:
            category_info = {
                "id": category.id,
                "name": category.name,
                "attractions": []
            }

            attractions = Attraction.query.filter_by(id_category=category.id).filter(Attraction.is_delete == 0).all()

            for attraction in attractions:
                attraction_info = {
                    "category_name": category.name,
                    "id": attraction.id,
                    "name": attraction.name,
                    "lat": attraction.lat,
                    "lng": attraction.lng,
                    "description": attraction.description,
                    "img": attraction.img
                }
                category_info["attractions"].append(attraction_info)

            categories_info.append(category_info)

        return jsonify(categories_info), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener la información de categorias por atracciones: " + str(e)}), 500
    
@attraction_bp.route("/GetAllCategories", methods=["GET"])
def get_all_categories():
    """
    Obtener todas las categorías
    ---
    responses:
      200:
        description: Información de todas las categorías para filtrado.
        schema:
          type: object
          properties:
            categories:
              type: array
              description: Lista de categorías.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID de la categoría.
                  name:
                    type: string
                    description: Nombre de la categoría.
      500:
        description: Error al obtener la información.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
    """
    try:
        categories = Category.query.filter(Category.is_delete == 0).all()

        categories_info = []
        for category in categories:
            category_info = {
                "id": category.id,
                "name": category.name,
                "description":category.description
            }
            categories_info.append(category_info)

        return jsonify(categories_info), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener la información de todas las categorias : " + str(e)}), 500
    
@attraction_bp.route("/GetAttractionById/<int:_id>", methods=["GET"])
def get_attraction_details(_id):
    """
    Obtener detalles de una atracción por su ID
    ---
    parameters:
      - name: id_attraction
        in: path
        type: integer
        required: true
        description: ID de la atracción que se desea obtener detalles.
    responses:
      200:
        description: Detalles de la atracción.
        schema:
          type: object
          properties:
            id_category:
              type: integer
              description: ID de la categoría de la atracción.
            category_name:
              type: string
              description: Nombre de la categoría de la atracción.
            name:
              type: string
              description: Nombre de la atracción.
            description:
              type: string
              description: Descripción de la atracción.
            author_name:
              type: string
              description: Nombre del autor de la atracción.
            lat:
              type: number
              description: Latitud de la atracción.
            lng:
              type: number
              description: Longitud de la atracción.
            tecnique_name:
              type: string
              description: Nombre de la técnica asociada a la atracción.
            material_name:
              type: string
              description: Nombre del material asociado a la atracción.
            size:
              type: integer
              description: Tamaño de la atracción.
            style_name:
              type: string
              description: Nombre del estilo de la atracción.
            img:
              type: string
              description: URL de la imagen de la atracción.
      404:
        description: Atracción no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al obtener los detalles de la atracción.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
    """
    try:
        # Obtener la atracción por su ID
        attraction = Attraction.query.get(_id)

        if attraction is None:
            return jsonify({"error": "Atracción no encontrada"}), 404

        # Obtener datos relacionados a través de consultas
        category = Category.query.get(attraction.id_category)
        author = Author.query.get(attraction.id_author)
        style = Style.query.get(attraction.id_style)
        user = User.query.get(attraction.id_user)

        # Consulta de material asociado a la atracción
        material = DetailMaterial.query.filter_by(id_attraction=attraction.id).first()

        # Consulta de técnica asociada a la atracción
        tecnique = DetailTecnique.query.filter_by(id_attraction=attraction.id).first()

        # Crear un diccionario para almacenar los detalles de la atracción
        attraction_details = {
            "id_category": category.id,
            "category_name": category.name if category else None,
            "name": attraction.name,
            "description": attraction.description,
            "author_name": author.name if author else None,
            "lat": attraction.lat,
            "lng": attraction.lng,
            "tecnique_name": Tecnique.query.get(tecnique.id_tecnique).name if tecnique else None,
            "material_name": Material.query.get(material.id_material).name if material else None,
            "size": attraction.size,
            "style_name": style.name if style else None,
            "img": attraction.img,
        }

        return jsonify(attraction_details), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener los detalles de la atracción: " + str(e)}), 500


@attraction_bp.route("/GetAttractionsByCategory/<_id>", methods=["GET"])
def get_attractions_by_category(_id):
    """
    Obtener atracciones por ID de categoría
    ---
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
        description: ID de la categoría de la cual se desean obtener las atracciones.
    responses:
      200:
        description: Lista de atracciones de la categoría.
        schema:
          type: array
          items:
            type: object
            properties:
              category_name:
                type: string
                description: Nombre de la categoría de la atracción.
              name:
                type: string
                description: Nombre de la atracción.
              size:
                type: number
                description: Dimension de la atraccion.
              lat:
                type: number
                description: Latitud de la ubicacion.
              lng:
                type: number
                description: Longitud de la ubicacion.
              description:
                type: string
                description: Descripción de la atracción.
              img:
                type: string
                description: URL de la imagen de la atracción.
      404:
        description: Categoría no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al obtener las atracciones de la categoría.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
    """
    try:
        # Obtener la categoría por su ID
        category = Category.query.get(_id)

        if category is None:
            return jsonify({"error": "Categoría no encontrada"}), 404

        # Obtener todas las atracciones de la categoría
        attractions = Attraction.query.filter_by(id_category=_id).filter(Attraction.is_delete == 0).all()

        # Crear una lista para almacenar la información de las atracciones
        attractions_info = []

        for attraction in attractions:
            attraction_info = {
                "category_name": category.name,
                "id": attraction.id,
                "name": attraction.name,
                "size": attraction.size,
                "lat": attraction.lat,
                "lng": attraction.lng,
                "description": attraction.description,
                "img": attraction.img
                
            }
            attractions_info.append(attraction_info)

        return jsonify(attractions_info), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las atracciones de la categoría: " + str(e)}), 500
    
@attraction_bp.route("/GetAttractionsByCategoryFull/<_id>", methods=["GET"])
def get_attractions_by_category_full(_id):
    """
    Obtener atracciones completas por ID de categoría
    ---
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
        description: ID de la categoría de la cual se desean obtener las atracciones.
    responses:
      200:
        description: Lista de atracciones de la categoría.
        schema:
          type: array
          items:
            type: object
            properties:
              category_name:
                type: string
                description: Nombre de la categoría de la atracción.
              name:
                type: string
                description: Nombre de la atracción.
              size:
                type: number
                description: Dimension de la atraccion.
              lat:
                type: number
                description: Latitud de la ubicacion.
              lng:
                type: number
                description: Longitud de la ubicacion.
              description:
                type: string
                description: Descripción de la atracción.
              img:
                type: string
                description: URL de la imagen de la atracción.
              category:
                type: object
                properties:
                  id:
                    type: number
                    description: identificador.
                  name:
                    type: string
                    description: nombre del elemento.
              materials:
                type: array
                description: Lista de materiales de la atracción.
                items:
                  type: object
                  properties:
                    id:
                      type: number
                      description: identificador.
                    name:
                      type: string
                      description: nombre del elemento.
              tecnicas:
                type: array
                description: Lista de técnicas de la atracción.
                items:
                  type: object
                  properties:
                    id:
                      type: number
                      description: identificador.
                    name:
                      type: string
                      description: nombre del elemento.
      404:
        description: Categoría no encontrada.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
      500:
        description: Error al obtener las atracciones de la categoría.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
    """
    try:
        # Obtener la categoría por su ID
        category = Category.query.get(_id)

        if category is None:
            return jsonify({"error": "Categoría no encontrada"}), 404

        # Obtener todas las atracciones de la categoría
        attractions = Attraction.query.filter_by(id_category=_id).filter(Attraction.is_delete == 0).all()

        # Crear una lista para almacenar la información de las atracciones
        attractions_info = []

        for attraction in attractions:
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
                attraction_info["author"] = {
                  "id":author.id,
                  "name":author.name}

            style = Style.query.get(attraction.id_style)
            if style:
                attraction_info["style"] = {
                  "id":style.id,
                  "name":style.name
                  }

            user = User.query.get(attraction.id_user)
            if user:
                attraction_info["userName"] = user.name

            category = Category.query.get(attraction.id_category)
            if category:
                attraction_info["category"] = {
                  "id":category.id,
                  "name":category.name
                  }

            materials = DetailMaterial.query.filter(
                DetailMaterial.id_attraction == attraction.id
            ).all()
            tecnicas = DetailTecnique.query.filter(
                DetailTecnique.id_attraction == attraction.id
            ).all()

            material_data = []
            tecnica_data = []

            for material in materials:
                # Obtener el nombre del material a partir de su ID
                material = Material.query.get(material.id_material)
                material_info = {
                    "id": material.id,
                    "material_name": material.name,
                }
                material_data.append(material_info)

            for tecnica in tecnicas:
                # Obtener el nombre de la técnica a partir de su ID
                tecnica = Tecnique.query.get(tecnica.id_tecnique)
                tecnica_info = {
                    "id": tecnica.id,
                    "tecnique_name": tecnica.name,
                }
                tecnica_data.append(tecnica_info)

            attraction_info["materials"] = material_data
            attraction_info["tecnicas"] = tecnica_data

            attractions_info.append(attraction_info)

        return jsonify(attractions_info), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener las atracciones de la categoría: " + str(e)}), 500
    
@attraction_bp.route("/GetTopAttracions/<string:lat>/<string:lng>", methods=["GET"])
def get_nearby_attractions(lat,lng):
    """
    Get Top Attractions based on provided latitude and longitude.
    ---
    parameters:
      - name: lat
        in: path
        type: string
        required: true
        description: Latitude of the user's location.
      - name: lng
        in: path
        type: string
        required: true
        description: Longitude of the user's location.
    responses:
      200:
        description: Top 3 attractions closest to the provided coordinates.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID of the attraction.
              name:
                type: string
                description: Name of the attraction.
              lat:
                type: number
                description: Latitude of the attraction.
              lng:
                type: number
                description: Longitude of the attraction.
              description:
                type: string
                description: Description of the attraction.
              img:
                type: string
                description: URL of the attraction's image.
              size:
                type: integer
                description: Size of the attraction.
              distance:
                type: number
                description: Distance from the user's coordinates.
      400:
        description: Invalid latitude or longitude provided.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message.
      500:
        description: Error encountered while fetching attractions.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message.
    """
    try:
      lat_float = float(lat)
      lng_float = float(lng)
      print("try")
      Atractions =  Attraction.query.filter(Attraction.is_delete == 0).all()
      print("done")
      points = []
      for attraction in Atractions:
        points.append({
                "id": attraction.id,
                "name": attraction.name,
                "lat": attraction.lat,
                "lng": attraction.lng,
                "description": attraction.description,
                "img": attraction.img,
                "size": attraction.size,
                "distance": 0
            })
        
      user_coords = (lat_float,lng_float)
      close_points = []
      for point in points :
        try:
          point["distance"] = geodesic(user_coords, (point['lat'],point['lng'])).kilometers
          if point["distance"]  <= 6:
            close_points.append(point)
        except Exception as ex:
          print("la atracción {} se registro de forma incorrecta".format(point['name']))
      ordered_points=sorted(close_points, key=lambda x: x['distance'])
      return jsonify(ordered_points[:3])
        

    except Exception as e:
        return jsonify({"error": "Error al obtener las atracciones cercanas: " + str(e)}), 500




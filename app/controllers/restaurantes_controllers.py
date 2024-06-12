from flask import Blueprint, jsonify, request

from app.models.restaurant_model import Restaurante
from app.utils.decorators import jwt_required, roles_required
from app.views.restaurant_view import render_restaurante_detail, render_restaurante_list

# Crear un blueprint para el controlador de restaurantes
restaurant_bp = Blueprint("restaurants", __name__)


# Ruta para obtener la lista de restaurante
@restaurant_bp.route("/restaurants", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_restaurante():
    restaurant = restaurant.get_all()
    return jsonify(render_restaurant_list(restaurant))


# Ruta para obtener un restaurante específico por su ID
@restaurant_bp.route("/restaurats/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_restaurant(id):
    restaurant = Restaurant.get_by_id(id)
    if restaurant:
        return jsonify(render_restaurante_detail(restaurant))
    return jsonify({"error": "Restaurant no encontrado"}), 404


# Ruta para crear un nuevo restaurante
@restaurant_bp.route("/restaurants", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_restaurant():
    data = request.json
    id = data.get("id")
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("descripton")
    rating = data.get("rating")

    # Validación simple de datos de entrada
    if not id or not name or not address or not city or not phone or not description or rating is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo restaurante y guardarlo en la base de datos
    restaurant = Restaurante(id=id, name=name, address=address, city=city, phone=phone, description=description, rating=rating)
    restaurant.save()

    return jsonify(render_restaurante_detail(restaurant)), 201


# Ruta para actualizar un restaurante existente
@restaurant_bp.route("/restaurants/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_restaurant(id):
    restaurant = restaurant.get_by_id(id)

    if not restaurant:
        return jsonify({"error": "Restaurant no encontrado"}), 404

    data = request.json
    id = data.get("id")
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("descripton")
    rating = data.get("rating")

    # Actualizar los datos del restaurante
    restaurant.update(id=id, name=name, address=address, city=city, phone=phone, description=description, rating=rating)

    return jsonify(render_restaurante_detail(restaurant))


# Ruta para eliminar un restaurante existente
@restaurant_bp.route("/restaurants/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_restaurant(id):
    restaurant = restaurant.get_by_id(id)

    if not restaurant:
        return jsonify({"error": "Restaurante no encontrado"}), 404

    # Eliminar el restaurante de la base de datos
    restaurant.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flaskr.models import User
from flaskr.schemas import user_schema, users_schema
from flaskr.db import db
from marshmallow import ValidationError

main_bp = Blueprint('main', __name__)

@main_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"msg": f"Hello {get_jwt_identity()}!"})

@main_bp.route("/")
def home():
    return "Flask CRUD API is running!"

@main_bp.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        validated_data = user_schema.load(data)
        new_user = User(**validated_data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User Added"}), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/users", methods=["GET"])
def show_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@main_bp.route("/users/<int:id>", methods=["PUT", "GET"])
def change_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"msg": "No User found"}), 404

    if request.method == "GET":
        return user_schema.jsonify(user)

    try:
        data = request.get_json()
        validated_data = user_schema.load(data, partial=True)
        user.name = validated_data.get("name", user.name)
        user.email = validated_data.get("email", user.email)
        db.session.commit()
        return user_schema.jsonify(user)
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

@main_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted!"})
    return jsonify({"message": "User not found"}), 404

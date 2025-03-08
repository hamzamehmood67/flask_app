from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flaskr.models import User
from flaskr.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "User not Found"}), 404

    token = create_access_token(identity=email)
    return jsonify({"token": token})

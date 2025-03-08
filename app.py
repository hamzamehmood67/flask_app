from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, ValidationError
from flask_marshmallow import Marshmallow
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"]="mykey"

db = SQLAlchemy(app)
mm = Marshmallow(app)
jwt=JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

class UserSchema(mm.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)  # Fix: Allow input validation
    email = fields.Email(required=True)  # Fix: Allow input validation

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/login", methods=["POST"])
def login():
    data= request.get_json()
    emaill= data.get("email")

    user=User.query.filter_by(
        email=emaill
    )

    if not user:
        return jsonify({"msg": "User not Found"})
    
   
    token=create_access_token(identity=emaill)
    return jsonify({"token": token})


@app.route("/protected", methods=["GET"])
@jwt_required()
def protect():
    return jsonify({"msg": f"Hello {get_jwt_identity()}!"})

@app.route('/')
def home():
    return "Flask CRUD API is running!"

@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        validated_data = user_schema.load(data)  # Fix: Proper schema usage

        new_user = User(name=validated_data["name"], email=validated_data["email"])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User Added"}), 201

    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400  # Fix: Return validation errors

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["GET"])
def show_user():
    users = User.query.all()
    return users_schema.jsonify(users)  # Fix: Use schema serialization

@app.route("/users/<int:id>", methods=["PUT", "GET"])
def change_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"msg": "No User found"}), 404

    if request.method == "GET":
        return jsonify({"name": user.name, "email": user.email})

    try:
        data = request.get_json()
        validated_data = user_schema.load(data, partial=True)  # Allow partial updates

        user.name = validated_data.get("name", user.name)
        user.email = validated_data.get("email", user.email)
        db.session.commit()

        return jsonify({"name": user.name, "email": user.email})

    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted!"})
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

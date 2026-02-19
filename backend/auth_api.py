from flask import Blueprint, request, jsonify
from models.models import User, Patient, db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"message": "Username and password required"}, 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "User not found"}, 404

    if not check_password_hash(user.password, password):
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(
        identity=str(user.id),     
        additional_claims={
            "role": user.role     
        }
    )

    return {
        "access_token": access_token,
        "role": user.role
    }, 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    contact = data.get("contact")

    if not username or not password:
        return {"message": "Username and password required"}, 400

    if User.query.filter_by(username=username).first():
        return {"message": "Username already exists"}, 409

    if User.query.filter_by(email=email).first():
        return {"message": "Email already exists"}, 409

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        password=hashed_password,
        email=email,
        role="patient"
    )

    db.session.add(new_user)
    db.session.commit()

    new_patient = Patient(user_id=new_user.id, contact=contact)
    db.session.add(new_patient)
    db.session.commit()

    return {"message": "Patient registered successfully"}, 201

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.services.auth_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}

    required_fields = [
        "name",
        "username",
        "email",
        "password"
    ]

    missing = [
        field for field in required_fields
        if not data.get(field)
    ]

    if missing:
        return {
            "error": "Missing required fields",
            "fields": missing
        }, 400

    try:
        user = register_user(
        name=data["name"],
        username=data["username"],
        email=data["email"],
        password=data["password"],
        address=data.get("address"),
        created_from=request.remote_addr
    )

        return {
            "message": "Registration successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }, 201

    except ValueError as error:
        return {
            "error": str(error)
        }, 409


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {
            "error": "Username and password are required"
        }, 400

    user = authenticate_user(username, password)

    if not user:
        return {
            "error": "Invalid username or password"
        }, 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }, 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    from app.models.user import User

    user = User.query.get(int(user_id))

    if not user:
        return {
            "error": "User not found"
        }, 404

    return {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }, 200
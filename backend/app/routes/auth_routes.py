from flask import Blueprint, request, jsonify

from app.services.auth_service import (
    register_user,
    login_user
)

from app.utils.jwt_utils import generate_jwt

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    required_fields = [
        "name",
        "email",
        "password",
        "role"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    try:

        user = register_user(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role=data["role"]
        )

        token = generate_jwt(user)

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 201

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception:

        return jsonify({
            "error": "Internal server error"
        }), 500
    


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    required_fields = [
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    try:

        user = login_user(
            email=data["email"],
            password=data["password"]
        )

        token = generate_jwt(user)

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }), 200

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 401

    except Exception:

        return jsonify({
            "error": "Internal server error"
        }), 500
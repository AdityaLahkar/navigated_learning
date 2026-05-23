from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt
)


def get_current_user_identity():

    return {
        "user_id": get_jwt_identity(),
        "role": get_jwt().get("role")
    }
from flask_jwt_extended import create_access_token


def generate_jwt(user):

    additional_claims = {
        "role": user.role
    }

    token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims
    )

    return token
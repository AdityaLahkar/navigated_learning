from app.extensions import db
from app.models.user import User
from app.utils.auth_utils import hash_password
from app.utils.auth_utils import verify_password


def register_user(
    name: str,
    email: str,
    password: str,
    role: str
):

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        raise ValueError(
            "Email already registered"
        )

    hashed_password = hash_password(password)

    user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role=role
    )

    db.session.add(user)

    db.session.commit()

    return user

def login_user(
    email: str,
    password: str
):

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        raise ValueError(
            "Invalid email or password"
        )

    is_valid_password = verify_password(
        password,
        user.password_hash
    )

    if not is_valid_password:
        raise ValueError(
            "Invalid email or password"
        )

    return user
import bcrypt

from app.extensions import db
from app.models.user import User
from app.models.portfolio import Portfolio


def register_user(
        name,
        username,
        email,
        password,
        address=None,
        created_from=None
    ):
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")

    if User.query.filter_by(email=email).first():
        raise ValueError("Email already exists")

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        name=name,
        username=username,
        email=email,
        address=address,
        password_hash=password_hash,
        role="TRADER",
        created_from=created_from
    )

    db.session.add(user)
    db.session.flush()

    portfolio = Portfolio(
        user_id=user.id,
        cash_balance=10000.00
    )

    db.session.add(portfolio)
    db.session.commit()

    return user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()

    if not user:
        return None

    password_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    )

    if not password_valid:
        return None

    return user
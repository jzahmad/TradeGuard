from flask import Flask

from app.config import Config
from app.extensions import db, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app import models

    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "message": "TradeGuard API is running"
        }, 200

    @app.get("/api/test-db")
    def test_db():
        from app.models.user import User

        users = User.query.limit(5).all()

        return {
            "status": "ok",
            "database": "connected",
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
                for user in users
            ]
        }, 200

    return app
from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, jwt
from prometheus_flask_exporter import PrometheusMetrics


def create_app():
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    jwt.init_app(app)

    # Load models
    from app import models

    # Register authentication routes
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # Register dashboard routes
    from app.controllers.dashboard_controller import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # Register stock routes
    from app.controllers.stock_controller import stock_bp
    app.register_blueprint(stock_bp)

    # Register order routes
    from app.controllers.order_controller import order_bp
    app.register_blueprint(order_bp)

    # Register admin routes
    from app.controllers.admin_controller import admin_bp
    app.register_blueprint(admin_bp)

    # Root endpoint
    @app.get("/")
    def index():
        return {
            "application": "TradeGuard API",
            "status": "running",
            "version": "1.0.0"
        }, 200

    # Health endpoint
    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "message": "TradeGuard API is running"
        }, 200

    # Database test endpoint
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
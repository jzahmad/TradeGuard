from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def roles_required(*allowed_roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()
            role = claims.get("role")

            if role not in allowed_roles:
                return jsonify({
                    "error": "Access denied"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator
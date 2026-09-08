from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# --- Tambahkan Decorator Admin di bawah ini ---
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Pastikan request membawa token JWT yang valid
            verify_jwt_in_request()
            
            # 2. Ambil payload/claims dari token
            claims = get_jwt()
            
            # 3. Cek apakah role bernilai 'admin'
            user_role = str(claims.get("role", "")).lower()
            if user_role != "admin":
                return jsonify({
                    "success": False,
                    "message": "Access denied! Admin privileges required."
                }), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper
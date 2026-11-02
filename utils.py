from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import re
import unicodedata

db = SQLAlchemy()
migrate = Migrate()


# utils.py bagian paling bawah:

# --- Tambahkan Decorator Admin di bawah ini ---
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = str(claims.get("role", "")).lower()
            if user_role != "admin":
                return jsonify({
                    "success": False,
                    "message": "Access denied! Admin privileges required."
                }), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def slugify(text):
    if not text:
        return ""
    # Normalisasi karakter unicode
    text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')
    # Hapus karakter selain huruf, angka, spasi, dan tanda strip
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Ganti spasi berlebih atau underscore dengan strip tunggal
    return re.sub(r'[-\s]+', '-', text).strip('-_')

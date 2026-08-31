from flask import Blueprint ,jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from utils import db

home_bp = Blueprint('home', __name__, url_prefix='/home')


# GET home route
@home_bp.route('/new')
def home():
    return jsonify({"message": "demo, status, oke "})

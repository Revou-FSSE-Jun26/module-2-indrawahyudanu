from flask import Blueprint, jsonify, request
from utils import db
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
        data = request.get_json() or {}

        email_input = data.get('email')
        raw_password = data.get ('password')

        if not email_input or not raw_password:
            return jsonify({
            "success": False,
            "message": "please fill email and password"
        }), 400

        is_user = User.query.filter_by(email=email_input).first()

        if not is_user or not is_user.check_password(raw_password):
            return jsonify({
            "success": False,
            "message": "Wrong email or password"
        }), 401

        access_token = create_access_token(
        identity=str(is_user.id),
        additional_claims={"email": is_user.email})

        return jsonify({
        "success": True,
        "access_token": access_token
        }), 200
        

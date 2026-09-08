from flask import Blueprint, jsonify, request
from utils import db
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token, verify_jwt_in_request, get_jwt


auth_bp = Blueprint('auth', __name__)


#1=============================== user Login =========================
@auth_bp.route("/login", methods=["POST"])
def user_login():
    
    data = request.get_json() or {}

    email_input = data.get('email')
    raw_password = data.get('password')

    if not email_input or not raw_password:
        return jsonify({
            "success": False,
            "message": "please fill email or password"
        }), 400

    is_user = User.query.filter_by(email=email_input).first()

    if not is_user or not is_user.check_password(raw_password):
        return jsonify({
            "success": False,
            "message": "Wrong email or password"
        }), 401

    access_token = create_access_token(
        identity=str(is_user.id),
        additional_claims={"email": is_user.email,
                            "role" : is_user.role}
    )

    refresh_token = create_refresh_token(identity=str(is_user.id))

    return jsonify({
        "success": True,
        "access_token": access_token
    }), 200

#2=============================== Admin Login =========================
@auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json() or {}

    email_input = data.get("email")
    raw_password = data.get("password")


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

    if is_user.role.lower() != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied. Only admin can login here"
        }), 403

    access_token = create_access_token(
        identity=str(is_user.id),
        additional_claims={
            "email": is_user.email,
            "role": is_user.role
        }
    )

    refresh_token = create_refresh_token(identity=str(is_user.id))

    return jsonify({
        "success": True,
        "access_token": access_token
    }), 200
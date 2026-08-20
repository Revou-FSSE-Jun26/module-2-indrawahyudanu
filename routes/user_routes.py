from flask import Blueprint ,jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from utils import db

from models import User

user_bp = Blueprint('users', __name__, url_prefix='/users')

# POST — create new user
@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        raw_password = data.get('password')
        hashed_password = generate_password_hash(raw_password) if raw_password else None
        # TODO: Create a user instance from 'data', add to session, commit, return 201
        user = User(
            customer_name=data.get('customer_name'),
            email=data.get('email'),
            password_hash=hashed_password,
            role=data.get('role', 'user')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"user created",
                        "user": user.to_dict(),
                        "status":"ok"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" :"error creating user",
                        "error" : str(e),
                        "status" : "error"}),400

# GET one user by ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # TODO: Fetch product by ID; return 404 if not found
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error" : "user not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
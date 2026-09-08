from flask import Blueprint ,jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from utils import db
from flask_jwt_extended import jwt_required

from models import User

user_bp = Blueprint('users', __name__, url_prefix='/users')


#1== POST — create new user ====
@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json() or {}

        customer_name = data.get('customer_name')
        email = data.get('email')
        raw_password = data.get('password') or data.get('password_hash') # Mendukung key 'password' maupun 'password_hash'

        if not customer_name or not email or not raw_password:
            return jsonify({'error': 'customer_name, email, and password are required'}), 400

        #2. Tangani role dengan aman (default ke 'user' jika kosong/None)
        user_role = data.get('role') or 'user'
        
        hashed_password = generate_password_hash(raw_password)

        # TODO: Create a user instance from 'data', add to session, commit, return 201
        new_user = User(customer_name=data.get('customer_name'),
                    email=data.get('email'),
                    password_hash=hashed_password,
                    role=data.get('role', 'user')
                    )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"New user created",
                        "new_user": new_user.to_dict(),
                        "status":"ok"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" :"error creating user",
                        "error" : str(e),
                        "status" : "error"}),400


#2=== GET one user by ID ====
@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required ()
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
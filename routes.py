from flask import Blueprint ,jsonify, request
from werkzeug.security import generate_password_hash
from utils import db

from models import Category
from models import Product
from models import User

main_bp = Blueprint('main', __name__, url_prefix='/shop')



# GET home route
@main_bp.route('/')
def home():
    return jsonify({"message": "demo, status, oke "})


# POST — create a product
@main_bp.route('/product', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        # TODO: Create a Product instance from 'data', add to session, commit, return 201
        product = Product(
            name=data.get('name'),
            sku=data.get('sku'),
            stock=data.get('stock'),
            price=data.get('price'),
            category_id=data.get('category_id'),
            is_in_stock=data.get('is_in_stock',True)
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"product created",
                        "product": product.to_dict(),
                        "status":"ok"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" :"error creating product",
                        "error" : str(e),
                        "status" : "error"}),400


# GET all products
@main_bp.route('/products', methods=['GET'])
def get_products():
    # TODO: Query all products, return as JSON list
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error" : str(e)}), 500


# GET one product by ID
@main_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # TODO: Fetch product by ID; return 404 if not found
    try:
        product = Product.query.get(product_id)
        if product:
            return jsonify(product.to_dict()), 200
        else:
            return jsonify({"error" : "product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET product by category ID
@main_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)


    return jsonify({
    "id" : category.id,
    "name" :category.name,
    "products" : [
        {
            "id" :  product.id,
            "name" : product.name,
            "sku" : product.sku,
            "price" : product.price,
            "stock" : product.stock,
            "is_in_stock": product.is_in_stock,
        } for product in category.products
        ]

    }), 200


# POST — create new user
@main_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        raw_password = data.get('password')
        hashed_password = generate_password_hash(raw_password) if raw_password else None
        # TODO: Create a user instance from 'data', add to session, commit, return 201
        user = User(
            username=data.get('username'),
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
@main_bp.route('/users/<int:user_id>', methods=['GET'])
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
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from app import app, db
from models import Product
from models import User

# GET home route
@app.route('/')
def home():
    return jsonify({"message": "demo, status, oke "})




# GET all products
@app.route('/products', methods=['GET'])
def get_products():
    # TODO: Query all products, return as JSON list
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error" : str(e)}), 500




    # POST — create a product
@app.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        # TODO: Create a Product instance from 'data', add to session, commit, return 201
        product = Product(
            name=data.get('name'),
            sku=data.get('sku'),
            stock=data.get('stock'),
            price=data.get('price'),
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





# GET one product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
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




# POST — create new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        raw_password = data.get('password')
        hashed_password = generate_password_hash(raw_password) if raw_password else None
        # TODO: Create a user instance from 'data', add to session, commit, return 201
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=hashed_password
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

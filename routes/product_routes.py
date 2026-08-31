from flask import Blueprint ,jsonify, request
from utils import db
from models import Product

product_bp = Blueprint('product', __name__, url_prefix='/products')


#1=================== POST — create new a product=================
@product_bp.route('/', methods=['POST'])
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
        price = data.get('price')
        if price is None or price < 0:
            return jsonify({
        "message": "invalid price",
        "error": "price must be a non-negative number",
        "status": "error"
            }), 400


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


#2=============== GET, List all products===============================
@product_bp.route('/', methods=['GET'])
def get_products():
    # TODO: Query all products, return as JSON list
    try:
        products = Product.query.filter_by(is_deleted=False).all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error" : str(e)}), 500


# 3 ================ GET specific product by ID============================
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # TODO: Fetch product by ID; return 404 if not found
    try:
        product = Product.query.filter_by(id=product_id, is_deleted=False).first()
        if product:
            return jsonify(product.to_dict()), 200
        else:
            return jsonify({"error" : "product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4 ===============PUT, update product==================================
@product_bp.route('/<int:product_id>',methods = ['PUT'])
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error" : "product not found"}), 404

        data = request.get_json()
        product.name = data.get('name', product.name)
        product.sku = data.get('sku', product.sku)
        product.stock = data.get('stock', product.stock)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)

        db.session.commit()

        return jsonify({"message" : "product updated",
        "product" : product.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}), 500



#DELETE product by ID
@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id, is_deleted=False).first()
        if not product:
            return jsonify({"error" : "product not found"}), 404

        product.is_deleted = True
        db.session.commit()

        return jsonify({"message" : "product deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}), 500
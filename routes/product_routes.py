from flask import Blueprint ,jsonify, request
from utils import db
from models import Product

product_bp = Blueprint('main', __name__, url_prefix='/products')


# POST — create new a product
@product_bp.route('/new', methods=['POST'])
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
@product_bp.route('/all', methods=['GET'])
def get_products():
    # TODO: Query all products, return as JSON list
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error" : str(e)}), 500


# GET one product by ID
@product_bp.route('/<int:product_id>', methods=['GET'])
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

# PUTT update product
@product_bp.route('/update/<int:product_id>',methods = ['PUT'])
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

# GET product by category ID
@product_bp.route('/categories/<int:category_id>', methods=['GET'])
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

#DELETE product by ID
@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error" : "product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message" : "product deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}), 500
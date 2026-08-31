from flask import Blueprint ,jsonify, request
from utils import db
from models import Category


category_bp = Blueprint('category', __name__, url_prefix='/categories')

#Create a new category
@category_bp.route('/', methods=['POST'])
def create_category():
    try:
        data = request.get_json()
        category = Category (
            name=data.get('name')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({"message" :"category created",
                        "category" : category.to_dict(),
                        "status"  : "ok"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message" : "error. creating category",
                        "error"   : str(e),
                        "status"  : "error"}), 400

# GET list all categories
@category_bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET product by category ID
@category_bp.route('/<int:category_id>', methods=['GET'])
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
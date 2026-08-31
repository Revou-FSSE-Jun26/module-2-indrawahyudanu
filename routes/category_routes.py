from flask import Blueprint ,jsonify, request
from utils import db
from models import Category


category_bp = Blueprint('category', __name__, url_prefix='/categories')

#1=============Create a new category=======================
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

#2============== GET list all categories==================
@category_bp.route('/', methods=['GET'])
def get_categories():
    try:
        category = Category.query.filter_by(is_deleted=False).all()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#3 ================GET product by category ID======================
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

#4 =======================Update a cactegory======================
@category_bp.route('/<int:category_id>', methods=['PUT'])
def put_category(category_id): 
    try:
        category = Category.query.get(category_id)
        if not category:
                    return jsonify({"error" : "product not found"}), 404

        data = request.get_json()
        category.name = data.get('name', category.name)

        db.session.commit()
        return jsonify({"message" : "category updated",
                "category" : category.to_dict()}), 200
    
    except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 500

# #5 =======================Delete a cactegory======================
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id): 
    try:
        category = Category.queery.filter_by(id=category_id, is_deleted=False).first()      
        if not category:
            return jsonify({"error" : "category not found"}), 404

        category.is_deleted = True
        db.session.commit()

        return jsonify({"message" : "category deleted"}), 200

    except Exception as e:
            db.session.rollback()
            return jsonify({"error" : str(e)}), 500
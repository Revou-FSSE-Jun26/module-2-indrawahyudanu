from flask import Blueprint, jsonify, request
from utils import db, slugify
from models import Category
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

category_bp = Blueprint("category", __name__, url_prefix="/categories")

# 1 ============== Create a new category =================
@category_bp.route("/", methods=["POST"])
def create_category():
    try:
        data = request.get_json(silent=True) if request.is_json else (request.form or {})

        image_name = None
        file = request.files.get('image')
        if file and file.filename != '':
            image_name = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))

        cat_name = data.get("name")
        cat_slug = data.get("slug") or slugify(cat_name)

        category = Category(
            name=cat_name,
            slug=cat_slug,
            image=image_name
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({
            "message": "category created",
            "category": category.to_dict(),
            "status": "ok"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "error creating category",
            "error": str(e),
            "status": "error"
        }), 400


# 2 ============== GET list all categories =================
@category_bp.route('/', methods=['GET'])
def get_all_categories():
    try:
        categories = Category.query.filter_by(is_deleted=False).all()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3 ============== GET category by ID or Slug =================
@category_bp.route('/<category_identifier>', methods=['GET'])
def get_category(category_identifier):
    try:
        # Jika angka, cari berdasarkan ID. Jika teks, cari berdasarkan slug.
        if category_identifier.isdigit():
            category = Category.query.filter_by(id=int(category_identifier), is_deleted=False).first()
        else:
            category = Category.query.filter_by(slug=category_identifier, is_deleted=False).first()

        if not category:
            return jsonify({"error": "category not found"}), 404

        return jsonify({
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "image": f"/static/uploads/{category.image}" if category.image else None,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "sku": product.sku,
                    "price": product.price,
                    "stock": product.stock,
                    "is_in_stock": product.is_in_stock,
                } for product in category.products if not product.is_deleted
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4 ======================= Update a category ======================
@category_bp.route('/<int:category_id>', methods=['PUT'])
def put_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "category not found"}), 404

        data = request.get_json(silent=True) if request.is_json else (request.form or {})

        file = request.files.get('image')
        if file and file.filename != '':
            image_name = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))
            category.image = image_name

        if 'name' in data:
            category.name = data.get('name')
            category.slug = data.get('slug') or slugify(category.name)
        elif 'slug' in data:
            category.slug = slugify(data.get('slug'))

        db.session.commit()
        return jsonify({
            "message": "category updated",
            "category": category.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 5 ======================= Delete a category ======================
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.filter_by(id=category_id, is_deleted=False).first()
        if not category:
            return jsonify({"error": "category not found"}), 404

        category.is_deleted = True
        db.session.commit()

        return jsonify({"message": "category deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 6 ================ Restore category by ID ======================
@category_bp.route('/<int:category_id>/restore', methods=['PUT'])
def restore_category(category_id):
    try:
        category = Category.query.filter_by(id=category_id, is_deleted=True).first()
        if not category:
            return jsonify({"error": "category not found"}), 404

        category.is_deleted = False
        db.session.commit()

        return jsonify({"message": "category restored successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

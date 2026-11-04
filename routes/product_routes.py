from flask import Blueprint ,jsonify, request
from utils import db
from models import Product, Category
from sqlalchemy import or_, func

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


product_bp = Blueprint('product', __name__, url_prefix='/products')


def _check_category(raw):
    """Cek category_id: harus integer, ada, dan belum dihapus.
    Return None jika valid, atau (status_code, pesan) jika tidak."""
    if isinstance(raw, bool):
        return 400, "category_id must be an integer"
    try:
        cid = int(raw)
    except (ValueError, TypeError):
        return 400, "category_id must be an integer"
    if not Category.query.filter_by(id=cid, is_deleted=False).first():
        return 404, "category not found"
    return None


#1=================== POST — create new a product=================
@product_bp.route('/', methods=['POST'])
def create_product():
    try:
        data = request.get_json(silent=True) if request.is_json else (request.form or {})

        if data.get('category_id') is not None:
            category_error = _check_category(data.get('category_id'))
            if category_error:
                code, msg = category_error
                return jsonify({
                    "message": "invalid category",
                    "error": msg,
                    "status": "error"
                }), code

        image_name = None
        file = request.files.get('image')
        if file and file.filename != '':
            image_name = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))


        product = Product(
            name=data.get('name'),
            sku=data.get('sku'),
            stock=data.get('stock'),
            price=data.get('price'),
            category_id=data.get('category_id'),
            is_in_stock=data.get('is_in_stock',True),
            is_sale=data.get('is_sale', False),
            image=image_name

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
    try:
        # outerjoin: produk tanpa kategori tetap tampil, produk dengan kategori terhapus disembunyikan
        query = Product.query.outerjoin(Category, Product.category_id == Category.id).filter(
            Product.is_deleted == False,
            or_(Product.category_id.is_(None), Category.is_deleted == False)
        )

        is_sale = request.args.get('is_sale')   # baca query param
        if is_sale == 'true':
            query = query.filter(Product.is_sale == True)

        category_id = request.args.get('category_id')
        if category_id not in (None, ''):
            try:
                cid = int(category_id)
            except ValueError:
                return jsonify({"error": "category_id must be an integer"}), 400
            query = query.filter(Product.category_id == cid, Category.is_deleted == False)

        category = (request.args.get('category') or '').strip().lower()
        if category:
            query = query.filter(
                Category.is_deleted == False,
                or_(func.lower(Category.slug) == category, func.lower(Category.name) == category)
            )

        q = request.args.get('q')          # baca ?q= dari URL
        if q:
            query = query.filter(Product.name.ilike(f"%{q}%"))

            
        products = query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
@product_bp.route('/<int:product_id>', methods=['PUT'])
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "product not found"}), 404

        # Aman: baca JSON jika JSON, baca form jika form-data
        data = request.get_json(silent=True) if request.is_json else (request.form or {})

        if data.get('category_id') is not None:
            category_error = _check_category(data.get('category_id'))
            if category_error:
                code, msg = category_error
                return jsonify({"error": msg}), code

        # Handle jika ada upload foto
        file = request.files.get('image')
        if file and file.filename != '':
            image_name = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_name))
            product.image = image_name

        product.name = data.get('name', product.name)
        product.sku = data.get('sku', product.sku)
        product.stock = data.get('stock', product.stock)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)
        product.is_sale = data.get('is_sale', product.is_sale)

        db.session.commit()

        return jsonify({
            "message": "product updated",
            "product": product.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




#5 ================DELETE product by ID======================
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id, is_deleted=False).first()
        if not product:
            return jsonify({"error" : "product not found"}), 404

        product.is_deleted = True
        db.session.commit()

        return jsonify({"message": "product deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}), 500

#6 ================Restore product from delete by ID======================
@product_bp.route('/<int:product_id>/restore', methods=['PUT'])
def restore_product(product_id):
    try:
        product = Product.query.filter_by(id=product_id, is_deleted=True).first()
        if not product:
            return jsonify({"error" : "product not found"}), 404

        product.is_deleted = False
        db.session.commit()

        return jsonify({"message": "product restored successfully" }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}), 500

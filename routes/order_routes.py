from flask import Blueprint ,jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import db
from models import Order, OrderItem, Product


order_bp = Blueprint('order', __name__, url_prefix='/orders')

#1=========new orders===========
@order_bp.route('/', methods=['POST'])
@jwt_required()

def create_order():
    current_user_id = get_jwt_identity()

    data = request.get_json () or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id:
        return jsonify({"succes":False, "Message" : "product_id is required"}), 400


    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    item_subtotal = float(product.price)*quantity
    total_amount = item_subtotal
    

    new_order = Order(
        user_id=int(current_user_id),
        total_amount=total_amount,
        status='pending'
    )
    db.session.add(new_order)
    db.session.flush()

    order_item = OrderItem(
    order_id=new_order.id,
        product_id=product_id,
        quantity=quantity,
        subtotal=item_subtotal
    )
    db.session.add(order_item)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Order created successfully",
        "data": {
            "order_id": new_order.id,
            "user_id": new_order.user_id,
            "total_amount": new_order.total_amount,
            "status": new_order.status
        }
    }), 201


#2=========List all orders===========
@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_order():
    try:
            orders = Order.query.filter_by(is_deleted=False).all()

            if not orders:
                return jsonify({"succes":False,
                                "message":"Data order tidak ditemukan"}), 404
            return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
            return jsonify({"error" : str(e)}), 500


#3=========View a specific order===========
@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_by_id(order_id):
    try:
        order = Order.query.filter_by(id=order_id, is_deleted=False).first()
        if order:
            return jsonify(order.to_dict()), 200
        else:
            return jsonify({"error" : "Order not found"}), 404
    except Exception as e:
            return jsonify({"error": str(e)}), 500


#4=========Delete order===========
@order_bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    try:
        order = Order.query.filter_by(id=order_id, is_deleted=False).first()
        if not order:
            return jsonify({"error" : "orders not found"}), 404

        order.is_deleted = True
        db.session.commit()

        return jsonify({"message" : "order deleted"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : str(e)}), 500

#4=========Delete order item ===========

@order_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_order_item(item_id):
    try:
        current_user_id = get_jwt_identity()
        
        item = OrderItem.query.get(item_id)
        
        if not item:
            return jsonify({"message": "Item not found"}), 404
            
        #  Validasi keamanan:item ini milik order pengguna yang sedang login
        if item.order.user_id != int(current_user_id):
            return jsonify({"message": "Acces denied"}), 403
            

        db.session.delete(item)
        
        #.Recalculate total_amount 
        order = item.order
        order.total_amount -= item.subtotal
        
        db.session.commit()
        
        return jsonify({"message": "Delete order Item Succesfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
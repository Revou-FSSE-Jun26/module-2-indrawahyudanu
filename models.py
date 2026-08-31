from datetime import datetime
from utils import db
from werkzeug.security import generate_password_hash, check_password_hash


#== 1. Table users====
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, server_default="'customer'")
    password_hash = db.Column(db.String(255), nullable=False, server_default="'passwordhas123'")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self): 
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "email": self.email,
            "role" : self.role,
            "created_at": ( self.created_at.isoformat() if self.created_at else None),
        }

    def hashed_password(self, raw_pass):
        self.password_hash = generate_password_hash(raw_pass)

    def check_password(self, raw_pass):
        return check_password_hash(self.password_hash, raw_pass)

#=== 2. Table category====
class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, server_default='false')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


#== 3. Table Products===
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, server_default='false')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "stock": self.stock,
            "is_in_stock": self.is_in_stock,
            "category_id": self.category_id,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "is_deleted" : self.is_deleted,
            "category_name" : self.category.name if self.category else None
        }

#==4. Table orders===
class Order(db.Model):
    __tablename__= "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='pending')
    

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "customer_name" : self.user.customer_name if self.user else None,
            "total_amount": ( float(self.total_amount) if self.total_amount else 0.0),
            "order_date": ( self.order_date.isoformat() if self.order_date else None),
            "status": self.status
        }

#==5. Table orders_item===
class OrderItem(db.Model):
    __tablename__= "orders_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
                "id": self.id,
                "order_id": self.order_id,
                "product_id": self.product_id,
                "quantity": self.quantity,
                "subtotal": float(self.subtotal) if self.subtotal else 0.0
                }
from config import Config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

from models import Product, User, Category, Order
import routes

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "Flask is connected to PostgreSQL!", "status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
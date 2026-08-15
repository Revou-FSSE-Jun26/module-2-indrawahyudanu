from config import Config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

with app.app_context():
    from models import Product, User

    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "Flask is connected to PostgreSQL!", "status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify
from flask_migrate import Migrate 
from config import Config
from utils import db
from routes import main_bp


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

from models import Product
from models import User
from models import Category
from models import Order
import routes

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
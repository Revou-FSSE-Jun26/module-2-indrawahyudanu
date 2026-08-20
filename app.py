from flask import Flask, jsonify
from flask_migrate import Migrate 
from config import Config
from utils import db
from flask_jwt_extended import JWTManager

import os
from dotenv import load_dotenv


app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

import models

from routes.routes import home_bp
from routes.user_routes import user_bp
from routes.product_routes import product_bp

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run(debug=True)
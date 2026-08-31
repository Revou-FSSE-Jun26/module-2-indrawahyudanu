from flask import Flask, jsonify
from flask_migrate import Migrate 
from config import Config
from utils import db
from flask_jwt_extended import JWTManager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    # Allow overriding config with a dict (e.g. in tests)
    if isinstance(config_class, dict):
        app.config.update(config_class)
    elif config_class is not Config:
        app.config.from_object(config_class)


    db.init_app(app)
    migrate = Migrate(app, db)

    import models

    from routes.routes import home_bp
    from routes.user_routes import user_bp
    from routes.product_routes import product_bp
    from routes.category_routes import category_bp
    from routes.auth_routes import auth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

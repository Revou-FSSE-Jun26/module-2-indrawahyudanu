# tests/conftest.py
import pytest
from app import create_app
from utils import db as _db
from models import Product, Category

@pytest.fixture(scope='module')
def app():
    flask_app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with flask_app.app_context():
        _db.create_all()

        # TODO: seed one Category and two Products here
         # Hint: _db.session.add(obj) then _db.session.commit()
        category = Category(name="Electronics")
        _db.session.add(category)
        _db.session.flush()

        product1 = Product(name="iphone", sku="PHN-001", price=999.99, stock=10, category_id=category.id)
        product2 = Product(name="samsung", sku="SMN-001", price=699.99, stock=5, category_id=category.id)
        _db.session.add_all([product1, product2])
        _db.session.commit()

        yield flask_app

        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


# tests/conftest.py
import pytest
from app import create_app  # App factory asli kamu
from utils import db as _db  # Database instance asli kamu
from models import Product, Category  # Model SQLAlchemy asli kamu


@pytest.fixture(scope="module")
def app():
    # 1. Jalankan app asli kamu dengan konfigurasi TESTING
    flask_app = create_app({
        "TESTING": True,
        # Menggunakan SQLite memory supaya database testing cepat & bersih otomatis
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with flask_app.app_context():
        _db.create_all()  # Membikin tabel berdasarkan skema Model aslimu

        # 2. Masukkan data dummy awal (seeding) menggunakan Model aslimu
        category = Category(name="Electronics")
        _db.session.add(category)
        _db.session.flush()

        p1 = Product(
            name="iphone",
            sku="PHN-001",
            price=999.99,
            stock=10,
            category_id=category.id,
        )
        _db.session.add(p1)
        _db.session.commit()

        yield flask_app

        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
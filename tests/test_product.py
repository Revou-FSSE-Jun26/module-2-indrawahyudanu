from models import Product, Category
from utils import db


def _make_category(app, name, deleted=False):
    with app.app_context():
        category = Category(name=name)
        category.is_deleted = deleted
        db.session.add(category)
        db.session.commit()
        return category.id


def _make_product(app, name, sku, category_id, **kwargs):
    with app.app_context():
        product = Product(name=name, sku=sku, price=1000, stock=5, category_id=category_id, **kwargs)
        db.session.add(product)
        db.session.commit()
        return product.id


#POST test
def test_create_real_product(client):
    new_product_data = {
        "name": "Samsung Flip",
        "sku": "Samsung-flip",
        "price": 20000000,
        "stock": 30,
        "category_id": 1,
    }

    response = client.post("/products/", json=new_product_data)

    assert response.status_code == 201
    assert response.get_json()["product"]["name"] == "Samsung Flip"

# GET test

def test_get_all_products_success(client):
    #Happy Path: Mengambil seluruh daftar produk (harus mengembalikan 200 OK & List)."""
    response = client.get('/products/')

    # Assert Status Code
    assert response.status_code == 200

    # Assert Tipe Data Response
    data = response.get_json()
    assert isinstance(data, list)

    # Assert Data Seed dari conftest.py ter-load dengan benar (minimal ada 2 produk)
    assert len(data) >= 2


# Filter kategori
def test_filter_by_category_id(client, app):
    tv_id = _make_category(app, "TV")
    audio_id = _make_category(app, "Audio")
    _make_product(app, "Smart TV", "TV-001", tv_id)
    _make_product(app, "Speaker", "AUD-001", audio_id)

    response = client.get(f'/products/?category_id={tv_id}')

    assert response.status_code == 200
    data = response.get_json()
    assert [p["name"] for p in data] == ["Smart TV"]
    assert all(p["category_id"] == tv_id for p in data)


def test_filter_by_category_slug_and_name_case_insensitive(client, app):
    ha_id = _make_category(app, "Home Appliances")
    _make_product(app, "Blender", "HA-001", ha_id)

    for value in ("tv", "TV", "Tv"):
        data = client.get(f'/products/?category={value}').get_json()
        assert [p["name"] for p in data] == ["Smart TV"]

    for value in ("home appliances", "Home Appliances", "home-appliances", "HOME-APPLIANCES"):
        response = client.get(f'/products/?category={value}')
        assert response.status_code == 200
        assert [p["name"] for p in response.get_json()] == ["Blender"]


def test_invalid_category_id_returns_400(client):
    response = client.get('/products/?category_id=abc')

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_unknown_category_returns_empty_list(client):
    response = client.get('/products/?category=nope')

    assert response.status_code == 200
    assert response.get_json() == []


def test_deleted_category_excluded(client, app):
    cat_id = _make_category(app, "Old Stuff", deleted=True)
    _make_product(app, "Ghost Item", "OLD-001", cat_id)

    assert client.get(f'/products/?category_id={cat_id}').get_json() == []
    assert client.get('/products/?category=old-stuff').get_json() == []
    names = [p["name"] for p in client.get('/products/').get_json()]
    assert "Ghost Item" not in names


def test_null_category_product_still_listed(client, app):
    _make_product(app, "No Category Item", "NOCAT-001", None)

    names = [p["name"] for p in client.get('/products/').get_json()]
    assert "No Category Item" in names


def test_is_sale_and_q_still_work(client, app):
    cat_id = _make_category(app, "Gadget")
    _make_product(app, "Gadget Sale", "GAD-001", cat_id, is_sale=True)
    _make_product(app, "Gadget Normal", "GAD-002", cat_id)

    sale = client.get(f'/products/?category_id={cat_id}&is_sale=true').get_json()
    assert [p["name"] for p in sale] == ["Gadget Sale"]

    searched = client.get(f'/products/?category_id={cat_id}&q=normal').get_json()
    assert [p["name"] for p in searched] == ["Gadget Normal"]


# Validasi category_id pada create/update
def test_create_product_invalid_category(client, app):
    deleted_id = _make_category(app, "Removed Cat", deleted=True)
    base = {"name": "Bad Cat Product", "price": 1000, "stock": 1}

    r = client.post("/products/", json={**base, "sku": "BAD-1", "category_id": 99999})
    assert r.status_code == 404
    r = client.post("/products/", json={**base, "sku": "BAD-2", "category_id": deleted_id})
    assert r.status_code == 404
    r = client.post("/products/", json={**base, "sku": "BAD-3", "category_id": "abc"})
    assert r.status_code == 400

    with app.app_context():
        assert Product.query.filter_by(name="Bad Cat Product").count() == 0


def test_update_product_invalid_category(client, app):
    cat_id = _make_category(app, "Update Cat")
    deleted_id = _make_category(app, "Update Deleted Cat", deleted=True)
    pid = _make_product(app, "Updatable", "UPD-001", cat_id)

    assert client.put(f'/products/{pid}', json={"category_id": 99999}).status_code == 404
    assert client.put(f'/products/{pid}', json={"category_id": deleted_id}).status_code == 404
    with app.app_context():
        assert db.session.get(Product, pid).category_id == cat_id

    other_id = _make_category(app, "Update Other Cat")
    response = client.put(f'/products/{pid}', json={"category_id": other_id})
    assert response.status_code == 200
    assert response.get_json()["product"]["category_id"] == other_id

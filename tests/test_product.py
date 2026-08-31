# ─── GET /products ───────────────────────────────────────────────────
def test_get_all_products_not_empty(client):
    response = client.get('/products/')

    # 1: assert status code is 200
    assert response.status_code == 200

    # 2: parse JSON and assert it is a list
    data = response.get_json()
    assert isinstance(data, list)

    # 3: assert the first item has keys 'id', 'name', 'price'
    assert len(data) > 0
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'price' in data[0]


# ─── POST /products ──────────────────────────────────────────────────
def test_create_product_returns_201(client):
    payload = {
        'name': 'webcam',
        'sku': 'sku_004',
        'price': 590000,
        'stock': 67,
        'category_id': 1,
    }
    response = client.post('/products/', json=payload)

    assert response.status_code == 201

    data = response.get_json()
    # route mengembalikan {"message":..., "product": {...}, "status":"ok"}
    product = data['product']
    assert product['name'] == 'webcam'
    assert product['price'] == 590000
    assert product['sku'] == 'sku_004'
    assert product['stock'] == 67
    assert 'id' in product    # server must have assigned a new ID


def test_create_product_missing_name_returns_400(client):
    # POST tanpa 'name' — lihat apa yang dikembalikan route
    payload = {
        # 'name' is intentionally missing
        'sku': 'sku_missing_name',
        'price': 590000,
        'stock': 67,
        'category_id': 1,
    }
    response = client.post('/products/', json=payload)

    data = response.get_json()
    print(f"\n[MISSING NAME] status={response.status_code}")
    print(f"[MISSING NAME] data={data}")


def test_create_product_negative_price_returns_400(client):
    # POST dengan price negatif — lihat apa yang dikembalikan route
    payload = {
        'name': 'webcam',
        'sku': 'sku_negative',
        'price': -590000,
        'stock': 67,
        'category_id': 1,
    }
    response = client.post('/products/', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    


# # ─── GET /products/<id> ──────────────────────────────────────────────
# def test_get_product_by_id_returns_200(client):
#     # TODO: GET /products/1 (seeded as 'Laptop' in conftest.py)
#     # Assert: status_code == 200, data['id'] == 1, data['name'] == 'Laptop'
#     pass


# def test_get_product_nonexistent_returns_404(client):
#     # TODO: GET /products/9999
#     # Assert: status_code == 404
#     pass


# # ─── PUT /products/<id> ──────────────────────────────────────────────
# def test_update_product_returns_200(client):
#     # TODO: PUT /products/2 with {'price': 19.99}
#     # Assert: status_code == 200, data['price'] == 19.99
#     pass
#POST test
def test_create_real_product(client):
    new_product_data = {
        "name": "Samsung Flip",
        "sku": "Samsung-flip",
        "price": 20000000,
        "stock": 30,
        "category_id": 2,
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


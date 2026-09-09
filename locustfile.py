from locust import HttpUser, task, between

class RevoShopUser(HttpUser):
    wait_time = between(1, 2)
    token = None

    def on_start(self):
        login_payload = {
            "email": "cak.edo@example.com",  
            "password": "rahasia123"        
        }
        res = self.client.post("/user/login", json=login_payload, name="[Auth] Login")
        
        if res.status_code == 200:
            self.token = res.json().get("access_token")
        else:
            print(f"Login gagal! Status Code: {res.status_code}, Response: {res.text}")

    # 1. Test Public Endpoints
    @task(4)
    def get_products(self):
        self.client.get("/products/", name="[Public] Get Products")

    @task(3)
    def get_categories(self):
        self.client.get("/categories/", name="[Public] Get Categories")

    # 2. Test Protected Endpoints (Butuh JWT Token)
    @task(2)
    def get_orders(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/orders/", headers=headers, name="[Protected] Get Orders")

    @task(1)
    def create_order(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "product_id": 1,
                "quantity": 1
            }
            self.client.post("/orders/", json=payload, headers=headers, name="[Protected] Post Order")
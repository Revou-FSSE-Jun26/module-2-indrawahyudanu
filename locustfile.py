from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_products(self):
        self.client.get("/products")

    @task
    def get_categories(self):
        self.client.get("/products")
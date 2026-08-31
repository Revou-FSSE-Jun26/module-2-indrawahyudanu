from locust import HttpUser, task, between


class FlaskAPIUser(HttpUser):
    # TODO 1: set wait_time to a random between 1 and 2 seconds
    wait_time =between(1,2)

    @task(3)
    def browse_products(self):
        # TODO 2: send a GET request to /products
        self.client.get('/products/')

    @task(1)
    def view_product(self):
        # TODO 3: send a GET request to /products/1
        # Remember: use name='/products/<id>' to group dynamic URLs in the UI
        self.client.get('/products/5', name='/products/<id>')
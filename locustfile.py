from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_temperature(self):
        self.client.get("/temperature")

    @task
    def get_rain(self):
        self.client.get("/rain")

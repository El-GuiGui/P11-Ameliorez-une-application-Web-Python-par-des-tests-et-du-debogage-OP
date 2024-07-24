from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces", data={"club": "Simply Lift", "competition": "Spring Festival", "places": "1"}
        )

    @task
    def points_board(self):
        self.client.get("/pointsdisplayboard")

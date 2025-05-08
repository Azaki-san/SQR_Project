from locust import HttpUser, task, between
import random
import os


def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


class FastAPIUser(HttpUser):
    wait_time = between(0.5, 2.5)
    test_video_path = "test.mp4"

    def on_start(self):
        """Initialize a random IP for each virtual user"""
        self.viewer_ip = generate_random_ip()

    @task(3)
    def get_video(self):
        with self.client.get("/video", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to get video: {response.status_code}")

    @task(2)
    def send_ping(self):
        headers = {"X-Forwarded-For": self.viewer_ip}
        with self.client.post("/ping", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Ping failed: {response.status_code}")

    @task(1)
    def check_status(self):
        self.client.get("/status")

    @task(1)
    def get_weather(self):
        self.client.get("/weather")

    @task(1)
    def get_stats(self):
        self.client.get("/stats")

    @task(1)
    def upload_video(self):
        if not os.path.exists(self.test_video_path):
            raise Exception("Test video file not found")

        with open(self.test_video_path, "rb") as file:
            headers = {"X-Forwarded-For": self.viewer_ip}
            files = {"file": (self.test_video_path, file, "video/mp4")}
            with self.client.post("/upload", files=files, headers=headers, catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Upload failed: {response.status_code}")
import pytest
from unittest import mock
import requests
import time
import threading
from frontend.api import get_video_status, start_ping_thread, get_weather_status


def test_get_video_status_success():
    mock_response = mock.Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "status": "playing",
        "elapsed": 100,
        "filename": "test_video.mp4"
    }

    with mock.patch("requests.get", return_value=mock_response):
        elapsed, filename = get_video_status()
        assert elapsed == 100
        assert filename == "test_video.mp4"


def test_get_video_status_failure():
    mock_response = mock.Mock()
    mock_response.ok = False

    with mock.patch("requests.get", return_value=mock_response):
        elapsed, filename = get_video_status()
        assert elapsed == 0
        assert filename is None


def test_get_video_status_exception():
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException):
        elapsed, filename = get_video_status()
        assert elapsed == 0
        assert filename is None


# Test the get_weather_status function with mock responses
def test_get_weather_status_success():
    mock_response = mock.Mock()
    mock_response.json.return_value = {"temperature": 22, "condition": "sunny"}

    with mock.patch("requests.get", return_value=mock_response):
        weather = get_weather_status()
        assert weather == {"temperature": 22, "condition": "sunny"}


def test_get_weather_status_failure():
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException):
        weather = get_weather_status()
        assert weather == {"error": "Failed to fetch weather status"}


def test_start_ping_thread():
    with mock.patch("requests.post") as mock_post:
        with mock.patch("time.sleep", return_value=None):
            thread = threading.Thread(target=start_ping_thread)
            thread.daemon = True
            thread.start()
            time.sleep(1)
            mock_post.assert_called()

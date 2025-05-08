from app.services.weather import get_weather


def test_get_weather_success(mocker):
    mock_response = {
        "current_condition": [{
            "temp_C": "15",
            "weatherDesc": [{"value": "Clear"}]
        }]
    }

    mocker.patch("httpx.get", return_value=MockResponse(mock_response))

    result = get_weather()
    assert result["temp_C"] == "15"
    assert result["weatherDesc"] == "Clear"
    assert result["time_of_day"] in ["day", "night"]


def test_get_weather_exception(mocker):
    mocker.patch("httpx.get", side_effect=Exception("Timeout"))

    result = get_weather()
    assert "error" in result
    assert result["error"] == "Timeout"


class MockResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import httpx
from cta_bus import Client
from cta_bus.constants import API_BASE
from cta_bus.models import Direction, ErrorObject, Route, SystemTime
from cta_bus.utils import local_tz, to_datetime

gettime_response = {
    "bustime-response": {
        "error": [
            {
                "rt": "900",
                "msg": "No data found for parameter"
            }
        ],
        "tm": "20230812 00:50:15"
    }
}


gettime_unix_response = {
    "bustime-response": {
        "tm": "1691896079566"
    }
}


getdirections_response = {
    "bustime-response": {
        "directions": [
            {
                "id": "Eastbound",
                "name": "Eastbound"
            },
            {
                "id": "Westbound",
                "name": "Westbound"
            }
        ]
    }
}


getroutes_response = {
    "bustime-response": {
        "routes": [
            {
                "rt": "1",
                "rtnm": "Bronzeville/Union Station",
                "rtclr": "#336633",
                "rtdd": "1"
            },
            {
                "rt": "2",
                "rtnm": "Hyde Park Express",
                "rtclr": "#993366",
                "rtdd": "2"
            }
        ]
    }
}


getstops_response = {
    "bustime-response": {
        "stops": [
            {
                "stpid": "566",
                "stpnm": "700 W Chicago",
                "lat": 41.89639,
                "lon": -87.645590000001
            }
        ]
    }
    }


class TestClient(unittest.TestCase):
    def setUp(self: "TestClient") -> None:
        self.mocked_data = {"data": "mocked_response_data"}
        self.client = Client(api_key="your_api_key")

    @patch("httpx.get")
    def test_send_method(self: "TestClient", mock_get: Mock) -> None:
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = gettime_unix_response
        mock_get.return_value = mock_response

        response = self.client.send("/gettime", params={"unixTime": True})

        params = {
            "key": "your_api_key",
            "format": "json",
            "unixTime": True
        }

        mock_get.assert_called_once_with(f"{API_BASE}/gettime", params=params)

        assert response.json() == gettime_unix_response

    def test_to_datetime(self: "TestClient") -> None:
        fmt = "%Y-%m-%d %H:%M:%S"

        assert to_datetime("20230812 00:50:15") == datetime.strptime("2023-08-12 00:50:15", fmt).astimezone(local_tz)
        assert to_datetime("20230812 00:50") == datetime.strptime("2023-08-12 00:50:00", fmt).astimezone(local_tz)
        assert to_datetime("1691903426449") == datetime.strptime("2023-08-13 00:10:26", fmt).astimezone(local_tz)

    @patch("httpx.get")
    def test_get_time_method(self: "TestClient", mock_get: Mock) -> None:
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = gettime_response
        mock_get.return_value = mock_response

        data = self.client.get_time()

        assert isinstance(data, list)
        assert len(data) == 2

        assert isinstance(data[0], ErrorObject)
        assert isinstance(data[1], SystemTime)

        assert len(data[0].__dict__) == 2
        assert data[0].message == "No data found for parameter"
        assert data[0].error_data["rt"] == "900"

        assert len(data[1].__dict__) == 1
        assert data[1].timestamp == datetime.strptime("2023-08-12 00:50:15", "%Y-%m-%d %H:%M:%S").astimezone(local_tz)

    @patch("httpx.get")
    def test_get_directions_method(self: "TestClient", mock_get: Mock) -> None:
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = getdirections_response
        mock_get.return_value = mock_response

        data = self.client.get_directions(route_id="")  # Doesn't matter what route_id is for mock.

        assert isinstance(data, list)
        assert len(data) == 2

        assert isinstance(data[0], Direction)
        assert isinstance(data[1], Direction)

        assert len(data[0].__dict__) == 2
        assert data[0]._id == "Eastbound"
        assert data[0].name == "Eastbound"

        assert len(data[1].__dict__) == 2
        assert data[1]._id == "Westbound"
        assert data[1].name == "Westbound"

    @patch("httpx.get")
    def test_get_routes_method(self: "TestClient", mock_get: Mock) -> None:
        mock_response = Mock(spec=httpx.Response)
        mock_response.json.return_value = getroutes_response
        mock_get.return_value = mock_response

        data = self.client.get_routes()

        assert isinstance(data, list)
        assert len(data) == 2

        assert isinstance(data[0], Route)
        assert isinstance(data[1], Route)

        assert len(data[0].__dict__) == 4
        assert data[0].route_id == "1"
        assert data[0].route_name == "Bronzeville/Union Station"
        assert data[0].route_color == "#336633"
        assert data[0].route_display == "1"

        assert len(data[1].__dict__) == 4
        assert data[1].route_id == "2"
        assert data[1].route_name == "Hyde Park Express"
        assert data[1].route_color == "#993366"
        assert data[1].route_display == "2"


if __name__ == "__main__":
    unittest.main()

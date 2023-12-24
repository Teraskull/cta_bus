from __future__ import annotations

from cta_bus import Client


class TestClient(Client):
    __test__ = False

    def send(self: Client, path: str, params: dict | None = None) -> None:
        print(params, path)   # noqa: T201


bustime_response_prd = {
    "bustime-response": {
        "error": [
            {
                "msg": "No service scheduled",
                "stpid": "1"
            },
            {
                "msg": "No service scheduled",
                "stpid": "2"
            }
        ],
        "prd": [
            {
                "tmstmp": "20230724 15:16",
                "typ": "A",
                "stpnm": "Madison & Hoyne",
                "stpid": "427",
                "vid": "1901",
                "dstp": 12873,
                "rt": "20",
                "rtdd": "20",
                "rtdir": "Eastbound",
                "des": "Illinois Center",
                "prdtm": "20230724 15:33",
                "tablockid": "20 -856",
                "tatripid": "88357908",
                "origtatripno": "245964349",
                "dly": False,
                "dyn": 0,
                "prdctdn": "16",
                "zone": "",
                "psgld": "",
                "stst": 54720,
                "stsd": "2023-07-24",
                "flagstop": 0,
                "test": True
            },
            {
                "tmstmp": "20230724 15:16",
                "typ": "A",
                "stpnm": "Madison & Hoyne",
                "stpid": "427",
                "vid": "1927",
                "dstp": 18097,
                "rt": "20",
                "rtdd": "20",
                "rtdir": "Eastbound",
                "des": "Illinois Center",
                "prdtm": "20230724 15:39",
                "tablockid": "20 -851",
                "tatripid": "88357909",
                "origtatripno": "245964352",
                "dly": False,
                "dyn": 0,
                "prdctdn": "23",
                "zone": "",
                "psgld": "",
                "stst": 54210,
                "stsd": "2023-07-24",
                "flagstop": 0
            },
            {
                "tmstmp": "20230724 15:16",
                "typ": "A",
                "stpnm": "Madison & Hoyne",
                "stpid": "427",
                "vid": "1976",
                "dstp": 21761,
                "rt": "20",
                "rtdd": "20",
                "rtdir": "Eastbound",
                "des": "Illinois Center",
                "prdtm": "20230724 15:43",
                "tablockid": "20 -802",
                "tatripid": "88357907",
                "origtatripno": "245964351",
                "dly": False,
                "dyn": 0,
                "prdctdn": "27",
                "zone": "",
                "psgld": "",
                "stst": 54720,
                "stsd": "2023-07-24",
                "flagstop": 0
            }
        ]
    }
}


bustime_response_time = {
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



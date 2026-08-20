"""Cookie round-trip and JSON parsing on the session layer."""

from __future__ import annotations

import json
from pathlib import Path

import httpx

from infomentor.session import HubSession


def test_cookie_roundtrip(tmp_path: Path) -> None:
    session = HubSession()
    try:
        session.import_cookies(
            [
                {
                    "name": "imhome",
                    "value": "abc",
                    "domain": "hub.infomentor.se",
                    "path": "/",
                }
            ]
        )
        path = tmp_path / "cookies.json"
        session.save_cookies(path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload[0]["name"] == "imhome"
        other = HubSession()
        try:
            other.load_cookies(path)
            names = {cookie["name"] for cookie in other.export_cookies()}
            assert "imhome" in names
        finally:
            other.close()
    finally:
        session.close()


def test_api_post_parses_json_and_bool_text() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("isauthenticated"):
            return httpx.Response(200, text="true")
        return httpx.Response(200, json={"items": [{"id": 1, "title": "Hello"}]})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://hub.infomentor.se")
    session = HubSession(client=client)
    try:
        assert session.api_post("/authentication/authentication/isauthenticated") is True
        data = session.api_post("/Communication/News/GetNewsList", json={"pageSize": -1})
        assert data["items"][0]["title"] == "Hello"
    finally:
        session.close()
        client.close()

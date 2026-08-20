"""HTTP session with cookie persistence and Hub-aware redirect following."""

from __future__ import annotations

import json as jsonlib
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import httpx

from infomentor.constants import API_HEADERS, BROWSER_HEADERS, HUB_BASE
from infomentor.exceptions import ApiError
from infomentor.htmlutil import absolute_url

REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class HubSession:
    """Cookie-aware HTTP client used for both login and Hub API calls."""

    def __init__(
        self,
        *,
        hub_base: str = HUB_BASE,
        timeout: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        self.hub_base = hub_base.rstrip("/")
        self._owns_client = client is None
        self.client = client or httpx.Client(
            headers=BROWSER_HEADERS,
            follow_redirects=False,
            timeout=timeout,
        )

    def close(self) -> None:
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> HubSession:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def hub_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return urljoin(f"{self.hub_base}/", path.lstrip("/"))

    def request(
        self,
        method: str,
        url: str,
        *,
        follow: bool = False,
        default_origin: str | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        kwargs.setdefault("follow_redirects", False)
        response = self.client.request(method, url, **kwargs)
        if follow:
            response = self.follow(response, default_origin=default_origin)
        return response

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", url, **kwargs)

    def follow(
        self,
        response: httpx.Response,
        *,
        default_origin: str | None = None,
        max_redirects: int = 20,
    ) -> httpx.Response:
        for _ in range(max_redirects):
            if response.status_code not in REDIRECT_STATUSES:
                return response
            location = response.headers.get("location")
            if not location:
                return response
            url = absolute_url(location, str(response.url), default_origin)
            response = self.client.get(url, follow_redirects=False)
        raise ApiError(f"Exceeded {max_redirects} redirects ending at {response.url}")

    def api_request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        data: Any = None,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        expect_json: bool = True,
    ) -> Any:
        merged = dict(API_HEADERS)
        if headers:
            merged.update(headers)
        if json is not None:
            merged.setdefault("Content-Type", "application/json; charset=UTF-8")
        cache_bust = dict(params or {})
        if "_" not in cache_bust and method.upper() == "POST" and json is None and data is None:
            cache_bust["_"] = int(time.time() * 1000)
        response = self.client.request(
            method,
            self.hub_url(path),
            json=json,
            data=data,
            params=cache_bust or None,
            headers=merged,
            follow_redirects=False,
        )
        if response.status_code >= 400:
            raise ApiError(
                f"{method} {path} failed with HTTP {response.status_code}",
                status_code=response.status_code,
                body=response.text,
            )
        if not expect_json:
            return response
        if not response.content:
            return None
        content_type = response.headers.get("content-type", "")
        if "json" in content_type or response.text[:1] in "{[":
            try:
                return response.json()
            except jsonlib.JSONDecodeError as exc:
                raise ApiError(
                    f"{method} {path} returned invalid JSON",
                    status_code=response.status_code,
                    body=response.text,
                ) from exc
        text = response.text.strip()
        if text.lower() in {"true", "false"}:
            return text.lower() == "true"
        return text.strip('"')

    def api_post(self, path: str, **kwargs: Any) -> Any:
        return self.api_request("POST", path, **kwargs)

    def api_get(self, path: str, **kwargs: Any) -> Any:
        return self.api_request("GET", path, **kwargs)

    def export_cookies(self) -> list[dict[str, Any]]:
        cookies: list[dict[str, Any]] = []
        for cookie in self.client.cookies.jar:
            cookies.append(
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "secure": bool(cookie.secure),
                    "expires": cookie.expires,
                }
            )
        return cookies

    def import_cookies(self, cookies: list[dict[str, Any]]) -> None:
        for item in cookies:
            self.client.cookies.set(
                item["name"],
                item["value"],
                domain=item.get("domain") or None,
                path=item.get("path") or "/",
            )

    def save_cookies(self, path: str | Path) -> None:
        Path(path).write_text(
            jsonlib.dumps(self.export_cookies(), indent=2),
            encoding="utf-8",
        )

    def load_cookies(self, path: str | Path) -> None:
        payload = jsonlib.loads(Path(path).read_text(encoding="utf-8"))
        self.import_cookies(payload)

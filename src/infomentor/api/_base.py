"""Shared Hub resource helpers."""

from __future__ import annotations

from typing import Any

from infomentor.session import HubSession


class HubResource:
    def __init__(self, session: HubSession) -> None:
        self.session = session

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.session.api_post(path, **kwargs)

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.session.api_get(path, **kwargs)

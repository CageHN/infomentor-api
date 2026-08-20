from __future__ import annotations

from datetime import datetime, timezone

from infomentor.api._base import HubResource


class HomeworkAPI(HubResource):
    """Legacy homework endpoint used by m42e/infomentor."""

    def get(self, when: datetime | str | None = None, *, is_week: bool = True) -> dict | list:
        if when is None:
            stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00.000Z")
        elif isinstance(when, datetime):
            stamp = when.strftime("%Y-%m-%dT00:00:00.000Z")
        else:
            stamp = when
        return self.post("/Homework/homework/GetHomework", json={"date": stamp, "isWeek": is_week})

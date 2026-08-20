from __future__ import annotations

from datetime import date, datetime

from infomentor.api._base import HubResource
from infomentor.models import CalendarEntry


def format_calendar_date(value: date | datetime | str) -> str:
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value.strftime("%Y/%m/%d")
    return value.replace("-", "/")


class CalendarAPI(HubResource):
    def app_data(
        self,
        *,
        tab: str = "whole_week",
        selected_week: int | None = None,
        selected_year: int | None = None,
    ) -> dict:
        params: dict[str, str | int] = {
            "codename": "calendarv2",
            "action": tab,
            "tab": tab,
        }
        if selected_week is not None:
            params["selectedWeek"] = selected_week
        if selected_year is not None:
            params["selectedYear"] = selected_year
        return self.post("/calendarv2/calendarv2/appData", params=params) or {}

    def get_entries(
        self,
        start: date | datetime | str,
        end: date | datetime | str,
    ) -> list[CalendarEntry]:
        payload = {
            "startDate": format_calendar_date(start),
            "endDate": format_calendar_date(end),
        }
        data = self.post("/calendarv2/calendarv2/getentries", json=payload) or []
        if isinstance(data, dict):
            data = data.get("items") or data.get("entries") or []
        return [CalendarEntry.model_validate(item) for item in data]

    def get_ical_subscription_uri(self) -> str:
        payload = self.post("/calendarv2/calendarv2/geticalsubscriptionuri")
        if isinstance(payload, str):
            return payload.strip().strip('"')
        if isinstance(payload, dict):
            return str(payload.get("uri") or payload.get("url") or "")
        return str(payload or "")

    def legacy_entries(self, start: str, end: str, utc_offset: int = 0) -> dict | list:
        """Older Calendar/Calendar/getEntries used by m42e/infomentor."""
        return self.post(
            "/Calendar/Calendar/getEntries",
            data={"UTCOffset": str(utc_offset), "start": start, "end": end},
        )

    def legacy_entry(self, event_id: int | str) -> dict:
        return self.post("/Calendar/Calendar/getEntry", data={"id": event_id}) or {}

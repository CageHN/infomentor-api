from __future__ import annotations

from datetime import date, datetime, timedelta

from infomentor.api._base import HubResource
from infomentor.models import TimetableLesson


def utc_offset_minutes(when: datetime | None = None) -> int:
    now = when or datetime.now().astimezone()
    offset = now.utcoffset() or timedelta(0)
    return int(offset.total_seconds() // 60)


def format_timetable_date(value: date | datetime | str) -> str:
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value


class TimetableAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/timetable/timetable/appData") or {}

    def get_timetable_list(
        self,
        start: date | datetime | str,
        end: date | datetime | str,
        *,
        utc_offset: int | None = None,
    ) -> list[TimetableLesson]:
        payload = {
            "UTCOffset": str(utc_offset if utc_offset is not None else utc_offset_minutes()),
            "start": format_timetable_date(start),
            "end": format_timetable_date(end),
        }
        data = self.post("/timetable/timetable/gettimetablelist", data=payload) or []
        if isinstance(data, dict):
            data = data.get("items") or []
        return [TimetableLesson.model_validate(item) for item in data]

    def this_week(self, *, offset_weeks: int = 0) -> list[TimetableLesson]:
        today = date.today()
        start = today - timedelta(days=today.weekday()) + timedelta(weeks=offset_weeks)
        end = start + timedelta(days=5)
        return self.get_timetable_list(start, end)

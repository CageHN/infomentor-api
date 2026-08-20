from __future__ import annotations

from datetime import date, datetime

from infomentor.api._base import HubResource


class TimeRegistrationAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/timeregistration/timeregistration/appData") or {}

    def get_time_registrations(
        self,
        start: date | datetime | str,
        *,
        show_next_week_if_no_more_school_days: bool = True,
    ) -> dict:
        if isinstance(start, datetime):
            formatted = start.isoformat()
        elif isinstance(start, date):
            formatted = datetime(start.year, start.month, start.day).isoformat()
        else:
            formatted = start
        return (
            self.post(
                "/TimeRegistration/TimeRegistration/GetTimeRegistrations/",
                json={
                    "date": formatted,
                    "showNextWeekIfNoMoreSchoolDays": show_next_week_if_no_more_school_days,
                },
            )
            or {}
        )

    def save_time_registrations(self, days: list[dict], series=None) -> dict:
        return (
            self.post(
                "/TimeRegistration/TimeRegistration/SaveTimeRegistrations/",
                json={"days": days, "series": series},
            )
            or {}
        )

from __future__ import annotations

from datetime import datetime
from typing import Any

from infomentor.api._base import HubResource
from infomentor.models import NotificationState, NotificationsResult


class NotificationsAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/NotificationApp/NotificationApp/appData") or {}

    def list(self, timestamp: datetime | str | None = None) -> NotificationsResult:
        if timestamp is None:
            payload: dict[str, Any] = {"timestamp": "1970-01-01T00:00:00"}
        elif isinstance(timestamp, datetime):
            payload = {"timestamp": timestamp.isoformat()}
        else:
            payload = {"timestamp": timestamp}
        data = self.post("/NotificationApp/NotificationApp/GetNotifications", json=payload) or {}
        return NotificationsResult.model_validate(data)

    def update_state(self, ids: list[int], state: NotificationState | str) -> dict:
        value = state.value if isinstance(state, NotificationState) else state
        return (
            self.post(
                "/NotificationApp/NotificationApp/UpdateNotificationState",
                json={"ids": ids, "state": value},
            )
            or {}
        )

    def update_assessment_state(self, ids: list[int], state: NotificationState | str) -> dict:
        value = state.value if isinstance(state, NotificationState) else state
        return (
            self.post(
                "/NotificationApp/NotificationApp/UpdateAssessmentNotificationState",
                json={"ids": ids, "state": value},
            )
            or {}
        )

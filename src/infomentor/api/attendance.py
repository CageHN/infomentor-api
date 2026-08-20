from __future__ import annotations

from infomentor.api._base import HubResource
from infomentor.models import AttendanceItem


class AttendanceAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/attendance/attendance/appData") or {}

    def get_attendance_list(self) -> list[AttendanceItem]:
        data = self.post("/attendance/attendance/GetAttendanceList") or {}
        items = data.get("items", data) if isinstance(data, dict) else data
        if not isinstance(items, list):
            return []
        return [AttendanceItem.model_validate(item) for item in items]

    def set_secondary_status(self, item_id: int, approved: bool) -> dict:
        return (
            self.post(
                "/attendance/attendance/SetSecondaryStatus",
                json={"id": item_id, "isApproved": approved},
            )
            or {}
        )

    def register_attendance(
        self,
        *,
        present: bool,
        day: str = "today",
        reg_type: str = "day",
    ) -> dict:
        return (
            self.post(
                "/attendance/attendance/registerAttendance",
                json={
                    "present": present,
                    "day": day,
                    "RegType": reg_type,
                    "canAddSicknessToTimeRegistration": False,
                },
            )
            or {}
        )

    def get_leave_request_list(self) -> list | dict:
        return self.post("/attendance/attendance/GetLeaveRequestList") or []

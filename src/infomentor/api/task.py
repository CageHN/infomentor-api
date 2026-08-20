from __future__ import annotations

from infomentor.api._base import HubResource


class TaskAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/task/task/appData") or {}

    def get_tasks(
        self,
        academic_year_id: int | str,
        *,
        subject: int | None = None,
        teacher: int | None = None,
        course: int | None = None,
    ) -> dict:
        payload = {
            "academicYearId": str(academic_year_id),
            "subjects": None if subject is None else str(subject),
            "teachers": None if teacher is None else str(teacher),
            "courses": None if course is None else str(course),
        }
        return self.post("/Task/Task/GetTasks", json=payload) or {}

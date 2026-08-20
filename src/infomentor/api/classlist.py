from __future__ import annotations

from infomentor.api._base import HubResource
from infomentor.models import ClasslistPerson


class ClasslistAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/classlist/classlist/appData") or {}

    def get_pupil(self, pupil_id: str | int, establishment_id: str | None = None) -> ClasslistPerson:
        data = (
            self.post(
                "/ClassList/classlist/GetPupil",
                json={"id": str(pupil_id), "establishmentId": establishment_id},
            )
            or {}
        )
        return ClasslistPerson.model_validate(data)

    def get_staff(self, staff_id: str | int, establishment_id: str | None = None) -> ClasslistPerson:
        data = (
            self.post(
                "/ClassList/classlist/GetStaff",
                json={"id": str(staff_id), "establishmentId": establishment_id},
            )
            or {}
        )
        return ClasslistPerson.model_validate(data)

    def staff_picture(self, staff_id: str | int) -> bytes:
        response = self.get(
            "/ClassList/ClassList/GetStaffPicture",
            params={"id": str(staff_id)},
            expect_json=False,
        )
        return response.content

from __future__ import annotations

from infomentor.api._base import HubResource


class AssessmentAPI(HubResource):
    def app_data(self, tab: str = "main") -> dict:
        return (
            self.post(
                "/assessmentv2/assessmentv2/appData",
                params={"codename": "assessmentsv2", "tab": tab, "action": tab},
            )
            or {}
        )

    def get_summary_assessments_lgr22(self, academic_year_ids: list[int]) -> dict:
        return (
            self.post(
                "/AssessmentV2/SummaryAssessments/GetSummaryAssessmentsLgr22",
                params={"termId": ",".join(str(i) for i in academic_year_ids)},
            )
            or {}
        )

    def get_navigation_items(self, academic_year_id: int) -> dict:
        return (
            self.post(
                "/AssessmentV2/AssessmentV2/GetNavigationItems",
                params={"academicYearId": str(academic_year_id)},
            )
            or {}
        )

    def get_self_assessment_items(self, self_assessment_id: int, academic_year_id: int) -> dict:
        return (
            self.post(
                f"/AssessmentV2/AssessmentV2SelfAssessment/GetItems/{self_assessment_id}",
                params={"academicYearId": str(academic_year_id)},
            )
            or {}
        )

    def get_task_items(self, task_id: int, academic_year_id: int) -> dict:
        return (
            self.post(
                f"/AssessmentV2/AssessmentV2Task/GetItems/{task_id}",
                params={"academicYearId": str(academic_year_id)},
            )
            or {}
        )

    def get_task_dialog(self, statement_id: int) -> dict:
        return (
            self.post(
                "/AssessmentV2/AssessmentV2Task/GetDialog/",
                params={"id": statement_id},
            )
            or {}
        )

    def get_self_assessment_dialog(
        self, item_id: int, aspect_id: int, academic_year_id: int
    ) -> dict:
        return (
            self.post(
                "/AssessmentV2/AssessmentV2SelfAssessment/GetDialog/",
                params={
                    "uol": item_id,
                    "aspectId": aspect_id,
                    "academicYearId": academic_year_id,
                },
            )
            or {}
        )

    def get_grades(self) -> dict:
        return self.post("/AssessmentV2/Grades/GetGrades") or {}

from __future__ import annotations

from infomentor.api._base import HubResource


class DocumentationAPI(HubResource):
    def app_data(self) -> dict:
        return self.post("/documentation/documentation/appData") or {}

    def get_journal_list(self) -> dict | list:
        return self.post("/Documentation/Journal/GetJournalList") or {}

    def portfolio_app_data(self) -> dict:
        return self.post("/Documentation/Portfolio/AppData") or {}

    def get_portfolios_by_semester(self, **payload) -> dict:
        return self.post("/Documentation/Portfolio/GetPortfoliosBySemester", json=payload) or {}

    def get_portfolio_detail(self, portfolio_id: int | str) -> dict:
        return self.post(f"/Documentation/Portfolio/GetPortfolioDetail/{portfolio_id}") or {}

    def save_portfolio_comment(self, **payload) -> dict:
        return self.post("/Documentation/Portfolio/SavePortfolioComment/", json=payload) or {}

    def get_pupil_iup_filter(self) -> dict:
        return self.post("/Documentation/IUP/GetPupilIUPFilter") or {}

    def get_pupil_iup_data(self, **payload) -> dict:
        return self.post("/Documentation/IUP/GetPupilIUPData", json=payload) or {}

    def get_special_plan(self) -> dict:
        return self.post("/Documentation/SpecialPlan/GetSpecialPlan") or {}

    def get_current_conference(self) -> dict:
        return self.post("/Documentation/Conference/GetCurrentConference") or {}

    def get_history_conference_list(self) -> dict | list:
        return self.post("/Documentation/Conference/GetHistoryConferenceList") or {}

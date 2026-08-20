from __future__ import annotations

from infomentor.api._base import HubResource


class UolAPI(HubResource):
    """Units of learning (UolV2)."""

    def app_data(self) -> dict:
        return self.post("/uolv2/uolv2/appData") or {}

    def get_uols(self, academic_year_id: int, state_filter: list[str] | None = None) -> dict:
        return (
            self.post(
                "/UolV2/UolV2/GetUols",
                json={
                    "academicYearId": academic_year_id,
                    "stateFilter": ",".join(state_filter or []),
                },
            )
            or {}
        )

    def get_uol(self, uol_id: int) -> dict:
        return self.post("/UolV2/UolV2/GetUol", json={"id": uol_id}) or {}

from __future__ import annotations

from infomentor.api._base import HubResource
from infomentor.htmlutil import extract_pupil_ids


class AccountAPI(HubResource):
    def preferences(self) -> dict:
        return self.post("/account/preferences/appData") or {}

    def switch_pupil(self, pupil_id: str | int) -> None:
        self.session.get(
            self.session.hub_url(f"/Account/PupilSwitcher/SwitchPupil/{pupil_id}"),
            follow=True,
            default_origin=self.session.hub_base,
        )

    def list_pupils(self) -> list[str]:
        """Return pupil ids embedded in the Hub home page HTML."""
        response = self.session.get(
            f"{self.session.hub_base}/",
            follow=True,
            default_origin=self.session.hub_base,
        )
        return extract_pupil_ids(response.text)

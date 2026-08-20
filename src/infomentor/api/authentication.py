from __future__ import annotations

from infomentor.api._base import HubResource
from infomentor.htmlutil import parse_bool_payload


class AuthenticationAPI(HubResource):
    def is_authenticated(self) -> bool:
        payload = self.post("/authentication/authentication/isauthenticated")
        return parse_bool_payload(payload)

    def logout(self) -> None:
        self.session.get(
            self.session.hub_url(
                "/Authentication/Authentication/LogOut?ApiType=IM1&ApiInstance="
            ),
            follow=True,
            default_origin=self.session.hub_base,
        )

from __future__ import annotations

from infomentor.api._base import HubResource


class ResourcesAPI(HubResource):
    def download(self, resource_id: int | str, *, api: str = "IM2") -> bytes:
        response = self.session.api_request(
            "POST",
            f"/Resources/Resource/Download/{resource_id}",
            params={"api": api, "ModuleType": "None", "ConnectionId": 0},
            expect_json=False,
        )
        return response.content

    def thumbnail(
        self,
        resource_id: int | str,
        width: int,
        height: int,
        *,
        api: str = "IM2",
    ) -> bytes:
        response = self.session.api_request(
            "POST",
            f"/Resources/Resource/Thumbnail/{resource_id}",
            params={
                "api": api,
                "ModuleType": "None",
                "ConnectionId": 0,
                "width": width,
                "height": height,
            },
            expect_json=False,
        )
        return response.content

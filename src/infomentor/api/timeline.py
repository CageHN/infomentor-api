from __future__ import annotations

from infomentor.api._base import HubResource


class TimelineAPI(HubResource):
    """Group timeline endpoints used by lnd3/im-tools."""

    def app_data(self) -> dict:
        return self.post("/grouptimeline/grouptimeline/appData") or {}

    def get_entries(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        group_id: int = -1,
        return_timeline_config: bool = True,
    ) -> dict:
        return (
            self.post(
                "/GroupTimeline/GroupTimeline/GetGroupTimelineEntries",
                json={
                    "page": page,
                    "pageSize": page_size,
                    "groupId": group_id,
                    "returnTimelineConfig": return_timeline_config,
                },
            )
            or {}
        )

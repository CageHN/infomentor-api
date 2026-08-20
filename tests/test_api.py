"""Mocked Hub resource calls."""

from __future__ import annotations

import json

import httpx

from infomentor.client import InfoMentor
from infomentor.models import NotificationState
from infomentor.session import HubSession


def handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    body = request.content.decode("utf-8", errors="replace")

    if path.endswith("isauthenticated"):
        return httpx.Response(200, text="true")
    if path.endswith("GetNewsList"):
        payload = json.loads(body) if body else {}
        assert payload.get("pageSize") == -1
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": 9,
                        "title": "School trip",
                        "content": "<p>Hi</p>",
                        "publishedDate": "2024-06-01",
                        "publishedBy": "Teacher",
                        "attachments": [],
                    }
                ]
            },
        )
    if path.endswith("GetNotifications"):
        return httpx.Response(
            200,
            json={
                "notifications": [
                    {
                        "id": 1,
                        "title": "New homework",
                        "appType": "HomeWork",
                        "state": "New",
                        "pupilIM2Id": 4242,
                    }
                ],
                "timestamp": "2024-06-01T00:00:00",
            },
        )
    if path.endswith("getentries"):
        payload = json.loads(body)
        assert "/" in payload["startDate"]
        return httpx.Response(
            200,
            json=[{"id": 3, "title": "Sports day", "startDate": payload["startDate"]}],
        )
    if path.endswith("gettimetablelist"):
        return httpx.Response(
            200,
            json=[
                {
                    "title": "Math",
                    "start": "2024-06-10T08:00:00",
                    "end": "2024-06-10T08:50:00",
                    "notes": {"roomInfo": "A12", "tutors": "Ada"},
                }
            ],
        )
    if path.endswith("GetPupil"):
        payload = json.loads(body)
        return httpx.Response(200, json={"id": payload["id"], "name": "Alex"})
    if path.endswith("GetGroupTimelineEntries"):
        payload = json.loads(body)
        assert payload["pageSize"] == 50
        return httpx.Response(200, json={"items": [{"id": 1, "text": "hello"}]})
    if path.endswith("UpdateNotificationState"):
        payload = json.loads(body)
        assert payload["state"] == "Read"
        return httpx.Response(200, json={"success": True})
    if "Download/" in path:
        return httpx.Response(200, content=b"%PDF-fake")
    return httpx.Response(404, text=f"unhandled {path}")


def _client() -> tuple[InfoMentor, httpx.Client]:
    http = httpx.Client(transport=httpx.MockTransport(handler))
    session = HubSession(client=http)
    return InfoMentor(session), http


def test_news_notifications_calendar_timetable() -> None:
    client, http = _client()
    try:
        news = client.communication.get_news_list()
        assert news.items[0].title == "School trip"
        notes = client.notifications.list()
        assert notes.notifications[0].title == "New homework"
        entries = client.calendar.get_entries("2024-05-20", "2024-07-07")
        assert entries[0].title == "Sports day"
        lessons = client.timetable.get_timetable_list("2024-06-10", "2024-06-15", utc_offset=-120)
        assert lessons[0].title == "Math"
        pupil = client.classlist.get_pupil("953908")
        assert pupil.name == "Alex"
        timeline = client.timeline.get_entries()
        assert timeline["items"][0]["text"] == "hello"
        updated = client.notifications.update_state([1], NotificationState.READ)
        assert updated["success"] is True
        blob = client.resources.download(55)
        assert blob.startswith(b"%PDF")
    finally:
        client.close()
        http.close()

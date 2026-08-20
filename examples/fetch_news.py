"""Fetch news, notifications, and this week's timetable.

Copy credentials.json.example to credentials.json first. Never commit that file.
"""

from __future__ import annotations

import json
from pathlib import Path

from infomentor import InfoMentor

CREDS = Path(__file__).with_name("credentials.json")


def main() -> None:
    payload = json.loads(CREDS.read_text(encoding="utf-8"))
    with InfoMentor.from_credentials(payload["username"], payload["password"]) as client:
        print("authenticated:", client.is_authenticated())
        print("pupils:", client.pupil_ids or client.account.list_pupils())
        news = client.communication.get_news_list()
        print(f"news items: {len(news.items)}")
        for item in news.items[:5]:
            print("-", item.title)
        notes = client.notifications.list()
        print(f"notifications: {len(notes.notifications)}")
        lessons = client.timetable.this_week()
        print(f"lessons this week: {len(lessons)}")


if __name__ == "__main__":
    main()

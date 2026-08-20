"""Command-line interface for the InfoMentor Hub client."""

from __future__ import annotations

import argparse
import getpass
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from infomentor.client import InfoMentor


def _load_credentials(path: str | None) -> tuple[str | None, str | None]:
    if not path:
        return None, None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload.get("username"), payload.get("password")


def _build_client(args: argparse.Namespace) -> InfoMentor:
    if args.cookies and Path(args.cookies).exists() and args.command != "login":
        return InfoMentor.from_cookies(args.cookies)
    username = args.username
    password = args.password
    file_user, file_pass = _load_credentials(args.credentials)
    username = username or file_user
    password = password or file_pass
    if not username:
        username = input("Username: ")
    if not password:
        password = getpass.getpass("Password: ")
    if args.stockholm:
        client = InfoMentor.from_stockholm(username, password)
    else:
        client = InfoMentor.from_credentials(username, password)
    if args.cookies:
        client.save_cookies(args.cookies)
    return client


def _dump(payload: Any) -> None:
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(by_alias=True)
    json.dump(payload, sys.stdout, indent=2, default=str, ensure_ascii=False)
    sys.stdout.write("\n")


def _cmd_login(client: InfoMentor, _args: argparse.Namespace) -> None:
    _dump({"authenticated": client.is_authenticated(), "pupil_ids": client.pupil_ids})


def _cmd_news(client: InfoMentor, _args: argparse.Namespace) -> None:
    _dump(client.communication.get_news_list())


def _cmd_notifications(client: InfoMentor, _args: argparse.Namespace) -> None:
    _dump(client.notifications.list())


def _cmd_calendar(client: InfoMentor, args: argparse.Namespace) -> None:
    start = date.fromisoformat(args.start) if args.start else date.today()
    end = date.fromisoformat(args.end) if args.end else start + timedelta(days=14)
    _dump([item.model_dump(by_alias=True) for item in client.calendar.get_entries(start, end)])


def _cmd_timetable(client: InfoMentor, args: argparse.Namespace) -> None:
    if args.start and args.end:
        lessons = client.timetable.get_timetable_list(args.start, args.end)
    else:
        lessons = client.timetable.this_week()
    _dump([item.model_dump(by_alias=True) for item in lessons])


def _cmd_timeline(client: InfoMentor, _args: argparse.Namespace) -> None:
    _dump(client.timeline.get_entries())


def _cmd_pupils(client: InfoMentor, _args: argparse.Namespace) -> None:
    ids = client.pupil_ids or client.account.list_pupils()
    _dump({"pupil_ids": ids})


def _cmd_switch(client: InfoMentor, args: argparse.Namespace) -> None:
    client.switch_pupil(args.pupil_id)
    _dump({"switched": args.pupil_id, "authenticated": client.is_authenticated()})


def _cmd_attendance(client: InfoMentor, _args: argparse.Namespace) -> None:
    _dump([item.model_dump(by_alias=True) for item in client.attendance.get_attendance_list()])


def _cmd_logout(client: InfoMentor, args: argparse.Namespace) -> None:
    client.logout()
    if args.cookies and Path(args.cookies).exists():
        Path(args.cookies).unlink()
    _dump({"logged_out": True})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="infomentor", description="InfoMentor Hub CLI")
    parser.add_argument("-u", "--username", help="Hub username")
    parser.add_argument("-p", "--password", help="Hub password (prefer --credentials)")
    parser.add_argument("-c", "--credentials", help="JSON file with username/password")
    parser.add_argument("--cookies", default="cookies.json", help="Cookie jar path")
    parser.add_argument(
        "--stockholm",
        action="store_true",
        help="Use Stockholm student SSO instead of Hub username/password",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("login", help="Log in and print pupil ids")
    sub.add_parser("news", help="Fetch the news list")
    sub.add_parser("notifications", help="Fetch notifications")
    cal = sub.add_parser("calendar", help="Fetch calendar entries")
    cal.add_argument("--start", help="Start date YYYY-MM-DD")
    cal.add_argument("--end", help="End date YYYY-MM-DD")
    tt = sub.add_parser("timetable", help="Fetch timetable lessons")
    tt.add_argument("--start", help="Start date YYYY-MM-DD")
    tt.add_argument("--end", help="End date YYYY-MM-DD")
    sub.add_parser("timeline", help="Fetch group timeline entries")
    sub.add_parser("pupils", help="List pupil ids on the account")
    switch = sub.add_parser("switch", help="Switch the selected pupil")
    switch.add_argument("pupil_id")
    sub.add_parser("attendance", help="Fetch attendance items")
    sub.add_parser("logout", help="Log out and delete the cookie jar")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "login": _cmd_login,
        "news": _cmd_news,
        "notifications": _cmd_notifications,
        "calendar": _cmd_calendar,
        "timetable": _cmd_timetable,
        "timeline": _cmd_timeline,
        "pupils": _cmd_pupils,
        "switch": _cmd_switch,
        "attendance": _cmd_attendance,
        "logout": _cmd_logout,
    }
    client = _build_client(args)
    try:
        handlers[args.command](client, args)
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

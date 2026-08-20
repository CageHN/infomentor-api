"""CLI parsing smoke tests."""

from infomentor.cli import build_parser


def test_parser_requires_command() -> None:
    parser = build_parser()
    args = parser.parse_args(["--credentials", "credentials.json", "news"])
    assert args.command == "news"
    assert args.credentials == "credentials.json"


def test_calendar_flags() -> None:
    parser = build_parser()
    args = parser.parse_args(["calendar", "--start", "2024-05-20", "--end", "2024-07-07"])
    assert args.start == "2024-05-20"
    assert args.end == "2024-07-07"


def test_stockholm_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(["--stockholm", "login"])
    assert args.stockholm is True
    assert args.command == "login"

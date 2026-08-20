"""URL helpers and Hub payload formatting."""

from datetime import date, datetime

from infomentor.api.calendar import format_calendar_date
from infomentor.api.communication import communication_sort_key
from infomentor.api.timetable import format_timetable_date, utc_offset_minutes
from infomentor.htmlutil import absolute_url
from infomentor.session import HubSession


def test_communication_sort_key() -> None:
    assert communication_sort_key("desc", "date") == "lastPublishDate___SORT_DESC"
    assert communication_sort_key("asc", "title") == "title___SORT_ASC"
    assert communication_sort_key("none", "author") == "publishedBy___SORT_NONE"


def test_calendar_and_timetable_date_formats() -> None:
    assert format_calendar_date(date(2024, 5, 20)) == "2024/05/20"
    assert format_calendar_date("2024-07-07") == "2024/07/07"
    assert format_timetable_date(date(2024, 6, 10)) == "2024-06-10"
    assert format_timetable_date(datetime(2024, 6, 15, 8, 0)) == "2024-06-15"


def test_utc_offset_minutes_is_int() -> None:
    assert isinstance(utc_offset_minutes(), int)


def test_absolute_url_prefers_default_origin_for_relative_paths() -> None:
    assert (
        absolute_url(
            "/Authentication/Authentication/LoginCallback",
            "https://infomentor.se/swedish/production/mentor/",
            "https://hub.infomentor.se",
        )
        == "https://hub.infomentor.se/Authentication/Authentication/LoginCallback"
    )


def test_hub_url_join() -> None:
    session = HubSession()
    try:
        assert session.hub_url("/Communication/News/GetNewsList").endswith(
            "/Communication/News/GetNewsList"
        )
        assert session.hub_url("https://example.com/x") == "https://example.com/x"
    finally:
        session.close()

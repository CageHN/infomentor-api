"""Unofficial Python client for the InfoMentor Hub school API."""

from infomentor.client import InfoMentor
from infomentor.exceptions import (
    ApiError,
    AuthenticationError,
    InfomentorError,
    NotAuthenticatedError,
    ParseError,
)
from infomentor.models import (
    CalendarEntry,
    NewsItem,
    NewsList,
    Notification,
    NotificationState,
    NotificationsResult,
    TimetableLesson,
)
from infomentor.session import HubSession

__all__ = [
    "ApiError",
    "AuthenticationError",
    "CalendarEntry",
    "HubSession",
    "InfoMentor",
    "InfomentorError",
    "NewsItem",
    "NewsList",
    "NotAuthenticatedError",
    "Notification",
    "NotificationState",
    "NotificationsResult",
    "ParseError",
    "TimetableLesson",
]

__version__ = "0.1.0"

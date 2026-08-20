"""High-level InfoMentor Hub client."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from infomentor.api.account import AccountAPI
from infomentor.api.assessment import AssessmentAPI
from infomentor.api.attendance import AttendanceAPI
from infomentor.api.authentication import AuthenticationAPI
from infomentor.api.calendar import CalendarAPI
from infomentor.api.classlist import ClasslistAPI
from infomentor.api.communication import CommunicationAPI
from infomentor.api.documentation import DocumentationAPI
from infomentor.api.homework import HomeworkAPI
from infomentor.api.notifications import NotificationsAPI
from infomentor.api.resources import ResourcesAPI
from infomentor.api.task import TaskAPI
from infomentor.api.timeline import TimelineAPI
from infomentor.api.timeregistration import TimeRegistrationAPI
from infomentor.api.timetable import TimetableAPI
from infomentor.api.uol import UolAPI
from infomentor.auth.hub import is_authenticated, login_with_password, logout
from infomentor.auth.stockholm import login_with_stockholm_sso
from infomentor.exceptions import NotAuthenticatedError
from infomentor.session import HubSession


class InfoMentor:
    """Session-backed client for InfoMentor Hub.

    Typical use::

        client = InfoMentor.from_credentials(username, password)
        news = client.communication.get_news_list()
        client.close()
    """

    def __init__(self, session: HubSession | None = None) -> None:
        self.session = session or HubSession()
        self.pupil_ids: list[str] = []
        self.authentication = AuthenticationAPI(self.session)
        self.account = AccountAPI(self.session)
        self.notifications = NotificationsAPI(self.session)
        self.communication = CommunicationAPI(self.session)
        self.calendar = CalendarAPI(self.session)
        self.timetable = TimetableAPI(self.session)
        self.classlist = ClasslistAPI(self.session)
        self.attendance = AttendanceAPI(self.session)
        self.assessment = AssessmentAPI(self.session)
        self.documentation = DocumentationAPI(self.session)
        self.task = TaskAPI(self.session)
        self.uol = UolAPI(self.session)
        self.timeregistration = TimeRegistrationAPI(self.session)
        self.resources = ResourcesAPI(self.session)
        self.timeline = TimelineAPI(self.session)
        self.homework = HomeworkAPI(self.session)

    @classmethod
    def from_credentials(
        cls,
        username: str,
        password: str,
        *,
        session: HubSession | None = None,
    ) -> InfoMentor:
        client = cls(session)
        client.login(username, password)
        return client

    @classmethod
    def from_stockholm(
        cls,
        username: str,
        password: str,
        *,
        session: HubSession | None = None,
    ) -> InfoMentor:
        client = cls(session)
        client.login_stockholm(username, password)
        return client

    @classmethod
    def from_cookies(cls, path: str | Path, *, session: HubSession | None = None) -> InfoMentor:
        client = cls(session)
        client.session.load_cookies(path)
        return client

    def login(self, username: str, password: str) -> list[str]:
        self.pupil_ids = login_with_password(self.session, username, password)
        return self.pupil_ids

    def login_stockholm(self, username: str, password: str) -> list[str]:
        self.pupil_ids = login_with_stockholm_sso(self.session, username, password)
        return self.pupil_ids

    def logout(self) -> None:
        logout(self.session)
        self.pupil_ids = []

    def is_authenticated(self) -> bool:
        return is_authenticated(self.session)

    def require_auth(self) -> None:
        if not self.is_authenticated():
            raise NotAuthenticatedError("Not logged in to InfoMentor Hub")

    def switch_pupil(self, pupil_id: str | int) -> None:
        self.account.switch_pupil(pupil_id)

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Escape hatch for Hub endpoints that are not wrapped yet."""
        return self.session.api_request(method, path, **kwargs)

    def save_cookies(self, path: str | Path) -> None:
        self.session.save_cookies(path)

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> InfoMentor:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

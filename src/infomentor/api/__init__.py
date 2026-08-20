"""InfoMentor Hub API resource modules."""

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

__all__ = [
    "AccountAPI",
    "AssessmentAPI",
    "AttendanceAPI",
    "AuthenticationAPI",
    "CalendarAPI",
    "ClasslistAPI",
    "CommunicationAPI",
    "DocumentationAPI",
    "HomeworkAPI",
    "NotificationsAPI",
    "ResourcesAPI",
    "TaskAPI",
    "TimelineAPI",
    "TimeRegistrationAPI",
    "TimetableAPI",
    "UolAPI",
]

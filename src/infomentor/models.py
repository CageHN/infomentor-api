"""Pydantic models for the most commonly used Hub payloads."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HubModel(BaseModel):
    """Base model that keeps unknown Hub fields instead of dropping them."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class NotificationState(str, Enum):
    NEW = "New"
    SEEN = "Seen"
    READ = "Read"
    CLEARED = "Cleared"


class AppType(str, Enum):
    TIMELINE = "Timeline"
    ASSIGNMENT = "Assignment"
    NEWS = "News"
    ASSESSMENT = "Assessment"
    WEEKLY_PLAN = "WeeklyPlan"
    HOMEWORK = "HomeWork"
    PORTFOLIO = "Portfolio"
    CALENDAR = "Calendar"
    CALENDAR_V2 = "CalendarV2"
    PARENT_MEETING = "ParentMeeting"
    UOL = "Uol"
    ONLINE_TEST = "OnlineTest"
    SURVEY = "Survey"
    UNKNOWN = "Unknown"
    ATTENDANCE = "Attendance"
    IUP = "IUP"
    SPECIAL_PLAN = "SpecialPlan"
    JOURNAL = "Journal"
    CONSENT = "Consent"


class Attachment(HubModel):
    title: str | None = None
    url: str | None = None


class NewsItem(HubModel):
    id: int | None = None
    title: str | None = None
    content: str | None = None
    published_date: str | None = Field(default=None, alias="publishedDate")
    published_date_string: str | None = Field(default=None, alias="publishedDateString")
    published_by: str | None = Field(default=None, alias="publishedBy")
    news_image_url: str | None = Field(default=None, alias="newsImageUrl")
    news_thumbnail_image_url: str | None = Field(default=None, alias="newsThumbnailImageUrl")
    attachments: list[Any] = Field(default_factory=list)


class NewsList(HubModel):
    items: list[NewsItem] = Field(default_factory=list)
    total_item_count: int | None = Field(default=None, alias="totalItemCount")


class DocumentItem(HubModel):
    id: int | None = None
    title: str | None = None
    description: Any = None
    type: Any = None
    file_type: str | None = Field(default=None, alias="fileType")
    file_size: int | float | None = Field(default=None, alias="fileSize")
    file_url: str | None = Field(default=None, alias="fileUrl")
    published_date_string: str | None = Field(default=None, alias="publishedDateString")


class DocumentList(HubModel):
    items: list[DocumentItem] = Field(default_factory=list)
    total_item_count: int | None = Field(default=None, alias="totalItemCount")


class LinkItem(HubModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    type: Any = None
    url: str | None = None
    published_date: str | None = Field(default=None, alias="publishedDate")
    published_date_string: str | None = Field(default=None, alias="publishedDateString")
    published_by: str | None = Field(default=None, alias="publishedBy")


class LinkList(HubModel):
    items: list[LinkItem] = Field(default_factory=list)
    total_item_count: int | None = Field(default=None, alias="totalItemCount")


class Notification(HubModel):
    id: int | None = None
    title: str | None = None
    sub_title: str | None = Field(default=None, alias="subTitle")
    subjects_courses: str | None = Field(default=None, alias="subjectsCourses")
    date_sent: str | None = Field(default=None, alias="dateSent")
    app_type: str | None = Field(default=None, alias="appType")
    state: str | None = None
    type: str | None = None
    url: str | None = None
    order_date: str | None = Field(default=None, alias="orderDate")
    pupil_im2_id: int | None = Field(default=None, alias="pupilIM2Id")
    pupil_source_id: str | None = Field(default=None, alias="pupilSourceId")
    currently_selected_pupil: bool | None = Field(default=None, alias="currentlySelectedPupil")
    entity_type_string: str | None = Field(default=None, alias="entityTypeString")


class NotificationsResult(HubModel):
    notifications: list[Notification] = Field(default_factory=list)
    timestamp: str | None = None


class CalendarSubject(HubModel):
    id: int | None = None
    title: str | None = None


class CalendarEntry(HubModel):
    id: int | None = None
    title: str | None = None
    text: str | None = None
    description: str | None = None
    calendar_entry_type_id: int | None = Field(default=None, alias="calendarEntryTypeId")
    is_all_day_event: bool | None = Field(default=None, alias="isAllDayEvent")
    start_date: str | None = Field(default=None, alias="startDate")
    end_date: str | None = Field(default=None, alias="endDate")
    start_date_full: str | None = Field(default=None, alias="startDateFull")
    end_date_full: str | None = Field(default=None, alias="endDateFull")
    formatted_start_date: str | None = Field(default=None, alias="formattedStartDate")
    formatted_end_date: str | None = Field(default=None, alias="formattedEndDate")
    start_time: str | None = Field(default=None, alias="startTime")
    end_time: str | None = Field(default=None, alias="endTime")
    has_attachments: bool | None = Field(default=None, alias="hasAttachments")
    subjects: list[Any] = Field(default_factory=list)
    courses: list[Any] = Field(default_factory=list)
    url: str | None = None


class TimetableNotes(HubModel):
    room_info: str | None = Field(default=None, alias="roomInfo")
    timetable_notes: str | None = Field(default=None, alias="timetableNotes")
    tutors: str | None = None


class TimetableLesson(HubModel):
    start: str | None = None
    end: str | None = None
    title: str | None = None
    start_time: str | None = Field(default=None, alias="startTime")
    end_time: str | None = Field(default=None, alias="endTime")
    notes: TimetableNotes | dict[str, Any] | None = None
    all_day: bool | None = Field(default=None, alias="allDay")
    establishment_name: Any = Field(default=None, alias="establishmentName")
    details: str | None = None


class Pupil(HubModel):
    id: str
    name: str | None = None


class ClasslistPerson(HubModel):
    id: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    establishment_id: str | None = Field(default=None, alias="establishmentId")
    can_receive_email: bool | None = Field(default=None, alias="canReceiveEmail")


class AttendanceItem(HubModel):
    id: int | None = None
    short_date: str | None = Field(default=None, alias="shortDate")
    long_date: str | None = Field(default=None, alias="longDate")
    time: Any = None
    subject: Any = None
    reason: str | None = None
    comment: Any = None
    registered_by_name: Any = Field(default=None, alias="registeredByName")
    establishment_name: Any = Field(default=None, alias="establishmentName")
    minutes: Any = None


class TimelineRequest(HubModel):
    page: int = 1
    page_size: int = Field(default=50, alias="pageSize")
    group_id: int = Field(default=-1, alias="groupId")
    return_timeline_config: bool = Field(default=True, alias="returnTimelineConfig")

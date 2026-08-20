"""Pydantic model coercion for Hub payloads."""

from infomentor.models import NewsList, NotificationsResult


def test_news_list_keeps_unknown_fields() -> None:
    data = NewsList.model_validate(
        {"items": [{"id": 1, "title": "Hi", "customFlag": True}], "extra": 3}
    )
    assert data.items[0].title == "Hi"
    assert data.items[0].customFlag is True
    assert data.extra == 3


def test_notifications_alias_fields() -> None:
    result = NotificationsResult.model_validate(
        {
            "notifications": [
                {
                    "id": 8,
                    "subTitle": "Math",
                    "pupilIM2Id": 12,
                    "currentlySelectedPupil": True,
                }
            ]
        }
    )
    note = result.notifications[0]
    assert note.sub_title == "Math"
    assert note.pupil_im2_id == 12
    assert note.currently_selected_pupil is True

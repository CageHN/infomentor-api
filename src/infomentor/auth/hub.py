"""Username/password login against hub.infomentor.se and the IM1 mentor portal.

The handshake combines the Hub OAuth dance documented by dementor.net /
lib_smilingschool with the imhome callback + PIN skip used by im-tools.
"""

from __future__ import annotations

from infomentor.constants import (
    HUB_BASE,
    LOGIN_BUTTON_FIELD,
    LOGIN_BUTTON_VALUE,
    LOGIN_PASSWORD_FIELD,
    LOGIN_USERNAME_FIELD,
    MENTOR_URL,
)
from infomentor.exceptions import AuthenticationError
from infomentor.htmlutil import (
    extract_named_inputs,
    extract_oauth_token,
    extract_pupil_ids,
    has_login_form,
    is_pin_enable_page,
    parse_bool_payload,
)
from infomentor.session import HubSession


def is_authenticated(session: HubSession) -> bool:
    try:
        payload = session.api_post("/authentication/authentication/isauthenticated")
    except Exception:
        return False
    try:
        return parse_bool_payload(payload)
    except Exception:
        return False


def _skip_pin_if_needed(session: HubSession, response) -> object:
    if not is_pin_enable_page(str(response.url), response.text):
        return response
    fields = extract_named_inputs(response.text)
    fields["__EVENTTARGET"] = "aDontActivatePin"
    fields["__EVENTARGUMENT"] = ""
    next_response = session.post(str(response.url), data=fields)
    return session.follow(next_response, default_origin="https://infomentor.se")


def _submit_oauth_token(session: HubSession, token: str, default_origin: str):
    response = session.post(MENTOR_URL, data={"oauth_token": token})
    return session.follow(response, default_origin=default_origin)


def login_with_password(
    session: HubSession,
    username: str,
    password: str,
) -> list[str]:
    """Log in with Hub/IM1 username and password.

    Returns pupil ids discovered on the Hub home page (guardian accounts).
    """
    response = session.get(f"{session.hub_base}/")
    response = session.follow(response, default_origin=session.hub_base)

    token = extract_oauth_token(response.text)
    if token and not has_login_form(response.text):
        response = _submit_oauth_token(session, token, "https://infomentor.se")

    if not has_login_form(response.text):
        response = session.get(MENTOR_URL)
        response = session.follow(response, default_origin="https://infomentor.se")

    if not has_login_form(response.text):
        raise AuthenticationError("Could not load the InfoMentor login form")

    fields = extract_named_inputs(response.text)
    fields[LOGIN_USERNAME_FIELD] = username
    fields[LOGIN_PASSWORD_FIELD] = password
    fields[LOGIN_BUTTON_FIELD] = LOGIN_BUTTON_VALUE
    fields.setdefault("__EVENTTARGET", "")
    fields.setdefault("__EVENTARGUMENT", "")

    response = session.post(MENTOR_URL, data=fields)
    response = session.follow(response, default_origin="https://infomentor.se")
    response = _skip_pin_if_needed(session, response)

    token = extract_oauth_token(response.text)
    if token:
        response = _submit_oauth_token(session, token, session.hub_base)

    if not is_authenticated(session):
        # im-tools fallback: force a one-time OAuth login callback (sets imhome).
        forced = session.get(
            f"{session.hub_base}/authentication/authentication/login"
            "?apitype=im1&forceOAuth=true"
        )
        forced = session.follow(forced, default_origin=session.hub_base)
        token = extract_oauth_token(forced.text) or token
        if token:
            response = _submit_oauth_token(session, token, session.hub_base)

    if not is_authenticated(session):
        raise AuthenticationError(
            "InfoMentor rejected the credentials or the OAuth callback did not complete"
        )

    home = session.get(f"{session.hub_base}/")
    home = session.follow(home, default_origin=session.hub_base)
    return extract_pupil_ids(home.text)


def logout(session: HubSession) -> None:
    session.get(
        session.hub_url("/Authentication/Authentication/LogOut?ApiType=IM1&ApiInstance="),
        follow=True,
        default_origin=HUB_BASE,
    )

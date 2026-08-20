"""Stockholm student SSO login (skolplattformen / SiteMinder).

Documented by EduPatch in smilingschool_api/login/LOGIN.md.
"""

from __future__ import annotations

from infomentor.auth.hub import is_authenticated
from infomentor.constants import (
    MENTOR_URL,
    STOCKHOLM_LOGIN_FCC,
    STOCKHOLM_LOGIN_FORMS,
    STOCKHOLM_SSO_LOGIN,
)
from infomentor.exceptions import AuthenticationError, ParseError
from infomentor.htmlutil import (
    extract_hidden_fields,
    extract_login_form_href,
    extract_named_inputs,
    extract_oauth_token,
    extract_pupil_ids,
    extract_saml_response,
)
from infomentor.session import HubSession


def login_with_stockholm_sso(
    session: HubSession,
    username: str,
    password: str,
) -> list[str]:
    """Authenticate a Stockholm student account via ``idp=stockholm_stu``."""
    menu = session.get(STOCKHOLM_SSO_LOGIN, follow=True)
    try:
        login_href = extract_login_form_href(menu.text)
    except ParseError as exc:
        raise AuthenticationError("Stockholm SSO login form was not found") from exc

    login_page = session.get(
        STOCKHOLM_LOGIN_FORMS + login_href.lstrip("/"),
        follow=True,
        default_origin="https://login001.stockholm.se",
    )
    fields = extract_hidden_fields(login_page.text) or extract_named_inputs(login_page.text)
    fields.update(
        {
            "user": username,
            "password": password,
            "SMENC": fields.get("SMENC", ""),
            "SMLOCALE": fields.get("SMLOCALE", ""),
            "target": fields.get("target", ""),
            "smauthreason": fields.get("smauthreason", ""),
            "smagentname": fields.get("smagentname", ""),
            "smquerydata": fields.get("smquerydata", ""),
            "postpreservationdata": fields.get("postpreservationdata", ""),
            "submit": fields.get("submit", ""),
        }
    )

    saml_page = session.post(STOCKHOLM_LOGIN_FCC, data=fields)
    saml_page = session.follow(saml_page, default_origin="https://login001.stockholm.se")
    saml_response = extract_saml_response(saml_page.text)

    infomentor_page = session.post(STOCKHOLM_SSO_LOGIN, data={"SAMLResponse": saml_response})
    infomentor_page = session.follow(infomentor_page, default_origin="https://sso.infomentor.se")
    token = extract_oauth_token(infomentor_page.text, required=True)
    callback = session.post(MENTOR_URL, data={"oauth_token": token})
    session.follow(callback, default_origin=session.hub_base)

    if not is_authenticated(session):
        raise AuthenticationError("Stockholm SSO completed but Hub did not accept the session")

    home = session.get(f"{session.hub_base}/")
    home = session.follow(home, default_origin=session.hub_base)
    return extract_pupil_ids(home.text)

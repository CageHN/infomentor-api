"""Mocked Hub username/password login handshake."""

from __future__ import annotations

import httpx

from infomentor.auth.hub import login_with_password
from infomentor.client import InfoMentor
from infomentor.session import HubSession

OAUTH_PAGE = """
<html><body>
<input type="hidden" name="oauth_token" value="start-token" />
</body></html>
"""

LOGIN_PAGE = """
<html><body>
<input type="hidden" name="__VIEWSTATE" value="vs" />
<input type="hidden" name="__VIEWSTATEGENERATOR" value="gen" />
<input type="hidden" name="__EVENTVALIDATION" value="ev" />
<input name="login_ascx$txtNotandanafn" value="" />
<input name="login_ascx$txtLykilord" value="" />
<input type="submit" name="login_ascx$btnLogin" value="Logga in" />
</body></html>
"""

CALLBACK_PAGE = """
<html><body>
<input type="hidden" name="oauth_token" value="final-token" />
</body></html>
"""

HOME_PAGE = """
<html><body>
<a href="/Account/PupilSwitcher/SwitchPupil/4242">Kid</a>
</body></html>
"""


class HubState:
    def __init__(self) -> None:
        self.got_credentials = False
        self.got_final_token = False
        self.authenticated = False


def make_handler(state: HubState):
    def handler(request: httpx.Request) -> httpx.Response:
        host = request.url.host
        path = request.url.path
        method = request.method
        body = request.content.decode("utf-8", errors="replace")

        if host == "hub.infomentor.se" and path in {"/", ""} and method == "GET":
            if state.authenticated:
                return httpx.Response(200, text=HOME_PAGE)
            return httpx.Response(200, text=OAUTH_PAGE)

        if host == "infomentor.se" and path.endswith("/mentor/") and method == "POST":
            if "login_ascx%24txtNotandanafn=demo" in body or "login_ascx$txtNotandanafn=demo" in body:
                state.got_credentials = True
                return httpx.Response(200, text=CALLBACK_PAGE)
            if "oauth_token=final-token" in body:
                state.got_final_token = True
                state.authenticated = True
                return httpx.Response(
                    302,
                    headers={
                        "location": "/Authentication/Authentication/LoginCallback"
                    },
                )
            if "oauth_token=start-token" in body:
                return httpx.Response(200, text=LOGIN_PAGE)
            return httpx.Response(200, text=LOGIN_PAGE)

        if path.endswith("/LoginCallback"):
            state.authenticated = True
            return httpx.Response(200, text=HOME_PAGE)

        if path.lower().endswith("/isauthenticated") or "isauthenticated" in path.lower():
            return httpx.Response(200, text="true" if state.authenticated else "false")

        if path.endswith("/login"):
            return httpx.Response(200, text=CALLBACK_PAGE)

        return httpx.Response(200, text=HOME_PAGE if state.authenticated else OAUTH_PAGE)

    return handler


def test_password_login_sets_authenticated_and_pupil_ids() -> None:
    state = HubState()
    http = httpx.Client(transport=httpx.MockTransport(make_handler(state)))
    session = HubSession(client=http)
    try:
        pupils = login_with_password(session, "demo", "secret")
        assert state.got_credentials
        assert state.got_final_token
        assert pupils == ["4242"]
    finally:
        session.close()
        http.close()


def test_client_from_credentials_uses_login() -> None:
    state = HubState()
    http = httpx.Client(transport=httpx.MockTransport(make_handler(state)))
    session = HubSession(client=http)
    try:
        client = InfoMentor.from_credentials("demo", "secret", session=session)
        assert client.pupil_ids == ["4242"]
        assert client.is_authenticated()
        client.close()
    finally:
        http.close()

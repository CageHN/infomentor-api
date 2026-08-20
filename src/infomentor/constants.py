"""Hosts, paths, and headers used by InfoMentor Hub."""

from __future__ import annotations

HUB_BASE = "https://hub.infomentor.se"
MENTOR_BASE = "https://infomentor.se/swedish/production/mentor"
MENTOR_URL = f"{MENTOR_BASE}/"
SSO_BASE = "https://sso.infomentor.se"
STOCKHOLM_IDP = "stockholm_stu"
STOCKHOLM_SSO_LOGIN = f"{SSO_BASE}/login.ashx?idp={STOCKHOLM_IDP}"
STOCKHOLM_LOGIN_FORMS = "https://login001.stockholm.se/siteminderagent/forms/"
STOCKHOLM_LOGIN_FCC = "https://login001.stockholm.se/siteminderagent/forms/login.fcc"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
)

BROWSER_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8"
    ),
    "Accept-Language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
    "Upgrade-Insecure-Requests": "1",
}

API_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": HUB_BASE,
    "Referer": f"{HUB_BASE}/",
}

# ASP.NET login form field names used by the IM1 mentor portal.
LOGIN_USERNAME_FIELD = "login_ascx$txtNotandanafn"
LOGIN_PASSWORD_FIELD = "login_ascx$txtLykilord"
LOGIN_BUTTON_FIELD = "login_ascx$btnLogin"
LOGIN_BUTTON_VALUE = "Logga in"

PUPIL_SWITCH_RE = r"/Account/PupilSwitcher/SwitchPupil/(\d+)"

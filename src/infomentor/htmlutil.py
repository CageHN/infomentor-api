"""Helpers for scraping login forms and pupil ids from InfoMentor HTML."""

from __future__ import annotations

import html
import re
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from infomentor.constants import PUPIL_SWITCH_RE
from infomentor.exceptions import ParseError

_OAUTH_INPUT_RE = re.compile(
    r"""<input[^>]*name=["']oauth_token["'][^>]*value=["']([^"']+)["']"""
    r"""|"""
    r"""<input[^>]*value=["']([^"']+)["'][^>]*name=["']oauth_token["']""",
    re.IGNORECASE | re.DOTALL,
)
_PUPIL_RE = re.compile(PUPIL_SWITCH_RE)
_LOGIN_FORM_RE = re.compile(r'loginForm[^"]*', re.IGNORECASE)


def parse_html(markup: str) -> BeautifulSoup:
    return BeautifulSoup(markup, "html.parser")


def extract_named_inputs(markup: str) -> dict[str, str]:
    """Return name/value pairs for every ``<input>`` that has a name."""
    soup = parse_html(markup)
    fields: dict[str, str] = {}
    for inp in soup.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        fields[str(name)] = html.unescape(str(inp.get("value") or ""))
    return fields


def extract_hidden_fields(markup: str) -> dict[str, str]:
    soup = parse_html(markup)
    fields: dict[str, str] = {}
    for inp in soup.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        itype = str(inp.get("type") or "text").lower()
        if itype == "hidden":
            fields[str(name)] = html.unescape(str(inp.get("value") or ""))
    return fields


def extract_oauth_token(markup: str, *, required: bool = False) -> str | None:
    soup = parse_html(markup)
    inp = soup.find("input", attrs={"name": re.compile(r"^oauth_token$", re.I)})
    if inp and inp.get("value"):
        return html.unescape(str(inp.get("value")))
    match = _OAUTH_INPUT_RE.search(markup)
    if match:
        return html.unescape(match.group(1) or match.group(2))
    if required:
        raise ParseError("oauth_token was not found in the InfoMentor login page")
    return None


def extract_saml_response(markup: str) -> str:
    soup = parse_html(markup)
    inp = soup.find("input", attrs={"name": re.compile(r"SAMLResponse", re.I)})
    if inp and inp.get("value"):
        return html.unescape(str(inp.get("value")))
    raise ParseError("SAMLResponse was not found in the Stockholm SSO page")


def extract_login_form_href(markup: str) -> str:
    """Return the relative loginForm.jsp path used by Stockholm SiteMinder."""
    for line in markup.splitlines():
        if "loginForm" not in line:
            continue
        quoted = re.search(r'["\']([^"\']*loginForm[^"\']*)["\']', line, re.I)
        if quoted:
            return quoted.group(1)
        match = _LOGIN_FORM_RE.search(line)
        if match:
            return match.group(0)
    raise ParseError("loginForm path was not found on the Stockholm SSO page")


def extract_pupil_ids(markup: str) -> list[str]:
    ids = sorted(set(_PUPIL_RE.findall(markup)))
    return ids


def has_login_form(markup: str) -> bool:
    return "txtNotandanafn" in markup or "login_ascx" in markup


def is_pin_enable_page(url: str, markup: str = "") -> bool:
    haystack = f"{url}\n{markup}"
    return "EnablePin" in haystack or "PinLogin" in haystack


def absolute_url(location: str, current_url: str, default_origin: str | None = None) -> str:
    if location.startswith("http://") or location.startswith("https://"):
        return location
    if location.startswith("/") and default_origin:
        return default_origin.rstrip("/") + location
    return urljoin(current_url, location)


def parse_bool_payload(payload: Any) -> bool:
    if isinstance(payload, bool):
        return payload
    text = str(payload).strip().strip('"').lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no", "", "none", "null"}:
        return False
    raise ParseError(f"Could not parse boolean payload: {payload!r}")

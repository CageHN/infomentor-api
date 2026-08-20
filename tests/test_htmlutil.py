"""Offline tests for HTML / form parsing used during login."""

from infomentor.htmlutil import (
    extract_login_form_href,
    extract_named_inputs,
    extract_oauth_token,
    extract_pupil_ids,
    extract_saml_response,
    has_login_form,
    is_pin_enable_page,
    parse_bool_payload,
)

LOGIN_HTML = """
<html>
  <body>
    <form>
      <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="abc+1" />
      <input type="hidden" name="__VIEWSTATEGENERATOR" value="F357C404" />
      <input type="hidden" name="__EVENTVALIDATION" value="ev" />
      <input name="login_ascx$txtNotandanafn" type="text" value="" />
      <input name="login_ascx$txtLykilord" type="password" value="" />
      <input type="submit" name="login_ascx$btnLogin" value="Logga in" />
    </form>
  </body>
</html>
"""

OAUTH_HTML = """
<html>
  <input type="hidden" name="oauth_token" value="tok/en+=1" />
</html>
"""

HOME_HTML = """
<a href="/Account/PupilSwitcher/SwitchPupil/111">A</a>
<a href="/Account/PupilSwitcher/SwitchPupil/222">B</a>
<a href="/Account/PupilSwitcher/SwitchPupil/111">A again</a>
"""

SAML_HTML = """
<form>
  <input type="hidden" name="SAMLResponse" value="PHNhbWw+" />
</form>
"""

SITEMINDER_HTML = """
<p>Choose login</p>
<a href="loginForm.jsp?SMAUTHREASON=0">loginForm here</a>
"""


def test_extract_named_inputs_and_login_form() -> None:
    fields = extract_named_inputs(LOGIN_HTML)
    assert fields["__VIEWSTATE"] == "abc+1"
    assert fields["login_ascx$btnLogin"] == "Logga in"
    assert has_login_form(LOGIN_HTML)


def test_extract_oauth_token() -> None:
    assert extract_oauth_token(OAUTH_HTML) == "tok/en+=1"


def test_extract_pupil_ids_unique_sorted() -> None:
    assert extract_pupil_ids(HOME_HTML) == ["111", "222"]


def test_extract_saml_and_login_form_href() -> None:
    assert extract_saml_response(SAML_HTML) == "PHNhbWw+"
    assert extract_login_form_href(SITEMINDER_HTML) == "loginForm.jsp?SMAUTHREASON=0"


def test_parse_bool_payload() -> None:
    assert parse_bool_payload(True) is True
    assert parse_bool_payload("true") is True
    assert parse_bool_payload('"false"') is False
    assert parse_bool_payload(False) is False


def test_is_pin_enable_page() -> None:
    assert is_pin_enable_page(
        "https://infomentor.se/Swedish/Production/mentor/Oryggi/PinLogin/EnablePin.aspx"
    )
    assert not is_pin_enable_page("https://hub.infomentor.se/")

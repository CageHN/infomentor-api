# infomentor-api

Unofficial Python client for [InfoMentor Hub](https://hub.infomentor.se). It logs in the same way the Hub web app does, then calls the JSON endpoints parents and students already use in the browser.

This project is **not affiliated with or endorsed by InfoMentor**. Use it only with accounts you are allowed to access.

## What it covers

The client wraps the Hub apps documented by the open-source civic-tech work around InfoMentor:

| Area | Endpoints |
| --- | --- |
| Auth | Hub username/password, Stockholm student SSO, cookie reuse, logout, pupil switch |
| Communication | news, documents, links, consents |
| Notifications | list + state updates |
| Calendar v2 | entries, iCal subscription URI |
| Timetable | week list |
| Class list | pupils and staff |
| Attendance | list, leave requests, register |
| Assessment, tasks, UoL, documentation, time registration, resources | Hub `appData` + list/detail calls |
| Timeline / homework | group timeline (im-tools) and legacy homework (m42e) |

Raw Hub paths that are not wrapped yet are available through `client.request("POST", "/some/path", json=...)`.

## Install

```bash
pip install -e ".[dev]"
```

Python 3.11+ is required.

## Quick start

```python
from infomentor import InfoMentor

with InfoMentor.from_credentials("username", "password") as client:
    print(client.is_authenticated())
    news = client.communication.get_news_list()
    for item in news.items:
        print(item.title)
    notes = client.notifications.list()
    lessons = client.timetable.this_week()
```

Stockholm student SSO (skolplattformen / SiteMinder):

```python
client = InfoMentor.from_stockholm("username", "password")
```

Reuse a saved session:

```python
client.save_cookies("cookies.json")
client = InfoMentor.from_cookies("cookies.json")
```

Guardian accounts can switch the selected child:

```python
print(client.pupil_ids)
client.switch_pupil("123456")
```

## CLI

```bash
# credentials.json is the same shape dementor.net uses
cp examples/credentials.json.example credentials.json

infomentor --credentials credentials.json login
infomentor --cookies cookies.json news
infomentor --cookies cookies.json notifications
infomentor --cookies cookies.json calendar --start 2026-08-01 --end 2026-08-31
infomentor --cookies cookies.json timetable
infomentor --cookies cookies.json timeline
infomentor --cookies cookies.json logout
```

`--stockholm` selects the Stockholm student identity provider instead of the Hub password form.

## How login works

InfoMentor Hub does not ship a public OAuth API. After a browser-style handshake you get session cookies (`ASP.NET_SessionId`, `.ASPXAUTH`, `imhome`, …) that authorize the same POST endpoints the Hub SPA calls.

Password accounts (dementor.net / lib_smilingschool / im-tools):

1. `GET https://hub.infomentor.se/` and follow redirects.
2. Post the `oauth_token` hidden field to `https://infomentor.se/swedish/production/mentor/`.
3. Submit the ASP.NET login form (`login_ascx$txtNotandanafn` / `login_ascx$txtLykilord`) including `__VIEWSTATE`.
4. Skip PIN enrolment when that page appears.
5. Post the one-time `oauth_token` callback so Hub sets `imhome`.
6. Confirm with `POST /authentication/authentication/isauthenticated`.

Stockholm students follow the SiteMinder + SAML flow documented in [EduPatch/smilingschool_api](https://github.com/EduPatch/smilingschool_api/blob/main/login/LOGIN.md). You cannot be logged in in two places at once; a second login forces a loop.

## API map

The OpenAPI file in [`spec/openapi.yml`](spec/openapi.yml) is the EduPatch SmilingSchool Hub spec. Resource classes live under `src/infomentor/api/`.

```text
client.authentication.is_authenticated()
client.account.preferences() / .list_pupils() / .switch_pupil(id)
client.communication.get_news_list()
client.notifications.list()
client.calendar.get_entries(start, end)
client.timetable.get_timetable_list(start, end)
client.classlist.get_pupil(id)
client.attendance.get_attendance_list()
client.timeline.get_entries()
client.resources.download(id)
```

## Tests

```bash
pip install -e ".[dev]"
pytest
```

Tests are offline. They mock the login HTML and Hub JSON; they do not contact InfoMentor.

## Prior art

This library reimplements the publicly documented Hub flows. It does not copy those repositories:

- [kolplattformen/dementor.net](https://github.com/kolplattformen/dementor.net) — C# lab for Hub login + sample POSTs
- [lnd3/im-tools](https://github.com/lnd3/im-tools) — bash/curl suite (`imhome` callback, news, group timeline, pupil switch)
- [m42e/infomentor](https://github.com/m42e/infomentor) — archived Python notifier (IM1 calendar/homework/news)
- [EduPatch/smilingschool_api](https://github.com/EduPatch/smilingschool_api) — OpenAPI spec + Stockholm SSO notes
- [EduPatch/lib_smilingschool-dart](https://github.com/EduPatch/lib_smilingschool-dart) — typed Dart client

## Disclaimer

School data is sensitive. Store credentials and cookie jars locally, never commit them, and treat this as an unofficial integration that can break when InfoMentor changes Hub.

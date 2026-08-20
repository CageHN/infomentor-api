"""Errors raised by the InfoMentor client."""


class InfomentorError(Exception):
    """Base error for all client failures."""


class AuthenticationError(InfomentorError):
    """Login failed or the session is no longer authenticated."""


class ParseError(InfomentorError):
    """A login or SSO page did not contain an expected field."""


class ApiError(InfomentorError):
    """A Hub API request failed or returned an unexpected payload."""

    def __init__(self, message: str, status_code: int | None = None, body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class NotAuthenticatedError(AuthenticationError):
    """The client was used before a successful login."""

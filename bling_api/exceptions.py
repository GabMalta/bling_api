class BlingApiError(Exception):
    pass


class BlingAuthenticationError(BlingApiError):
    pass


class BlingRequestError(BlingApiError):
    def __init__(self, message: str, status_code: int | None = None, response_body: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body or {}

class NotFoundError(Exception):
    def __init__(self, detail: str = "Not found") -> None:
        self.detail = detail
        super().__init__(detail)


class ConflictError(Exception):
    def __init__(self, detail: str = "Conflict") -> None:
        self.detail = detail
        super().__init__(detail)


class ForbiddenError(Exception):
    def __init__(self, detail: str = "Forbidden") -> None:
        self.detail = detail
        super().__init__(detail)


class AuthenticationError(Exception):
    def __init__(self, detail: str = "Could not validate credentials") -> None:
        self.detail = detail
        super().__init__(detail)

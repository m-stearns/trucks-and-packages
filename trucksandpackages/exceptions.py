class AuthError(Exception):

    def __init__(self, error, status_code) -> None:
        self.error = error
        self.status_code = status_code

class NoAuthHeaderError(AuthError):

    def __init__(self, error, status_code) -> None:
        super().__init__(error, status_code)

class InvalidHeaderError(AuthError):

    def __init__(self, error, status_code) -> None:
        super().__init__(error, status_code)

class TokenExpiredError(AuthError):

    def __init__(self, error, status_code) -> None:
        super().__init__(error, status_code)

class InvalidClaimsError(AuthError):

    def __init__(self, error, status_code) -> None:
        super().__init__(error, status_code)

class NoRSAKeyError(AuthError):

    def __init__(self, error, status_code) -> None:
        super().__init__(error, status_code)
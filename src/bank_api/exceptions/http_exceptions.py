from bank_api.exceptions.base_exception import BaseException


class HttpException(BaseException):
    def __init__(
            self,
            code: int,
            message: str,
    ):
        self.code = code
        self.message = message

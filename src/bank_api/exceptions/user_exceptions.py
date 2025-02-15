from bank_api.exceptions.base_exception import BaseException


class UserException(BaseException):
    def __init__(self, message='An error occurred with the user', code=500):
        self.code = code
        self.message = message
        super().__init__(self.code, self.message)

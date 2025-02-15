

class BaseException(Exception):
    """Base exception class for all exceptions in this project."""

    code: int
    message: str

    def __init__(
        self, code: int = 400, message: str = 'Bad Request'
    ):
        self.code = code
        self.message = message

    def __str__(self):
        return f'''
            code: {self.code}
            message: {self.message}
            traceback: {self.__traceback__}
            '''

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
        }

from typing import Any


class Logger:
    def __log(self, msg: Any, level_type: str):
        print(f"[{level_type.upper()}] {msg}")

    def debug(self, msg: Any):
        self.__log(msg, 'debug')

    def info(self, msg: Any):
        self.__log(msg, 'info')

    def warning(self, msg: Any):
        self.__log(msg, 'warning')

    def error(self, msg: Any):
        self.__log(msg, 'error')

    def critical(self, msg: Any):
        self.__log(msg, 'critical')


logger = Logger()

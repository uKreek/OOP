from abc import ABC, abstractmethod
from enum import Enum
from re import search
import socket
import datetime
from typing import List


class LogLevel(Enum):
    INFO = 1
    WARN = 2
    ERROR = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented


# region Interfaces

class ILogFilter(ABC):
    @abstractmethod
    def match(self, log_level: LogLevel, text: str) -> bool:
        pass


class ILogHandler(ABC):
    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None:
        pass


class ILogFormatter(ABC):
    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str:
        pass


# endregion

# region Filters


class SimpleLogFilter(ILogFilter):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, log_level, text) -> bool:
        return self.pattern in text


class ReLogFilter(ILogFilter):
    def __init__(self, re_pattern: str):
        self.re_pattern = re_pattern

    def match(self, log_level: LogLevel, text: str) -> bool:
        match_object = search(self.re_pattern, text)
        return bool(match_object)


class LevelFilter(ILogFilter):
    def __init__(self, min_level):
        self.min_level = min_level

    def match(self, log_level: LogLevel, text: str) -> bool:
        return log_level >= self.min_level


# endregion


class FileHandler(ILogHandler):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with open(self.file_path, 'a', encoding='utf-8') as file:
                file.write(text + '\n')
        except Exception as e:
            print(f"Writing to file error: {e}")


class ConsoleHandler(ILogHandler):
    def __init__(self):
        pass

    def handle(self, log_level: LogLevel, text: str) -> None:
        print(text)


class SocketHandler(ILogHandler):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            data = text.encode('utf-8')
            self.sock.sendto(data, (self.host, self.port))
        except Exception as e:
            print(f'Socket error: {e}')

    def __del__(self):
        self.sock.close()


class SyslogHandler(ILogHandler):
    def __init__(self, app_name: str):
        self.app_name = app_name

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            print(f'--- [writing to SYSLOG] {self.app_name} ---')
        except Exception as e:
            print(f'writing to syslog error: {e}')


class FtpHandler(ILogHandler):
    def __init__(self, ftp_host: str, user: str):
        self.ftp_host = ftp_host
        self.user = user

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            print(f"--- [FTP Upload to {self.ftp_host} as {self.user}]: {text} ---")
        except Exception as e:
            print(f'FTP upload error: {e}')


# region Formatters

class Formatter(ILogFormatter):
    def __init__(self, datetime_format):
        self.datetime_format = datetime_format

    def format(self, log_level: LogLevel, text: str) -> str:
        return f'[{log_level}] [{datetime.datetime.now().strftime(self.datetime_format)}] {text}'


# endregion

# region Logger


class Logger:
    def __init__(self, filters: List[ILogFilter], handlers: List[ILogHandler], formatters: List[ILogFormatter]):
        self.filters = filters
        self.handlers = handlers
        self.formatters = formatters

    def log(self, log_level: LogLevel, text: str) -> None:
        for log_filter in self.filters:
            if not log_filter.match(log_level, text):
                return

        processed_text = text
        for formatter in self.formatters:
            processed_text = formatter.format(log_level, processed_text)

        for handler in self.handlers:
            handler.handle(log_level, processed_text)

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)

# endregion

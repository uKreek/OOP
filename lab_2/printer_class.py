import sys
import json
import os
from enum import Enum
from typing import Tuple, Dict, List


class AnsiCodes:
    RESET = f'\033[0m'
    CLEAR_SCREEN = f'\033[2J'
    HOME = f'\033[H'

    @staticmethod
    def move_cursor(x: int, y: int) -> str:
        return f'\033[{y};{x}H'


class Color(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = f'\033[0m'

class Printer:
    _font = {}
    _height = 0

    def __init__(self, color: Color, position: Tuple[int, int], symbol: str):
        self.color = color
        self.position = position
        self.symbol = symbol

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write(Color.RESET.value)
        sys.stdout.flush()

    @classmethod
    def print(cls, text: str, color: Color, position: Tuple[int, int], symbol: str):
        x, y = position
        for row in range(cls._height):
            sys.stdout.write(f'\033[{y + row};{x}H')
            sys.stdout.write(color.value)

    @classmethod
    def load_font(cls, path: str) -> Dict[str, List[str]]:
        with open(path) as f:
            cls._font = json.load(f)
            if cls._font:
                first_char = next(iter(cls._font))
                cls._height = len(cls._font[first_char])



with Printer(Color.RED, (0, 0), '#') as p:
    p.print('апfg', Color.RED, (0, 0), '#')
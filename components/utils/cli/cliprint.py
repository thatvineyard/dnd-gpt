from enum import Enum
import logging
from textwrap import indent

from colorama import Fore, Style


class CliStyle(Enum):
    BLUE = Fore.LIGHTBLUE_EX
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    DEFAULT = Fore.RESET
    LOW_CONTRAST = Style.DIM


class CliPrefix:
    ENGINE = "🚀  ENGINE: "
    CHAT = "🤖    CHAT: "
    PARSER = "🔍  PARSER: "
    SESSION = "📜 SESSION: "


_level = logging.INFO


def cli_setup_logging(level: int):
    global _level
    _level = level


def cli_print_info(
    message: str,
    prefix: str = "",
    message_style: CliStyle = CliStyle.DEFAULT,
    prefix_style: CliStyle = CliStyle.BLUE,
):
    if _level <= logging.INFO:
        print(
            f"{_wrap_in_style(prefix, prefix_style)}{_wrap_in_style(message, message_style)}"
        )


def cli_print_debug(message: str, prefix: str = ""):
    if _level <= logging.DEBUG:
        if prefix != "" and "\n" in message:
            message = indent(message, "    ")
            message = f"\n{message}"
        print(
            f"{_wrap_in_style(prefix, CliStyle.LOW_CONTRAST)}{_wrap_in_style(message, CliStyle.LOW_CONTRAST)}"
        )


def cli_print_warn(message: str):
    if _level <= logging.ERROR:
        print(_wrap_in_style(message, CliStyle.YELLOW))


def cli_print_error(message: str):
    if _level <= logging.ERROR:
        print(_wrap_in_style(message, CliStyle.RED))


def cli_input(prompt: str = None):
    return input(_wrap_in_style(prompt, CliStyle.GREEN))


def _wrap_in_style(message: str, color: CliStyle):
    return f"{color.value}{message}{Style.RESET_ALL}"

"""Some of utilities."""

from dataclasses import dataclass
from itertools import count, takewhile


def readable_time(second: int) -> str:
    """
    Convert a duration in seconds to a human-readable time format (HH:MM:SS).
    Handles negative durations by prefixing a '-' to the time.

    Args:
        second (int): The duration in seconds (can be negative).

    Returns:
        str: The formatted time string in HH:MM:SS format.

    Example:
        >>> readable_time(338087)
        '94:08:07'
        >>> readable_time(-3661)
        '-01:01:01'
    """
    sec = abs(second)
    hours = sec // 3600
    minutes = (sec % 3600) // 60
    seconds = sec % 60
    time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"-{time_string}" if second < 0 else time_string


def closed_float_range(start: float, stop: float, step: float) -> takewhile:
    """
    Generates a closed range of floating-point numbers from `start` to `stop` with a step of `step`.

    This solution comes from "https://stackoverflow.com/a/34114983".

    Args:
        start: The starting value of the range (inclusive).
        stop: The ending value of the range (inclusive).
        step: The step size between values in the range.

    Returns:
        An iterator that generates the values in the range.

    Examples:
        >>> list(float_closed_crange(1.0, 2.0, 0.5))
        [1.0, 1.5, 2.0]

        >>> list(float_closed_crange(2.0, 1.0, -0.5))
        [2.0, 1.5, 1.0]

        >>> list(float_closed_crange(1.0, 1.0, 0.1))
        [1.0]
    """
    # return takewhile(lambda x: x <= stop, count(start, step))
    return takewhile(lambda x: x <= stop, (start + i * step for i in count()))


def in_closed_range(value: int, range_: tuple[int, int]) -> bool:
    """
    Check if a value is within a closed range.

    Args:
        value (int): The value to check.
        range (tuple[int, int]): A tuple representing the closed range (start, end).

    Returns:
        bool: True if the value is within the range, False otherwise.
    """
    return min(range_) <= int(value) <= max(range_)


@dataclass
class Inset:
    "CSS-like Rectangle Descriptor."
    top: int
    right: int
    bottom: int
    left: int

    def __init__(self, *args: int) -> None:
        match len(args):
            case 1:
                self.top, self.right, self.bottom, self.left = args[0], args[0], args[0], args[0]
            case 2:
                self.top, self.right, self.bottom, self.left = args[0], args[1], args[0], args[1]
            case 3:
                self.top, self.right, self.bottom, self.left = args[0], args[1], args[2], args[1]
            case 4:
                self.top, self.right, self.bottom, self.left = args[0], args[1], args[2], args[3]
            case _:
                raise ValueError("Invalid number of arguments.")

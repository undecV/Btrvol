"""Some of utilities."""

from dataclasses import dataclass
from itertools import count, takewhile


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

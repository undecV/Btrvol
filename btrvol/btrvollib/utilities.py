"""Some of utilities."""

from itertools import count, takewhile


def cloaed_range(start: int, stop: int, step: int = 1) -> list:
    if start <= stop:
        return list(range(start, stop + 1, step))
    else:
        return list(range(stop, start + 1, step))[::-1]


def float_closed_range(start: float, stop: float, step: float) -> takewhile:
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

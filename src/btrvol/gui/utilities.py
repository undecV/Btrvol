"""Utility functions for the BtrVol GUI."""


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


def in_closed_range(value: int, range_: tuple[int, int]) -> bool:
    """
    Check if a value is within a closed range.

    Args:
        value (int): The value to check.
        range (tuple[int, int]): A tuple representing the closed range
            (start, end).

    Returns:
        bool: True if the value is within the range, False otherwise.
    """
    return min(range_) <= int(value) <= max(range_)

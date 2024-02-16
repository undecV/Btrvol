"""Formulas for Btrvol."""

import math

from .selectors import BtrvolTone


def btrvol_formula(time: float, start: float, end: float, duration: float, method: BtrvolTone) -> float:
    """Calculates the volume scalar at a given time using a specific method.

    This function calculates the volume level (between 0.0 and 1.0) at a specific time point
    based on the provided start volume, end volume, duration, and chosen method. It supports four methods:

    - LINEAR: Linearly interpolates between start and end volume over time.
    - SMOOTH: Uses a cosine curve for a smooth transition between volumes.
    - GRADUAL: Similar to smooth but with a steeper incline/decline at the start/end.
    - RAPID: Uses a sine curve for a quicker ramp-up/down between volumes.

    Args:
        time: The current time point within the duration (in seconds).
        start: The starting volume level (between 0.0 and 1.0).
        end: The ending volume level (between 0.0 and 1.0).
        duration: The total duration of the volume change (in seconds).
        method: The chosen BtrvolMethod for volume calculation.

    Returns:
        The calculated volume level as a float (between 0.0 and 1.0).

    Raises:
        AssertionError: If any input parameter is outside its valid range.
    """
    # assert 0.0 <= start <= 1.0
    # assert 0.0 <= end <= 1.0
    assert 0.0 < duration
    assert 0.0 <= time <= duration

    volume_scalar: float = 0.0  # in range [0, 1]

    match method:
        case BtrvolTone.LINEAR:
            volume_scalar = (time * (end - start) / duration) + start
        case BtrvolTone.SMOOTH:
            volume_scalar = math.cos(time * math.pi / duration) * ((start - end) / 2.0) + ((start + end) / 2.0)
        case BtrvolTone.GRADUAL:
            volume_scalar = math.cos((time * math.pi) / (2.0 * duration)) * (start - end) + end
        case BtrvolTone.RAPID:
            volume_scalar = math.sin((time * math.pi) / (2.0 * duration)) * (end - start) + start
        case _:
            raise NotImplementedError("Bad method selector.")

    return volume_scalar


def btrvol_formula_simple(time: float, start: float, end: float, duration: float, method: BtrvolTone) -> int:
    """Calculates the volume level at a given time with rounding or ceiling/floor.

    This function simplifies the output of `btrvol_formula` by converting the
    floating-point volume scalar to an integer using floor, ceil, or round
    depending on the relationship between start and end volumes.

    Args:
        time: The current time point within the duration (in seconds).
        start: The starting volume level (between 0.0 and 1.0).
        end: The ending volume level (between 0.0 and 1.0).
        duration: The total duration of the volume change (in seconds).
        method: The chosen BtrvolMethod for volume calculation.

    Returns:
        The calculated volume level as an integer.

    Raises:
        AssertionError: If any input parameter is outside its valid range.
    """
    volume_scalar = btrvol_formula(time, start, end, duration, method)
    volume: int
    if start < end:
        volume = math.floor(volume_scalar)
    elif start > end:
        volume = math.ceil(volume_scalar)
    else:
        volume = round(volume_scalar)
    return volume


def btrvol_formula_inverse(volume: float, start: float, end: float, duration: float, method: BtrvolTone) -> float:
    """Calculates the time corresponding to a given volume level using a specific method.

    This function finds the time point within the duration that corresponds to a
    specific volume level based on the provided start volume, end volume, and method.

    Args:
        volume: The target volume level (between 0.0 and 1.0).
        start: The starting volume level (between 0.0 and 1.0).
        end: The ending volume level (between 0.0 and 1.0).
        duration: The total duration of the volume change (in seconds).
        method: The chosen BtrvolMethod used for the volume change.

    Returns:
        The calculated time point within the duration (in seconds).

    Raises:
        AssertionError: If any input parameter is outside its valid range.
    """

    # assert 0 <= start <= 1
    # assert 0 <= end <= 1
    assert min(start, end) <= volume <= max(start, end)
    assert 0 < duration

    if start == end:
        return 0.0

    time: float = 0.0
    match method:
        case BtrvolTone.LINEAR:
            time = ((volume - start) * duration) / (end - start)
        case BtrvolTone.SMOOTH:
            time = (duration / math.pi) * math.acos((2 * volume - start - end) / (start - end))
        case BtrvolTone.GRADUAL:
            time = (2 * duration / math.pi) * math.acos((volume - end) / (start - end))
        case BtrvolTone.RAPID:
            time = (2 * duration / math.pi) * math.asin((volume - start) / (end - start))
        case _:
            raise NotImplementedError("Bad method selector.")
    return time

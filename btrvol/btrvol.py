"""Btrvol Formulas."""

import logging

from rich.logging import RichHandler

from .formulas import btrvol_formula_inverse, btrvol_formula_simple
from .selectors import BtrvolTone, BtrvolMode
from .utilities import cloaed_range, float_closed_range


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=[RichHandler(),])
log = logging.getLogger()


MINIMIUM_INTERVAL: float = 0.1


def btrvol(
    start: int, end: int, duration: int, method: BtrvolTone, minimium_interval: float = MINIMIUM_INTERVAL
) -> tuple[list[int], list[float], list[float], BtrvolMode]:
    """
    Calculates the volume levels and time points for a volume ramp using the BTR (Bellman-Tremblay-Roth) method.

    Args:
        start (int): Starting volume level (0-100).
        end (int): Ending volume level (0-100).
        duration (int): Duration of the volume ramp in seconds.
        method (BtrvolMethod): The BTR method to use (e.g., `BtrvolMethod.TIME`, `BtrvolMethod.INTERVAL`).
        minimum_interval (float, optional): Minimum interval between volume changes in seconds.
            Defaults to `MINIMIUM_INTERVAL`.

    Returns:
        - `volumes`: A list of volume levels (0-100).
        - `time_points`: A list of time points in seconds.
        - `intervals`: A list of intervals between time points in seconds.
        - The BTR mode used (`BtrvolMode.TIME` or `BtrvolMode.INTERVAL`).

    Raises:
        ValueError: If any of the arguments are invalid.

    Notes:
        - The BTR method is a commonly used algorithm for creating smooth volume ramps.
        - The `minimum_interval` argument ensures that the volume changes frequently enough to avoid audible artifacts.
        - The function logs debug information about the calculated volumes, time points, and intervals.
    """

    mode: BtrvolMode = BtrvolMode.TIME
    volumes: list[int] = cloaed_range(start, end)
    time_points: list[float] = []
    for volume in volumes:
        time_point: float = \
            btrvol_formula_inverse(volume, start, end, float(duration), method)
        time_points.append(time_point)

    intervals: list[float] = [time_points[0]]
    intervals += [j-i for i, j in zip(time_points[:-1], time_points[1:])]

    # Fixed interval mode.
    if len(intervals) > 1 and min(intervals[1:]) < minimium_interval:
        mode = BtrvolMode.INTERVAL
        time_points = list(float_closed_range(0.0, float(duration), minimium_interval))
        intervals = [minimium_interval] * len(time_points)
        volumes = []
        for time_point in time_points:
            volume = btrvol_formula_simple(time_point, start, end, float(duration), method)
            volumes.append(volume)

    log.debug("volumes: %r", volumes)
    log.debug("time_points: %r", [round(time_point, 4) for time_point in time_points])
    log.debug("intervals: %r", [round(interval, 4) for interval in intervals])
    return volumes, time_points, intervals, mode

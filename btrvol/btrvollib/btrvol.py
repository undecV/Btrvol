"""Btrvol Formulas."""

import logging

from rich.logging import RichHandler


from .configuration import BtrvolConfiguration
from .formulas import btrvol_formula_inverse, btrvol_formula_simple
from .selectors import BtrvolTone, BtrvolMode
from .utilities import closed_float_range


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=[RichHandler(),])
log = logging.getLogger()


MINIMIUM_INTERVAL: float = 0.1


def btrvol(
    configuration: BtrvolConfiguration, minimium_interval: float = MINIMIUM_INTERVAL
) -> tuple[list[int], list[float], list[float], BtrvolMode]:
    """Calculates the volume levels and time points for a volume ramp."""
    start: int = configuration.volume_start
    end: int = configuration.volume_end
    duration: int = configuration.duration
    tone: BtrvolTone = configuration.tone

    mode: BtrvolMode = BtrvolMode.TIME
    volumes: list[int] = list(range(start, end + (1 if start <= end else -1), (1 if start <= end else -1)))
    time_points: list[float] = []
    for volume in volumes:
        time_point: float = \
            btrvol_formula_inverse(volume, start, end, float(duration), tone)
        time_points.append(time_point)

    intervals: list[float] = [time_points[0]]
    intervals += [j-i for i, j in zip(time_points[:-1], time_points[1:])]

    # Fixed interval mode.
    if len(intervals) > 1 and min(intervals[1:]) < minimium_interval:
        mode = BtrvolMode.INTERVAL
        time_points = list(closed_float_range(0.0, float(duration), minimium_interval))
        intervals = [minimium_interval] * len(time_points)
        volumes = []
        for time_point in time_points:
            volume = btrvol_formula_simple(time_point, start, end, float(duration), tone)
            volumes.append(volume)

    log.debug("Volumes: %r", volumes)
    log.debug("Time Points: %r", [round(time_point, 4) for time_point in time_points])
    log.debug("Intervals: %r", [round(interval, 4) for interval in intervals])
    return volumes, time_points, intervals, mode

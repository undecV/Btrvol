"""BtrVol: A Python Library for Smooth Volume Adjustment."""

from __future__ import annotations

import enum
import math
from fractions import Fraction
from typing import TypeAlias, TypeVar

MINIMUM_INTERVAL_THRESHOLD: Fraction = Fraction(1, 10)  # 0.1 seconds


Real: TypeAlias = int | float | Fraction
RealT = TypeVar("RealT", int, float, Fraction)


class BtrVol:
    """
    BtrVol: A class to calculate volume levels and time points for smooth
    volume adjustment.
    """
    # Configuration for BtrVol.
    _config: BtrVol.Config

    # Cached calculated results:
    _minimum_interval: float
    _mode: BtrVol.Mode
    _volume_levels: list[int]
    _time_points: list[float]
    _time_intervals: list[float]

    class Config:
        """BtrVol Configuration with Validation."""
        _start: int
        _end: int
        _duration: int
        _tone: BtrVol.Tone
        _minimum_interval_threshold: Fraction = MINIMUM_INTERVAL_THRESHOLD

        @property
        def start(self) -> int:
            """Volume adjustment start value, between [0, 100]."""
            return self._start

        @start.setter
        def start(self, value: int):
            if not 0 <= value <= 100:
                raise ValueError("Start volume must be between 0 and 100.")
            self._start = value

        def safe_set_start(self, value: int) -> int:
            """Set start volume without raising ValueError."""
            self.start = min(max(value, 0), 100)
            return self.start

        @property
        def end(self) -> int:
            """Volume adjustment end value, between [0, 100]."""
            return self._end

        @end.setter
        def end(self, value: int):
            if not 0 <= value <= 100:
                raise ValueError("End volume must be between 0 and 100.")
            self._end = value

        def safe_set_end(self, value: int) -> int:
            """Set end volume without raising ValueError."""
            self.end = min(max(value, 0), 100)
            return self.end

        @property
        def duration(self) -> int:
            """Volume adjustment duration, larger than 0."""
            return self._duration

        @duration.setter
        def duration(self, value: int):
            if not 0 < value:
                raise ValueError("Duration must be larger than 0.")
            self._duration = value

        def safe_set_duration(self, value: int) -> int:
            """Set duration without raising ValueError."""
            self.duration = max(value, 1)
            return self.duration

        @property
        def tone(self) -> BtrVol.Tone:
            """Volume adjustment tone, one of `BtrVol.Tone`."""
            return self._tone

        @tone.setter
        def tone(self, value: BtrVol.Tone):
            self._tone = value

        @property
        def minimum_interval_threshold(self) -> Fraction:
            """
            Minimum interval between volume adjustments.
            When the calculated interval is less than this value,
            switch to fixed interval mode.
            """
            return self._minimum_interval_threshold

        @minimum_interval_threshold.setter
        def minimum_interval_threshold(self, value: Fraction):
            if not 0.01 <= value <= 1:
                raise ValueError(
                    "Minimum interval threshold must be in the range"
                    "`[0.01, 1]`."
                )
            self._minimum_interval_threshold = value

        def __init__(
            self, start: int, end: int, duration: int, tone: BtrVol.Tone,
            minimum_interval_threshold: Fraction = MINIMUM_INTERVAL_THRESHOLD
        ):
            self.start = start
            self.end = end
            self.duration = duration
            self.tone = tone
            self.minimum_interval_threshold = minimum_interval_threshold

        def serialize(self) -> dict:
            """Serialize the configuration to a dictionary."""
            return {
                "start": self.start,
                "end": self.end,
                "duration": self.duration,
                "tone": self.tone.name,
                "minimum_interval_threshold": float(
                    self.minimum_interval_threshold
                )
            }

        @classmethod
        def deserialize(cls, data: dict) -> BtrVol.Config:
            """Deserialize the configuration from a dictionary."""
            return cls(
                start=data.get("start", 20),
                end=data.get("end", 80),
                duration=data.get("duration", 42),
                tone=BtrVol.Tone[data.get("tone", "LINEAR")],
                minimum_interval_threshold=Fraction(
                    data.get("minimum_interval_threshold", 0.1)
                )
            )

    class Tone(enum.StrEnum):
        """Tone Selector for BtrVol Formulas."""
        LINEAR = enum.auto()
        SMOOTH = enum.auto()
        GRADUAL = enum.auto()
        RAPID = enum.auto()

    class Mode(enum.Enum):
        """Mode Selector for BtrVol Formulas."""
        INTERVAL = enum.auto()
        TIME = enum.auto()

    def __init__(
        self, start: int, end: int, duration: int, tone: BtrVol.Tone,
        minimum_interval_threshold: Fraction = MINIMUM_INTERVAL_THRESHOLD
    ) -> None:
        self._volume_levels = []
        self._time_points = []
        self._time_intervals = []
        self._config = BtrVol.Config(
            start=start, end=end, duration=duration, tone=tone,
            minimum_interval_threshold=minimum_interval_threshold
        )
        self._calc()

    @property
    def config(self) -> BtrVol.Config:
        """Get the current configuration."""
        return self._config

    def update(
        self, start: int | None = None, end: int | None = None,
        duration: int | None = None, tone: BtrVol.Tone | None = None,
        minimum_interval_threshold: Fraction | None = None
    ) -> None:
        """Update the configuration and recalculate the results."""
        if start is not None:
            self._config.start = start
        if end is not None:
            self._config.end = end
        if duration is not None:
            self._config.duration = duration
        if tone is not None:
            self._config.tone = tone
        if minimum_interval_threshold is not None:
            self._config.minimum_interval_threshold = \
                minimum_interval_threshold
        self._calc()

    @property
    def volume_start(self) -> int:
        """Volume adjustment start value, between [0, 100]."""
        return self._config.start

    @volume_start.setter
    def volume_start(self, value: int):
        self._config.start = value
        self._calc()

    def safe_set_volume_start(self, value: int) -> int:
        """Set start volume without raising ValueError."""
        self._config.safe_set_start(value)
        self._calc()
        return self._config.start

    @property
    def volume_end(self) -> int:
        """Volume adjustment end value, between [0, 100]."""
        return self._config.end

    @volume_end.setter
    def volume_end(self, value: int):
        self._config.end = value
        self._calc()

    def safe_set_volume_end(self, value: int) -> int:
        """Set end volume without raising ValueError."""
        self._config.safe_set_end(value)
        self._calc()
        return self._config.end

    @property
    def duration(self) -> int:
        """Volume adjustment duration, larger than 0."""
        return self._config.duration

    @duration.setter
    def duration(self, value: int):
        self._config.duration = value
        self._calc()

    def safe_set_duration(self, value: int) -> int:
        """Set duration without raising ValueError."""
        self._config.safe_set_duration(value)
        self._calc()
        return self._config.duration

    @property
    def tone(self) -> BtrVol.Tone:
        """Volume adjustment tone, one of `BtrVol.Tone`."""
        return self._config.tone

    @tone.setter
    def tone(self, value: BtrVol.Tone):
        self._config.tone = value
        self._calc()

    @property
    def minimum_interval_threshold(self) -> Fraction:
        """
        Minimum interval between volume adjustments.
        When the calculated interval is less than this value,
        switch to fixed interval mode.
        """
        return self._config.minimum_interval_threshold

    @minimum_interval_threshold.setter
    def minimum_interval_threshold(self, value: Fraction):
        """
        When the calculated interval is less than this value,
        switch to fixed interval mode.
        """
        self._config.minimum_interval_threshold = value
        self._calc()

    @classmethod
    def _clamp(
        cls, value: float, min_value: float = 0.0, max_value: float = 1.0
    ) -> float:
        """Clamp a value between min_value and max_value."""
        if min_value > max_value:
            raise ValueError(
                "`min_value` must be less than or equal to `max_value`."
            )

        return max(min_value, min(value, max_value))

    @classmethod
    def time_to_volume(
        cls, time: float, start: float, end: float, duration: float,
        method: BtrVol.Tone
    ) -> float:
        """
        BtrVol formulas to calculate volume at a given time point.
        """
        volume: float = 0.0

        match method:
            case BtrVol.Tone.LINEAR:
                volume = (time * (end - start) / duration) + start
            case BtrVol.Tone.SMOOTH:
                volume = math.cos(time * math.pi / duration) * \
                    ((start - end) / 2.0) + ((start + end) / 2.0)
            case BtrVol.Tone.GRADUAL:
                volume = math.cos((time * math.pi) / (2.0 * duration)) * \
                    (start - end) + end
            case BtrVol.Tone.RAPID:
                volume = math.sin((time * math.pi) / (2.0 * duration)) * \
                    (end - start) + start
        return volume

    @classmethod
    def volume_to_time(
        cls, volume: float, start: float, end: float, duration: float,
        method: BtrVol.Tone
    ) -> float:
        """
        Inverse BtrVol formulas to calculate time at a given volume level.
        """
        time: float = 0.0

        if start == end:
            return 0.0

        match method:
            case BtrVol.Tone.LINEAR:
                time = ((volume - start) * duration) / (end - start)
            case BtrVol.Tone.SMOOTH:
                time = (duration / math.pi) * math.acos(cls._clamp(
                    (2 * volume - start - end) / (start - end), -1, 1
                ))
            case BtrVol.Tone.GRADUAL:
                time = (2 * duration / math.pi) * math.acos(
                    cls._clamp((volume - end) / (start - end), -1, 1))
            case BtrVol.Tone.RAPID:
                time = (2 * duration / math.pi) * math.asin(
                    cls._clamp((volume - start) / (end - start), -1, 1))

        return time

    @classmethod
    def get_minimum_interval(
        cls, start: int, end: int, duration: int, method: BtrVol.Tone
    ) -> float:
        """
        Calculate the minimum interval between volume adjustments.
        Mathematically,
        it is the minimum of the derivative of the volume function.
        """
        if start == end:
            return float(duration)

        delta = abs(end - start)

        match method:
            case BtrVol.Tone.LINEAR:
                return duration / delta
            case BtrVol.Tone.SMOOTH | BtrVol.Tone.GRADUAL | BtrVol.Tone.RAPID:
                return (2 / math.pi) * (duration / delta)

    @property
    def minimum_interval(self) -> float:
        """Minimum interval between volume adjustments."""
        return self._minimum_interval

    @property
    def mode(self) -> BtrVol.Mode:
        """
        Mode of volume adjustment.

        when `minimum_interval < minimum_interval_threshold`,
        switch to fixed interval mode `BtrVol.Mode.INTERVAL`,
        which change volume with fixed time intervals.

        Else wise, use variable interval mode `BtrVol.Mode.TIME`,
        which change volume to next step with variable time intervals.
        """
        return self._mode

    def __str__(self):
        return f"<BtrVol {self._config.serialize()}>"

    def _calc(self) -> None:
        start = self.volume_start
        end = self.volume_end
        duration = self.duration
        tone = self.tone

        self._minimum_interval = \
            self.get_minimum_interval(start, end, duration, tone)

        if self._minimum_interval < self.minimum_interval_threshold:
            self._mode = BtrVol.Mode.INTERVAL
        else:
            self._mode = BtrVol.Mode.TIME

        volume_levels: list[int] = []
        time_points: list[float] = []
        time_intervals: list[float] = []

        match self._mode:
            case BtrVol.Mode.TIME:
                step = 1 if self.volume_end >= self.volume_start else -1
                volume_levels = list(range(start, end + step, step))
                for volume in volume_levels:
                    time_point: float = self.volume_to_time(
                        float(volume), float(start), float(end),
                        float(duration), tone
                    )
                    time_points.append(
                        self._clamp(time_point, 0.0, float(duration))
                    )
                time_intervals = self._get_intervals(time_points)

            case BtrVol.Mode.INTERVAL:
                steps = max(1, math.ceil(
                    self.duration / self.minimum_interval_threshold))
                interval = Fraction(self.duration, steps)
                time_point_fractions = [i * interval for i in range(steps + 1)]
                # time_intervals = [float(frac) for frac in
                #                   self._get_intervals(time_point_fractions)]

                for i, time_point_fraction in enumerate(time_point_fractions):
                    volume_level = round(self.time_to_volume(
                        float(time_point_fraction), float(start), float(end),
                        float(duration), tone))
                    if (
                        volume_levels
                        and i != len(time_point_fractions) - 1
                        and volume_level == volume_levels[-1]
                    ):
                        continue
                    time_points.append(float(time_point_fraction))
                    volume_levels.append(volume_level)
                time_intervals = self._get_intervals(time_points)

        self._volume_levels = volume_levels
        self._time_points = time_points
        self._time_intervals = time_intervals

    @classmethod
    def _get_intervals(cls, time_points: list[RealT]) -> list[RealT]:
        """Calculate time intervals from time points."""
        if not time_points:
            return []
        return [time_points[0]] + [
            j - i for i, j in zip(time_points[:-1], time_points[1:])
        ]

    @property
    def volume_levels(self) -> list[int]:
        """Calculated volume levels."""
        return list(self._volume_levels)

    @property
    def time_points(self) -> list[float]:
        """Calculated time points."""
        return list(self._time_points)

    @property
    def time_intervals(self) -> list[float]:
        """Calculated time intervals."""
        return list(self._time_intervals)

    def serialize(self) -> dict:
        """Serialize the configuration to a dictionary."""
        return self._config.serialize()

    @classmethod
    def deserialize(cls, data: dict) -> BtrVol:
        """Deserialize the configuration from a dictionary."""
        config = BtrVol.Config.deserialize(data)
        return cls(
            start=config.start,
            end=config.end,
            duration=config.duration,
            tone=config.tone,
            minimum_interval_threshold=config.minimum_interval_threshold
        )

"""Configurations for BtrVol."""


from typing import ClassVar
from btrvol.btrvollib.selectors import BtrvolTone


DEFAULT_VOLUME_START: int = 20
DEFAULT_VOLUME_END: int = 80
DEFAULT_DURATION: int = 3600
DEFAULT_TONE: BtrvolTone = BtrvolTone.SMOOTH


class BtrvolConfiguration:
    """Configurations for BtrVol."""
    volume_range: ClassVar[tuple[int, int]] = (0, 100)
    duration_range: ClassVar[tuple[int, int]] = (1, 86400)

    _volume_start: int = DEFAULT_VOLUME_START
    _volume_end: int = DEFAULT_VOLUME_END
    _duration: int = DEFAULT_DURATION
    _tone: BtrvolTone = DEFAULT_TONE

    def __init__(
        self,
        volume_start: int = DEFAULT_VOLUME_START,
        volume_end: int = DEFAULT_VOLUME_END,
        duration: int = DEFAULT_DURATION,
        tone: BtrvolTone = DEFAULT_TONE,
    ) -> None:

        self.volume_start: int = volume_start
        self.volume_end: int = volume_end
        self.duration: int = duration
        self.tone: BtrvolTone = tone

    def __repr__(self) -> str:
        return f"<BtrvolConfiguration {vars(self)}>"

    @property
    def volume_start(self) -> int:
        """Volume adjustment start value, between [0, 100]."""
        return self._volume_start

    @volume_start.setter
    def volume_start(self, value: int):
        self._volume_start = max(self.volume_range[0], min(value, self.volume_range[1]))

    @property
    def volume_end(self) -> int:
        """Volume adjustment end value, between [0, 100]."""
        return self._volume_end

    @volume_end.setter
    def volume_end(self, value: int):
        self._volume_end = max(self.volume_range[0], min(value, self.volume_range[1]))

    @property
    def duration(self) -> int:
        """Volume adjustment duration."""
        return self._duration

    @duration.setter
    def duration(self, value: int):
        self._duration = max(self.duration_range[0], min(value, self.duration_range[1]))

    @property
    def tone(self) -> BtrvolTone:
        """Volume adjustment tone."""
        return self._tone

    @tone.setter
    def tone(self, value: BtrvolTone):
        self._tone = value

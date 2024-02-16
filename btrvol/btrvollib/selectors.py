import enum


class BtrvolMode(enum.Enum):
    """Mode Selector for Btrvol Formulas."""
    INTERVAL = enum.auto()
    TIME = enum.auto()


class BtrvolTone(enum.Enum):
    """Tone Selector for Btrvol Formulas."""
    LINEAR = enum.auto()
    SMOOTH = enum.auto()
    GRADUAL = enum.auto()
    RAPID = enum.auto()

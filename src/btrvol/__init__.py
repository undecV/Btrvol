"""BtrVol: A simple automatic system volume controller."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("btrvol")  # ← 用你 pyproject 裡的 name
except PackageNotFoundError:
    __version__ = "0.0.0.dev"

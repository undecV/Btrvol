"""
This module provides a way to load the awthemes themes into Tkinter.
"""

__version__: str = "0.1.0"


import contextlib
import logging
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Any, Generator

from rich.logging import RichHandler
import tksvg  # type: ignore


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=(RichHandler(), ))
log = logging.getLogger()


AWTHEMES_PATH: Path = Path(__file__).parent / "awthemes-10.4.0"


@contextlib.contextmanager
def temporary_chdir(path: Path) -> Generator[Any, Any, Any]:
    """Context manager to temporarily change the working directory."""
    cwd: Path = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


class AwthemesStyle(ttk.Style):
    """A style class that loads the awthemes themes into Tkinter."""
    awthemes_scalable: list[str] = [
        "awarc", "awblack", "awclearlooks", "awwinxpblue", "awbreeze", "awbreezedark", "awtemplate"
    ]
    awthemes: list[str] = ["awdark", "awlight"]

    def __init__(self, *args, **kwargs) -> None:
        ttk.Style.__init__(self, *args, **kwargs)
        self._load_themes()

    def _load_themes(self):
        """Load the themes into the Tkinter interpreter."""
        # with temporary_chdir(AWTHEMES_PATH):
        #     self.tk.call("lappend", "auto_path", f"[{AWTHEMES_PATH}]")
        self.tk.eval(f"set dir {AWTHEMES_PATH.as_posix()}")
        self.tk.eval(f"source {AWTHEMES_PATH.as_posix()}/pkgIndex.tcl")

    def get_themes(self) -> list[str]:
        """Return a list of names of available themes."""
        return list(set(self.tk.call("ttk::themes")))

    def theme_use(self, themename=None):
        is_tksvg_loaded = getattr(self.master, "_tksvg_loaded", False)
        if (themename in self.awthemes_scalable) and (not is_tksvg_loaded):
            tksvg.load(self.master)
        self.tk.call("package", "require", f"ttk::theme::{themename}")
        self.tk.call("ttk::setTheme", themename)
        return ttk.Style.theme_use(self)


if __name__ == "__main__":
    log.debug(AWTHEMES_PATH)
    root = tk.Tk()
    log.debug("_tksvg_loaded: %r", getattr(root, "_tksvg_loaded", None))
    style = AwthemesStyle(root)
    log.debug(style.get_themes())
    log.debug("_tksvg_loaded: %r", getattr(root, "_tksvg_loaded", None))
    style.theme_use("awdark")
    log.debug("_tksvg_loaded: %r", getattr(root, "_tksvg_loaded", None))
    style.theme_use("awblack")
    log.debug("_tksvg_loaded: %r", getattr(root, "_tksvg_loaded", None))

    # # Tkinter scaling windows automatically
    # scale_factor: int = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # log.debug("scale_factor: %.2f", scale_factor/100)
    # root.tk.call('tk', 'scaling', f"{scale_factor/100:.2f}")

    label = ttk.Label(root, text="Hello, world!")
    label.pack()
    root.update()
    log.debug("%d x %d", label.winfo_width(), label.winfo_height())
    root.mainloop(0)

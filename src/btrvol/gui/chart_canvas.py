"""A Canvas widget for drawing charts with axes and labels."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional, Sequence
from dataclasses import dataclass
from itertools import pairwise


@dataclass
class Inset:
    """CSS-like Rectangle Descriptor: top/right/bottom/left."""
    top: int
    right: int
    bottom: int
    left: int

    def __init__(self, *args: int) -> None:
        match len(args):
            case 1:
                t = args[0]
                self.top = self.right = self.bottom = self.left = t
            case 2:
                t, r = args
                self.top = self.bottom = t
                self.right = self.left = r
            case 3:
                t, r, b = args
                self.top = t
                self.right = self.left = r
                self.bottom = b
            case 4:
                self.top, self.right, self.bottom, self.left = args
            case _:
                raise ValueError("Inset expects 1, 2, 3, or 4 integers")


def liang_barsky_clip(
    x1: float, y1: float, x2: float, y2: float,
    xlo: float, xhi: float, ylo: float, yhi: float
) -> Optional[tuple[float, float, float, float]]:
    """
    Liang–Barsky line clipping. Returns clipped segment (nx1, ny1, nx2, ny2),
    or None if fully outside.
    """
    dx, dy = x2 - x1, y2 - y1
    u0, u1 = 0.0, 1.0
    for p, q in (
        (-dx, x1 - xlo),  # x >= xlo
        (dx, xhi - x1),  # x <= xhi
        (-dy, y1 - ylo),  # y >= ylo
        (dy, yhi - y1),  # y <= yhi
    ):
        if p == 0.0:
            if q < 0.0:
                return None
            continue
        t = q / p
        if p < 0.0:                # entering
            u0 = max(u0, t)
            if u0 > u1:
                return None
        else:                       # leaving
            u1 = min(u1, t)
            if u1 < u0:
                return None
    nx1, ny1 = x1 + u0 * dx, y1 + u0 * dy
    nx2, ny2 = x1 + u1 * dx, y1 + u1 * dy
    return nx1, ny1, nx2, ny2


Point = tuple[float, float]
Line = tuple[Point, Point]


class ChartCanvas(tk.Canvas):
    """A Canvas widget for drawing charts with axes and labels."""

    x_label: str
    y_label: str
    x_range: tuple[float, float]
    y_range: tuple[float, float]
    trace: Sequence[Line]

    def __init__(self, master: Any, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)

        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.foreground_color = kwargs.get("fg", "black")
        self.background_color = kwargs.get("bg", "white")
        self.style = ttk.Style(master)

        self.padding: Inset = Inset(10, 20, 20, 30)
        self.x_label = "X"
        self.y_label = "Y"
        self.x_range = (0.0, 100.0)
        self.y_range = (0.0, 100.0)
        self.trace = []

        self.on_theme_changed()
        self.bind("<Configure>", self._on_resize)
        self.bind_all("<<ThemeChanged>>", self.on_theme_changed)

    def on_theme_changed(self, _event: tk.Event | None = None) -> None:
        self.style = ttk.Style(self.master)
        self.foreground_color = \
            self.style.lookup("TLabel", "foreground") or self.foreground_color
        self.background_color = \
            self.style.lookup("TFrame", "background") or self.background_color
        self.configure(bg=self.background_color)
        self.configure(highlightthickness=0)
        self._draw()

    def set_ranges(self,
                   x_range: tuple[float, float],
                   y_range: tuple[float, float]) -> None:
        """Set the x and y ranges and redraw the chart."""
        xmin, xmax = x_range
        ymin, ymax = y_range
        # 嚴格：零長度直接拋錯（避免除以 0）
        if not all(isinstance(v, (int, float)) and math.isfinite(v)
                   for v in (xmin, xmax, ymin, ymax)):
            raise ValueError(f"Non-finite range: {x_range=}, {y_range=}")
        if xmax == xmin:
            raise ValueError(
                f"x_range must have non-zero length, got {x_range}")
        if ymax == ymin:
            raise ValueError(
                f"y_range must have non-zero length, got {y_range}")
        self.x_range = (float(xmin), float(xmax))
        self.y_range = (float(ymin), float(ymax))
        self._draw()

    def set_trace(self, trace: Sequence[Line]) -> None:
        """Set the trace data (list of segments) and redraw the chart."""
        self.trace = trace
        self._draw()

    def _on_resize(self, event: tk.Event) -> None:
        self.width = int(event.width)
        self.height = int(event.height)
        self._draw()

    def _draw(self) -> None:
        self.delete("all")

        plot_left = self.padding.left
        plot_top = self.padding.top
        plot_right = self.width - self.padding.right
        plot_bottom = self.height - self.padding.bottom
        plot_w = max(plot_right - plot_left, 1)
        plot_h = max(plot_bottom - plot_top, 1)

        xmin, xmax = self.x_range
        ymin, ymax = self.y_range

        self.create_rectangle(
            plot_left, plot_top, plot_right, plot_bottom,
            width=2, outline=self.foreground_color
        )

        self.create_text(
            plot_left // 2, plot_top,
            text=f"{ymax:g}", fill=self.foreground_color
        )
        self.create_text(
            plot_left // 2, plot_top + (plot_h // 2),
            text=self.y_label, angle=90, fill=self.foreground_color
        )
        self.create_text(
            plot_left // 2, plot_bottom,
            text=f"{ymin:g}", fill=self.foreground_color
        )

        x_axis_label_y = self.height - (self.padding.bottom // 2)
        self.create_text(
            plot_left, x_axis_label_y,
            text=f"{xmin:g}", fill=self.foreground_color
        )
        self.create_text(
            plot_left + (plot_w // 2), x_axis_label_y,
            text=self.x_label, fill=self.foreground_color
        )
        self.create_text(
            plot_right, x_axis_label_y,
            text=f"{xmax:g}", fill=self.foreground_color
        )

        xlo, xhi = sorted((xmin, xmax))
        ylo, yhi = sorted((ymin, ymax))

        sx = plot_w / (xmax - xmin)
        sy = plot_h / (ymax - ymin)

        def to_canvas(point: Point) -> Point:
            x, y = point
            return (plot_left + (x - xmin) * sx,
                    plot_bottom - (y - ymin) * sy)

        for (tx1, ty1), (tx2, ty2) in self.trace:
            clipped = liang_barsky_clip(tx1, ty1, tx2, ty2, xlo, xhi, ylo, yhi)
            if clipped is None:
                continue
            cx1, cy1, cx2, cy2 = clipped
            self.create_line(*to_canvas((cx1, cy1)), *to_canvas((cx2, cy2)),
                             fill=self.foreground_color, width=1)


if __name__ == "__main__":
    from btrvol.core.btrvol import BtrVol

    root = tk.Tk()
    root.title("Chart Canvas Example")

    chart = ChartCanvas(root, width=640, height=360,
                        x_label="Duration", y_label="Volume")
    chart.pack(fill=tk.BOTH, expand=True)

    btrvol = BtrVol(20, 80, 3600, BtrVol.Tone.SMOOTH)
    # 產生線段資料（pairwise）
    xs = list(btrvol.time_points)
    ys = [float(v) for v in btrvol.volume_levels]
    segments = [((x1, y1), (x2, y2)) for (x1, y1), (x2, y2) in pairwise(zip(xs, ys))]

    # 自動範圍
    all_x = [x for seg in segments for x, _ in seg]
    all_y = [y for seg in segments for _, y in seg]
    auto_x_range = (min(all_x), max(all_x))
    auto_y_range = (min(all_y), max(all_y))

    # chart.set_ranges(auto_x_range, auto_y_range)
    # chart.set_trace(segments)

    root.mainloop()

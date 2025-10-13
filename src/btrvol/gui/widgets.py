"""Custom Pygubu widgets."""

from pygubu.api.v1 import BuilderObject, register_widget  # type: ignore

from btrvol.gui.chart_canvas import ChartCanvas


class ChartCanvasBuilder(BuilderObject):
    """ChartCanvas custom widget for Pygubu."""
    class_ = ChartCanvas


register_widget(
    "btrvol.gui.chart_canvas.ChartCanvas",
    ChartCanvasBuilder,
    "ChartCanvas",
    ("ttk", "Chart Canvas"),
)

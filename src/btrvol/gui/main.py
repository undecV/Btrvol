"""GUI of Btrvol."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import sys
import logging
import json
import enum
from typing import Any, Callable
from threading import Event, Thread
from pathlib import Path
from itertools import pairwise
from importlib.resources import files, as_file
import ctypes

# import ttkwidgets  # type: ignore
import pygubu  # type: ignore
import keyboard  # type: ignore
import platformdirs  # type: ignore
from awthemes import AwthemesStyle

from btrvol.core.btrvol import BtrVol
from btrvol.core.volume_control import VolumeControl
from btrvol import __version__
from btrvol.gui.utilities import readable_time
from btrvol.gui.chart_canvas import ChartCanvas

from btrvol.gui import chart_canvas
from btrvol.gui import widgets
sys.modules.setdefault("chart_canvas", chart_canvas)
sys.modules.setdefault("widgets", widgets)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


PROJECT_PATH = files("btrvol.gui")
PROJECT_UI = PROJECT_PATH / "main.ui"
ASSETS_PATH = PROJECT_PATH / "assets"
ICON_FILE = ASSETS_PATH / "icons" / "icon.16.ico"
IMAGE_FILE = ASSETS_PATH / "icons" / "icon.png"


VOLUME_FAST_STEP = 5
VOLUME_FASTER_STEP = 10
DURATION_FAST_STEP = 30
DURATION_FASTER_STEP = 60


application_folder = Path(__file__).parent
if getattr(sys, 'frozen', False):
    application_folder = Path(sys.executable).parent


CONFIG_FILE_PATH = \
    Path(platformdirs.user_config_dir("BtrVol", "BtrVol")) / "config.json"
CONFIG_ENCODING = "utf-8"


class TkStringVarHandler(logging.Handler):
    """
    A logging handler that updates a Tkinter StringVar with log messages.

    Args:
        stringvar (tk.StringVar): The Tkinter StringVar to update with log
            messages.
        level (int, optional): The logging level for the handler. Defaults to
            `logger.NOTSET`.
    """

    def __init__(self, stringvar: tk.StringVar, level: int = 0) -> None:
        super().__init__(level)
        self.stringvar: tk.StringVar = stringvar

    def emit(self, record: logging.LogRecord):
        if record.levelno >= self.level:
            self.stringvar.set(self.format(record))


class PostAction:
    """Post action after volume control."""
    _delay: int
    _enable: bool
    _action: PostAction.Action

    class Action(enum.StrEnum):
        """Post action types."""
        PLAY_PAUSE = enum.auto()
        STOP = enum.auto()

    def __init__(
        self, enable: bool = False, delay: int = 0,
        action: PostAction.Action = Action.STOP
    ):
        self.enable = enable
        self.delay = delay
        self.action = action

    @property
    def delay(self) -> int:
        """Delay before post action in seconds."""
        return self._delay

    @delay.setter
    def delay(self, value: int):
        if not 0 <= value:
            raise ValueError("Delay must be non-negative.")
        self._delay = value

    @property
    def enable(self) -> bool:
        """Whether to enable post action."""
        return self._enable

    @enable.setter
    def enable(self, value: bool) -> None:
        self._enable = value

    @property
    def action(self) -> PostAction.Action:
        """Post action."""
        return self._action

    @action.setter
    def action(self, value: PostAction.Action) -> None:
        self._action = value

    def serialize(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "delay": self.delay,
            "enable": self.enable,
            "action": self.action.name
        }

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> PostAction:
        """Deserialize from dictionary."""
        return cls(
            delay=data.get("delay", 0),
            enable=data.get("enable", False),
            action=cls.Action[data.get("action", "STOP")]
        )


class MainApp:
    """GUI of Btrvol."""

    def __init__(self):
        self.model = self.Model()
        self.view = self.View()
        self.controller = self.Controller(self.model, self.view)

    class Model:
        btrvol: BtrVol
        theme: str
        post_action: PostAction
        allowed_themes: tuple[str, ...]

        def __init__(self):
            self.btrvol = BtrVol(20, 80, 1800, BtrVol.Tone.SMOOTH)
            self.theme = "awdark"
            self.post_action = PostAction(False, 0, PostAction.Action.STOP)
            self.allowed_themes = ()

        def save(self):
            data = self.serialize()
            CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_FILE_PATH.write_text(
                json.dumps(data, indent=4, ensure_ascii=False),
                CONFIG_ENCODING
            )
            logger.info("Configuration saved to %s.", CONFIG_FILE_PATH)

        def load(self):
            if not CONFIG_FILE_PATH.exists():
                logger.warning("Configuration file %s does not exist.",
                               CONFIG_FILE_PATH)
                return
            try:
                data = json.loads(CONFIG_FILE_PATH.read_text(CONFIG_ENCODING))
                model = self.deserialize(data)
                if model.theme not in self.allowed_themes:
                    raise ValueError(f"Unknown theme name: {model.theme}")
            except (json.JSONDecodeError, ValueError, KeyError) as exception:
                logger.error("Failed to load configuration from %s: %s",
                             CONFIG_FILE_PATH, exception)
                return
            self.btrvol = model.btrvol
            self.theme = model.theme
            self.post_action = model.post_action
            logger.info("Configuration loaded from %s.", CONFIG_FILE_PATH)

        def serialize(self) -> dict[str, Any]:
            """Serialize to dictionary."""
            return {
                "btrvol": self.btrvol.serialize(),
                "theme": self.theme,
                "post_action": self.post_action.serialize()
            }

        @classmethod
        def deserialize(cls, data: dict[str, Any]) -> MainApp.Model:
            """Deserialize from dictionary."""
            model = cls()
            model.btrvol = BtrVol.deserialize(data.get("btrvol", {}))
            model.theme = data.get("theme", "awdark")
            model.post_action = PostAction.deserialize(
                data.get("post_action", {}))
            return model

    class Controller:
        running: bool = False
        continuous_volume_control_event: Event

        def __init__(self, model: MainApp.Model, view: MainApp.View):
            self.model = model
            self.view = view
            self.model.allowed_themes = self.view.themes

            self.volume_control = VolumeControl()

            self.running = False
            self.continuous_volume_control_event = Event()
            self.continuous_volume_control_thread: Thread | None = None

            self.view.set_callbacks({
                "on_volume_start_scale_changed":
                    self.on_volume_start_scale_changed,
                "on_volume_end_scale_changed":
                    self.on_volume_end_scale_changed,
                "on_duration_changed":
                    self.on_duration_changed,
                "on_duration_text_changed":
                    self.on_duration_text_changed,
                "duration_value_validate":
                    self.duration_value_validate,
                "on_tone_radiobutton_clicked":
                    self.on_tone_radiobutton_clicked,
                "on_faster_change_value_clicked":
                    self.on_faster_change_value_clicked,
                "on_start_button_clicked":
                    self.on_start_button_clicked,
                "on_post_action_enable_checkbutton_toggle":
                    self.on_post_action_enable_checkbutton_toggle,
                "on_post_action_combobox_selected":
                    self.on_post_action_combobox_selected,
                "on_post_action_delay_spinbox_changed":
                    self.on_post_action_delay_spinbox_changed,
                "on_post_action_delay_spinbox_text_changed":
                    self.on_post_action_delay_spinbox_text_changed,
                "post_action_delay_value_validate":
                    self.post_action_delay_value_validate,
                "on_post_action_test_button_clicked":
                    self.on_post_action_test_button_clicked,
                "on_load_button_clicked":
                    self.on_load_button_clicked,
                "on_save_button_clicked":
                    self.on_save_button_clicked,
                "on_theme_selector_combobox_selected":
                    self.on_theme_selector_combobox_selected
            })

            self.model.load()
            self.on_configuration_change()
            self.view.change_theme(self.model.theme)

        def on_configuration_change(self):
            """Update UI Widgets when values update."""
            logger.debug(
                "Configuration changed: %r",
                self.model.btrvol.config.serialize()
            )
            logger.debug(
                "Configuration changed: %r",
                self.model.post_action.serialize()
            )
            self.view.volume_start_scale_value.set(
                self.model.btrvol.volume_start)
            self.view.volume_start_value_label_value.set(
                self.model.btrvol.volume_start)
            self.view.volume_end_scale_value.set(
                self.model.btrvol.volume_end)
            self.view.volume_end_value_label_value.set(
                self.model.btrvol.volume_end)
            self.view.duration_spinbox_value.set(
                self.model.btrvol.duration)
            self.view.duration_value_label_value.set(
                readable_time(self.model.btrvol.duration))
            self.view.tone_value.set(
                self.model.btrvol.tone.name)

            self.view.post_action_enable_checkbutton_value.set(
                self.model.post_action.enable)
            self.view.post_action_combobox_value.set(
                self.model.post_action.action.name)
            self.view.post_action_delay_value.set(
                self.model.post_action.delay)
            self.view.post_action_delay_value_label_value.set(
                readable_time(self.model.post_action.delay))

            segments = list(pairwise(zip(
                self.model.btrvol.time_points,
                self.model.btrvol.volume_levels)
            ))
            self.view.chart.set_ranges(
                (0, self.model.btrvol.duration),
                (0, 100)
            )
            self.view.chart.set_trace(segments)

        def on_theme_selector_combobox_selected(self, _event: Any) -> None:
            """on_theme_selector_combobox_selected"""
            self.model.theme = self.view.theme_selector_combobox_value.get()
            self.view.change_theme(self.model.theme)

        def duration_value_validate(self, p_entry_value: str) -> bool:
            """Validate duration spinbox input."""
            try:
                val = int(p_entry_value)
                return 0 < val
            except ValueError:
                return False

        def on_volume_start_scale_changed(self, _scale_value) -> None:
            """on_volume_start_scale_changed"""
            self.model.btrvol.volume_start = \
                self.view.volume_start_scale_value.get()
            self.on_configuration_change()

        def on_volume_end_scale_changed(self, _scale_value) -> None:
            """on_volume_end_scale_changed"""
            self.model.btrvol.volume_end = \
                self.view.volume_end_scale_value.get()
            self.on_configuration_change()

        def on_duration_text_changed(self, _event: tk.Event):
            """on_duration_text_changed"""
            self.on_duration_changed()

        def on_duration_changed(self):
            """on_duration_changed"""
            self.model.btrvol.duration = self.view.duration_spinbox_value.get()
            self.on_configuration_change()

        def on_tone_radiobutton_clicked(self, _widget_id: str):
            """on_tone_radiobutton_clicked"""
            self.model.btrvol.tone = BtrVol.Tone[self.view.tone_value.get()]
            self.on_configuration_change()

        def on_faster_change_value_clicked(self, widget_id: str):
            """on_faster_change_value_clicked"""

            delta_map: dict[str, tuple[str, int]] = {
                "volume_start_faster_decrease_button":
                    ("volume_start", -VOLUME_FASTER_STEP),
                "volume_start_fast_decrease_button":
                    ("volume_start", -VOLUME_FAST_STEP),
                "volume_start_faster_increase_button":
                    ("volume_start", VOLUME_FASTER_STEP),
                "volume_start_fast_increase_button":
                    ("volume_start", VOLUME_FAST_STEP),
                "volume_end_faster_decrease_button":
                    ("volume_end", -VOLUME_FASTER_STEP),
                "volume_end_fast_decrease_button":
                    ("volume_end", -VOLUME_FAST_STEP),
                "volume_end_faster_increase_button":
                    ("volume_end", VOLUME_FASTER_STEP),
                "volume_end_fast_increase_button":
                    ("volume_end", VOLUME_FAST_STEP),
                "duration_faster_decrease_button":
                    ("duration", -DURATION_FASTER_STEP),
                "duration_fast_decrease_button":
                    ("duration", -DURATION_FAST_STEP),
                "duration_faster_increase_button":
                    ("duration", DURATION_FASTER_STEP),
                "duration_fast_increase_button":
                    ("duration", DURATION_FAST_STEP),
            }

            if widget_id not in delta_map:
                raise ValueError(f"Unknown widget_id found: {widget_id}")

            target, delta = delta_map[widget_id]

            match target:
                case "volume_start":
                    new_value = min(
                        max(0, self.model.btrvol.volume_start + delta), 100)
                    self.model.btrvol.volume_start = new_value
                case "volume_end":
                    new_value = min(
                        max(0, self.model.btrvol.volume_end + delta), 100)
                    self.model.btrvol.volume_end = new_value
                case "duration":
                    new_value = max(1, self.model.btrvol.duration + delta)
                    self.model.btrvol.duration = new_value
            self.on_configuration_change()

        def on_start_button_clicked(self):
            """on_start_button_clicked"""
            logger.debug("Start button clicked, is running: %r.", self.running)

            if self.running:
                self.continuous_volume_control_event.set()
                if self.continuous_volume_control_thread.is_alive():
                    self.continuous_volume_control_thread.join(0)

                self.on_continuous_volume_control_end()
            else:
                self.on_continuous_volume_control_start()

                self.continuous_volume_control_thread = \
                    Thread(
                        target=self.continuous_volume_control,
                        args=(
                            self.model.btrvol.volume_levels,
                            self.model.btrvol.time_points,
                            self.model.btrvol.time_intervals,
                        ),
                        daemon=True
                    )
                self.continuous_volume_control_event.clear()
                self.continuous_volume_control_thread.start()

        def on_save_button_clicked(self):
            """on_save_button_clicked"""
            self.model.save()

        def on_load_button_clicked(self) -> None:
            """on_load_button_clicked"""
            self.model.load()
            self.on_configuration_change()
            self.view.change_theme(self.model.theme)

        def on_post_action_enable_checkbutton_toggle(self) -> None:
            """on_post_action_enable_checkbutton_toggle"""
            self.model.post_action.enable = \
                self.view.post_action_enable_checkbutton_value.get()
            self.on_configuration_change()

        def on_post_action_combobox_selected(self, _event: Any) -> None:
            """on_post_action_combobox_selected"""
            self.model.post_action.action = PostAction.Action[
                self.view.post_action_combobox_value.get()]
            self.on_configuration_change()

        def on_post_action_delay_spinbox_changed(self) -> None:
            """on_post_action_delay_spinbox_changed"""
            self.model.post_action.delay = \
                self.view.post_action_delay_value.get()
            self.on_configuration_change()

        def on_post_action_delay_spinbox_text_changed(self, _event: tk.Event):
            """on_post_action_delay_spinbox_text_changed"""
            self.on_post_action_delay_spinbox_changed()

        def on_post_action_test_button_clicked(self) -> None:
            """on_post_action_test_button_clicked"""
            self.execute_post_action()

        def post_action_delay_value_validate(self, p_entry_value: str) -> bool:
            """Validate post action delay spinbox input."""
            try:
                val = int(p_entry_value)
                return 0 <= val
            except ValueError:
                return False

        def execute_post_action(self) -> None:
            """execute_post_action"""
            match self.model.post_action.action:
                case PostAction.Action.PLAY_PAUSE:
                    logger.info("Post action: Play/Pause.")
                    keyboard.send("play/pause media")
                case PostAction.Action.STOP:
                    logger.info("Post action: Stop.")
                    keyboard.send("stop media")

        def continuous_volume_control(
            self, volume_levels: list[int], time_points: list[float],
            intervals: list[float]
        ):
            """continuous_volume_control"""
            volume: int
            interval: float
            # last_stat: tuple[bool, float] | None = None

            logger.info("Continuous volume control begins")
            logger.debug("Current configuration: %r",
                         self.model.btrvol.config.serialize())

            for volume, time_point, interval in zip(
                volume_levels, time_points, intervals
            ):
                logger.info(
                    "Next adjustment volume to %3d in %0.4f second...",
                    volume, interval
                )
                if self.continuous_volume_control_event.wait(interval):
                    logger.info("Continuous volume control interrupted.")
                    break

                # current_stat: tuple[bool, float] = (
                #     bool(self.volume_control.get_mute()),
                #     float(self.volume_control.get_volume())
                # )
                # if (
                #     self.running
                #     and (last_stat is not None)
                #     and (last_stat != current_stat)
                # ):
                #     logger.warning("Last status: %r, current status: %r.",
                #                    last_stat, current_stat)
                #     print("System volume status changed, break.")
                #     break

                self.volume_control.set_mute(False)
                self.volume_control.set_volume(volume / 100)
                # last_stat = (
                #     bool(self.volume_control.mute),
                #     float(self.volume_control.volume)
                # )
                self.view.progressbar["maximum"] = self.model.btrvol.duration
                self.view.progressbar["value"] = time_point

            if self.model.post_action.enable:
                logger.info(
                    "Waiting for %d seconds before executing post action...",
                    self.model.post_action.delay
                )
                for tick in range(self.model.post_action.delay):
                    if self.continuous_volume_control_event.wait(tick):
                        logger.info("Post action interrupted.")
                        break
                    self.view.progressbar["maximum"] = \
                        self.model.post_action.delay
                    self.view.progressbar["value"] = tick
                else:
                    self.execute_post_action()

            self.on_continuous_volume_control_end()
            logger.info("Continuous volume control finished.")

        def on_continuous_volume_control_start(self):
            """on_continuous_volume_control_start"""
            self.running = True
            self.view.set_widgets_state(False)
            self.view.start_button["text"] = "End"

        def on_continuous_volume_control_end(self):
            """on_continuous_volume_control_end"""
            self.running = False
            self.view.set_widgets_state(True)
            self.view.start_button["text"] = "Start"

    class View:
        themes: tuple[str, ...]
        root: tk.Tk

        def __init__(self) -> None:
            self.builder = pygubu.Builder()
            with as_file(PROJECT_PATH) as PROJECT_PATH_PATH:
                logger.debug(
                    "Loading resource path from %s.", PROJECT_PATH_PATH)
                self.builder.add_resource_path(str(PROJECT_PATH_PATH))

            with as_file(PROJECT_UI) as PROJECT_UI_PATH:
                logger.debug("Loading UI file from %s.", PROJECT_UI_PATH)
                self.builder.add_from_file(str(PROJECT_UI_PATH))

            if sys.platform == "win32":
                app_id = "BtrVol.GUI.App"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    app_id
                )

            self.root = self.builder.get_object("mainwindow")
            self.style = AwthemesStyle(self.root)
            self.themes = self.style.theme_names()
            with as_file(ICON_FILE) as ICON_FILE_PATH:
                self.root.iconbitmap(default=str(ICON_FILE_PATH))

            # Tkinter Widgets
            self.chart: ChartCanvas = \
                self.builder.get_object("formula_canvas", self.root)
            self.chart.x_label = "Duration"
            self.chart.y_label = "Volume"
            self.start_button = self.builder.get_object("start_button")
            self.progressbar = self.builder.get_object("progressbar")

            self.theme_selector: ttk.Combobox = \
                self.builder.get_object("theme_selector_combobox")
            self.theme_selector["values"] = self.themes

            self.post_action_combobox = \
                self.builder.get_object("post_action_combobox")
            self.post_action_combobox["values"] = [
                action.name for action in PostAction.Action
            ]

            # Tkinter Variables
            self.volume_start_scale_value: tk.IntVar
            self.volume_start_value_label_value: tk.IntVar
            self.volume_end_scale_value: tk.IntVar
            self.volume_end_value_label_value: tk.IntVar
            self.duration_spinbox_value: tk.IntVar
            self.duration_value_label_value: tk.StringVar
            self.tone_value: tk.StringVar
            self.version_label_value: tk.StringVar
            self.status_label_value: tk.StringVar
            self.theme_selector_combobox_value: tk.StringVar
            self.post_action_enable_checkbutton_value: tk.BooleanVar
            self.post_action_combobox_value: tk.StringVar
            self.post_action_delay_value: tk.IntVar
            self.post_action_delay_value_label_value: tk.StringVar

            self.builder.import_variables(self)

            self.version_label_value.set(__version__)

            logger.addHandler(
                TkStringVarHandler(self.status_label_value, logging.INFO))

        def change_theme(self, theme_name: str) -> None:
            """Change the theme of the application."""
            if theme_name not in self.themes:
                raise ValueError(f"Unknown theme name: {theme_name}")
            self.style.theme_use(theme_name)
            self.theme_selector_combobox_value.set(theme_name)
            self.root.after_idle(
                lambda: self.root.event_generate("<<ThemeChanged>>"))

        def set_callbacks(self, callbacks: dict[str, Callable]) -> None:
            self.builder.connect_callbacks(callbacks)

        def set_widgets_state(self, state: bool) -> None:
            """Set state for widgets."""

            normal_widget_ids: list[str] = [
                "volume_start_faster_decrease_button",
                "volume_start_fast_decrease_button",
                "volume_start_scale",
                "volume_start_fast_increase_button",
                "volume_start_faster_increase_button",
                "volume_end_faster_decrease_button",
                "volume_end_fast_decrease_button",
                "volume_end_scale",
                "volume_end_fast_increase_button",
                "volume_end_faster_increase_button",
                "duration_faster_decrease_button",
                "duration_fast_decrease_button",
                "duration_spinbox",
                "duration_fast_increase_button",
                "duration_faster_increase_button",
                "tone_1_radiobutton",
                "tone_2_radiobutton",
                "tone_3_radiobutton",
                "tone_4_radiobutton",
                "load_button",
                "save_button",
                "post_action_enable_checkbutton",
                "post_action_delay_spinbox",
            ]

            readonly_widget_ids: list[str] = [
                "post_action_combobox",
            ]

            match state:
                case True:
                    for widget_id in normal_widget_ids:
                        widget = self.builder.get_object(widget_id)
                        widget["state"] = tk.NORMAL
                    for readonly_widget_id in readonly_widget_ids:
                        widget = self.builder.get_object(readonly_widget_id)
                        widget["state"] = "readonly"
                case False:
                    for widget_id in normal_widget_ids + readonly_widget_ids:
                        widget = self.builder.get_object(widget_id)
                        widget["state"] = tk.DISABLED
                case _:
                    raise ValueError(f"Unknown state: {state}")

        def mainloop(self):
            self.root.mainloop()

    def run(self):
        self.view.mainloop()


def main():
    """Main entry point for the GUI application."""
    app = MainApp()
    app.run()


if __name__ == "__main__":
    main()

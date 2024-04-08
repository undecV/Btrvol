#!python -m btrvol.btrvolgui


"""GUI of Btrvol."""


import sys
import tkinter as tk
import pickle
import logging
from typing import Any
from threading import Thread, Event
from pathlib import Path

import pygubu  # type: ignore
from rich.logging import RichHandler

from btrvol import __version__
from btrvol.btrvollib.configuration import BtrvolConfiguration
from btrvol.btrvollib.utilities import Inset, in_closed_range
from btrvol.btrvollib.volume_control import VolumeControl
from btrvol.btrvollib.selectors import BtrvolTone
from btrvol.btrvollib.btrvol import btrvol

logging.basicConfig(format="%(message)s", handlers=[RichHandler(),])
log = logging.getLogger()
log.setLevel(logging.DEBUG)


PROJECT_PATH = Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "btrvolgui.ui"
ICON_FILE = PROJECT_PATH / "resources" / "icon.16.ico"
IMAGE_FILE = PROJECT_PATH / "resources" / "icon.png"


VOLUME_FAST_STEP = 5
VOLUME_FASTER_STEP = 10
DURATION_FAST_STEP = 30
DURATION_FASTER_STEP = 60


if getattr(sys, 'frozen', False):
    application_folder = Path(sys.executable).parent
elif __file__:
    application_folder = Path(__file__).parent

CONFIG_FILE_PATH = application_folder / "config.pkl"


class MainApp:
    """GUI of Btrvol."""

    def __init__(self, master: Any | None = None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = self.builder.get_object("mainwindow", master)
        self.mainwindow.iconbitmap(ICON_FILE)

        self.volume_control = VolumeControl()
        self.continuous_volume_control_thread: Thread | None = None
        self.continuous_volume_control_event: Event = Event()
        self.running: bool = False

        self.canva = self.builder.get_object("formula_canva")
        self.canva_size: tuple[int, int] = (0, 0)

        self.volume_start_scale_value: tk.DoubleVar
        self.volume_start_value_label_value: tk.IntVar
        self.volume_end_scale_value: tk.DoubleVar
        self.volume_end_value_label_value: tk.IntVar
        self.duration_spinbox_value: tk.IntVar
        self.tone_value: tk.IntVar
        self.version_label_value: tk.StringVar

        self.start_button = self.builder.get_object("start_button")
        self.progressbar = self.builder.get_object("progressbar")

        self.builder.import_variables(self)
        self.builder.connect_callbacks(self)

        self.version_label_value.set(__version__)

        # Load default configuration
        self.configuration = BtrvolConfiguration()
        self.load_configuration()
        self.on_configuration_change()

    def run(self):
        """Start the gui main loop."""
        log.debug("Main loop start.")
        self.mainwindow.mainloop()

    def on_canva_resize(self, event: tk.Event):
        """on_canva_resize"""
        self.canva_size = (event.width, event.height)
        self.formula_draw()

    def formula_draw(self):
        """Draw the figure."""
        self.canva.delete("all")
        width, height = self.canva_size
        padding = Inset(10, 20, 20, 30)

        self.canva.create_rectangle(padding.left, padding.top, width - padding.right, height - padding.bottom, width=2)
        self.canva.create_text(padding.left // 2, padding.top, {"text": "100"})
        self.canva.create_text(padding.left // 2, padding.top + ((height - padding.bottom) // 2),
                               text="Volume", angle=90)
        self.canva.create_text(padding.left // 2, height - padding.bottom, {"text": "0"})
        self.canva.create_text(padding.left, height - (padding.bottom // 2), {"text": "0"})
        self.canva.create_text(padding.left + ((width - padding.right) // 2), height - (padding.bottom // 2),
                               text="Duration")
        self.canva.create_text(width - padding.right, height - (padding.bottom // 2),
                               {"text": str(self.configuration.duration)})

        volumes, time_points, _, _ = btrvol(self.configuration)

        x_scale = (width - padding.left - padding.right) / self.configuration.duration
        y_scale = (height - padding.top - padding.bottom) / 100
        for i in range(len(volumes)-1):
            x1 = padding.left + int(time_points[i] * x_scale)
            y1 = height - padding.bottom - int(volumes[i] * y_scale)
            x2 = padding.left + int(time_points[i+1] * x_scale)
            y2 = height - padding.bottom - int(volumes[i] * y_scale)
            self.canva.create_line(x1, y1, x2, y2, width=1)

    def on_configuration_change(self):
        """Update UI Widgets when values update."""
        log.debug("Confifuration changed: %r", self.configuration)
        self.volume_start_scale_value.set(self.configuration.volume_start)
        self.volume_start_value_label_value.set(self.configuration.volume_start)
        self.volume_end_scale_value.set(self.configuration.volume_end)
        self.volume_end_value_label_value.set(self.configuration.volume_end)
        self.duration_spinbox_value.set(self.configuration.duration)
        self.tone_value.set(self.enum_to_tone_value[self.configuration.tone])
        self.formula_draw()

    def duration_spinbox_validate(self, p_entry_value):
        """Validator for duration."""
        try:
            assert in_closed_range(p_entry_value, BtrvolConfiguration.duration_range)
        except (ValueError, AssertionError):
            return False
        return True

    tone_value_to_enum: dict[int, BtrvolTone] = {
        1: BtrvolTone.LINEAR,
        2: BtrvolTone.SMOOTH,
        3: BtrvolTone.GRADUAL,
        4: BtrvolTone.RAPID,
    }
    enum_to_tone_value: dict[BtrvolTone, int] = {v: k for k, v in tone_value_to_enum.items()}

    def on_volume_start_scale_changed(self, scale_value):
        """on_volume_start_scale_changed"""
        self.configuration.volume_start = round(float(scale_value))
        self.on_configuration_change()

    def on_volume_end_scale_changed(self, scale_value):
        """on_volume_end_scale_changed"""
        self.configuration.volume_end = round(float(scale_value))
        self.on_configuration_change()

    def on_duration_text_changed(self, event: tk.Event):
        """on_duration_text_changed"""
        _ = event
        self.on_duration_changed()

    def on_duration_changed(self):
        """on_duration_changed"""
        self.configuration.duration = self.duration_spinbox_value.get()
        self.on_configuration_change()

    def on_tone_radiobutton_clicked(self, widget_id: str):
        """on_tone_radiobutton_clicked"""
        _ = widget_id
        value = self.tone_value.get()
        tone = self.tone_value_to_enum[value]
        log.debug("on_tone_radiobutton_clicked: %r -> %r", value, tone)
        self.configuration.tone = tone
        self.on_configuration_change()

    def on_faster_change_value_clicked(self, widget_id: str):
        """on_faster_change_value_clicked"""
        match widget_id:
            case "volume_start_faster_decrease_button":
                self.configuration.volume_start -= VOLUME_FASTER_STEP
            case "volume_start_fast_decrease_button":
                self.configuration.volume_start -= VOLUME_FAST_STEP
            case "volume_start_faster_increase_button":
                self.configuration.volume_start += VOLUME_FASTER_STEP
            case "volume_start_fast_increase_button":
                self.configuration.volume_start += VOLUME_FAST_STEP
            case "volume_end_faster_decrease_button":
                self.configuration.volume_end -= VOLUME_FASTER_STEP
            case "volume_end_fast_decrease_button":
                self.configuration.volume_end -= VOLUME_FAST_STEP
            case "volume_end_faster_increase_button":
                self.configuration.volume_end += VOLUME_FASTER_STEP
            case "volume_end_fast_increase_button":
                self.configuration.volume_end += VOLUME_FAST_STEP
            case "duration_faster_decrease_button":
                self.configuration.duration -= DURATION_FASTER_STEP
            case "duration_fast_decrease_button":
                self.configuration.duration -= DURATION_FAST_STEP
            case "duration_faster_increase_button":
                self.configuration.duration += DURATION_FASTER_STEP
            case "duration_fast_increase_button":
                self.configuration.duration += DURATION_FAST_STEP
            case _:
                raise ValueError(f"Unkown widget_id find: {widget_id}")
        self.on_configuration_change()

    def set_wdigets_state(self, state: str = tk.NORMAL):
        """Set state for wdigets."""
        assert state in (tk.NORMAL, tk.DISABLED)
        wdiget_ids: list[str] = [
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
            "load_button", "save_button"
        ]  # Wdigets that need to be disabled when running.
        for wdiget_id in wdiget_ids:
            wdiget = self.builder.get_object(wdiget_id)
            wdiget["state"] = state

    def on_start_button_clicked(self):
        """on_start_button_clicked"""
        log.debug("continuous_volume_control begins, current configuration: %r", self.configuration)

        if self.running:
            self.continuous_volume_control_event.set()
            if self.continuous_volume_control_thread.is_alive():
                self.continuous_volume_control_thread.join(0)

            self.on_continuous_volume_control_end()
        else:
            self.on_continuous_volume_control_start()

            volumes, time_points, intervals, _ = btrvol(self.configuration)
            self.continuous_volume_control_thread = \
                Thread(target=self.continuous_volume_control, args=(volumes, time_points, intervals), daemon=True)
            self.continuous_volume_control_event.clear()
            self.continuous_volume_control_thread.start()

    def on_continuous_volume_control_start(self):
        """on_continuous_volume_control_start"""
        self.running = True
        self.set_wdigets_state(tk.DISABLED)
        self.start_button["text"] = "End"

    def on_continuous_volume_control_end(self):
        """on_continuous_volume_control_end"""
        self.running = False
        self.set_wdigets_state(tk.NORMAL)
        self.start_button["text"] = "Start"

    def continuous_volume_control(self, volumes: list[int], time_points: list[float], intervals: list[float]):
        """continuous_volume_control"""
        volume: int
        interval: float
        # last_stat: tuple[bool, float] | None = None
        for volume, time_point, interval in zip(volumes, time_points, intervals):
            message = f"Next adjustment volume to {volume} in {interval:0.4f} second..."
            log.info(message)
            if self.continuous_volume_control_event.wait(interval):
                log.info("Got break event.")
                break
            # current_stat: tuple[bool, float] = (bool(self.volume_control.mute), float(self.volume_control.volume))
            # if self.running and (last_stat is not None) and (last_stat != current_stat):
            #     log.warning("Last status: %r, current status: %r.", last_stat, current_stat)
            #     print("System volume status changed, break.")
            #     break
            self.volume_control.mute = False
            self.volume_control.volume = volume / 100
            # last_stat = (bool(self.volume_control.mute), float(self.volume_control.volume))

            self.progressbar["maximum"] = self.configuration.duration
            self.progressbar["value"] = time_point

        self.on_continuous_volume_control_end()
        log.debug("End of continuous volume control.")
        return None

    def on_save_button_clicked(self):
        """on_save_button_clicked"""
        self.save_configuration()

    def on_load_button_clicked(self) -> None:
        """on_load_button_clicked"""
        self.load_configuration()

    def save_configuration(self) -> None:
        """Save configuration to a file."""
        pickle.dump(self.configuration, CONFIG_FILE_PATH.open("wb"))

    def load_configuration(self) -> None:
        """Load configuration from a file."""
        config: BtrvolConfiguration
        try:
            config = pickle.load(CONFIG_FILE_PATH.open("rb"))
            assert isinstance(config, BtrvolConfiguration)
            self.configuration = config
            self.on_configuration_change()
        except Exception:  # pylint: disable=broad-exception-caught
            log.error("Can not read the config file.")


if __name__ == "__main__":
    app = MainApp()
    app.run()

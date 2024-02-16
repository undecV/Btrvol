"""GUI of Btrvol."""

import sys
import tkinter as tk
# import tkinter.ttk as ttk
import pickle
import logging
from typing import Any
from threading import Thread, Event
from pathlib import Path

import pygubu
from rich.logging import RichHandler
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from btrvollib.volume_control import VolumeControl
from btrvollib.selectors import BtrvolTone
from btrvollib.btrvol import btrvol

logging.basicConfig(format="%(message)s", handlers=[RichHandler(),])
log = logging.getLogger()
log.setLevel(logging.DEBUG)


PROJECT_PATH = Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "btrvolgui.ui"
ICON_FILE = PROJECT_PATH / "resources" / "icon.16.ico"

MINIMUM_VOLUME: int = 0
MAXIMUM_VOLUME: int = 100
MINIMUM_DURATION: int = 1
MAXIMUM_DURATION: int = 86400
VOLUME_FAST_STEP = 5
VOLUME_FASTER_STEP = 10
DURATION_FAST_STEP = 30
DURATION_FASTER_STEP = 60


if getattr(sys, 'frozen', False):
    application_path = Path(sys.executable).parent
elif __file__:
    application_path = Path(__file__).parent

CONFIG_FILE_PATH = application_path / "config.pkl"


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
        self._volume_start: int = 0
        self._volume_end: int = 0
        self._duration: int = 1
        self._tone: BtrvolTone = BtrvolTone.LINEAR

        self.fig = Figure(figsize=(1, 1))
        matplotlib.rc('xtick', labelsize=8)
        matplotlib.rc('ytick', labelsize=8)
        self.axs = self.fig.add_subplot(111)
        self.formula_frame = self.builder.get_object("formula_frame")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.formula_frame)
        self.canvas.get_tk_widget().pack(expand=tk.TRUE, fill=tk.BOTH)

        self.volume_start_scale_value: tk.DoubleVar
        self.volume_start_value_label_value: tk.IntVar
        self.volume_end_scale_value: tk.DoubleVar
        self.volume_end_value_label_value: tk.IntVar
        self.duration_spinbox_value: tk.IntVar
        self.tone_value: tk.IntVar

        self.start_button = self.builder.get_object("start_button")
        self.progressbar = self.builder.get_object("progressbar")

        self.builder.import_variables(self)
        self.builder.connect_callbacks(self)

    def run(self):
        """Start the gui main loop."""
        self.initial_config()
        self.mainwindow.mainloop()

    def formula_draw(self):
        """Draw the figure."""
        log.debug(self.get_config())
        volumes, time_points, _, _ = btrvol(self.volume_start, self.volume_end, self.duration, self.tone)
        self.axs.clear()
        self.axs.plot(time_points, volumes)
        self.axs.set_xlim(0, self.duration)
        self.axs.set_ylim(MINIMUM_VOLUME, MAXIMUM_VOLUME)
        self.axs.grid()
        self.canvas.draw()

    @property
    def volume_start(self) -> int:
        """Volume adjustment start value, between [0, 1]."""
        return self._volume_start

    @volume_start.setter
    def volume_start(self, value: int):
        value = max(MINIMUM_VOLUME, min(value, MAXIMUM_VOLUME))
        self._volume_start = value
        self.volume_start_scale_value.set(value)
        self.volume_start_value_label_value.set(value)
        self.formula_draw()

    @property
    def volume_end(self) -> int:
        """Volume adjustment end value, between [0, 1]."""
        return self._volume_end

    @volume_end.setter
    def volume_end(self, value: int):
        value = max(MINIMUM_VOLUME, min(value, MAXIMUM_VOLUME))
        self._volume_end = value
        self.volume_end_scale_value.set(value)
        self.volume_end_value_label_value.set(value)
        self.formula_draw()

    @property
    def duration(self) -> int:
        """Volume adjustment duration."""
        return self._duration

    @duration.setter
    def duration(self, value: int):
        value = max(MINIMUM_DURATION, min(value, MAXIMUM_DURATION))
        self._duration = value
        self.duration_spinbox_value.set(value)
        self.formula_draw()

    def duration_spinbox_validate(self, p_entry_value):
        """Validator for duration."""
        try:
            assert MINIMUM_DURATION <= int(p_entry_value) <= MAXIMUM_DURATION
        except (ValueError, AssertionError):
            return False
        return True

    @property
    def tone(self) -> BtrvolTone:
        """Volume adjustment tone."""
        return self._tone

    @tone.setter
    def tone(self, value: BtrvolTone):
        self._tone = value
        self.tone_value.set(self.enum_to_tone_value[value])
        self.formula_draw()

    tone_value_to_enum: dict[int, BtrvolTone] = {
        1: BtrvolTone.LINEAR,
        2: BtrvolTone.SMOOTH,
        3: BtrvolTone.GRADUAL,
        4: BtrvolTone.RAPID,
    }
    enum_to_tone_value: dict[BtrvolTone, int] = {v: k for k, v in tone_value_to_enum.items()}

    def on_volume_start_scale_changed(self, scale_value):
        """on_volume_start_scale_changed"""
        self.volume_start = round(float(scale_value))

    def on_volume_end_scale_changed(self, scale_value):
        """on_volume_end_scale_changed"""
        self.volume_end = round(float(scale_value))

    def on_duration_changed(self):
        """on_duration_changed"""
        log.debug(self.duration_spinbox_value.get())
        self.duration = self.duration_spinbox_value.get()

    def on_tone_radiobutton_clicked(self, widget_id: str):
        """on_tone_radiobutton_clicked"""
        _ = widget_id
        log.debug("on_tone_radiobutton_clicked: %r", self.tone_value.get())
        self.tone = self.tone_value_to_enum[self.tone_value.get()]

    def on_faster_change_value_clicked(self, widget_id: str):
        """on_faster_change_value_clicked"""
        match widget_id:
            case "volume_start_faster_decrease_button":
                self.volume_start -= VOLUME_FASTER_STEP
            case "volume_start_fast_decrease_button":
                self.volume_start -= VOLUME_FAST_STEP
            case "volume_start_faster_increase_button":
                self.volume_start += VOLUME_FASTER_STEP
            case "volume_start_fast_increase_button":
                self.volume_start += VOLUME_FAST_STEP
            case "volume_end_faster_decrease_button":
                self.volume_end -= VOLUME_FASTER_STEP
            case "volume_end_fast_decrease_button":
                self.volume_end -= VOLUME_FAST_STEP
            case "volume_end_faster_increase_button":
                self.volume_end += VOLUME_FASTER_STEP
            case "volume_end_fast_increase_button":
                self.volume_end += VOLUME_FAST_STEP
            case "duration_faster_decrease_button":
                self.duration -= DURATION_FASTER_STEP
            case "duration_fast_decrease_button":
                self.duration -= DURATION_FAST_STEP
            case "duration_faster_increase_button":
                self.duration += DURATION_FASTER_STEP
            case "duration_fast_increase_button":
                self.duration += DURATION_FAST_STEP
            case _:
                log.debug(widget_id)

    def get_config(self) -> dict[str, Any]:
        """Collect the config."""
        config: dict[str, Any] = {
            "start": self.volume_start,
            "end": self.volume_end,
            "duration": self.duration,
            "tone": self.tone,
        }
        return config

    def initial_config(self, config: dict[str, Any] | None = None):
        """Load config safily."""
        self.volume_start = 20 if not config else config["start"]
        self.volume_end = 50 if not config else config["end"]
        self.duration = 10 if not config else config["duration"]
        self.tone = BtrvolTone.SMOOTH if not config else config["tone"]

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
        ]
        for wdiget_id in wdiget_ids:
            wdiget = self.builder.get_object(wdiget_id)
            wdiget["state"] = state

    def on_start_button_clicked(self):
        """on_start_button_clicked"""
        log.debug("%r", self.get_config())

        if self.running:
            self.continuous_volume_control_event.set()
            if self.continuous_volume_control_thread.is_alive():
                self.continuous_volume_control_thread.join(0)

            self.on_continuous_volume_control_end()
        else:
            self.on_continuous_volume_control_start()

            volumes, time_points, intervals, _ = btrvol(self.volume_start, self.volume_end, self.duration, self.tone)
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
        last_stat: tuple[bool, float] | None = None
        for volume, time_point, interval in zip(volumes, time_points, intervals):
            message = f"Next adjustment volume to {volume} in {interval:0.4f} second..."
            log.info(message)
            if self.continuous_volume_control_event.wait(interval):
                log.info("Got break event.")
                break
            current_stat: tuple[bool, float] = (self.volume_control.mute, self.volume_control.volume)
            if self.running and (last_stat is not None) and (last_stat != current_stat):
                log.warning("Last status: %r, current status: %r.", last_stat, current_stat)
                print("System volume status changed, break.")
                break
            self.volume_control.mute = False
            self.volume_control.volume = volume / 100
            last_stat = (self.volume_control.mute, self.volume_control.volume)

            self.progressbar["maximum"] = self.duration
            self.progressbar["value"] = time_point

        self.on_continuous_volume_control_end()
        log.debug("End of continuous volume control.")
        return None

    def on_save_button_clicked(self):
        """on_save_button_clicked"""
        config = self.get_config()
        pickle.dump(config, CONFIG_FILE_PATH.open("wb"))

    def on_load_button_clicked(self) -> None:
        """on_load_button_clicked"""
        config: dict[str, Any] | None = None
        try:
            config = pickle.load(CONFIG_FILE_PATH.open("rb"))
        except Exception:  # pylint: disable=broad-exception-caught
            log.error("Can not read the config file.")
        self.initial_config(config)

    def on_duration_text_changed(self, event: tk.Event):
        """on_duration_text_changed"""
        _ = event
        self.on_duration_changed()


if __name__ == "__main__":
    app = MainApp()
    app.run()

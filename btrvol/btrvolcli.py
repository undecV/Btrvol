import time
import logging

import click
from rich.logging import RichHandler

from btrvol.btrvollib.btrvol import btrvol
from btrvol.btrvollib.selectors import BtrvolTone, BtrvolMode
from btrvol.btrvollib.volume_control import VolumeControl


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=[RichHandler(),])
log = logging.getLogger()


MINIMIUM_INTERVAL: float = 0.1


@click.command()
@click.argument("start", type=click.IntRange(0, 100, False, False, clamp=True))
@click.argument("end", type=click.IntRange(0, 100, False, False, clamp=True))
@click.argument("duration", type=click.IntRange(1, clamp=True))
@click.argument("method", type=click.Choice(BtrvolTone.__members__, case_sensitive=False),
                callback=lambda c, p, v: getattr(BtrvolTone, v) if v else None,
                default=BtrvolTone.LINEAR.name)
@click.option("-v", "--verbose", "verbose", count=True)
def cli(start: int, end: int, duration: int, method: BtrvolTone, verbose: int):
    """Command line interface."""
    match verbose:
        case 0:
            log.setLevel(logging.WARNING)
        case 1:
            log.setLevel(logging.INFO)
        case 2:
            log.setLevel(logging.DEBUG)

    log.debug("Argument `start` = %d", start)
    log.debug("Argument `end` = %d", end)
    log.debug("Argument `duration` = %d", duration)
    log.debug("Argument `method` = %r", method)
    log.debug("Argument `verbose` = %r", verbose)

    timer: zip
    mode: BtrvolMode
    volumes, time_points, intervals, mode = btrvol(start, end, duration, method, MINIMIUM_INTERVAL)
    print(f"Mode: {mode.name}")

    volume_control = VolumeControl()
    last_stat: tuple[bool, float] | None = None

    volume: int
    interval: float
    for volume, interval in zip(volumes, intervals):
        print(f"Next adjustment volume to {volume} in {interval:0.4f} second...")
        time.sleep(interval)
        current_stat: tuple[bool, float] = (volume_control.mute, volume_control.volume)
        if (last_stat is not None) and (last_stat != current_stat):
            log.warning("Last status: %r, current status: %r.", last_stat, current_stat)
            print("System volume status changed, break.")
            break
        volume_control.mute = False
        volume_control.volume = volume / 100
        last_stat = (volume_control.mute, volume_control.volume)


if __name__ == "__main__":
    cli.main()

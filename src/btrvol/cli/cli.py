import logging
import time
import click
from btrvol.core.btrvol import BtrVol
from btrvol.core.volume_control import VolumeControl


logger = logging.getLogger(__name__)


def setup_logging(verbose: int = 0) -> None:
    """Configure logger.
    """
    root = logging.getLogger()
    # determine level from verbosity
    level: int = logging.WARNING
    match verbose:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG
    root.setLevel(level)


@click.command()
@click.argument("start", type=click.IntRange(0, 100, False, False, clamp=True))
@click.argument("end", type=click.IntRange(0, 100, False, False, clamp=True))
@click.argument("duration", type=click.IntRange(1, clamp=True))
@click.argument("method",
                type=click.Choice(BtrVol.Tone, case_sensitive=False),
                default=BtrVol.Tone.LINEAR)
@click.option("--verbose", "-v", count=True, help="Enable verbose output")
def main(start: int, end: int, duration: int, method: BtrVol.Tone,
         verbose: int) -> None:
    """A CLI for BtrVol library."""
    setup_logging(verbose)
    logger.debug("Args: start=%d, end=%d, duration=%d, method=%s, verbose=%d",
                 start, end, duration, method, verbose)

    volume_control = VolumeControl()
    btrvol = BtrVol(start, end, duration, method)

    print(f"Changing volume from {start} to {end} over {duration} "
          f"seconds using {method} method with {btrvol.mode} mode.")

    for volume, interval, time_point in zip(btrvol.volume_levels,
                                            btrvol.time_intervals,
                                            btrvol.time_points):
        print(f"Setting volume to {volume:3d} at {time_point:10.2f} "
              f"after {interval:10.2f} seconds...")
        time.sleep(interval)
        volume_control.set_volume(volume / 100)


if __name__ == "__main__":
    main.main()

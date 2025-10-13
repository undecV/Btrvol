# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from fractions import Fraction
import logging
import unittest
from itertools import product

from btrvol_lib.btrvol import BtrVol


logger = logging.getLogger(__name__)


class TestBtrVol(unittest.TestCase):
    def test_initialization(self):
        volume_start = 20
        volume_end = 80
        duration = 3600  # 1 hour
        tone = BtrVol.Tone.SMOOTH
        minimum_interval_threshold = Fraction(1, 10)

        btrvol = BtrVol(
            start=volume_start, end=volume_end, duration=duration,
            tone=tone, minimum_interval_threshold=minimum_interval_threshold
        )

        self.assertEqual(btrvol.volume_start, volume_start)
        self.assertEqual(btrvol.volume_end, volume_end)
        self.assertEqual(btrvol.duration, duration)
        self.assertEqual(btrvol.tone, tone)
        self.assertEqual(btrvol.minimum_interval_threshold,
                         minimum_interval_threshold)
        self.assertIsInstance(btrvol.volume_levels, list)
        self.assertIsInstance(btrvol.time_points, list)
        self.assertIsInstance(btrvol.time_intervals, list)
        self.assertIn(btrvol.mode, (BtrVol.Mode.TIME, BtrVol.Mode.INTERVAL))
        self.assertEqual(len(btrvol.volume_levels), len(btrvol.time_intervals))
        self.assertEqual(len(btrvol.volume_levels), len(btrvol.time_points))

    def test_increasing_time_mode(self):
        volume_start = 20
        volume_end = 80
        duration = 3600  # 1 hour

        btrvol = BtrVol(
            start=volume_start, end=volume_end, duration=duration,
            tone=BtrVol.Tone.SMOOTH
        )
        print(btrvol.volume_levels)
        print(btrvol.time_points)
        print(btrvol.time_intervals)
        self.assertEqual(btrvol.minimum_interval_threshold, Fraction(1, 10))
        self.assertEqual(btrvol.volume_levels[0], volume_start)
        self.assertEqual(btrvol.volume_levels[-1], volume_end)
        self.assertEqual(btrvol.time_points[0], 0.0)
        self.assertEqual(btrvol.time_points[-1], duration)

    def test_increasing_interval_mode(self):
        volume_start = 20
        volume_end = 80
        duration = 1  # Very short duration to force interval mode
        minimum_interval_threshold = 0.1
        btrvol = BtrVol(
            start=volume_start, end=volume_end, duration=duration,
            tone=BtrVol.Tone.SMOOTH,
            minimum_interval_threshold=minimum_interval_threshold
        )
        print(btrvol.volume_levels)
        print(btrvol.time_points)
        print(btrvol.time_intervals)
        self.assertEqual(btrvol.mode, BtrVol.Mode.INTERVAL)
        self.assertEqual(btrvol.volume_levels[0], volume_start)
        self.assertEqual(btrvol.volume_levels[-1], volume_end)
        self.assertEqual(btrvol.time_points[0], 0.0)
        self.assertEqual(btrvol.time_points[-1], duration)
        # self.assertTrue(all(interval >= minimum_interval_threshold
        #                     for interval in btrvol.time_intervals[1:]))

    def test_decreasing_volume(self):
        start_volume = 80
        end_volume = 20
        duration = 3600  # 1 hour
        btrvol = BtrVol(
            start=start_volume, end=end_volume, duration=duration,
            tone=BtrVol.Tone.SMOOTH
        )
        self.assertEqual(btrvol.volume_levels[0], start_volume)
        self.assertEqual(btrvol.volume_levels[-1], end_volume)
        self.assertEqual(btrvol.time_points[0], 0.0)
        self.assertEqual(btrvol.time_points[-1], duration)
        self.assertEqual(btrvol.mode, BtrVol.Mode.TIME)

    def test_decreasing_interval_mode(self):
        start_volume = 80
        end_volume = 20
        duration = 1  # Very short duration to force interval mode
        minimum_interval_threshold = 0.1
        btrvol = BtrVol(
            start=start_volume, end=end_volume, duration=duration,
            tone=BtrVol.Tone.SMOOTH,
            minimum_interval_threshold=minimum_interval_threshold
        )
        self.assertEqual(btrvol.mode, BtrVol.Mode.INTERVAL)
        self.assertEqual(btrvol.volume_levels[0], start_volume)
        self.assertEqual(btrvol.volume_levels[-1], end_volume)
        self.assertEqual(btrvol.time_points[0], 0.0)
        self.assertEqual(btrvol.time_points[-1], duration)
        # self.assertTrue(all(interval >= minimum_interval_threshold
        #                     for interval in btrvol.time_intervals[1:]))

    def test_tones(self):
        for (start, end), tone in product(
            [(20, 80), (80, 20)], BtrVol.Tone
        ):
            btrvol = BtrVol(
                start=start, end=end, duration=3600, tone=tone
            )
            self.assertEqual(btrvol.tone, tone)
            self.assertEqual(btrvol.volume_levels[0], start)
            self.assertEqual(btrvol.volume_levels[-1], end)
            self.assertEqual(btrvol.time_points[0], 0.0)
            self.assertEqual(btrvol.time_points[-1], 3600)
            self.assertEqual(btrvol.time_intervals[0], 0.0)
            self.assertEqual(btrvol.mode, BtrVol.Mode.TIME)

    def test_edge_cases(self):
        for (start, end), tone in product(
            [(0, 0), (50, 50), (100, 100)], BtrVol.Tone
        ):
            btrvol = BtrVol(start=start, end=end, duration=10, tone=tone)
            self.assertEqual(btrvol.volume_levels, [start])
            self.assertEqual(btrvol.time_points, [0.0])
            self.assertEqual(btrvol.volume_levels, [start])
            self.assertEqual(btrvol.time_points, [0.0])
            self.assertEqual(btrvol.time_intervals, [0.0])
            self.assertEqual(btrvol.tone, tone)
            self.assertEqual(btrvol.mode, BtrVol.Mode.TIME)

    def test_volume_to_time(self):
        print(BtrVol.volume_to_time(1, 0, 1, 3600, BtrVol.Tone.SMOOTH))

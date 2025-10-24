# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import unittest

from btrvol.core.volume_control import VolumeControl


class VolumeControlTest(unittest.TestCase):
    def test_mute(self):
        volume_control = VolumeControl()
        for mute_state in (True, False):
            volume_control.set_mute(mute_state)
            self.assertEqual(volume_control.get_mute(), mute_state)

    def test_volume_levels(self):
        volume_control = VolumeControl()
        for volume_level in (0.0, 0.5, 1.0):
            volume_control.set_volume(volume_level)
            self.assertEqual(volume_control.get_volume(), volume_level)

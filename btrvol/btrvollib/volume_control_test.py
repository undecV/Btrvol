import unittest

from .utilities import closed_float_range

from .volume_control import VolumeControl


# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class VolumeControlTest(unittest.TestCase):
    def test_float_closed_crange(self):
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        result = [round(e, 1) for e in closed_float_range(0.0, 0.5, 0.1)]
        self.assertEqual(expected, result)
        print(list(closed_float_range(0.0, 1.0, 0.1)))

    def test_volume_control(self):
        volume_ctrl = VolumeControl()
        volume_ctrl.mute = False
        self.assertEqual(volume_ctrl.mute, False)
        volume_ctrl.volume = 0.75
        self.assertEqual(volume_ctrl.volume, 0.75)

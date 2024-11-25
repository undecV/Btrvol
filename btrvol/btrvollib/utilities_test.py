"""Testcases for utilities."""

import unittest

from .utilities import Inset, in_closed_range, readable_time


# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


class TestReadableTime(unittest.TestCase):
    def test_zero_seconds(self):
        self.assertEqual(readable_time(0), "00:00:00")

    def test_only_seconds(self):
        self.assertEqual(readable_time(59), "00:00:59")

    def test_only_minutes(self):
        self.assertEqual(readable_time(3600), "01:00:00")

    def test_mixed_time(self):
        self.assertEqual(readable_time(3661), "01:01:01")

    def test_large_time(self):
        self.assertEqual(readable_time(338887), "94:08:07")

    def test_edge_case(self):
        self.assertEqual(readable_time(86400), "24:00:00")  # Exactly one day

    def test_negative_seconds(self):
        self.assertEqual(readable_time(-59), "-00:00:59")

    def test_negative_minutes(self):
        self.assertEqual(readable_time(-3661), "-01:01:01")

    def test_large_negative_time(self):
        self.assertEqual(readable_time(-338887), "-94:08:07")

    def test_negative_edge_case(self):
        self.assertEqual(readable_time(-86400), "-24:00:00")  # Exactly negative one day


class TestInClosedRange(unittest.TestCase):
    def test_in_range(self):
        self.assertTrue(in_closed_range(5, (0, 10)))
        self.assertTrue(in_closed_range(0, (0, 10)))
        self.assertTrue(in_closed_range(10, (0, 10)))
        self.assertTrue(in_closed_range(5, (10, 0)))
        self.assertTrue(in_closed_range(0, (10, 0)))
        self.assertTrue(in_closed_range(10, (10, 0)))
        self.assertTrue(in_closed_range(5, (5, 5)))
        self.assertTrue(in_closed_range(10, (10, 10)))
        self.assertTrue(in_closed_range(0, (0, 0)))

    def test_out_of_range(self):
        self.assertFalse(in_closed_range(-5, (0, 10)))
        self.assertFalse(in_closed_range(15, (0, 10)))
        self.assertFalse(in_closed_range(100, (0, 10)))
        self.assertFalse(in_closed_range(-5, (10, 0)))
        self.assertFalse(in_closed_range(15, (10, 0)))
        self.assertFalse(in_closed_range(100, (10, 0)))
        self.assertFalse(in_closed_range(-5, (5, 5)))
        self.assertFalse(in_closed_range(15, (10, 10)))
        self.assertFalse(in_closed_range(100, (0, 0)))

    def test_boundary_values(self):
        self.assertTrue(in_closed_range(0, (0, 10)))
        self.assertTrue(in_closed_range(10, (0, 10)))
        self.assertFalse(in_closed_range(0, (1, 10)))
        self.assertFalse(in_closed_range(10, (0, 9)))
        self.assertTrue(in_closed_range(0, (10, 0)))
        self.assertTrue(in_closed_range(10, (10, 0)))
        self.assertFalse(in_closed_range(0, (10, 1)))
        self.assertFalse(in_closed_range(10, (9, 0)))
        self.assertTrue(in_closed_range(5, (5, 5)))


class TestInset(unittest.TestCase):
    def test_one_argument(self):
        inset = Inset(5)
        self.assertEqual((inset.top, inset.right, inset.bottom, inset.left), (5, 5, 5, 5))

    def test_two_arguments(self):
        inset = Inset(1, 2)
        self.assertEqual((inset.top, inset.right, inset.bottom, inset.left), (1, 2, 1, 2))

    def test_three_arguments(self):
        inset = Inset(1, 2, 3)
        self.assertEqual((inset.top, inset.right, inset.bottom, inset.left), (1, 2, 3, 2))

    def test_four_arguments(self):
        inset = Inset(1, 2, 3, 4)
        self.assertEqual((inset.top, inset.right, inset.bottom, inset.left), (1, 2, 3, 4))

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            Inset(1, 2, 3, 4, 5)


def generate_range(start: int, end: int) -> list[int]:
    """
    Generate a list of integers within a range, inclusive.

    Args:
        start (int): The starting value of the range.
        end (int): The ending value of the range.

    Returns:
        list[int]: A list containing integers within the range [start, end], inclusive.
    """
    return list(range(start, end + (1 if start <= end else -1), (1 if start <= end else -1)))


class TestGenerateRange(unittest.TestCase):
    def test_incrementing_range(self):
        self.assertEqual(generate_range(1, 5), [1, 2, 3, 4, 5])

    def test_decrementing_range(self):
        self.assertEqual(generate_range(5, 1), [5, 4, 3, 2, 1])

    def test_single_element_range(self):
        self.assertEqual(generate_range(5, 5), [5])

    def test_negative_range(self):
        self.assertEqual(generate_range(-5, -1), [-5, -4, -3, -2, -1])

    def test_mixed_range(self):
        self.assertEqual(generate_range(5, 1), [5, 4, 3, 2, 1])


if __name__ == "__main__":
    unittest.main()

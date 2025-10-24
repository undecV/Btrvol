# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import math
import unittest
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar


Real = int | float | Decimal | Fraction
RealT = TypeVar("RealT", int, float, Decimal, Fraction)


def clamp(value: RealT, closing_range: tuple[Real, Real]) -> RealT:
    """Clamp a value within a specified range."""
    lo, hi = sorted(closing_range)
    if value < lo:
        return type(value)(lo)
    if value > hi:
        return type(value)(hi)
    return value


class TestClamp(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(5, (1.0, 10.0)), 5)
        self.assertEqual(clamp(0, (1.0, 10.0)), 1)
        self.assertEqual(clamp(11, (1.0, 10.0)), 10)

    def test_equal_bounds(self):
        values = [
            5,
            -5,
            5.0,
            -5.0,
            Decimal(5),
            Decimal(-5),
            Fraction(5),
            Fraction(-5),
        ]

        for value in values:
            result = clamp(value, (value, value))
            self.assertEqual(result, value)
            self.assertIsInstance(result, type(value))

    def test_mixed_bounds(self):
        self.assertEqual(clamp(5.5, (0, Decimal("10"))), 5.5)
        self.assertEqual(clamp(Decimal("5.5"), (0, 10.0)), Decimal("5.5"))
        self.assertEqual(
            clamp(Fraction(3, 2), (Decimal("0"), 1)), Fraction(1, 1)
        )
        self.assertEqual(clamp(5, (Fraction(1, 1), Fraction(10, 1))), 5)

    def test_infinite_bounds(self):
        self.assertEqual(clamp(5, (-math.inf, 10)), 5)
        self.assertEqual(clamp(5, (-10, math.inf)), 5)
        self.assertEqual(clamp(5.5, (-math.inf, math.inf)), 5.5)
        self.assertEqual(
            clamp(Decimal(5), (Decimal("-Infinity"), Decimal("Infinity"))),
            Decimal(5),
        )
        self.assertEqual(
            clamp(Fraction(5), (-math.inf, math.inf)), Fraction(5)
        )

    def test_degenerate_infinite_ranges_int_fraction_overflow(self):
        with self.assertRaises(OverflowError):
            clamp(5, (math.inf, math.inf))
        with self.assertRaises(OverflowError):
            clamp(5, (-math.inf, -math.inf))
        with self.assertRaises(OverflowError):
            clamp(5, (Decimal("Infinity"), Decimal("Infinity")))
        with self.assertRaises(OverflowError):
            clamp(5, (Decimal("-Infinity"), Decimal("-Infinity")))
        with self.assertRaises(OverflowError):
            clamp(Fraction(5), (math.inf, math.inf))
        with self.assertRaises(OverflowError):
            clamp(Fraction(5), (-math.inf, -math.inf))
        with self.assertRaises(OverflowError):
            clamp(Fraction(5), (Decimal("Infinity"), Decimal("Infinity")))
        with self.assertRaises(OverflowError):
            clamp(Fraction(5), (Decimal("-Infinity"), Decimal("-Infinity")))

    def test_degenerate_infinite_ranges_float_decimal(self):
        self.assertEqual(clamp(5.0, (math.inf, math.inf)), math.inf)
        self.assertEqual(clamp(5.0, (-math.inf, -math.inf)), -math.inf)
        self.assertEqual(
            clamp(5.0, (Decimal("Infinity"), Decimal("Infinity"))), math.inf
        )
        self.assertEqual(
            clamp(5.0, (Decimal("-Infinity"), Decimal("-Infinity"))), -math.inf
        )
        self.assertEqual(
            clamp(Decimal(5), (math.inf, math.inf)), Decimal("Infinity")
        )
        self.assertEqual(
            clamp(Decimal(5), (-math.inf, -math.inf)), Decimal("-Infinity")
        )
        self.assertEqual(
            clamp(Decimal(5), (Decimal("Infinity"), Decimal("Infinity"))),
            Decimal("Infinity"),
        )
        self.assertEqual(
            clamp(Decimal(5), (Decimal("-Infinity"), Decimal("-Infinity"))),
            Decimal("-Infinity"),
        )

    def test_value_is_infinite(self):
        self.assertEqual(clamp(float("inf"), (0, 10)), 10.0)
        self.assertEqual(clamp(float("-inf"), (0, 10)), 0.0)
        self.assertEqual(
            clamp(float("inf"), (Fraction(0), Fraction(10))), 10.0
        )
        self.assertEqual(
            clamp(float("-inf"), (Fraction(0), Fraction(10))), 0.0
        )
        self.assertEqual(
            clamp(float("inf"), (-math.inf, math.inf)), float("inf")
        )
        self.assertEqual(
            clamp(float("-inf"), (-math.inf, math.inf)), float("-inf")
        )
        self.assertEqual(
            clamp(float("inf"), (Decimal("-Infinity"), Decimal("Infinity"))),
            float("inf"),
        )
        self.assertEqual(
            clamp(float("-inf"), (Decimal("-Infinity"), Decimal("Infinity"))),
            float("-inf"),
        )
        self.assertEqual(clamp(Decimal("Infinity"), (0, 10)), Decimal(10))
        self.assertEqual(clamp(Decimal("-Infinity"), (0, 10)), Decimal(0))
        self.assertEqual(
            clamp(Decimal("Infinity"), (-math.inf, math.inf)),
            Decimal("Infinity"),
        )
        self.assertEqual(
            clamp(Decimal("-Infinity"), (-math.inf, math.inf)),
            Decimal("-Infinity"),
        )
        self.assertEqual(
            clamp(
                Decimal("Infinity"),
                (Decimal("-Infinity"), Decimal("Infinity")),
            ),
            Decimal("Infinity"),
        )
        self.assertEqual(
            clamp(
                Decimal("-Infinity"),
                (Decimal("-Infinity"), Decimal("Infinity")),
            ),
            Decimal("-Infinity"),
        )

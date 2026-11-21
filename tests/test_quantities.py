"""Tests for the conversion between the raw values of the protocol and SI units."""

import random
from decimal import Decimal

import pytest

from tinkerforge_async.quantities import CELSIUS_ZERO, TEMPERATURE, Quantity


def test_scale():
    """The raw value is divided by the scale."""
    millivolt = Quantity(1000)
    assert millivolt.to_si(12345) == Decimal("12.345")
    assert millivolt.from_si(Decimal("12.345")) == 12345


def test_offset():
    """The raw temperature is in 1/100 °C, the SI value is in K."""
    assert TEMPERATURE.to_si(2345) == Decimal("296.60")
    assert TEMPERATURE.to_si(-1000) == Decimal("263.15")
    assert TEMPERATURE.to_si(0) == CELSIUS_ZERO
    assert TEMPERATURE.from_si(Decimal("296.60")) == 2345
    assert TEMPERATURE.from_si(CELSIUS_ZERO) == 0


def test_result_types():
    """The SI value is a Decimal, the raw value is an int, whatever type the SI value is passed as."""
    assert isinstance(TEMPERATURE.to_si(1), Decimal)
    for value in (296, 296.6, Decimal("296.6")):
        assert isinstance(TEMPERATURE.from_si(value), int)


@pytest.mark.parametrize("quantity", [Quantity(10), Quantity(100), Quantity(1000), Quantity(10**9), TEMPERATURE])
def test_round_trip(quantity):
    """Converting a raw value to SI and back returns the raw value, also for floats."""
    generator = random.Random(1234)
    for _ in range(1000):
        raw = generator.randint(-(2**31), 2**31 - 1)
        assert quantity.from_si(quantity.to_si(raw)) == raw
        assert quantity.from_si(float(quantity.to_si(raw))) == raw


def test_floats_are_rounded_not_truncated():
    """0.29 * 100 = 28.999999999999996 must not become 28."""
    assert Quantity(100).from_si(0.29) == 29
    assert Quantity(10**9).from_si(0.0029) == 2_900_000
    assert TEMPERATURE.from_si(296.6) == 2345


def test_rounding_of_ties_matches_the_builtin_round():
    """Values exactly between two raw values are rounded to the even value, like round() does. The offset is applied
    after rounding."""
    assert Quantity(10).from_si(Decimal("0.25")) == 2
    assert Quantity(10).from_si(Decimal("0.35")) == 4
    assert TEMPERATURE.from_si(Decimal("296.605")) == round(Decimal("29660.5")) - 27315


def test_matches_the_formulas_of_the_bricklets():
    """The generic conversion gives the same result as the formulas that were used by the Bricklets before."""
    for raw in range(-30000, 30000, 7):
        assert TEMPERATURE.to_si(raw) == Decimal(raw + 27315) / 100
        assert Quantity(1000).to_si(raw) == Decimal(raw) / 1000
    for value in (Decimal("273.15"), Decimal("300.01"), Decimal("12.34")):
        assert TEMPERATURE.from_si(value) == round(value * 100) - 27315

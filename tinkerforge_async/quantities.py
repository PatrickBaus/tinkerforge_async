"""
Conversion between the raw values of the Tinkerforge protocol and SI units.

The Bricks and Bricklets transfer physical quantities as integers in a fixed unit, e.g. the temperature in hundredths
of a degree Celsius. The library always uses SI units and `Decimal` to preserve the precision. A `Quantity` describes
how to convert between both.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

CELSIUS_ZERO = Decimal("273.15")
"""0 degrees Celsius in K. It is the default of the temperature thresholds, i.e. a raw temperature of 0."""


@dataclass(frozen=True, slots=True)
class Quantity:
    """
    A physical quantity that is transferred as an integer. The SI value is `(raw + offset) / scale`.

    Parameters
    ----------
    scale: int
        The number of raw units per SI unit, e.g. 1000 if the raw value is in thousandths of a volt.
    offset: int
        The raw value that is added to the raw value, before it is scaled. It is used for the zero point of the
        temperature, e.g. 27315 if the raw value is in hundredths of a degree Celsius and the SI unit is K.
    """

    scale: int
    offset: int = 0

    def to_si(self, raw: int) -> Decimal:
        """
        Convert a raw value to SI units.
        """
        return Decimal(raw + self.offset) / self.scale

    def from_si(self, value: float | Decimal) -> int:
        """
        Convert a value in SI units to the raw value. The result is rounded to the nearest integer. The value is
        converted to a `Decimal` first, so there are no floating point errors, e.g. 0.0029 * 1e9 = 2899999.9999999995.
        """
        return round(Decimal(value) * self.scale) - self.offset


TEMPERATURE = Quantity(scale=100, offset=27315)
"""The temperature in K. Raw values are in hundredths of a degree Celsius."""

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


@dataclass(frozen=True, slots=True)
class LinearQuantity:
    """
    A physical quantity that is transferred as an integer, with an arbitrary rational scale. The SI value is
    `raw * numerator / denominator + offset`. Unlike `Quantity`, the scale does not need to be the inverse of an
    integer, e.g. 1/16 °/s, 9.80665 m/s² per g or 5/18 m/s per km/h. The offset is given in SI units, e.g. 273.15 K for
    a temperature, that is transferred in degrees Celsius.

    Parameters
    ----------
    numerator: int
        The numerator of the scale.
    denominator: int
        The denominator of the scale.
    offset: Decimal
        The SI value of the raw value 0.
    """

    numerator: int
    denominator: int = 1
    offset: Decimal = Decimal(0)

    def to_si(self, raw: int | float) -> Decimal:
        """
        Convert a raw value to SI units.
        """
        value = Decimal(str(raw)) if isinstance(raw, float) else Decimal(raw)
        return value * self.numerator / self.denominator + self.offset

    def from_si(self, value: float | Decimal) -> int:
        """
        Convert a value in SI units to the raw value. The result is rounded to the nearest integer.
        """
        return round((Decimal(str(value)) - self.offset) * self.denominator / self.numerator)

    def from_si_float(self, value: float | Decimal) -> float:
        """
        Convert a value in SI units to the raw value of a device, that uses floating point numbers.
        """
        return float((Decimal(str(value)) - self.offset) * self.denominator / self.numerator)

import pint
from enum import Enum
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


ureg= pint.UnitRegistry()
Quantity = ureg.Quantity

class QuantityType(Enum):
    LENGTH = ('[length]', 'mm')
    AREA = ('[length]^2', 'mm**2')
    PRESSURE = ('[pressure]', 'MPa')
    FORCE = ('[force]', 'N')

    def __init__(self, dim, unit):
        self.dim = dim
        self.unit = unit

    def matches(self, q):
        return q.check(self.dim)

    def convert(self, q):
        return q.to(self.unit).magnitude


def from_Quantity(quantity: Quantity) -> float:
    if not isinstance(quantity, Quantity):
        return quantity

    for qt in QuantityType:
        if qt.matches(quantity):
            return qt.convert(quantity)

    logger.info(
        f"{quantity} not recognized, base units are {quantity.to_base_units().units}"
    )
    return quantity.to_base_units().magnitude
from dataclasses import dataclass, field
from math import pi
from elements.units import Quantity, ureg


@dataclass
class BaseElement:
    pass

@dataclass
class ReinforcementBar(BaseElement):
    d: float

    @property
    def area(self) -> float:
        return pi * (self.d**2) / 4

@dataclass
class ReinforcementLayer(BaseElement):
    bars: list[ReinforcementBar] | ReinforcementBar = field(default_factory=list)
    number_of_bars: list[int] | int = field(default_factory=list)

    @property
    def area(self) -> float:
        if isinstance(self.bars, ReinforcementBar) and isinstance(self.number_of_bars, int):
            bars = [self.bars]
            nums = [self.number_of_bars]
        elif isinstance(self.bars, list) and isinstance(self.number_of_bars, list):
            if len(self.number_of_bars) != len(self.bars):
                raise ValueError("Number of bars and number of bars do not match")
            bars = self.bars
            nums = self.number_of_bars
        else:
            raise TypeError("bars and number_of_bars should be a list or a reinforcement bar")
        return sum(bar.area * num for bar, num in zip(bars, nums))

@dataclass
class Slab(BaseElement):
    height: float
    width: float

    @property
    def area(self) -> float:
        return self.height * self.width

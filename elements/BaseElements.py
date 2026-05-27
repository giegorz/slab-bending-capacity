from dataclasses import dataclass, field
from math import pi
import numpy as np

from elements.BaseMaterial import BaseMaterial, SteelCS454, ConcreteCS454


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

@dataclass
class Section:
    slab: Slab
    concrete_material: ConcreteCS454
    reinforcement: list[ReinforcementLayer] | ReinforcementLayer
    reinforcement_material: SteelCS454
    number_of_slices: int = 2000

    @property
    def _delta(self) -> float:
        return self.slab.height / self.number_of_slices


    @property
    def z_from_top(self,) -> np.ndarray:
        return np.linspace(0, self.slab.height, self.number_of_slices)

    @staticmethod
    def bisection():
        pass

    def strain_distribution(self, x: float) -> np.ndarray:
        e = self.concrete_material.eps_max
        result = e * (1 - self.z_from_top / x )

        return result

    def calcualte_Fc(self, x: float) -> float:
        strain_distribution = self.strain_distribution(x)
        slice_area = self._delta * self.slab.width
        return np.sum(
            self.concrete_material.strain_stress(
                strain_distribution)
        ) * slice_area

    def calcualte_Fs(self, x: float) -> float:
        pass


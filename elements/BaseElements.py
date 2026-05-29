from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from math import pi
import numpy as np
from scipy.optimize import bisect

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
    bar: ReinforcementBar
    number_of_bars: int | float
    z_from_top: float

    @property
    def area(self) -> float:
        return self.bar.area * self.number_of_bars

    # @property
    # def area(self) -> float:
    #     if isinstance(self.bars, ReinforcementBar) and isinstance(self.number_of_bars, int):
    #         bars = [self.bars]
    #         nums = [self.number_of_bars]
    #     elif isinstance(self.bars, list) and isinstance(self.number_of_bars, list):
    #         if len(self.number_of_bars) != len(self.bars):
    #             raise ValueError("Number of bars and number of bars do not match")
    #         bars = self.bars
    #         nums = self.number_of_bars
    #     else:
    #         raise TypeError("bars and number_of_bars should be a list or a reinforcement bar")
    #     return sum(bar.area * num for bar, num in zip(bars, nums))

@dataclass
class Slab(BaseElement):
    height: float
    width: float

    @property
    def area(self) -> float:
        return self.height * self.width

@dataclass
class Section:
    """
    slab: Slab
    concrete_material: ConcreteCS454
    reinforcement_layers: ReinforcementLayer
    reinforcement_material: ReinforcementMaterial
    """
    slab: Slab
    concrete_material: ConcreteCS454
    reinforcement_layers: ReinforcementLayer | list[ReinforcementLayer]
    reinforcement_material: SteelCS454
    number_of_slices: int = 2000
    strain_top: float = None
    compressive_zone: float = None

    def __post_init__(self):
        self.strain_top = self.concrete_material.eps_max
        if self.number_of_slices <=1:
            raise ValueError("Number of slices must be greater than 1")

    @cached_property
    def _delta(self) -> float:
        return self.slab.height / (self.number_of_slices - 1)

    @cached_property
    def z_centres(self) -> np.ndarray:
        a = self.z_from_top
        return (a[:-1] + a[1:]) / 2

    @cached_property
    def z_from_top(self,) -> np.ndarray:
        return np.linspace(0, self.slab.height, self.number_of_slices)

    def strain_bottom(self, x: float) -> float:
        pass

    def strain_at_z(self, x: float, z: float) -> float:
        e = self.concrete_material.eps_max
        try:
            result = e * (1 - z / x )
        except ZeroDivisionError:
            raise ZeroDivisionError("x must be greater than 0")
        return result

    def strain_distribution(self, x: float) -> np.ndarray:
        if x<=0:
            raise ValueError("x must be greater than 0")
        e = self.concrete_material.eps_max
        result = e * (1 - self.z_centres / x )

        return result

    def calculate_Fc(self, x: float) -> float:
        strain_distribution = self.strain_distribution(x)
        slice_area = self._delta * self.slab.width
        return np.sum(
            self
            .concrete_material
            .strain_stress(
                strain_distribution
            ) * slice_area
        )

    def calculate_Fs(self, x: float) -> float:
        r = self.reinforcement_layers

        layers = [r] if isinstance(r, ReinforcementLayer) else r

        total_force = 0.0

        for layer in layers:
            strain = self.strain_at_z(x, layer.z_from_top)
            stress = self.reinforcement_material.strain_stress(strain)
            total_force += stress * layer.area

        return total_force

    def equilibrium(self, x: float) -> float:
        return self.calculate_Fc(x) + self.calculate_Fs(x)

    def find_equilibrium(self):
        solution = bisect(self.equilibrium, 1, self.slab.height)
        if solution:
            self.compressive_zone = solution
        return solution

    @cached_property
    def _Sy(self):
        dz = self._delta * self.slab.width
        return np.sum(self.z_centres * dz)

    @cached_property
    def cog_from_top(self, return_transformed_section: bool = False) -> float:
        area = self.slab.area
        Sy = self._Sy
        try:
            return Sy/area
        except ZeroDivisionError:
            raise ZeroDivisionError("Area of the slab cannot be zero")

    def Fc_distance_from_top(self):
        x= self.find_equilibrium()
        strains = self.strain_distribution(x)
        stresses = self.concrete_material.strain_stress(strains)
        z = self.z_centres
        dz = self._delta * self.slab.width
        Fc = self.calculate_Fc(x)
        return np.sum(
            stresses * dz * z
        ) / Fc
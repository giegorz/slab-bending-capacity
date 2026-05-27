from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from elements.units import *


@dataclass
class BaseMaterial(ABC):
    pass

    @abstractmethod
    def strain_stress(self, eps: float | np.ndarray) -> float | np.ndarray:
        pass

    def plot_strain_stress(
            self,
            *,
            eps_end: float = 0.0035,
            number_of_points: int = 500
    ) -> Figure:

        fig, ax = plt.subplots()

        if isinstance(self, SteelCS454):
            eps_end = 0.01

        x = np.linspace(0, eps_end, number_of_points)
        y = self.strain_stress(x)
        plt.plot(x, y)

        return fig

@dataclass
class SteelCS454(BaseMaterial):
    fyk: float
    E: float = 200_000
    gamma_m: float = 1.5

    def strain_stress(self, eps: float | np.ndarray) -> float | np.ndarray:
        eps = np.asarray(eps)

        s1 = 0.8 * self.fyk / self.gamma_m
        s2 = self.fyk / self.gamma_m
        e1 = s1 / self.E
        e2 = s2 / self.E + 0.002

        part_1 = eps * self.E
        part_2 = (s2 - s1) / (e2 - e1) * (eps - e1) + \
                 0.8 * self.fyk / self.gamma_m
        part_3 = s2

        mask_1 = eps < e1
        mask_2 = (e1 <= eps) & (eps < e2)
        mask_3 = eps >= e2

        result = np.zeros_like(eps)
        result[mask_1] = part_1[mask_1]
        result[mask_2] = part_2[mask_2]
        result[mask_3] = part_3

        return result

    @property
    def fyd(self) -> float:
        try:
            return self.fyk / self.gamma_m
        except ZeroDivisionError:
            raise ZeroDivisionError(f"gamma cannot be zero!")

    @fyd.setter
    def fyd(self, value):
        self._fyd = value


@dataclass
class ConcreteCS454(BaseMaterial):
    fcu: float
    gamma_m: float = 1.5

    def strain_stress(self, eps: float | np.ndarray) -> float | np.ndarray:

        eps = np.asarray(eps)

        strain_parabolic = 2.44e-4 * np.sqrt(self.fcu / self.gamma_m)
        stress_linear = 0.67* self.fcu / self.gamma_m

        f_parabolic = (5500 * np.sqrt(self.fcu / self.gamma_m)) * eps \
                      - ((5500**2)/2.68) * eps **2

        mask_parabolic = eps < strain_parabolic
        mask_linear = (eps >= strain_parabolic) & (eps <= 0.0035)

        result = np.zeros_like(eps)

        result[mask_parabolic] = f_parabolic[mask_parabolic]
        result[mask_linear] = stress_linear

        return result

    @property
    def fcd(self) -> float:
        return self.fcu / self.gamma_m

    @property
    def E(self) -> float:
        return 20 + 0.27 * self.fcu
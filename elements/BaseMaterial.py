from abc import abstractmethod
from dataclasses import dataclass
import numpy as np

from elements.units import *


@dataclass
class BaseMaterial:
    pass

    @abstractmethod
    def strain_stress(self, eps: float | np.ndarray) -> float | np.ndarray:
        pass

@dataclass
class SteelCS454(BaseMaterial):
    fyk: Quantity
    E: float = 200_000
    gamma_m: float = 1.5

    def strain_stress(self, eps: float | np.ndarray) -> float | np.ndarray:
        return eps * self.E

    @property
    def fyd(self) -> float:
        return self.fyk / self.gamma_m


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
from abc import abstractmethod
from dataclasses import dataclass

import numpy as np

from elements.units import Quantity, ureg


@dataclass
class BaseMaterial:
    pass

    @abstractmethod
    def strain_stress(self, eps: float) -> Quantity:
        pass

@dataclass
class SteelCS454(BaseMaterial):
    fyk: Quantity
    E: Quantity = 200 * ureg.GPa
    gamma_m: Quantity = 1.5


    def strain_stress(self, eps: Quantity) -> Quantity:
        return eps * self.E

    @property
    def fyd(self) -> Quantity:
        return self.fyk / self.gamma_m


@dataclass
class ConcreteCS454(BaseMaterial):
    fcu: Quantity
    gamma_m: float = 1.5

    def strain_stress(self, eps) -> Quantity:

        eps = np.asarray(eps)

        strain_parabolic = 2.44e-4 * np.sqrt(self.fcu.magnitude / self.gamma_m)
        stress_linear = 0.67* self.fcu / self.gamma_m

        f_parabolic =  (
                    (5500 * np.sqrt(self.fcu.magnitude / self.gamma_m)) * eps - ((5500**2)/2.68) * eps **2
        ) * ureg.MPa

        mask_parabolic = eps < strain_parabolic
        mask_linear = (eps >= strain_parabolic) & (eps <= 0.0035)

        result = np.zeros_like(eps) * ureg.MPa

        result[mask_parabolic] = f_parabolic[mask_parabolic]
        result[mask_linear] = stress_linear

        return result

    @property
    def fcd(self) -> Quantity:
        return self.fcu / self.gamma_m

    @property
    def E(self) -> Quantity:
        return 20 * ureg.GPa + 270 * self.fcu
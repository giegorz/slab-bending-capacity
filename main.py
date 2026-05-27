from matplotlib.figure import Figure

from elements.BaseElements import *
from elements.BaseMaterial import ConcreteCS454, SteelCS454
from elements.units import Quantity, ureg, from_Quantity
import numpy as np
import logging
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def plot(x, y)  -> Figure:
    fig, ax = plt.subplots()

    plt.plot(x, y)
    return fig


def main ():
    bar = ReinforcementBar(from_Quantity(12*ureg.mm))
    bar2 = ReinforcementBar(12)
    layer = ReinforcementLayer([bar, bar2], [10, 5])
    print(bar.d, bar2.d)
    print(layer.area)
    steel = SteelCS454(435)


    concrete = ConcreteCS454(fcu= from_Quantity(35*ureg.MPa))
    print(concrete.E)

    x = np.linspace(0, 0.0035, 25)
    y = concrete.strain_stress(x)

    print(10 * "+-")

    slab = Slab(from_Quantity(720*ureg.mm), from_Quantity(1000*ureg.mm))
    print(slab.area)

    xz = np.linspace(0, 0.010, 500)
    z = steel.strain_stress(xz)


    steel.plot_strain_stress().show()
    concrete.plot_strain_stress().show()


if __name__ == "__main__":
    main()
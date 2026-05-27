from elements.BaseElements import *
from elements.BaseMaterial import ConcreteCS454
from elements.units import Quantity, ureg, from_Quantity
import numpy as np
import logging

logger = logging.getLogger(__name__)


def main ():
    bar = ReinforcementBar(from_Quantity(12*ureg.mm))
    bar2 = ReinforcementBar(12)
    layer = ReinforcementLayer([bar, bar2], [10, 5])
    print(bar.d, bar2.d)
    print(layer.area)

    concrete = ConcreteCS454(fcu= from_Quantity(35*ureg.MPa))
    print(concrete.E)

    x = np.linspace(0, 0.0035, 25)
    y = concrete.strain_stress(x)

    print(10 * "+-")

    slab = Slab(from_Quantity(720*ureg.mm), from_Quantity(1000*ureg.mm))
    print(slab.area)


if __name__ == "__main__":
    main()
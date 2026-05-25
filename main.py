from elements.BaseElements import *
from elements.BaseMaterial import ConcreteCS454
from elements.units import Quantity, ureg
import numpy as np
import matplotlib.pyplot as plt


def main ():
    bar = ReinforcementBar(12 * ureg.mm)
    bar2 = ReinforcementBar(25 * ureg.mm)
    layer = ReinforcementLayer([bar, bar2], [10, 5])
    print(layer.area.to("cm**2"))

    concrete = ConcreteCS454(fcu= 35 * ureg.MPa)
    print(concrete.E)

    x = np.linspace(0, 0.0035, 25)
    y = concrete.strain_stress(x)
    print(y)



if __name__ == '__main__':
    main()
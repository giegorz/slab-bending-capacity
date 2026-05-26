from elements.BaseElements import *
from elements.BaseMaterial import ConcreteCS454
from elements.units import Quantity, ureg, as_mm, as_N , as_MPa
import numpy as np

def main ():
    bar = ReinforcementBar.from_quantity(1.2*ureg.cm)
    bar2 = ReinforcementBar(12)
    layer = ReinforcementLayer([bar, bar2], [10, 5])
    print(bar.d, bar2.d)
    print(layer.area)

    concrete = ConcreteCS454(fcu= 35)
    print(concrete.E)

    x = np.linspace(0, 0.0035, 25)
    y = concrete.strain_stress(x)
    print(y)


if __name__ == '__main__':
    main()
import timeit
from functools import wraps

from decorator import decorator
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

def time_this(func, n: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t = timeit.timeit(lambda: func(*args, **kwargs), number= n)
            print(f"{func.__name__}: {t}")
            return None
        return wrapper
    return decorator

def main ():

    slab = Slab(1000, 1000)
    concrete_material= ConcreteCS454(30)
    reinforcement_material = SteelCS454(500)
    reinforcement = ReinforcementLayer(ReinforcementBar(35), number_of_bars=10, z_from_top=950)

    section = Section(slab= slab,
                      concrete_material= concrete_material,
                      reinforcement_material= reinforcement_material,
                      reinforcement_layers= reinforcement,
                      number_of_slices=10000)
    section.find_equilibrium()
    precise = section.compressive_zone

    # section.find_equilibrium()
    # x = section.compressive_zone
    # print(x)
    # print(x / 3)
    # print(section.Fc_distance_from_top())

    x = range(100)[2:]
    y = []

    for i in x:
        s = Section(slab= slab,
                      concrete_material= concrete_material,
                      reinforcement_material= reinforcement_material,
                      reinforcement_layers= reinforcement,
                      number_of_slices=i)
        s.find_equilibrium()

        y.append(1 - s.compressive_zone/ precise)


    print(y)
    plt.plot(x,y)

    plt.show()


if __name__ == "__main__":
    main()
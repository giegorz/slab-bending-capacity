import pytest
import numpy as np

from elements.BaseElements import ReinforcementLayer, Slab, Section, ReinforcementBar
from elements.BaseMaterial import SteelCS454, ConcreteCS454

def test_Section():
    bar = ReinforcementBar(12)
    reinforcement_layer = ReinforcementLayer(bar, 10)
    slab = Slab(460, 1000)
    steel = SteelCS454(435)
    concrete = ConcreteCS454(30)
    section = Section(slab, concrete, reinforcement_layer, steel)
    return section


def test_steel_strain_stress_scalar():
    steel = SteelCS454(500)
    eps = 0.0001
    stress = steel.strain_stress(eps)
    assert pytest.approx(stress) == eps * steel.E

def test_Fc():
    section = test_Section()
    result = 5523145
    assert section.calcualte_Fc(460) == pytest.approx(result)


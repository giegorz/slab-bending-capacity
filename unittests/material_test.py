import pytest
import numpy as np

from elements.BaseElements import ReinforcementLayer, Slab, Section, ReinforcementBar
from elements.BaseMaterial import SteelCS454, ConcreteCS454

@pytest.fixture
def section():
    bar = ReinforcementBar(34.925)
    reinforcement_layer = ReinforcementLayer(bar, number_of_bars=8.756, z_from_top=694)
    slab = Slab(762, 1000)
    steel = SteelCS454(413.685)
    concrete = ConcreteCS454(31)
    return Section(slab, concrete, reinforcement_layer, steel, number_of_slices=2000)

@pytest.fixture
def section_2():
    bar = ReinforcementBar(12)
    reinforcement_layer = ReinforcementLayer(bar, 10, 900)
    slab = Slab(1000, 1000)
    steel = SteelCS454(500)
    concrete = ConcreteCS454(30)
    return Section(slab, concrete, reinforcement_layer, steel, number_of_slices=2000)

class TestSection:
    def test_steel_strain_stress_scalar(self, section):
        steel = SteelCS454(500)
        eps = 0.0001
        stress = steel.strain_stress(eps)
        assert pytest.approx(stress) == eps * steel.E

    def test_max_stress_in_concrete(self, section):
        stress = 13.847
        assert section.concrete_material.strain_stress(0.0035) == pytest.approx(stress, abs=0.001)

    def test_Fc_full_compression(self, section_2):
        expected = 13400000
        assert section_2.calculate_Fc(np.inf) == pytest.approx(expected, abs=100)

    def test_Fc(self, section):
        result = 3017456.21
        assert section.calculate_Fc(243.66) == pytest.approx(result, rel= 0.001)

    def test_bar_area(self, section):
        expected = 8388.11
        assert section.reinforcement_layers.area == pytest.approx(expected, abs = 1)

    def test_Fs(self, section):
        expected = -3017424.8
        assert section.calculate_Fs(243.66) == pytest.approx(expected, abs=100)

    def test_equilibrium(self, section):
        x = section.find_equilibrium()
        assert section.equilibrium(x= x) == pytest.approx(0, abs = 0.001)
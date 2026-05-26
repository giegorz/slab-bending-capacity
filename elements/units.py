import pint

ureg= pint.UnitRegistry()
Quantity = ureg.Quantity

#--------------------------
#   Helpers
#--------------------------

def as_mm(x: int | float | Quantity) -> float:
    if isinstance(x, Quantity):
        return x.to("mm").magnitude
    return float(x)


def as_MPa(x: int | float | Quantity) -> float:
    if isinstance(x, Quantity):
        return x.to("MPa").magnitude
    return float(x)

def as_N(x: int | float | Quantity) -> float:
    if isinstance(x, Quantity):
        return x.to("N").magnitude
    return float(x)
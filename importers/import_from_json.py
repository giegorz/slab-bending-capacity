import json
from pathlib import Path

from elements.BaseMaterial import SteelCS454

_path = "C:\\Users\\CZERPAG\\GitHub\\slab-bending-capacity\\unittests\\fixtures\\materials.json"

def load_json(path):
    if not path:
        raise FileNotFoundError()
    with open(path) as f:
        return json.load(f)

def load_parameters(path):
    data = load_json(path)

    r = data.get("reinforcement")
    c = data.get("concrete")
    s = data.get("slab")
    return r, c, s
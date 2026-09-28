# test_drc.py
from drc_tool import check_metal_spacing

def test_drc_safe_spacing():
    # Wires are 0.6µm apart (Passes 0.5µm rule)
    wire1 = [(0, 0), (1, 0), (1, 5), (0, 5)]
    wire2 = [(1.6, 0), (2.6, 0), (2.6, 5), (1.6, 5)]
    assert check_metal_spacing(wire1, wire2, min_spacing=0.5) == True

def test_drc_violation():
    # Wires are 0.3µm apart (Fails 0.5µm rule)
    wire1 = [(0, 0), (1, 0), (1, 5), (0, 5)]
    wire2 = [(1.3, 0), (2.3, 0), (2.3, 5), (1.3, 5)]
    assert check_metal_spacing(wire1, wire2, min_spacing=0.5) == False
    
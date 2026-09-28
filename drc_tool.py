import gdsfactory as gf
from shapely.geometry import Polygon
gf.gpdk.PDK.activate()

def check_metal_spacing(coords1, coords2, min_spacing=0.5):
    """
    Calculates the distance between two polygons.
    Returns True if they pass the rule, False if they violate it.
    """
    poly1 = Polygon(coords1)
    poly2 = Polygon(coords2)
    
    # Calculate the absolute shortest distance between the two shapes
    distance = poly1.distance(poly2)
    
    if distance < min_spacing:
        print(f"❌ DRC VIOLATION: Wires are {distance:.2f}µm apart!")
        print(f"   Minimum allowed spacing is {min_spacing}µm. GDSII generation blocked.\n")
        return False
    else:
        print(f" DRC PASS: Wires are {distance:.2f}µm apart. Safe to manufacture.\n")
        return True

# --- SIMULATE A LAYOUT ---
c = gf.Component("DRC_TEST_CELL")
LAYER_METAL = (4, 0)

# Wire 1: A vertical metal routing trace
wire1_coords = [(0, 0), (1, 0), (1, 5), (0, 5)]

# Wire 2: Another trace placed right next to it
# Set to 1.3 to create a 0.3µm gap (This should fail our 0.5µm rule!)
x_offset = 1.6
wire2_coords = [(x_offset, 0), (x_offset+1, 0), (x_offset+1, 5), (x_offset, 5)]

# Run the automated check before generating the file
print("Running DRC Engine...")
is_drc_clean = check_metal_spacing(wire1_coords, wire2_coords, min_spacing=0.5)

if is_drc_clean:
    c.add_polygon(wire1_coords, layer=LAYER_METAL)
    c.add_polygon(wire2_coords, layer=LAYER_METAL)
    # Ensure the PDK is active before writing (Fixes the generic PDK error from earlier)
    gf.gpdk.PDK.activate() 
    c.write_gds("drc_passed_layout.gds")
    print("Success: drc_passed_layout.gds generated!")
else:
    print("Error: Layout aborted due to DRC violations. Fix your code.")

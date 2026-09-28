import gdsfactory as gf
gf.gpdk.PDK.activate()


# ==========================================
# PHASE 1: Parametric MOSFET Generation
# ==========================================
@gf.cell
def generate_mosfet(gate_length=1.0, gate_width=5.0, mos_type="nmos"):
    # Initialize the component
    c = gf.Component(f"{mos_type}_L{gate_length}_W{gate_width}")
    
    # Define standard foundry layer numbers (Layer, Datatype)
    LAYER_ACTIVE = (1, 0)  # Diffusion area
    LAYER_POLY = (2, 0)    # Gate
    LAYER_CONTACT = (3, 0) # Vias to connect metal to silicon
    LAYER_METAL1 = (4, 0)  # Metal routing
    LAYER_NWELL = (5, 0)   # Substrate well (for PMOS)
    
    # Static Design Rules (in microns)
    sd_length = 2.0      # Length of Source/Drain regions
    poly_overhang = 1.0  # How far Poly extends past Active area
    contact_size = 0.5   # Size of the contact squares
    
    # Helper function to draw centered rectangles
    def draw_rect(layer, w, h, center_x, center_y):
        c.add_polygon([
            (center_x - w/2, center_y - h/2),
            (center_x + w/2, center_y - h/2),
            (center_x + w/2, center_y + h/2),
            (center_x - w/2, center_y + h/2)
        ], layer=layer)

    # 1. Draw Active (Diffusion) Region
    active_length = gate_length + (2 * sd_length)
    draw_rect(LAYER_ACTIVE, active_length, gate_width, 0, 0)
    
    # 2. Draw Poly Gate (Overlaps the center to form the channel)
    poly_width = gate_width + (2 * poly_overhang)
    draw_rect(LAYER_POLY, gate_length, poly_width, 0, 0)
    
    # 3. Draw Contacts & Metal 1 Pads
    source_x = -(gate_length/2 + sd_length/2) # Left side
    drain_x = (gate_length/2 + sd_length/2)   # Right side
    
    # Source Side
    draw_rect(LAYER_CONTACT, contact_size, contact_size, source_x, 0)
    draw_rect(LAYER_METAL1, sd_length, gate_width, source_x, 0)
    
    # Drain Side
    draw_rect(LAYER_CONTACT, contact_size, contact_size, drain_x, 0)
    draw_rect(LAYER_METAL1, sd_length, gate_width, drain_x, 0)
    
    # 4. Draw N-Well (Only required if this is a PMOS transistor)
    if mos_type == "pmos":
        well_margin = 1.0
        draw_rect(LAYER_NWELL, active_length + 2*well_margin, gate_width + 2*well_margin, 0, 0)
        
    return c

# ==========================================
# PHASE 2: Building the CMOS Inverter
# ==========================================
@gf.cell
def generate_inverter(gate_length=0.5):
    c = gf.Component("cmos_inverter")
    
    # PMOS is usually wider than NMOS to balance mobility differences
    nmos_width = 3.0
    pmos_width = 6.0
    
    # 1. Instantiate the transistors from Phase 1
    nmos = c << generate_mosfet(gate_length=gate_length, gate_width=nmos_width, mos_type="nmos")
    pmos = c << generate_mosfet(gate_length=gate_length, gate_width=pmos_width, mos_type="pmos")
    
    # 2. Place PMOS 12 microns above the NMOS
    pmos_y_offset = 12.0
    pmos.movey(pmos_y_offset)
    
    # 3. Route the Wires Algorithmically
    LAYER_POLY = (2, 0)
    LAYER_METAL1 = (4, 0)
    sd_length = 2.0 
    
    drain_x = (gate_length/2 + sd_length/2)
    source_x = -(gate_length/2 + sd_length/2)
    
    # INPUT ROUTE: Gate to Gate (Poly wire)
    c.add_polygon([
        (-gate_length/2, 0), (gate_length/2, 0), 
        (gate_length/2, pmos_y_offset), (-gate_length/2, pmos_y_offset)
    ], layer=LAYER_POLY)
    
    # OUTPUT ROUTE: Drain to Drain (Metal 1 wire)
    c.add_polygon([
        (drain_x - sd_length/2, 0), (drain_x + sd_length/2, 0),
        (drain_x + sd_length/2, pmos_y_offset), (drain_x - sd_length/2, pmos_y_offset)
    ], layer=LAYER_METAL1)
    
    # POWER ROUTE (VDD): PMOS Source routed upwards
    c.add_polygon([
        (source_x - sd_length/2, pmos_y_offset), (source_x + sd_length/2, pmos_y_offset),
        (source_x + sd_length/2, pmos_y_offset + 3), (source_x - sd_length/2, pmos_y_offset + 3)
    ], layer=LAYER_METAL1)
    
    # GROUND ROUTE (GND): NMOS Source routed downwards
    c.add_polygon([
        (source_x - sd_length/2, 0), (source_x + sd_length/2, 0),
        (source_x + sd_length/2, -3), (source_x - sd_length/2, -3)
    ], layer=LAYER_METAL1)

    return c

# ==========================================
# EXECUTION (Run this to generate the GDS files)
# ==========================================
if __name__ == "__main__":
    # Test Phase 1 (Individual Transistors)
    my_nmos = generate_mosfet(gate_length=0.5, gate_width=3.0, mos_type="nmos")
    my_pmos = generate_mosfet(gate_length=0.5, gate_width=6.0, mos_type="pmos")
    my_nmos.write_gds("nmos_parametric.gds")
    my_pmos.write_gds("pmos_parametric.gds")
    print("Phase 1 Complete: Parametric Transistors generated!")
    
    # Test Phase 2 (Full Inverter Logic)
    my_inverter = generate_inverter()
    my_inverter.write_gds("cmos_inverter.gds")
    print("Phase 2 Complete: Fully routed CMOS Inverter generated!")

    
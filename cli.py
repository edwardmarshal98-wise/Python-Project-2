import argparse
import gdsfactory as gf

gf.gpdk.PDK.activate()

# Re-use our parametric generator logic
@gf.cell
def generate_mosfet(gate_length, gate_width, mos_type):
    c = gf.Component(f"{mos_type}_L{gate_length}_W{gate_width}")
    # Standard layers
    LAYER_ACTIVE = (1, 0); LAYER_POLY = (2, 0)
    # Simplified drawing logic for the CLI demonstration
    c.add_polygon([(-gate_length/2, -gate_width/2), (gate_length/2, -gate_width/2), 
                   (gate_length/2, gate_width/2), (-gate_length/2, gate_width/2)], layer=LAYER_POLY)
    return c

def main():
    # Set up the terminal command parser
    parser = argparse.ArgumentParser(description="Automated VLSI Layout Generator")
    parser.add_argument("--type", choices=["nmos", "pmos"], required=True, help="Type of transistor")
    parser.add_argument("--width", type=float, default=5.0, help="Gate width in microns")
    parser.add_argument("--length", type=float, default=1.0, help="Gate length in microns")
    
    args = parser.parse_args()

    print(f"Compiling {args.type.upper()} Layout (Width: {args.width}µm, Length: {args.length}µm)...")
    
    # Generate the geometry based on terminal inputs
    device = generate_mosfet(gate_length=args.length, gate_width=args.width, mos_type=args.type)
    
    # Save the file
    filename = f"{args.type}_custom.gds"
    device.write_gds(filename)
    print(f"Success! {filename} has been generated.")

if __name__ == "__main__":
    main()

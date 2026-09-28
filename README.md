# Programmatic CMOS Standard Cell Layout & DRC Automation

## Overview
This project is a Python-based Electronic Design Automation (EDA) tool that automatically generates physical semiconductor layouts (GDSII) using pure code. It mimics the behavior of commercial foundry tools by algorithmically generating components, routing them, and verifying manufacturing limits.

## Features
* **Parametric MOSFET Generation:** Automatically draws N-Well, active diffusion, poly-silicon gates, and metal contacts for NMOS and PMOS devices.
* **Algorithmic Routing:** Instantiates individual transistors and dynamically routes metal and poly traces to build a functional CMOS Inverter.
* **Automated Design Rule Checking (DRC):** Uses geometric math to calculate polygon spacing, automatically blocking layout generation if traces violate the 0.5µm minimum foundry spacing rules to prevent short-circuits.
* **Command-Line Interface (CLI):** Allows users to generate custom transistors on the fly via terminal commands.

## Tech Stack
* **Python 3**
* **gdsfactory:** For algorithmic layout generation and GDSII compilation.
* **Shapely:** For mathematical polygon distance calculations (DRC engine).
* **KLayout:** For visual inspection of the generated GDSII silicon blueprints.

## How to Use the CLI Tool
You can generate custom parametric transistors directly from your terminal. 

**Example Command:**
```bash
python cli.py --type pmos --width 12.5 --length 0.8
<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The Sum output is computed using XOR operations, which effectively add the bits without considering carry overflow.
The Cout output determines if a carry is generated when at least two of the three inputs are high.

## How to test

Place the design file in the src/ directory.
Ensure info.yaml includes:
top_module: full_adder
Correct source_files
Run simulation using your preferred Verilog simulator (e.g., Icarus Verilog).
Check outputs against the truth table.

## External hardware

No external hardware is required. The design can be fully simulated and verified using a Verilog testbench.

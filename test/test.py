# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_fulladder(dut):
    dut._log.info("Start")

    # Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await Timer(50, units="ns")
    dut.rst_n.value = 1
    await Timer(50, units="ns")

    # Define correct test cases: (A, B, Cin, Sum, Cout)
    test_cases = [
        (0, 0, 0, 0, 0),
        (0, 0, 1, 1, 0),
        (0, 1, 0, 1, 0),
        (0, 1, 1, 0, 1),
        (1, 0, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (1, 1, 0, 0, 1),
        (1, 1, 1, 1, 1),
    ]

    for a, b, cin, e_sum, e_cout in test_cases:

        # Apply inputs
        dut.uio_in.value = (cin << 2) | (b << 1) | a

        # Wait for output to settle
        await Timer(20, units="ns")

        try:
            output_val = int(dut.uo_out.value)
            actual_sum = output_val & 1
            actual_cout = (output_val >> 1) & 1

            assert actual_sum == e_sum, f"Sum Error: A={a} B={b} Cin={cin}"
            assert actual_cout == e_cout, f"Cout Error: A={a} B={b} Cin={cin}"

            dut._log.info(
                f"Input: {a},{b},{cin} -> Sum: {actual_sum}, Cout: {actual_cout} [PASS]"
            )

        except ValueError:
            # Helps debug 'x' or 'z' states
            dut._log.error(f"Logic error: uo_out is {str(dut.uo_out.value)}")
            raise

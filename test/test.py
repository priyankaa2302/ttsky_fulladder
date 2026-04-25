# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
#from cocotb.clock import Clock
from cocotb.triggers import Timer


@cocotb.test()
async def test_fulladder(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    #clock = Clock(dut.clk, 10, unit="us")
    #cocotb.start_soon(clock.start())
    #initialize inputs
    dut.ena.value =1 
    dut.ui_in.value =0
    dut.uio_in.value =0
    # Reset
    dut.rst_n.value = 0
    await Timer(50,unit="ns")
    dut.rst_n.value = 1
    await Timer(50,unit="ns")
    

    #define test cases
    test_cases =[(0,0,0,0,0),
                 (1,0,1,0,0),
                 (0,1,0,1,1),
                 (0,0,1,1,1),
                 (1,1,0,1,0)]
    # Set the input values you want to test
    for a,b,cin,e_sum,e_cout in test_cases:
        dut.uio_in.value = (cin <<2)|(b <<1)|a

    # Wait for one clock cycle to see the output values
    await Timer(20,unit="ns")
    #safe conversion
    try:
        output_val = int(dut.uo_out.value)
        actual_sum = output_val & 1
        actual_cout = (output_val >> 1) & 1
    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert actual_sum == e_sum, f"Sum Error: A={a} B={b} Cin={cin}"
    assert actual_cout == e_cout, f"Cout Error: A={a} B={b} Cin={cin}"
    
    dut._log.info(f"Input: {a},{b},{cin} -> Sum: {actual_sum}, Cout: {actual_cout} [PASS]")
    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
     except ValueError:
        #helps debug 'x' states in the github action logs
        dut.log.error(f"Logi error: uo_out is {str(dut.uo_out.value)}")
        raise

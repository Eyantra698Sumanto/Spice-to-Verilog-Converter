//This is the parsed Verilog file
`include "rvmyth.v"
`include "10bitDAC.v"
module circuit(clk, reset, out);
input clk, reset;
output real out;
wire [9:0] rvtodac;
rvmyth uut1 (clk, reset, rvtodac);
10bitDAC uut2 (rvtodac, out);
endmodule;

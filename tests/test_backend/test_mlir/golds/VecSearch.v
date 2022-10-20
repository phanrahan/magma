module VecSearch(
  input        CLK,
  output [3:0] out);

  reg [2:0] Register_inst0;

  always_ff @(posedge CLK)
    Register_inst0 <= Register_inst0 + 3'h1;
  initial
    Register_inst0 = 3'h0;
  wire [6:0][3:0] _T = {{4'h0}, {4'h4}, {4'hF}, {4'hE}, {4'h2}, {4'h5}, {4'hD}};
  assign out = _T[Register_inst0];
endmodule


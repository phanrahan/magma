module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module TestSetSlice (
    input [5:0] I,
    input [1:0] x,
    output [11:0] O
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst10_out;
wire magma_Bit_and_inst11_out;
wire magma_Bit_and_inst12_out;
wire magma_Bit_and_inst13_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst5_out;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst7_out;
wire magma_Bit_and_inst8_out;
wire magma_Bit_and_inst9_out;
wire [3:0] magma_Bits_4_sub_inst0_out;
wire [3:0] magma_Bits_4_sub_inst10_out;
wire [3:0] magma_Bits_4_sub_inst12_out;
wire [3:0] magma_Bits_4_sub_inst14_out;
wire [3:0] magma_Bits_4_sub_inst16_out;
wire [3:0] magma_Bits_4_sub_inst18_out;
wire [3:0] magma_Bits_4_sub_inst2_out;
wire [3:0] magma_Bits_4_sub_inst20_out;
wire [3:0] magma_Bits_4_sub_inst22_out;
wire [3:0] magma_Bits_4_sub_inst4_out;
wire [3:0] magma_Bits_4_sub_inst6_out;
wire [3:0] magma_Bits_4_sub_inst8_out;
wire [5:0] magma_Bits_6_lshr_inst0_out;
wire [5:0] magma_Bits_6_lshr_inst1_out;
wire [5:0] magma_Bits_6_lshr_inst10_out;
wire [5:0] magma_Bits_6_lshr_inst11_out;
wire [5:0] magma_Bits_6_lshr_inst2_out;
wire [5:0] magma_Bits_6_lshr_inst3_out;
wire [5:0] magma_Bits_6_lshr_inst4_out;
wire [5:0] magma_Bits_6_lshr_inst5_out;
wire [5:0] magma_Bits_6_lshr_inst6_out;
wire [5:0] magma_Bits_6_lshr_inst7_out;
wire [5:0] magma_Bits_6_lshr_inst8_out;
wire [5:0] magma_Bits_6_lshr_inst9_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst0_out[0]),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst1_out[0]),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst10_out[0]),
    .S(magma_Bit_and_inst12_out),
    .O(Mux2xOutBit_inst10_O)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst11_out[0]),
    .S(magma_Bit_and_inst13_out),
    .O(Mux2xOutBit_inst11_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst2_out[0]),
    .S(magma_Bit_and_inst4_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst3_out[0]),
    .S(magma_Bit_and_inst5_out),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst4_out[0]),
    .S(magma_Bit_and_inst6_out),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst5_out[0]),
    .S(magma_Bit_and_inst7_out),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst6_out[0]),
    .S(magma_Bit_and_inst8_out),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst7_out[0]),
    .S(magma_Bit_and_inst9_out),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst8_out[0]),
    .S(magma_Bit_and_inst10_out),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst9_out[0]),
    .S(magma_Bit_and_inst11_out),
    .O(Mux2xOutBit_inst9_O)
);
assign magma_Bit_and_inst0_out = 1'b1 & (({1'b0,1'b0,x[1:0]}) <= 4'h0);
assign magma_Bit_and_inst10_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h8);
assign magma_Bit_and_inst11_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h9);
assign magma_Bit_and_inst12_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'ha);
assign magma_Bit_and_inst13_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'hb);
assign magma_Bit_and_inst2_out = (1'b1 & (({1'b0,1'b0,x[1:0]}) <= 4'h1)) & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h1);
assign magma_Bit_and_inst4_out = (1'b1 & (({1'b0,1'b0,x[1:0]}) <= 4'h2)) & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h2);
assign magma_Bit_and_inst5_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h3);
assign magma_Bit_and_inst6_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h4);
assign magma_Bit_and_inst7_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h5);
assign magma_Bit_and_inst8_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h6);
assign magma_Bit_and_inst9_out = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h7);
assign magma_Bits_4_sub_inst0_out = 4'(4'h0 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst10_out = 4'(4'h5 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst12_out = 4'(4'h6 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst14_out = 4'(4'h7 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst16_out = 4'(4'h8 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst18_out = 4'(4'h9 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst2_out = 4'(4'h1 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst20_out = 4'(4'ha - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst22_out = 4'(4'hb - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst4_out = 4'(4'h2 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst6_out = 4'(4'h3 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst8_out = 4'(4'h4 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_6_lshr_inst0_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst0_out[2:0]});
assign magma_Bits_6_lshr_inst1_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst2_out[2:0]});
assign magma_Bits_6_lshr_inst10_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst20_out[2:0]});
assign magma_Bits_6_lshr_inst11_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst22_out[2:0]});
assign magma_Bits_6_lshr_inst2_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst4_out[2:0]});
assign magma_Bits_6_lshr_inst3_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst6_out[2:0]});
assign magma_Bits_6_lshr_inst4_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst8_out[2:0]});
assign magma_Bits_6_lshr_inst5_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst10_out[2:0]});
assign magma_Bits_6_lshr_inst6_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst12_out[2:0]});
assign magma_Bits_6_lshr_inst7_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst14_out[2:0]});
assign magma_Bits_6_lshr_inst8_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst16_out[2:0]});
assign magma_Bits_6_lshr_inst9_out = I >> ({1'b0,1'b0,1'b0,magma_Bits_4_sub_inst18_out[2:0]});
assign O = {Mux2xOutBit_inst11_O,Mux2xOutBit_inst10_O,Mux2xOutBit_inst9_O,Mux2xOutBit_inst8_O,Mux2xOutBit_inst7_O,Mux2xOutBit_inst6_O,Mux2xOutBit_inst5_O,Mux2xOutBit_inst4_O,Mux2xOutBit_inst3_O,Mux2xOutBit_inst2_O,Mux2xOutBit_inst1_O,Mux2xOutBit_inst0_O};
endmodule


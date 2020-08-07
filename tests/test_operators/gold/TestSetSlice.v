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
wire Mux2xOutBit_inst0_I0;
wire Mux2xOutBit_inst0_I1;
wire Mux2xOutBit_inst0_S;
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_I0;
wire Mux2xOutBit_inst1_I1;
wire Mux2xOutBit_inst1_S;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_I0;
wire Mux2xOutBit_inst10_I1;
wire Mux2xOutBit_inst10_S;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_I0;
wire Mux2xOutBit_inst11_I1;
wire Mux2xOutBit_inst11_S;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst2_I0;
wire Mux2xOutBit_inst2_I1;
wire Mux2xOutBit_inst2_S;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_I0;
wire Mux2xOutBit_inst3_I1;
wire Mux2xOutBit_inst3_S;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_I0;
wire Mux2xOutBit_inst4_I1;
wire Mux2xOutBit_inst4_S;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_I0;
wire Mux2xOutBit_inst5_I1;
wire Mux2xOutBit_inst5_S;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst6_I0;
wire Mux2xOutBit_inst6_I1;
wire Mux2xOutBit_inst6_S;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_I0;
wire Mux2xOutBit_inst7_I1;
wire Mux2xOutBit_inst7_S;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_I0;
wire Mux2xOutBit_inst8_I1;
wire Mux2xOutBit_inst8_S;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_I0;
wire Mux2xOutBit_inst9_I1;
wire Mux2xOutBit_inst9_S;
wire Mux2xOutBit_inst9_O;
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
assign Mux2xOutBit_inst0_I0 = 1'b1;
assign Mux2xOutBit_inst0_I1 = magma_Bits_6_lshr_inst0_out[0];
assign Mux2xOutBit_inst0_S = 1'b1 & (({1'b0,1'b0,x[1:0]}) <= 4'h0);
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(Mux2xOutBit_inst0_I0),
    .I1(Mux2xOutBit_inst0_I1),
    .S(Mux2xOutBit_inst0_S),
    .O(Mux2xOutBit_inst0_O)
);
assign Mux2xOutBit_inst1_I0 = 1'b1;
assign Mux2xOutBit_inst1_I1 = magma_Bits_6_lshr_inst1_out[0];
assign Mux2xOutBit_inst1_S = (1'b1 & (({1'b0,1'b0,x[1:0]}) <= 4'h1)) & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h1);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst1_I0),
    .I1(Mux2xOutBit_inst1_I1),
    .S(Mux2xOutBit_inst1_S),
    .O(Mux2xOutBit_inst1_O)
);
assign Mux2xOutBit_inst10_I0 = 1'b1;
assign Mux2xOutBit_inst10_I1 = magma_Bits_6_lshr_inst10_out[0];
assign Mux2xOutBit_inst10_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'ha);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(Mux2xOutBit_inst10_I0),
    .I1(Mux2xOutBit_inst10_I1),
    .S(Mux2xOutBit_inst10_S),
    .O(Mux2xOutBit_inst10_O)
);
assign Mux2xOutBit_inst11_I0 = 1'b1;
assign Mux2xOutBit_inst11_I1 = magma_Bits_6_lshr_inst11_out[0];
assign Mux2xOutBit_inst11_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'hb);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst11_I0),
    .I1(Mux2xOutBit_inst11_I1),
    .S(Mux2xOutBit_inst11_S),
    .O(Mux2xOutBit_inst11_O)
);
assign Mux2xOutBit_inst2_I0 = 1'b1;
assign Mux2xOutBit_inst2_I1 = magma_Bits_6_lshr_inst2_out[0];
assign Mux2xOutBit_inst2_S = (1'b1 & (({1'b0,1'b0,x[1:0]}) <= 4'h2)) & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h2);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(Mux2xOutBit_inst2_I0),
    .I1(Mux2xOutBit_inst2_I1),
    .S(Mux2xOutBit_inst2_S),
    .O(Mux2xOutBit_inst2_O)
);
assign Mux2xOutBit_inst3_I0 = 1'b1;
assign Mux2xOutBit_inst3_I1 = magma_Bits_6_lshr_inst3_out[0];
assign Mux2xOutBit_inst3_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h3);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst3_I0),
    .I1(Mux2xOutBit_inst3_I1),
    .S(Mux2xOutBit_inst3_S),
    .O(Mux2xOutBit_inst3_O)
);
assign Mux2xOutBit_inst4_I0 = 1'b1;
assign Mux2xOutBit_inst4_I1 = magma_Bits_6_lshr_inst4_out[0];
assign Mux2xOutBit_inst4_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h4);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst4_I0),
    .I1(Mux2xOutBit_inst4_I1),
    .S(Mux2xOutBit_inst4_S),
    .O(Mux2xOutBit_inst4_O)
);
assign Mux2xOutBit_inst5_I0 = 1'b1;
assign Mux2xOutBit_inst5_I1 = magma_Bits_6_lshr_inst5_out[0];
assign Mux2xOutBit_inst5_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h5);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(Mux2xOutBit_inst5_I0),
    .I1(Mux2xOutBit_inst5_I1),
    .S(Mux2xOutBit_inst5_S),
    .O(Mux2xOutBit_inst5_O)
);
assign Mux2xOutBit_inst6_I0 = 1'b1;
assign Mux2xOutBit_inst6_I1 = magma_Bits_6_lshr_inst6_out[0];
assign Mux2xOutBit_inst6_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h6);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(Mux2xOutBit_inst6_I0),
    .I1(Mux2xOutBit_inst6_I1),
    .S(Mux2xOutBit_inst6_S),
    .O(Mux2xOutBit_inst6_O)
);
assign Mux2xOutBit_inst7_I0 = 1'b1;
assign Mux2xOutBit_inst7_I1 = magma_Bits_6_lshr_inst7_out[0];
assign Mux2xOutBit_inst7_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h7);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst7_I0),
    .I1(Mux2xOutBit_inst7_I1),
    .S(Mux2xOutBit_inst7_S),
    .O(Mux2xOutBit_inst7_O)
);
assign Mux2xOutBit_inst8_I0 = 1'b1;
assign Mux2xOutBit_inst8_I1 = magma_Bits_6_lshr_inst8_out[0];
assign Mux2xOutBit_inst8_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h8);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst8_I0),
    .I1(Mux2xOutBit_inst8_I1),
    .S(Mux2xOutBit_inst8_S),
    .O(Mux2xOutBit_inst8_O)
);
assign Mux2xOutBit_inst9_I0 = 1'b1;
assign Mux2xOutBit_inst9_I1 = magma_Bits_6_lshr_inst9_out[0];
assign Mux2xOutBit_inst9_S = 1'b1 & ((4'((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h9);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst9_I0),
    .I1(Mux2xOutBit_inst9_I1),
    .S(Mux2xOutBit_inst9_S),
    .O(Mux2xOutBit_inst9_O)
);
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


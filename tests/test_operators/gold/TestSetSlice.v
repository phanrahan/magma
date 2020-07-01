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
wire [3:0] magma_Bits_4_sub_inst0_out;
wire [3:0] magma_Bits_4_sub_inst1_out;
wire [3:0] magma_Bits_4_sub_inst10_out;
wire [3:0] magma_Bits_4_sub_inst11_out;
wire [3:0] magma_Bits_4_sub_inst2_out;
wire [3:0] magma_Bits_4_sub_inst3_out;
wire [3:0] magma_Bits_4_sub_inst4_out;
wire [3:0] magma_Bits_4_sub_inst5_out;
wire [3:0] magma_Bits_4_sub_inst6_out;
wire [3:0] magma_Bits_4_sub_inst7_out;
wire [3:0] magma_Bits_4_sub_inst8_out;
wire [3:0] magma_Bits_4_sub_inst9_out;
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
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h0) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h0)),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst1_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h1) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h1)),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst10_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'ha) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'ha)),
    .O(Mux2xOutBit_inst10_O)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst11_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'hb) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'hb)),
    .O(Mux2xOutBit_inst11_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst2_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h2) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h2)),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst3_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h3) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h3)),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst4_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h4) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h4)),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst5_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h5) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h5)),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst6_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h6) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h6)),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst7_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h7) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h7)),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst8_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h8) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h8)),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst9_out[0]),
    .S((({1'b0,1'b0,x[1:0]}) <= 4'h9) & ((4'(({1'b0,1'b0,x[1:0]}) + 4'h6)) > 4'h9)),
    .O(Mux2xOutBit_inst9_O)
);
assign magma_Bits_4_sub_inst0_out = 4'(4'h0 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst1_out = 4'(4'h1 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst10_out = 4'(4'ha - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst11_out = 4'(4'hb - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst2_out = 4'(4'h2 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst3_out = 4'(4'h3 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst4_out = 4'(4'h4 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst5_out = 4'(4'h5 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst6_out = 4'(4'h6 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst7_out = 4'(4'h7 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst8_out = 4'(4'h8 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_4_sub_inst9_out = 4'(4'h9 - ({1'b0,1'b0,x[1:0]}));
assign magma_Bits_6_lshr_inst0_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst0_out[3:0]});
assign magma_Bits_6_lshr_inst1_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst1_out[3:0]});
assign magma_Bits_6_lshr_inst10_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst10_out[3:0]});
assign magma_Bits_6_lshr_inst11_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst11_out[3:0]});
assign magma_Bits_6_lshr_inst2_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst2_out[3:0]});
assign magma_Bits_6_lshr_inst3_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst3_out[3:0]});
assign magma_Bits_6_lshr_inst4_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst4_out[3:0]});
assign magma_Bits_6_lshr_inst5_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst5_out[3:0]});
assign magma_Bits_6_lshr_inst6_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst6_out[3:0]});
assign magma_Bits_6_lshr_inst7_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst7_out[3:0]});
assign magma_Bits_6_lshr_inst8_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst8_out[3:0]});
assign magma_Bits_6_lshr_inst9_out = I >> ({1'b0,1'b0,magma_Bits_4_sub_inst9_out[3:0]});
assign O = {Mux2xOutBit_inst11_O,Mux2xOutBit_inst10_O,Mux2xOutBit_inst9_O,Mux2xOutBit_inst8_O,Mux2xOutBit_inst7_O,Mux2xOutBit_inst6_O,Mux2xOutBit_inst5_O,Mux2xOutBit_inst4_O,Mux2xOutBit_inst3_O,Mux2xOutBit_inst2_O,Mux2xOutBit_inst1_O,Mux2xOutBit_inst0_O};
endmodule


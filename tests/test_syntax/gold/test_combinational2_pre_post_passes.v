module Mux2xOutBits3 (
    input [2:0] I0,
    input [2:0] I1,
    input S,
    output [2:0] O
);
reg [2:0] coreir_commonlib_mux2x3_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x3_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x3_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x3_inst0_out;
endmodule

module pre_unroll (
    input [2:0] I,
    output [2:0] O
);
wire [2:0] Mux2xOutBits3_inst0_I0;
wire [2:0] Mux2xOutBits3_inst0_I1;
wire Mux2xOutBits3_inst0_S;
wire [2:0] Mux2xOutBits3_inst0_O;
wire [2:0] Mux2xOutBits3_inst1_I0;
wire [2:0] Mux2xOutBits3_inst1_I1;
wire Mux2xOutBits3_inst1_S;
wire [2:0] Mux2xOutBits3_inst1_O;
wire [2:0] Mux2xOutBits3_inst2_I0;
wire [2:0] Mux2xOutBits3_inst2_I1;
wire Mux2xOutBits3_inst2_S;
assign Mux2xOutBits3_inst0_I0 = 3'h4;
assign Mux2xOutBits3_inst0_I1 = 3'h2;
assign Mux2xOutBits3_inst0_S = I[2];
Mux2xOutBits3 Mux2xOutBits3_inst0 (
    .I0(Mux2xOutBits3_inst0_I0),
    .I1(Mux2xOutBits3_inst0_I1),
    .S(Mux2xOutBits3_inst0_S),
    .O(Mux2xOutBits3_inst0_O)
);
assign Mux2xOutBits3_inst1_I0 = Mux2xOutBits3_inst0_O;
assign Mux2xOutBits3_inst1_I1 = 3'h1;
assign Mux2xOutBits3_inst1_S = I[1];
Mux2xOutBits3 Mux2xOutBits3_inst1 (
    .I0(Mux2xOutBits3_inst1_I0),
    .I1(Mux2xOutBits3_inst1_I1),
    .S(Mux2xOutBits3_inst1_S),
    .O(Mux2xOutBits3_inst1_O)
);
assign Mux2xOutBits3_inst2_I0 = Mux2xOutBits3_inst1_O;
assign Mux2xOutBits3_inst2_I1 = 3'h0;
assign Mux2xOutBits3_inst2_S = I[0];
Mux2xOutBits3 Mux2xOutBits3_inst2 (
    .I0(Mux2xOutBits3_inst2_I0),
    .I1(Mux2xOutBits3_inst2_I1),
    .S(Mux2xOutBits3_inst2_S),
    .O(O)
);
endmodule


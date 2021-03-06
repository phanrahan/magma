module Mux2xBits3 (
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
wire [2:0] Mux2xBits3_inst0_O;
wire [2:0] Mux2xBits3_inst1_O;
Mux2xBits3 Mux2xBits3_inst0 (
    .I0(3'h4),
    .I1(3'h2),
    .S(I[2]),
    .O(Mux2xBits3_inst0_O)
);
Mux2xBits3 Mux2xBits3_inst1 (
    .I0(Mux2xBits3_inst0_O),
    .I1(3'h1),
    .S(I[1]),
    .O(Mux2xBits3_inst1_O)
);
Mux2xBits3 Mux2xBits3_inst2 (
    .I0(Mux2xBits3_inst1_O),
    .I1(3'h0),
    .S(I[0]),
    .O(O)
);
endmodule


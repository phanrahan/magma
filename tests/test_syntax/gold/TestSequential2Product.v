module Mux2xTuplea_OutBit (
    input I0_a,
    input I1_a,
    output O_a,
    input S
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0_a;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1_a;
end
end

assign O_a = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module Test (
    input CLK,
    output O_a,
    input sel
);
wire bit_const_0_None_out;
wire bit_const_1_None_out;
Mux2xTuplea_OutBit Mux2xTuplea_OutBit_inst0 (
    .I0_a(bit_const_1_None_out),
    .I1_a(bit_const_0_None_out),
    .O_a(O_a),
    .S(sel)
);
assign bit_const_0_None_out = 1'b0;
assign bit_const_1_None_out = 1'b1;
endmodule


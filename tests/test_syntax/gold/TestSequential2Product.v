module Mux2xTuplea_Bit (
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
Mux2xTuplea_Bit Mux2xTuplea_Bit_inst0 (
    .I0_a(1'b1),
    .I1_a(1'b0),
    .O_a(O_a),
    .S(sel)
);
endmodule


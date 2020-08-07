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
wire Mux2xTuplea_OutBit_inst0_I0_a;
wire Mux2xTuplea_OutBit_inst0_I1_a;
wire Mux2xTuplea_OutBit_inst0_S;
assign Mux2xTuplea_OutBit_inst0_I0_a = 1'b1;
assign Mux2xTuplea_OutBit_inst0_I1_a = 1'b0;
assign Mux2xTuplea_OutBit_inst0_S = sel;
Mux2xTuplea_OutBit Mux2xTuplea_OutBit_inst0 (
    .I0_a(Mux2xTuplea_OutBit_inst0_I0_a),
    .I1_a(Mux2xTuplea_OutBit_inst0_I1_a),
    .O_a(O_a),
    .S(Mux2xTuplea_OutBit_inst0_S)
);
endmodule


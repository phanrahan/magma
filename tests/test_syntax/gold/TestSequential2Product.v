module Mux2xTuplea_Bit (
    input I0_a,
    input I1_a,
    output O_a,
    input S
);
reg [0:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = I0_a;
end else begin
    mux_out = I1_a;
end
end

assign O_a = mux_out[0];
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


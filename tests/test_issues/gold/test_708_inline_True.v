module Mux2xTuplex_UInt8 (
    input [7:0] I0_x,
    input [7:0] I1_x,
    output [7:0] O_x,
    input S
);
reg [7:0] coreir_commonlib_mux2x8_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x8_inst0_out = I0_x;
end else begin
    coreir_commonlib_mux2x8_inst0_out = I1_x;
end
end

assign O_x = coreir_commonlib_mux2x8_inst0_out;
endmodule

module Test (
    input CLK,
    output [7:0] O_a_x,
    input c
);
wire [7:0] magma_UInt_8_add_inst0_out;
Mux2xTuplex_UInt8 Mux2xTuplex_UInt8_inst0 (
    .I0_x(8'h00),
    .I1_x(magma_UInt_8_add_inst0_out),
    .O_x(O_a_x),
    .S(c)
);
assign magma_UInt_8_add_inst0_out = 8'h00 + 8'h01;
endmodule


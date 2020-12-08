module Mux2xBits5 (
    input [4:0] I0,
    input [4:0] I1,
    input S,
    output [4:0] O
);
reg [4:0] coreir_commonlib_mux2x5_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x5_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x5_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x5_inst0_out;
endmodule

module TestReadyValidWhen (
    input [4:0] I_data,
    output I_ready,
    input I_valid,
    output [4:0] O_data,
    input O_ready,
    output O_valid
);
wire magma_Bit_or_inst1_out;
Mux2xBits5 Mux2xBits5_inst0 (
    .I0(5'h00),
    .I1(I_data),
    .S(magma_Bit_or_inst1_out),
    .O(O_data)
);
assign magma_Bit_or_inst1_out = I_valid | 1'b0;
assign I_ready = 1'b0 | I_valid;
assign O_valid = magma_Bit_or_inst1_out;
endmodule


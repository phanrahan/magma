module Mux2xBit (
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

module TestReadyValidNoDeqWhen (
    input I0,
    input [4:0] I1_data,
    output I1_ready,
    input I1_valid,
    output [4:0] O
);
Mux2xBit Mux2xBit_inst0 (
    .I0(1'b1),
    .I1(1'b0),
    .S(I0),
    .O(I1_ready)
);
assign O = I1_data;
endmodule


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
wire [2:0] __0_return_0;
wire [2:0] __0_return_1;
wire [2:0] __0_return_2;
wire [2:0] __0_return_3;
wire _cond_0;
wire _cond_1;
wire _cond_2;
Mux2xBits3 Mux2xBits3_inst0 (
    .I0(__0_return_3),
    .I1(__0_return_2),
    .S(_cond_2),
    .O(Mux2xBits3_inst0_O)
);
Mux2xBits3 Mux2xBits3_inst1 (
    .I0(Mux2xBits3_inst0_O),
    .I1(__0_return_1),
    .S(_cond_1),
    .O(Mux2xBits3_inst1_O)
);
Mux2xBits3 Mux2xBits3_inst2 (
    .I0(Mux2xBits3_inst1_O),
    .I1(__0_return_0),
    .S(_cond_0),
    .O(O)
);
assign __0_return_0 = 3'h0;
assign __0_return_1 = 3'h1;
assign __0_return_2 = 3'h2;
assign __0_return_3 = 3'h4;
assign _cond_0 = I[0];
assign _cond_1 = I[1];
assign _cond_2 = I[2];
endmodule


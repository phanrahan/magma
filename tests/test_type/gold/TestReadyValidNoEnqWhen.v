module Mux2xBits5 (
    input [4:0] I0,
    input [4:0] I1,
    input S,
    output [4:0] O
);
reg [4:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = I0;
end else begin
    mux_out = I1;
end
end

assign O = mux_out;
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] mux_out;
always @(*) begin
if (S == 0) begin
    mux_out = I0;
end else begin
    mux_out = I1;
end
end

assign O = mux_out[0];
endmodule

module TestReadyValidNoEnqWhen (
    input I,
    output [4:0] O_data,
    input O_ready,
    output O_valid
);
Mux2xBit Mux2xBit_inst0 (
    .I0(1'b1),
    .I1(1'b0),
    .S(I),
    .O(O_valid)
);
Mux2xBits5 Mux2xBits5_inst0 (
    .I0(5'h1e),
    .I1(5'h00),
    .S(I),
    .O(O_data)
);
endmodule


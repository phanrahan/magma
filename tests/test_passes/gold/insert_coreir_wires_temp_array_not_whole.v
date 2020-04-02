module Main (
    input I,
    output O0,
    output O1
);
wire [1:0] x;
assign x = {I,I};
assign O0 = x[0];
assign O1 = x[1];
endmodule


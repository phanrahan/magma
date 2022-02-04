module _Test (
    input [7:0] I0,
    input [3:0] I1,
    output [7:0] O1,
    output [15:0] O2
);
assign O1 = I0 << ({1'b0,1'b0,1'b0,1'b0,I1});
assign O2 = {1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,I0 << ({1'b0,1'b0,1'b0,1'b0,I1})};
endmodule


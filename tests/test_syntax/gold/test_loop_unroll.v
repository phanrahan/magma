module logic (input [3:0] a, output [3:0] O);
assign O = {a[0],a[1],a[2],a[3]};
endmodule

